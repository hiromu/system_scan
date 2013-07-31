$(function(){
    $('.score-distribution>table>tbody>tr').each(function(){
        $(this).animate({
            top: (840.0 - parseFloat($(this).find('td:nth-of-type(4)').text()) * 800.0 / parseFloat($('#summary-max-score').val()) - 20.0) + 'px'
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
                $(this).find('table').show();
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
