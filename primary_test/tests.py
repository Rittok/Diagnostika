from primary_test.models import Question, AnswerOption

answers = [
    {'question_id': 1, 'text': 'Создаёт компьютерные игры', 'is_correct': False},
    {'question_id': 1, 'text': 'Защищает компьютеры и данные от взлома', 'is_correct': True},
    {'question_id': 1, 'text': 'Рисует картинки на компьютере', 'is_correct': False},
    {'question_id': 1, 'text': 'Чинит сломанные компьютеры', 'is_correct': False},
    
    {'question_id': 2, 'text': 'Интернет-браузер (например, Chrome, Firefox)', 'is_correct': False},
    {'question_id': 2, 'text': 'Антивирусная программа', 'is_correct': True},
    {'question_id': 2, 'text': 'Текстовый редактор (например, Блокнот)', 'is_correct': False},
    {'question_id': 2, 'text': 'Графический редактор (например, Paint)', 'is_correct': False},
    
    {'question_id': 3, 'text': 'Настройка и поддержание компьютерных сетей', 'is_correct': False},
    {'question_id': 3, 'text': 'Разработка основного программного кода продукта', 'is_correct': False},
    {'question_id': 3, 'text': 'Имитация действий злоумышленников для поиска уязвимостей в системах безопасности', 'is_correct': True},
    {'question_id': 3, 'text': 'Тестирование программы, игры и приложения. Его задача — проверить, работает ли продукт так, как было задумано', 'is_correct': False},
    
    {'question_id': 4, 'text': 'Человек, который создаёт внешний вид сайтов', 'is_correct': True},
    {'question_id': 4, 'text': 'Специалист по ремонту компьютеров', 'is_correct': False},
    {'question_id': 4, 'text': 'Программист баз данных', 'is_correct': False},
    {'question_id': 4, 'text': 'Менеджер интернет-магазина', 'is_correct': False},
    
    {'question_id': 5, 'text': 'Microsoft Word', 'is_correct': False},
    {'question_id': 5, 'text': 'Adobe Photoshop', 'is_correct': True},
    {'question_id': 5, 'text': 'Google Chrome', 'is_correct': False},
    {'question_id': 5, 'text': 'Windows Media Player', 'is_correct': False},
    
    {'question_id': 6, 'text': 'Алгоритм', 'is_correct': False},
    {'question_id': 6, 'text': 'Программный код', 'is_correct': False},
    {'question_id': 6, 'text': 'Пользовательский интерфейс (UI)', 'is_correct': True},
    {'question_id': 6, 'text': 'Базу данных', 'is_correct': False},
    
    {'question_id': 7, 'text': 'Геймдизайнер', 'is_correct': True},
    {'question_id': 7, 'text': 'Системный администратор', 'is_correct': False},
    {'question_id': 7, 'text': 'Веб-мастер', 'is_correct': False},
    {'question_id': 7, 'text': 'Контент-менеджер', 'is_correct': False},
    
    {'question_id': 8, 'text': 'Подбирает костюмы и рисует грим актёрам', 'is_correct': False},
    {'question_id': 8, 'text': 'Выравнивает программный код, чтобы он был написан ровно и красиво', 'is_correct': False},
    {'question_id': 8, 'text': 'Рисует персонажей, локации и объекты', 'is_correct': True},
    {'question_id': 8, 'text': 'Пишет новости на сайт', 'is_correct': False},
    
    {'question_id': 9, 'text': 'Сценарист', 'is_correct': False},
    {'question_id': 9, 'text': 'Аналитик данных', 'is_correct': False},
    {'question_id': 9, 'text': 'Консультант по кибербезопасности', 'is_correct': False},
    {'question_id': 9, 'text': 'Тестировщик ', 'is_correct': True},
    
    {'question_id': 10, 'text': 'Установка программ на компьютер', 'is_correct': False},
    {'question_id': 10, 'text': 'Создание инструкций для компьютера на специальном языке', 'is_correct': True},
    {'question_id': 10, 'text': 'Настройка телевизионных каналов', 'is_correct': False},
    {'question_id': 10, 'text': 'Подключение сети интернет и грамотный поиск информации', 'is_correct': False},

    {'question_id': 11, 'text': 'Цикл', 'is_correct': True},
    {'question_id': 11, 'text': 'Пауза', 'is_correct': False},
    {'question_id': 11, 'text': 'Скриншот', 'is_correct': False},
    {'question_id': 11, 'text': 'Переименование', 'is_correct': False},

    {'question_id': 12, 'text': 'Занимается разработкой сайтов и веб-приложений', 'is_correct': False},
    {'question_id': 12, 'text': 'Настраивает процессы, чтобы программы быстро и без ошибок запускались', 'is_correct': False},
    {'question_id': 12, 'text': 'Программируют устройства, которые нас окружают: умные часы, стиральные машины, микроволновки', 'is_correct': False},
    {'question_id': 12, 'text': 'Создает приложения для смартфонов', 'is_correct': True},

    {'question_id': 13, 'text': 'Металлические части корпуса', 'is_correct': False},
    {'question_id': 13, 'text': "Компьютерные игры", 'is_correct': False,},
    {"question_id": 13,"text":"Физические компоненты компьютера (процессор, память, видеокарта)", "is_correct":True,},
    {"question_id": 13,"text":"Антивирусные программы", "is_correct":False},

    {"question_id":14,"text":"Веб-дизайнер", "is_correct":False,},
    {"question_id":14,"text":"Сетевой инженер", "is_correct":True,},
    {"question_id":14,"text":"Специалист по кибербезопасности", "is_correct":False,},
    {"question_id":14,"text":"Разработчик игр", "is_correct":False},

    {"question_id":15,"text":"Локальное хранение данных", "is_correct":False,},
    {"question_id":15,"text":"Облачные вычисления (Cloud Computing)", "is_correct":False,},
    {"question_id":15,"text":"Облачное хранилище данных", "is_correct":True,},
    {"question_id":15,"text":"Разработчик игр", "is_correct":False},

    {"question_id":16,"text":"Расследовать киберпреступления, собирать доказательства взломов, сотрудничать с правоохранительными органами", "is_correct":False,},
    {"question_id":16,"text":"Разрабатывать логотипы, верстать сайты, продумывать визуальный стиль приложения", "is_correct":False,},
    {"question_id":16,"text":"Прописывать сценарий, продумывать сюжетные повороты, описания мира, диалоги персонажей. Готовить текстовые посты, уведомления", "is_correct":False,},
    {"question_id":16,"text":"Создавать приложения и инструменты для мобильных телефонов, умных часов и колонок", "is_correct":False,},
    {"question_id":16,"text":"Программировать роботов, управлять их действиями, ставить перед ними сложные задачи", "is_correct":False,},
    
    {"question_id":17,"text":"Бороться с мошенниками, искать «лазейки» в защите, отслеживать подозрительные денежные переводы", "is_correct":False,},
    {"question_id":17,"text":"Разрабатывать иконки, интерфейс приложения, продумывать, чтобы всё было удобно и красиво", "is_correct":False,},
    {"question_id":17,"text":"Прописывать задачи, которые должен решать игрок на каждом уровне и локации, чтобы получить максимально интересный игровой опыт", "is_correct":False,},
    {"question_id":17,"text":"Создавать системы для бизнеса, продумывать сложные программы и драйверы для крупных заказчиков", "is_correct":False,},
    {"question_id":17,"text":"Находить рутинные операции (например, обработку заказов, отправку писем, сбор данных) и заменять их автоматизированными решениями", "is_correct":False,},
    
    {"question_id":18,"text":"Настраивать систему защиты, создавать инструменты и сервисы для ликвидации угроз, отражать атаки", "is_correct":False,},
    {"question_id":18,"text":"Продумывать дизайн интерьера, подбирать стили, разрабатывать 3D-план помещения", "is_correct":False,},
    {"question_id":18,"text":"Создавать различные симуляции на базе игрового движка: взрывы, разрушения, заклинания, дым, туман, капли и прочие запоминающиеся эффекты", "is_correct":False,},
    {"question_id":18,"text":"Работать с виртуальной реальностью (VR), создавать симуляции туристических туров, конструирования техники, проведения экспериментов, строительства т.п.", "is_correct":False,},
    {"question_id":18,"text":"Разрабатывать новые цифровые приборы для разных отраслей, изобретать, подбирать оборудование", "is_correct":False,},
    
    {'question_id': 19, 'text': 'Искать ошибки и уязвимые места в программе, «атаковать» их, чтобы найти слабые места', 'is_correct': False},
    {'question_id': 19, 'text': 'Оживлять изображения, добавлять анимацию в приложения, создавать рекламные видеоролики, рисовать титры', 'is_correct': False},
    {'question_id': 19, 'text': 'Подготавливать модели персонажа к анимации. Оснащать модели скелетом', 'is_correct': False},
    {'question_id': 19, 'text': 'Создавать боты и алгоритмы, работать с нейросетями, заниматься машинным обучением', 'is_correct': False},
    {'question_id': 19, 'text': 'Проектировать архитектуру приложения, выбирать технологии, сформировать команду разработчиков и проследить, чтобы всё работало без сбоев', 'is_correct': False},

    {'question_id': 20, 'text': 'Обучать и консультировать пользователей по вопросам защиты данных, рекомендовать эффективные стратегии', 'is_correct': False},
    {'question_id': 20, 'text': 'Создавать объёмные модели объектов, персонажей, зданий, техники — всего, что можно представить в объеме. Добавлять реалистичности и эстетики', 'is_correct': False},
    {'question_id': 20, 'text': 'Продумывать музыкальное наполнение: фоновая музыка в игре, подбор звука шагов, скрипа пола, сигнала предупреждения об опасности и т.п.', 'is_correct': False},
    {'question_id': 20, 'text': 'Проектировать сайты, встраивать в них аудио и видео, создавать страницы', 'is_correct': False},
    {'question_id': 20, 'text': 'Оценивать, какие современные технологии могут принести пользу бизнесу, и внедрять их', 'is_correct': False},
]

# Сохранение ответов в базе данных
for answer in answers:
    question = Question.objects.get(id=answer['question_id'])
    AnswerOption.objects.create(
        question=question,
        option_text=answer['text'],
        is_correct=answer['is_correct']
    )