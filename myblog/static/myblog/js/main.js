function vote() {
    const v = $(this)
    const type = v.data('type');
    const pk = v.data('id');
    const action = v.data('action');

    $.ajax({
        url: `/blog/${type}/${pk}/${action}`,
        type: 'POST',
        data: {'obj': pk},

        success: function (json) {
            document.querySelector(`[data-id="${pk}"][data-count="rating"]`).innerHTML = json.rating;
        }
    });

    return false;
}

// Подключение обработчиков
$(function () {
    $('[data-action="upvote"]').click(vote);
    $('[data-action="downvote"]').click(vote);
});

// Получение переменной cookie по имени
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; ++i) {
            const cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Настройка AJAX
$(function () {
    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });
});
