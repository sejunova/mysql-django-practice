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
        return Response(data)

    def _get_queryset(self):
        workout = self.request.query_params.get('workout', None)
        if not workout:
            raise ParseError(detail={"error": "workout 필드가 비어있습니다."})
        queryset = WorkoutRecord.objects.values('username').annotate(
            record_time=Min('record_time'))
        queryset = queryset.filter(workout_name=workout).order_by('record_time')
        return queryset


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
