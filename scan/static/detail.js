$(function(){
    $('.score-distribution>table>tbody>tr').each(function(){
        $(this).animate({
            top: (840.0 - parseFloat($(this).find('td:nth-of-type(4)').text()) * 800.0 / parseFloat($('#summary-max-score').val()) - 20.0) + 'px'
        }, 1000);
    });
});

