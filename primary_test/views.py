from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.urls import reverse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models import Sum
from diagnostic.models import *
from .models import *
import math, random
from django.db.models import Subquery, OuterRef
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect, render

# Константа: количество вопросов на одну страницу
QUESTIONS_PER_PAGE = 5

@login_required
def block1_test_view(request, page=1):
    block_obj = get_object_or_404(Block, number=1)
    session_key = f"questions_order_{block_obj.number}_{request.user.id}"

    # Генерируем случайный порядок вопросов
    if session_key not in request.session:
        all_questions = list(Question.objects.filter(block=block_obj))
        random.shuffle(all_questions)
        request.session[session_key] = [q.id for q in all_questions]

    # Загрузка вопросов из сессии
    ordered_questions_ids = request.session[session_key]
    ordered_questions = Question.objects.filter(id__in=ordered_questions_ids).order_by()

    # Определение текущей страницы вопросов
    total_pages = math.ceil(len(ordered_questions) / QUESTIONS_PER_PAGE)
    start_idx = (page - 1) * QUESTIONS_PER_PAGE
    end_idx = min(start_idx + QUESTIONS_PER_PAGE, len(ordered_questions))
    current_questions = ordered_questions[start_idx:end_idx]

    # Формируем форму с выбором ответов
    prepared_questions = []
    for question in current_questions:
        options = [(opt, False) for opt in question.answeroption_set.all()]
        prepared_questions.append((question, options))

    # Обработка POST-запроса
    if request.method == 'POST':
        cleaned_data = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.replace('question_', '')
                try:
                    question_id_int = int(question_id)
                except ValueError:
                    print(f"Ошибка при разборе ключа '{key}'. Значение: '{value}'")
                    continue
                else:
                    cleaned_data[question_id_int] = value

        # Обработка результатов и сохранение
        existing_result = DiagnosticResult.objects.filter(user=request.user).first()

        if existing_result:
            diagnostic_result = existing_result
        else:
            diagnostic_result = DiagnosticResult.objects.create(
                user=request.user,
                block_number=block_obj.number
            )

        correct_count = 0
        for question_id, option_id in cleaned_data.items():
            question = Question.objects.get(id=question_id)
            answer_option = AnswerOption.objects.get(id=int(option_id))
            AnswerRecord.objects.create(
                diagnostic_result=diagnostic_result,
                question=question,
                selected_answer=answer_option,
                is_correct=answer_option.is_correct
            )
            if answer_option.is_correct:
                correct_count += 1

        # Высчитываем процент правильных ответов
        percentage = (correct_count / len(current_questions)) * 100
        diagnostic_result.knowledge_percentage = percentage
        diagnostic_result.save()

        # Контрольная точка
        print("First block results saved successfully!")

        # Возвращаем JSON-ответ при AJAX-запросе
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Результаты сохранены'})

        # Обычный редирект при обычном POST-запросе
        if page < total_pages:
            next_page = page + 1
            return redirect(reverse('primary_test:block1_test', args=(next_page,)))
        else:
            return redirect(reverse('primary_test:block2_test'))

    context = {
        'prepared_questions': prepared_questions,
        'page': page,
        'total_pages': total_pages
    }
    return render(request, 'primary_test/block1_test.html', context)

@login_required
def block2_test_view(request):
    block_obj = get_object_or_404(Block, number=2)
    session_key = f"saved_answers_{block_obj.number}_{request.user.id}"

    # Получаем все вопросы второго блока
    all_questions = list(Question.objects.filter(block=block_obj))

    # Подготовленная форма с вариантами выбора
    prepared_questions = []
    for question in all_questions:
        options = [(opt, False) for opt in question.answeroption_set.all()]
        prepared_questions.append((question, options))

    if request.method == 'POST':
        cleaned_data = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                cleaned_data[int(key.split('_')[1])] = value

        # Анализ предпочтений
        recommendations = determine_preferences(cleaned_data)
        career_preference = recommendations[0]

        # Получаем последнюю запись результатов
        latest_result = DiagnosticResult.objects.filter(user=request.user).order_by('-created_at').first()

        # Обновляем существующее или создаем новое
        if latest_result:
            latest_result.career_preference = career_preference
            latest_result.save()
        else:
            diagnostic_result = DiagnosticResult.objects.create(
                user=request.user,
                block_number=block_obj.number,
                career_preference=career_preference
            )

        # Контрольная точка
        print("Second block results added successfully!")

        # AJAX-ответ при соответствующем запросе
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Выбор профессии зафиксирован'})

        # Обычное перенаправление
        return redirect(reverse('primary_test:diagnostic_results'))

    context = {
        'prepared_questions': prepared_questions
    }
    return render(request, 'primary_test/block2_test.html', context)

