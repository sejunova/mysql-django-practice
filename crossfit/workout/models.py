from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WorkoutRecord(models.Model):
    workout_name = models.CharField(max_length=20)
    record_time = models.PositiveIntegerField()
    workout_date = models.DateField()
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.workout_name