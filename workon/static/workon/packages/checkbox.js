$(document).ready(function(map, oldMarginTop)
{
    $(document).on('click', '.checkbox', function(e)
    {
        var $input = $(this).find('input');
        var checked = $input.is(':checked');
        $input.prop('checked', !checked);
        $(this)[checked ? 'removeClass':'addClass']('checked');
        $input.trigger('change');
        e.stopPropagation();
        return false;
    });
    $.fn.check = function() {
        $(this).find('input').prop('checked', true);
        $(this).addClass('checked');
    }
    $.fn.uncheck = function() {
        $(this).find('input').prop('checked', false);
        $(this).removeClass('checked');
    }

    $('.checkbox input:checked').parents('.checkbox').addClass('checked')
});