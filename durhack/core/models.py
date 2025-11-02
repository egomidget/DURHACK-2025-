from django.db import models

class Questionaire(models.Model):
    title           = models.CharField()

class Question(models.Model):
    text            = models.CharField(max_length=255)
    order           = models.IntegerField()
    questionaire    = models.ForeignKey(Questionaire, on_delete=models.CASCADE, related_name="questions", null=True)

    def __str__(self):
        return self.text

class Person(models.Model):
    session_id      = models.CharField()
    name            = models.CharField()

    def __str__(self):
        return self.name

class Answers(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)
    response        = models.BigIntegerField(null=True)
    person          = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return str(self.response)

class Match(models.Model):
    person_a        = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="person_a")
    person_b        = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="person_b")
    score           = models.FloatField()

    def format_score(self):
        return f"{round(self.score * 100, 2)}"
    
    @classmethod
    def find_match(self, person):
        try:
            return Match.objects.get(person_a = person)
        except:
            try:
                return Match.objects.get(person_b = person)
            except:
                return "no match"