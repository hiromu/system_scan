$(function(){
    $('input[name="type"]:radio').change(function(){
        $('#autoform').remove();
        switch($(this).val()){
            case '0': // RadioButton
                var li = function(num){
                    return $('<li>').attr({class:'clearfix'}).append($('<label>').text('#'+num))
                    .append($('<input>').attr({type:'text'}))
                    .append($('<input>').attr({type:'radio',name:'radio-result'}))
                }
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('選択肢:'))
                    .append($('<ul>').attr({id:'choices'})
                        .append(li(1)).append(li(2)))
                        .append($('<p id="add-choice">').append($('<input>').attr({type:'button',value:'+',class:'btn',onclick:'addChoice(\'radio\')'})));
                break;
            case '1': // CheckBox
                var li = function(num){
                    return $('<li>').attr({class:'clearfix'}).append($('<label>').text('#'+num))
                    .append($('<input>').attr({type:'text'}))
                    .append($('<input>').attr({type:'checkbox',name:'checkbox-result'}))
                }
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('選択肢:'))
                    .append($('<ul>').attr({id:'choices'})
                        .append(li(1)).append(li(2)))
                        .append($('<p id="add-choice">').append($('<input>').attr({type:'button',value:'+',class:'btn',onclick:'addChoice(\'checkbox\')'})));
                break;
            case '2': // Text
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('正解:'))
                    .append($('<p>').append($('<input>').attr({type:'text'})));
                break;
            case '3': // Textarea
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('正解:'))
                    .append($('<p>').append($('<textarea>')));
                break;
        }
        $('#action-buttons').before($(elm));
    });
    $('#edit-problem').submit(function(){
        setOption();
        setResult();
    });
});

function addChoice(input_type){
    var len = $('#autoform ul').children().length;
    $('#autoform ul').append(
        $('<li>').attr({class:'clearfix'}).append($('<label>').text('#'+(len+1)))
            .append($('<input>').attr({type:'text'}))
            .append($('<input>').attr({type:input_type,name:input_type+'-result'}))
    );
}

function setOption() {
    switch($('input[name="type"]:checked').val()){
        case '0': // RadioButton
        case '1': // CheckBox
            var param = new Array();
            $('#choices input[type="text"]').each(function(){param.push($(this).val())});
            $('textarea[name="option"]').val(JSON.stringify(param));
            break;
    }
}

function setResult() {
    switch($('input[name="type"]:checked').val()){
        case '0': // RadioButton
            $('#choices input[type="radio"]').each(function(i){if($(this).is(':checked')){$('textarea[name="result"]').val(i)}});
            break;
        case '1': // CheckBox
            var param = new Array();
            $('#choices input[type="checkbox"]').each(function(i){if($(this).is(':checked')){param.push(i)}});
            $('textarea[name="result"]').val(JSON.stringify(param));
            break;
        case '2': // Text
            $('textarea[name="result"]').val(('#autoform input').val())
            break;
        case '3': // Textarea
            $('textarea[name="result"]').val(('#autoform textarea').val())
            break;
    }
}
