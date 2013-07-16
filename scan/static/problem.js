$(function(){
    $('input[name="type"]:radio').change(remakeAutoForm);
    $('#edit-problem').submit(function(){
        setOption();
        setResult();
    });
    remakeAutoForm();
    restoreForm();
});

function remakeAutoForm(){
    $('#autoform').remove();
    switch($('input[name="type"]:checked').val()){
        case '0': // RadioButton
            var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('選択肢:'))
                .append(generateChoiceTable('radio'))
                .append($('<p id="add-choice">').append($('<input>').attr({type:'button',value:'+',class:'btn',onclick:'addChoice(\'radio\')'})));
            break;
        case '1': // CheckBox
            var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('選択肢:'))
                .append(generateChoiceTable('checkbox'))
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
}

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

function removeChoice(num){
    $('#choices>tbody').children()[num-1].remove();
    renumber();
}

function renumber(){
    $('#choices>tbody>tr').each(function(i){
        $(this).children('td:first').text('#'+(i+1));
        $(this).find('input.remove-choice').attr('onclick','removeChoice('+(i+1)+')');
    });
}

function setOption(){
    switch($('input[name="type"]:checked').val()){
        case '0': // RadioButton
        case '1': // CheckBox
            var param = new Array();
            $('#choices input[type="text"]').each(function(){param.push($(this).val())});
            $('textarea[name="option"]').val(JSON.stringify(param));
            break;
    }
}

function setResult(){
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
            $('textarea[name="result"]').val($('#autoform input').val());
            break;
        case '3': // Textarea
            $('textarea[name="result"]').val($('#autoform textarea').val());
            break;
    }
}

function restoreForm(){
    restoreOption();
    restoreResult();
}

function restoreOption(){
    type = $('input[name="type"]:checked').val();
    if (type=='0'||type=='1'){
        var param = JSON.parse($('textarea[name="option"]').val())
        if (type=='0')
            adjustNumberOfOptions('radio',param.length);
        if (type=='1')
            adjustNumberOfOptions('checkbox',param.length);
        inputs = $('#choices input[type="text"]');
        for (var i = 0; i < param.length; i++){
            inputs.eq(i).val(param[i]);
        }
    }
}

function adjustNumberOfOptions(input_type,num){
    var len = $('#choices>tbody').children().length;
    if (len < num){
        for (var i = 0; i < num - len; i++){
            addChoice(input_type);
        }
    }else if(len > num){
        for (var i = 0; i < len - num; i++){
            removeChoice(0);
        }
    }
}

function restoreResult(){
    switch($('input[name="type"]:checked').val()){
        case '0': // RadioButton
            var pos = $('textarea[name="result"]').val();
            $('#choices input[type="radio"]').eq(pos).prop('checked', true);
            break;
        case '1': // CheckBox
            var param = JSON.parse($('textarea[name="result"]').val());
            for (var i = 0; i < param.length; i++){
                $('#choices input[type="checkbox"]').eq(parseInt(param[i])).prop('checked', true);
            }
            break;
        case '2': //Text
            $('#autoform input').val($('textarea[name="result"]').val());
            break;
        case '3': // Textarea
            $('#autoform textarea').val($('textarea[name="result"]').val());
            break;
    }
}
