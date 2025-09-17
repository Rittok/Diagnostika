from django.contrib import admin
from .models import *
from diagnostic.models import *
from openpyxl import Workbook
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django import forms
from .forms import ReportFilterForm

def export_excel(modeladmin, request, queryset):
    form = ReportFilterForm(request.GET)
    if form.is_valid():
        school_id = form.cleaned_data.get('school')
        class_levels = form.cleaned_data.get('class_level')

        # Фильтруем отчёты по выбранной школе и классу
        reports = Report.objects.filter(school_id=school_id)
        if class_levels:
            reports = reports.filter(class_level_id__in=class_levels)

        wb = Workbook()
        ws = wb.active
        headers = ["Школа", "Класс", "Средний % знаний", "Количество учеников"]
        ws.append(headers)

        for report in reports:
            row = [
                report.school.name,
                report.class_level.level,
                report.knowledge_percentage_avg,
                report.students_count
            ]
            ws.append(row)

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="reports.xlsx"'
        response.write(output.read())
        return response

export_excel.short_description = "Экспорт в Excel"

# Экшн для экспорта в PDF
def export_pdf(modeladmin, request, queryset):
    form = ReportFilterForm(request.GET)
    if form.is_valid():
        school_id = form.cleaned_data.get('school')
        class_levels = form.cleaned_data.get('class_level')

        # Фильтруем отчёты по выбранной школе и классу
        reports = Report.objects.filter(school_id=school_id)
        if class_levels:
            reports = reports.filter(class_level_id__in=class_levels)

        elements = []
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(BytesIO(), pagesize=letter)

        elements.append(Paragraph("<b>Городской проект \"Курс на IT\"</b>", styles["Title"]))
        elements.append(Paragraph("IT-куб Тольятти", styles["Subtitle"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Данный отчет содержит результаты первичной диагностики.", styles["BodyText"]))
        elements.append(Spacer(1, 24))

        for report in reports:
            elements.append(Paragraph(f"<b>Школа: {report.school.name}</b>", styles["Heading2"]))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f"Класс: {report.class_level.level}", styles["Normal"]))
            elements.append(Paragraph(f"Средний % знаний: {report.knowledge_percentage_avg}%", styles["Normal"]))
            elements.append(Paragraph(f"Количество учеников: {report.students_count}", styles["Normal"]))
            elements.append(Spacer(1, 24))

        doc.build(elements)
        output = BytesIO()
        doc.save(output)
        output.seek(0)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
        response.write(output.read())
        return response

export_pdf.short_description = "Экспорт в PDF"

# Настройки для блока вопросов
@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('number', 'description')
    ordering = ('number',)

# Настройки для вопросов с inline-редактированием вариантов ответов
class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 3  # Кол-во пустых полей для новых вариантов ответов

@admin.register(Question)
class QuestionWithAnswersAdmin(admin.ModelAdmin):
    inlines = [AnswerOptionInline]
    list_display = ('id', 'text', 'test_type', 'block')
    search_fields = ('text',)
    list_filter = ('test_type', 'block')
    ordering = ('block', 'id')

# Настройки для вариантов ответов
@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'option_text', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('option_text',)
    ordering = ('question',)


# Класс для результатов диагностики
@admin.register(DiagnosticResult)
class DiagnosticResultAdmin(admin.ModelAdmin):
   user = models.ForeignKey(User, on_delete=models.CASCADE)    
   block_number = models.IntegerField()  # Номер блока (1 или 2)    
   knowledge_percentage = models.FloatField(null=True, blank=True)  # Оценка знаний (%)
   career_preference = models.CharField(max_length=50, blank=True, null=True)  # Профессиональные предпочтения    
   created_at = models.DateTimeField(auto_now_add=True)
   
   def __str__(self):
    return f"{self.user}'s Result ({self.block_number})"

@admin.register(AnswerRecord)
class AnswerRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'selected_answer', 'is_correct', 'diagnostic_result')
    list_filter = ('is_correct', 'question')
    search_fields = ('question__text', 'selected_answer__option_text')
    ordering = ('question',)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('level',)
    list_filter = ('level',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    actions = [export_excel, export_pdf]
    list_display = ('school', 'class_level', 'knowledge_percentage_avg', 'students_count', 'created_at')
    list_filter = ('school', 'class_level')
    search_fields = ('school__name', 'class_level__level')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)