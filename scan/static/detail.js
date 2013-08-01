$(function(){
    positions = {}
    $('.score-distribution').append((function(a){for(var i=0;i<$('.score-distribution>table>tbody>tr').size();i++){a.append($('<li>').text(i).css('z-index', $('.score-distribution>table>tbody>tr').size() - i))}return a})($('<ul class="meter-list">')));
    $('.score-distribution .meter-list li').each(function(i){
        $(this).animate({
            top: (json_param['scale_height'] + json_param['scale_offset'] - parseFloat($('.score-distribution>table>tbody>tr').eq(i).find('td:nth-of-type(4)').text()) * json_param['scale_height'] / parseFloat(json_param['max_score']) - 15.0) + 'px'
        }, 1000);
    });
    $('.score-distribution>table>tbody>tr').each(function(i){
        $(this).animate({
            top: calculatePosition(i,$(this).find('td:nth-of-type(4)').text()) + 'px'
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
                $(this).find('table').css('display','inline-block');
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

function calculatePosition(i,point){
    target = json_param['scale_height'] + json_param['scale_offset'] - parseFloat(point) * json_param['scale_height'] / parseFloat(json_param['max_score']) - 15.0;
    if (positions[i-1] && target - positions[i-1]< 42) {
        target = positions[i-1] + 42;
    }
    positions[i] = target;
    return target;
}
