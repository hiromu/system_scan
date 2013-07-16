$(function(){
    $('input[name="type"]:radio').change(function(){
        $('#autoform').remove();
        switch ($(this).val()){
            case '0': // RadioButton
                var li = function(num){
                    return $('<li>').attr({class:'clearfix'}).append($('<label>').text('#'+num))
                    .append($('<input>').attr({type:'text'}))
                    .append($('<input>').attr({type:'radio',name:'radio-result'}))
                }
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('選択肢:'))
                    .append($('<ul>').attr({id:'choices'})
                        .append(li(1)).append(li(2)));
                break;
            case '1': // CheckBox
                var li = function(num){
                    return $('<li>').attr({class:'clearfix'}).append($('<label>').text('#'+num))
                    .append($('<input>').attr({type:'text'}))
                    .append($('<input>').attr({type:'checkbox',name:'checkbox-result'}))
                }
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('選択肢:'))
                    .append($('<ul>').attr({id:'choices'})
                        .append(li(1)).append(li(2)));
                break;
            case '2': //Text
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('正解:'))
                    .append($('<p>').append($('<input>').attr({type:'text'})));
                break;
            case '3': //Textarea
                var elm = $('<div>').attr({id:'autoform'}).append($('<p>').text('正解:'))
                    .append($('<p>').append($('<textarea>')));
                break;
        }
        $('#action-buttons').before($(elm));
    });
});

