from django.db import models

class Questionaire(models.Model):
    title           = models.CharField()

class Question(models.Model):
    text            = models.CharField(max_length=255)
    order           = models.IntegerField()
    questionaire    = models.ForeignKey(Questionaire, on_delete=models.CASCADE, related_name="questions", null=True)

class Person(models.Model):
    session_id      = models.CharField()
    name            = models.CharField()

class Answers(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)
    response        = models.TextField()
    person          = models.ForeignKey(Person, on_delete=models.CASCADE)