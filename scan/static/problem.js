$(function(){
    $('input[name="type"]:radio').change(function(){
        $('#autoform').remove();
        switch($(this).val()){
            case '0': // RadioButton
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('選択肢:'))
                    .append(generateChoiceTable('radio'))
                    .append($('<p id="add-choice">').append($('<input>').attr({type:'button',value:'+',class:'btn',onclick:'addChoice(\'radio\')'})));
                break;
            case '1': // CheckBox
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('選択肢:'))
                    .append(generateChoiceTable('checkbox'))
                    .append($('<p id="add-choice">').append($('<input>').attr({type:'button',value:'+',class:'btn',onclick:'addChoice(\'radio\')'})));
                break;
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

function generateChoiceTable(input_type){
    return $('<table>').attr({id:'choices'})
            .append($('<thead>').append($('<tr>').append($('<th>').text('番号')).append($('<th>').text('正解')).append($('<th>').text('選択肢')).append($('<th>').text('削除'))))
            .append($('<tbody>').append(generateChoiceRow(input_type,1)).append(generateChoiceRow(input_type,2)));
}

function generateChoiceRow(input_type, num){
    return $('<tr>')
            .append($('<td>').text('#'+num))
            .append($('<td>').append($('<input>').attr({type:input_type,name:input_type+'-result'})))
            .append($('<td>').append($('<input>').attr({type:'text'})))
            .append($('<td>').append($('<input>').attr({type:'button',value:'-',class:'btn btn-warning remove-choice',onclick:'removeChoice('+(num)+')'})));
}

function addChoice(input_type){
    var len = $('#choices>tbody').children().length;
    $('#choices>tbody').append(generateChoiceRow(input_type,len+1));
}

function removeChoice(num) {
    $('#choices>tbody').children()[num-1].remove();
    renumber();
}

function renumber() {
    $('#choices>tbody>tr').each(function(i){
        $(this).children('td:first').text('#'+(i+1));
        $(this).find('input.remove-choice').attr('onclick','removeChoice('+(i+1)+')');
    });
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
