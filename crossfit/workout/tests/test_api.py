import pytest
from django.urls import reverse
from rest_framework.exceptions import ParseError
from rest_framework.test import APITestCase

from workout.api import RankRetrieveView


def test_give_rank(records_to_try, results_to_try):
    '''
    같은 record_time을 가진 경우 같은 rank가 주어지는지 확인
    conftest에 있는 데이터를 fixture로 사용
    '''
    repeat = len(records_to_try)
    for i in range(repeat):
        result = RankRetrieveView._add_rank_to_dict(data=records_to_try[i])
        assert result == results_to_try[i]


@pytest.mark.django_db
class TestRankRetrieveView(APITestCase):
    url = reverse('rank')

    def test_wrong_query_raise_eror(self):
        '''
        잘못된 query param을 보냈을 때 status_code가 400이 되는지 확인
        각각 'workout' param이 없는 경우, 잘못된 param을 보낸 경우, 전후 날짜중 한 쪽만 선택한 경우 테스트
        '''
        wrong_query_list = [{}, {'workoutt': 'eva'}, {'workout': 'eva', 'date_from': '2018-02-01'}]
        for wrong_query in wrong_query_list:
            response = self.client.get(self.url, wrong_query)
            assert response.status_code == 400

    def test_get_workout(self):
        '''
        GET 요청을 실제로 보냈을 때 예상한 대로 작동하는지 확인
        1. status_code 200 확인
        2. eva운동만 조회하는 경우 11개의 데이터만 반환하는지 확인
        '''
        response = self.client.get(self.url, {'workout': 'eva'})
        assert response.status_code == 200
        assert len(response.data) == 11

    def test_get_workout_with_date(self):
        '''
        GET 요청을 실제로 보냈을 때 예상한 대로 작동하는지 확인
        1. status_code 200 확인
        2. eva 운동 데이터 중 2월달의 데이터 6개만 반환하는지 확인
        '''
        response = self.client.get(self.url, {'workout': 'eva', 'date_from': '2018-02-01', 'date_to': '2018-02-28'})
        assert response.status_code == 200
        assert len(response.data) == 6
