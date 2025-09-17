from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DiagnosticResult, Report

@receiver(post_save, sender=DiagnosticResult)
def create_school_report(sender, instance, created, **kwargs):
    if created:
        # Получаем школу и класс ученика
        school = instance.user.studentprofile.school
        class_level = instance.user.studentprofile.class_level

        # Агрегируем средние результаты и количество учеников
        avg_knowledge_percentage = DiagnosticResult.objects.filter(
            user__studentprofile__school=school,
            user__studentprofile__class_level=class_level
        ).aggregate(avg=models.Avg('knowledge_percentage'))['avg']

        students_count = DiagnosticResult.objects.filter(
            user__studentprofile__school=school,
            user__studentprofile__class_level=class_level
        ).count()

        # Создаем отчет
        Report.objects.create(
            school=school,
            class_level=class_level,
            knowledge_percentage_avg=avg_knowledge_percentage,
            students_count=students_count
        )