def process_block_answers(cleaned_data, block_obj, user):
    """
    Сохранение результатов тестирования.
    """
    if block_obj.number == 1:
        # Обрабатываем результаты первого блока (оценка знаний)
        results = {}
        for key, val in cleaned_data.items():
            question_id = int(key.split('_')[-1])
            option_id = int(val)
            answer_option = AnswerOption.objects.get(pk=option_id)
            results[question_id] = {
                'selected_answer': answer_option,
                'is_correct': answer_option.is_correct
            }
        
        # Сохраняем результаты
        diagnostic_result = DiagnosticResult.objects.create(
            user=user,
            block_number=block_obj.number
        )
        for qid, data in results.items():
            AnswerRecord.objects.create(
                question_id=qid,
                selected_answer=data['selected_answer'],
                is_correct=data['is_correct'],
                diagnostic_result=diagnostic_result
            )
    elif block_obj.number == 2:
        # Обрабатываем результаты второго блока (предпочтения)
        responses = [
            {'choice': cleaned_data[key].split('_')[-1]}  # получаем ID выбранного варианта
            for key in cleaned_data.keys() if key.startswith('question_')
        ]
        recommendation, counts = determine_preferences(responses)
        diagnostic_result = DiagnosticResult.objects.create(
            user=user,
            block_number=block_obj.number,
            preference=recommendation
        )
        diagnostic_result.save()

def determine_preferences(cleaned_data):
    """
    Анализируем предпочтения пользователя на основе его выборов.
    """
    # Категории специальностей
    categories = {
        1: "Кибербезопасность",
        2: "Графический дизайн",
        3: "Разработка игр",
        4: "Программирование",
        5: "IT инженерия"
    }

    # Подсчет популярности категорий
    popularity_counts = {cat_id: 0 for cat_id in categories.keys()}
    for option_id in cleaned_data.values():  # Получаем идентификаторы выбранных ответов
        category_id = AnswerOption.objects.get(id=option_id).category_id
        if category_id:
            popularity_counts[category_id] += 1

    # Выбор наиболее популярной категории
    recommended_category_id = max(popularity_counts, key=popularity_counts.get)
    recommendation = categories.get(recommended_category_id, "")

    return recommendation, popularity_counts

def save_progress(user, block_number, results):
    """Сохранение результатов в БД и формирование отчета."""
    diagnostic_result = DiagnosticResult.objects.create(
        user=user,
        block_number=block_number
    )
    if isinstance(results, dict):
        # Первая часть (блок оценки знаний)
        for qid, data in results.items():
            AnswerRecord.objects.create(
                question_id=qid,
                selected_answer=data['selected_answer'],
                is_correct=data['is_correct'],
                diagnostic_result=diagnostic_result
            )
    else:
        # Вторая часть (выбор предпочтений)
        preference, counts = results
        diagnostic_result.preference = preference
        diagnostic_result.save()

    # Генерация отчёта
    generate_pdf_report(user)

@login_required
def diagnostic_results(request):
    results = DiagnosticResult.objects.filter(user=request.user).order_by('-created_at').first()

    if results:
        knowledge_percentage = results.knowledge_percentage
        career_preference = results.career_preference
        print(f"Получены результаты: {knowledge_percentage}% | {career_preference}")
    else:
        knowledge_percentage = None
        career_preference = None
        print("Результаты не найдены.")

    context = {
        'knowledge_percentage': knowledge_percentage,
        'career_preference': career_preference,
        'has_results': bool(knowledge_percentage and career_preference)
    }
    return render(request, 'primary_test/results.html', context)

def generate_pdf_report(user):
    """
    Создаем отчёт в формате PDF для пользователя.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, f"Отчёт по итогам тестирования для пользователя: {user.username}")

    # Основная информация
    p.drawString(100, 750, f"Уровень подготовки: {user.diagnosticresult_set.first().knowledge_percentage}%")
    p.drawString(100, 700, f"Рекомендуемая профессия: {user.diagnosticresult_set.first().career_preference}")

    p.showPage()
    p.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    # Сохраняем файл отчёта в профиль пользователя
    filename = f'{user.username}_report.pdf'
    user.profile.report_file.save(filename, ContentFile(pdf_bytes))

@login_required
def download_report(request, username):
    """
    Скачивание PDF-отчета.
    """
    profile = UserProfile.objects.get(user__username=username)
    response = FileResponse(profile.report_file.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={profile.report_file.name}'
    return response

@login_required
def reset_session(request):
    """
    Очищает сессию перед началом нового теста.
    """
    request.session.clear()
    return redirect(reverse('primary_test:block1_test', args=(1,)))