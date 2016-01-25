$(document).ready(function() {

    $(document).on('click', '.workon-icon-widget-tabs-control', function() {
        var target = $($(this).attr('href'));
        var visible = target.is(':visible');
        $(this).parents('.workon-icon-widget-tabs').eq(0).find('.workon-icon-widget-tabs-content').hide();

        if(!visible) {
            $($(this).attr('href')).show();
        }
        return false;
    })

    $(document).on('click', '.workon-icon-widget', function() {
         $('.workon-icon-widget.active').removeClass('active')
         $(this).addClass('active');
         $($(this).data('input')).val($(this).data('value'))
    });
});