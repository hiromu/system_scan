function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function editPoint(url, self) {
    point = $(self).text();
    $(self).empty();
    $(self).removeAttr('onclick');
    $(self).append($('<input>').attr({ type: 'text', value: point, size: 5 }));
    $(self).find('input').keypress(function (e) {
        if (e.which == 13) {
            updatePoint(url, $(this).val(), this);
        }
    });
}

function updatePoint(url, point, self){
    $.ajax({
        url: url,
        type: 'POST',
        data: {point: point},
        dataType: 'json',
        success: function (data) {
            if (data.status == 'success') {
                parent = $(self).parent();
                parent.empty();
                parent.text(point);
            }
        }
    });
}