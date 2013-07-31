$(function(){
    $('.score-distribution>table>tbody>tr').each(function(){
        $(this).animate({
            top: (json_param['scale_height'] + json_param['scale_offset'] - parseFloat($(this).find('td:nth-of-type(4)').text()) * json_param['scale_height'] / parseFloat(json_param['max_score']) - 20.0) + 'px'
        }, 1000);
    });

    $('.category-summary').each(function(){
        $(this).find('table').hide();
        $(this).find('i.category').removeClass('icon-chevron-up');
        $(this).find('i.category').addClass('icon-chevron-down');
    });

    $('.category-summary').click(function(data, handler){
        if ($(this).find('table').has(data.target).length == 0) {
            if ($(this).find('table').is(':hidden')) {
                $(this).find('table').css('display','block');
                $(this).find('i.category').removeClass('icon-chevron-down');
                $(this).find('i.category').addClass('icon-chevron-up');
            } else {
                $(this).find('table').hide();
                $(this).find('i.category').removeClass('icon-chevron-up');
                $(this).find('i.category').addClass('icon-chevron-down');
            }
        }
    });
});
