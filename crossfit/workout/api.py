from django.db.models import Min
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WorkoutRecord
from .serializer import WorkoutRankSerializer


class RankRetrieveView(APIView):
    def get(self, request):
        '''
        GET 요청을 처리합니다.
        workout, date_from, date_to가 추가적인 쿼리로 함께 전달될 수 있습니다.
        :return: 랭킹, 기록시간, 크로스핏 회원 아이디, 크로스핏 센터를 담은 OrderedDict 데이터 집합을 리스트에 담아 반환합니다
        '''
        params = self.check_query_params()
        queryset = self._get_queryset(**params)
        serializer = WorkoutRankSerializer(queryset, many=True)
        data = serializer.data
        return Response(self.add_rank_to_dict(data))

    def _get_queryset(self, **params):
        # Group by 조건으로 각 개인의 최고기록만 추출
        queryset = WorkoutRecord.objects.values('username').annotate(
            record_time=Min('record_time'))
        queryset = queryset.filter(workout_name=params['workout'])
        if params['date_from'] and params['date_to']:
            queryset = queryset.filter(workout_date__range=[params['date_from'], params['date_to']])
        queryset = queryset.order_by('record_time')
        return queryset

    def check_query_params(self):
        '''
        GET 요청과 함께 들어온 쿼리를 검사합니다.
        workout은 필수로 넣어야 하는 쿼리이고, date_from, date_to 를 포함하는 경우에는 두 개의 쿼리 모두 함께 요청되어야 합니다.
        :return: 쿼리를 dict로 반환합니다. 요청되지 않은 쿼리값은 None 으로 처리합니다.
        '''
        workout = self.request.query_params.get('workout', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if not workout:
            raise ParseError(detail={"error": "workout 필드가 비어있습니다."})
        if (date_from or date_to) and not (date_from and date_to):
            raise ParseError(detail={"error": "날짜 입력을 정확하게 해 주세요"})
        return dict(workout=workout, date_from=date_from, date_to=date_to)

    def add_rank_to_dict(self, data):
        '''
        :param data: 쿼리셋 조건에 맞게 필터링된 데이터 집합.
        :return: 각각의 데이터 집합에 rank를 추가해서 반환합니다.
        '''
        if len(data) == 0:
            return data
        data[0]['rank'] = 1
        previous_record = data[0].get('record_time')

        # 같은 기록을 가진 사람은 이전 사람과 같은 등수로 지정된다.
        cur_rank = 1
        for i, person in enumerate(data[1:]):
            if person.get('record_time') != previous_record:
                cur_rank = i + 2
                previous_record = person.get('record_time')
            person['rank'] = cur_rank
        return data
