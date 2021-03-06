
$.fn.checkbox = function ()
{
    return this.each(function(i, input, switcher, stick, overlay, touched, to)
    {
        input = $(this);
        if(!input[0].workon_checkbox && input.is('input[type="checkbox"]'))
        {
            touched = null;
            inner = false;
            switcher = $('<span class="workon-checkbox"></span>');
            switcher[input.is(':checked') ? 'addClass':'removeClass']('checked');
            stick = $('<span class="workon-checkbox-stick"></span>');
            overlay = $('<span></span>').css({ position:'fixed', top:0, left:0, bottom:0, right: 0, width: '100%', height: '100%' }).hide();
            switcher.append(stick);
            switcher.append(overlay);
            input.after(switcher).hide();
            input[0].workon_checkbox = true;

            /** WORKON FORMSET CROSS INTEGRATION **/
            $(input[0].form).find('label[for$="DELETE"] .workon-checkbox').addClass('red');

            switcher.on('click', function(e)
            {
                e.preventDefault();
                e.stopPropagation();
            });

            input.on('change', function()
            {
                switcher[input.is(':checked') ? 'addClass':'removeClass']('checked');
            });

            switcher.on('mousedown', function (e)
            {
                overlay.show();
                touched = {
                    x: e.clientX,
                    w: switcher.width(),
                    x2: stick.position().left,
                    w2: stick.width(),
                }
                stick.css('transition', 'none');
                e.stopPropagation();
            });
            $(document).on('mousemove', function (e)
            {
                if(touched)
                {
                    e.preventDefault();
                    var diff = e.clientX - touched.x;
                    touched.nx = Math.max(touched.w2, Math.min(touched.w, touched.x2+diff));
                    stick.css({ left: touched.nx });
                    e.stopPropagation();
                    return false;
                }
            });
            $(document).on('mouseup', function (e)
            {
                if(touched)
                {
                    var diff = Math.abs(e.clientX - touched.x);
                    var way = touched.nx / touched.w;
                    if(diff > 2)
                    {
                        if(way > 0.7)
                        {
                            input.prop('checked', true);
                            try { input.trigger('change'); } catch(e) {}
                        }
                        else
                        {
                            input.prop('checked', false);
                            try { input.trigger('change'); } catch(e) {}
                        }
                    }
                    else
                    {
                        input.prop('checked', !input.prop('checked'));
                        try { input.trigger('change'); } catch(e) {}
                    }
                    touched = null;
                    stick.css({ left: '' });
                    stick.css('transition', '');
                    overlay.hide();
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }
            });
        }
    });
};