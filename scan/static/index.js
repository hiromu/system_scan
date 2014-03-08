$(function(){
    if($('#top-slider>ul>li').size() > 1) {
        $('#top-slider').easySlider({
            auto: true,
            pause: 6000,
            continuous: true,
            numeric: true,
        });
        $('#controls').addClass('btn-group');
        $('#controls').children().each(function(){$(this).addClass('btn btn-default')});
    }
});
