$(document).ready(function() {
    // Обработчик формы регистрации
    $('#register-form').on('submit', function(e) {
        e.preventDefault(); // Отменяем стандартную отправку формы

        var formData = $(this).serialize(); // Сериализуем данные формы
        var csrfToken = $('input[name="csrfmiddlewaretoken"]', this).val(); // Получаем токен CSRF

        $.ajax({
            type: 'POST',
            url: '/register/', // URL для регистрации
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    window.location.href = response.redirect_url; // Перенаправляем пользователя
                } else {
                    $('#response-message').html('<div class="alert alert-danger">' + response.errors + '</div>');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error(textStatus, errorThrown);
            }
        });
    });

    // Обработчик формы входа
    $('#login-form').on('submit', function(e) {
        e.preventDefault(); // Отменяем стандартную отправку формы

        var formData = $(this).serialize(); // Сериализуем данные формы
        var csrfToken = $('input[name="csrfmiddlewaretoken"]', this).val(); // Получаем токен CSRF

        $.ajax({
            type: 'POST',
            url: '/login/', // URL для входа
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    window.location.href = response.redirect_url; // Перенаправляем пользователя
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