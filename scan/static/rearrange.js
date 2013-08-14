$(function(){
    $('#rearrange-table tbody').sortable({helper: helper, cursor: "move", opacity: 0.5});
    $('#post-sequence').submit(function(event){
        sequence = {}
        $('#rearrange-table tbody tr').each(function(i){
            sequence[$(this).find('td:nth-of-type(4)').text()] = i + 1;
        });
        $('#post-sequence input[name="sequence"]').val(JSON.stringify(sequence));
    });
});

function helper(e, tr){
    var origs = tr.children();
    var helper = tr.clone();
    helper.children().each(function(index) {
        $(this).width(origs.eq(index).width());
    });
    return helper;
}
