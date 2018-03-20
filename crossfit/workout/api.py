from rest_framework import generics

from .models import WorkoutRecord
from .serializer import WorkoutRankSerializer


class RankRetrieveView(generics.ListAPIView):
    serializer_class = WorkoutRankSerializer
    queryset = WorkoutRecord.objects.all()
