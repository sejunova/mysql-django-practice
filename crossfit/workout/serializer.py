from rest_framework import serializers

from .models import WorkoutRecord


class WorkoutRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutRecord
        fields = ('record_time', 'user')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['fitness'] = instance.user.fitness.name
        return ret