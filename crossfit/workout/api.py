from django.db import connection
# from rest_framework import generics
from django.db.models import Min, Q
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WorkoutRecord
from .serializer import WorkoutRankSerializer


# class RankRetrieveView(generics.ListAPIView):
#     serializer_class = WorkoutRankSerializer
#
#     def get_queryset(self):
#         queryset = WorkoutRecord.objects.all()
#
#         workout = self.request.query_params.get('workout', None)
#         if not workout:
#             raise ParseError(detail={"error": "workout 필드가 비어있습니다."})
#         queryset = queryset.filter(workout_name=workout)
#         queryset = queryset.order_by('record_time')
#         return queryset

class RankRetrieveView(APIView):
    def get(self, request):
        queryset = self._get_queryset()
        serializer = WorkoutRankSerializer(queryset, many=True)
        data = serializer.data
        return Response(self.add_rank_to_dict(data))

    def _get_queryset(self):
        workout = self.request.query_params.get('workout', None)
        if not workout:
            raise ParseError(detail={"error": "workout 필드가 비어있습니다."})
        queryset = WorkoutRecord.objects.values('username').annotate(
            record_time=Min('record_time'))
        queryset = queryset.filter(workout_name=workout).order_by('record_time')
        return queryset

    def add_rank_to_dict(self, data):
        data[0]['rank'] = 1
        previous_record = data[0].get('record_time')

        cur_rank = 1
        for i, person in enumerate(data[1:]):
            if person.get('record_time') != previous_record:
                cur_rank = i+2
                previous_record = person.get('record_time')
            person['rank'] = cur_rank
        return data

    # def add_rank_to_dict(self, data):
    #     cur_rank = 1
    #     num_of_same_record = 0
    #     previous_record = 0
    #     for person in data:
    #         if person['record_time'] != previous_record:
    #             cur_rank += num_of_same_record
    #             person['rank'] = cur_rank
    #         else:

    # def get(self, request):
    #     workout = self.request.query_params.get('workout', None)
    #     if not workout:
    #         raise ParseError(detail={"error": "workout 필드가 비어있습니다."})
    #
    #     cursor = connection.cursor()
    #     cursor.execute(
    #         "SELECT MIN(record_time), username_id FROM workout_workoutrecord "
    #         "WHERE workout_name=%s "
    #         "GROUP BY username_id ORDER BY MAX(record_time)",
    #         [workout]
    #     )
    #     rows = cursor.fetchall()
    #     print(rows[0][1].fitness)
    #     return Response({"1": "1"})
