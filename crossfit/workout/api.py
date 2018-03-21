from django.db import connection
# from rest_framework import generics
from django.db.models import Min, Q
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WorkoutRecord
from .serializer import WorkoutRankSerializer


class RankRetrieveView(APIView):
    def get(self, request):
        params = self.check_query_params()
        queryset = self._get_queryset(**params)
        serializer = WorkoutRankSerializer(queryset, many=True)
        data = serializer.data
        return Response(self.add_rank_to_dict(data))

    def _get_queryset(self, **params):
        queryset = WorkoutRecord.objects.values('username').annotate(
            record_time=Min('record_time'))
        queryset = queryset.filter(workout_name=params['workout'])
        if params['date_from'] and params['date_to']:
            queryset = queryset.filter(workout_date__range=[params['date_from'], params['date_to']])
        queryset = queryset.order_by('record_time')
        return queryset

    def check_query_params(self):
        workout = self.request.query_params.get('workout', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if not workout:
            raise ParseError(detail={"error": "workout 필드가 비어있습니다."})
        if (date_from or date_to) and not (date_from and date_to):
            raise ParseError(detail={"error": "날짜 입력을 정확하게 해 주세요"})
        return dict(workout=workout, date_from=date_from, date_to=date_to)

    def add_rank_to_dict(self, data):
        if len(data) == 0:
            return data
        data[0]['rank'] = 1
        previous_record = data[0].get('record_time')

        cur_rank = 1
        for i, person in enumerate(data[1:]):
            if person.get('record_time') != previous_record:
                cur_rank = i + 2
                previous_record = person.get('record_time')
            person['rank'] = cur_rank
        return data
