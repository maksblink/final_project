from django.db import models


class Game(models.Model):
    operator = models.CharField(max_length=1)
    range1_min = models.IntegerField()
    range1_max = models.IntegerField()
    range2_min = models.IntegerField()
    range2_max = models.IntegerField()
    number_of_correct_answers = models.IntegerField(default=0)
    number_of_wrong_answers = models.IntegerField(default=0)


class GameAnswers(models.Model):
    first_factor = models.IntegerField()
    second_factor = models.IntegerField()
    answer = models.IntegerField(null=True)
    correct_answer = models.IntegerField()
    was_this_answer_correct = models.BooleanField(null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
