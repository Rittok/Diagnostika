from django.db import models
from django.contrib.auth.models import User
from diagnostic.models import *

class Block(models.Model):
    number = models.PositiveIntegerField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Блок {self.number}"

TEST_TYPES = (
    ('primary', 'Первичная диагностика'),
    ('interim', 'Промежуточная диагностика'),
    ('final', 'Итоговая диагностика'),
)

class Question(models.Model):
    text = models.CharField(max_length=255, db_index=True)
    test_type = models.CharField(max_length=50, choices=TEST_TYPES)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, default=1)
    options = models.ManyToManyField('AnswerOption', related_name='linked_questions')


    def __str__(self):
        return self.text[:50]

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255, verbose_name="Вариант ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ?")
    category_id = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.option_text

class DiagnosticResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block_number = models.IntegerField()  # Номер блока (1 или 2)
    knowledge_percentage = models.FloatField(null=True, blank=True)  # Оценка знаний (%)
    career_preference = models.CharField(max_length=50, blank=True, null=True)  # Проф. предпочтения
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s Result ({self.block_number})"

class AnswerRecord(models.Model):
    diagnostic_result = models.ForeignKey(DiagnosticResult, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField(null=True)

    def __str__(self):
        return f"Answer to Q#{self.question.id}"
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.PROTECT)

    def __str__(self):
        return f"Профиль ученика: {self.user.username}"
  
class Report(models.Model):
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.PROTECT)
    knowledge_percentage_avg = models.FloatField()  # Средняя успешность учеников
    students_count = models.IntegerField()          # Количество учеников
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отчет для {self.school.name} ({self.class_level.level})"