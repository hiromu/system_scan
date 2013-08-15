$(function(){
    $('body').append($('<div>').attr({id:'figure-dialog'}));
});

function showFigureDialog(t){
    $('#figure-dialog').empty();
    $('#figure-dialog').append($('<img>').attr({src:$(t).find('img').attr('src'),alt:$(t).find('figcaption').text()}));
    $('#figure-dialog').dialog({
        title: $(t).find('figcaption').text(),
        closeOnEscape: true,
        modal: true,
        width: 'auto',
        height: 'auto',
    });
}
