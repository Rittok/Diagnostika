$(document).ready(function() {
    $('.ajax-button').click(function(e) {
        e.preventDefault(); // Предотвращение обычной отправки формы

        var form = $(this).closest('form'); // находим ближайшую родительскую форму
        var actionUrl = form.attr('action'); // URL формы
        var formData = form.serialize();     // сериализованные данные формы
        var csrfToken = $('input[name="csrfmiddlewaretoken"]', form).val(); // токен CSRF

        $.ajax({
            type: 'POST',
            url: actionUrl,
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                window.location.href = "{% url 'primary_test:diagnostic_results' %}";
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error(textStatus, errorThrown);
            }
        });
    });
});

$(document).ready(function() {
    // Обработчик отправки формы первого блока
    $('#block1-test-form').on('submit', function(e) {
        e.preventDefault(); // Отменяем стандартную отправку формы

        var formData = $(this).serialize(); // Данные формы
        var csrfToken = $('input[name="csrfmiddlewaretoken"]', this).val(); // Токен CSRF

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'), // Текущий URL формы
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    $('#response-message').html('<div class="alert alert-success">' + response.message + '</div>');
                } else {
                    $('#response-message').html('<div class="alert alert-danger">' + response.errors + '</div>');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error(textStatus, errorThrown);
            }
        });
    });

    // Аналогично для второго блока
    $('#block2-test-form').on('submit', function(e) {
        e.preventDefault(); // Отменяем стандартную отправку формы

        var formData = $(this).serialize(); // Данные формы
        var csrfToken = $('input[name="csrfmiddlewaretoken"]', this).val(); // Токен CSRF

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'), // Текущий URL формы
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    $('#response-message').html('<div class="alert alert-success">' + response.message + '</div>');
                } else {
                    $('#response-message').html('<div class="alert alert-danger">' + response.errors + '</div>');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error(textStatus, errorThrown);
            }
        });
    });
});