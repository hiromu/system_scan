$(function(){
    switch($('#id_type').val()) {
        case '0':
            $('.answer li').eq($('#id_result').val()).addClass('suggested');
            break;
        case '1':
            var param = JSON.parse($('#id_result').val());
            for (var i = 0; i < param.length; i++){
                $('.answer li').eq(parseInt(param[i])).addClass('suggested');
            }
            break;
            break;
    }
});
