from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import WorkoutRecord

User = get_user_model()


class WorkoutRankSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = WorkoutRecord
        fields = ('record_time', 'username')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = User.objects.get(username=instance['username'])
        ret['fitness'] = user.fitness.name
        return ret
