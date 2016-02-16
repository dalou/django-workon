window.workon_packages_form = true;

/* EVENTS

    workon.form_after_insert [data, inserted] --> Just after an ajax insert
    workon.form_data_received [data] --> Just after data ajax received

    workon.form_remove_success'  [data, removed] -->
    workon.form_remove_done'  [data, removed] ->

*/

(function($)
{
    $.unserialize = function(serializedString)
    {
        serializedString = serializedString.split("?");
        if(serializedString.length > 1)
        {
            serializedString = serializedString[1]
        }
        else {
            serializedString = serializedString[0]
        }
        var str = decodeURI(serializedString);
        var pairs = str.split('&');
        var obj = {}, p, idx, val;
        for (var i=0, n=pairs.length; i < n; i++) {
            p = pairs[i].split('=');
            idx = p[0];

            if (idx.indexOf("[]") == (idx.length - 2)) {
                // Eh um vetor
                var ind = idx.substring(0, idx.length-2)
                if (obj[ind] === undefined) {
                    obj[ind] = [];
                }
                obj[ind].push(p[1]);
            }
            else {
                obj[idx] = p[1];
            }
        }
        return obj;
    };
})(jQuery);

$(document).ready(function()
{
    window.workon_packages_form_apply_packages_on_insert = function(inserted)
    {
        if(window.workon_packages_slick === true)
        {
            $('[data-slick]').trigger('mouseenter');
        }
        if(window.workon_packages_modal === true)
        {
            $('[data-modal]').css({ cursor: 'pointer' });
        }
        if(window.workon_packages_isotope === true)
        {
            window.workon_packages_isotope_apply();
        }
        if(window.workon_packages_select === true)
        {
            window.workon_packages_select_apply();
        }
        $(document).trigger('workon.form_after_insert', [inserted]);
    }

    window.workon_packages_form_auto_fill_data = function(data)
    {
        //console.log(data, typeof data)
        if(typeof data === "object")
        {
            console.log(data)
            if(data.replace)
            {
                if(typeof data.replace !== 'array' && typeof data.replace !== 'object')
                {
                    var replaces = [data.replace]
                }
                else
                {
                    var replaces =  data.replace
                }
                for(var i in replaces)
                {
                    var html = $(replaces[i]);
                    var id = html.attr('id');
                    console.log('id',id)
                    if(id)
                    {
                        var repl = $('#'+id);
                        if(repl.length)
                        {
                            $('#'+id).replaceWith(html);
                            window.workon_packages_form_apply_packages_on_insert(html);
                            //new Switchery($('.view-publish input')[0]);
                        }
                        else
                        {
                            var id = html.attr('data-insert');
                            if(id)
                            {
                                $('#'+id).after(html);
                                window.workon_packages_form_apply_packages_on_insert(html);
                                //new Switchery($('.view-publish input')[0]);
                            }
                        }

                        var isotopes = html.parents('[data-isotopes]').eq(0);
                        if(isotopes.length)
                        {
                            var first = isotopes.find('[data-isotope]').eq(0);
                            isotopes.isotope( 'prepended', html )
                            isotopes.isotope('layout', 'packery');
                            isotopes.isotope( 'prepended', first )
                            isotopes.isotope('layout', 'packery');
                            // isotopes.isotope({
                            //   getSortData: {
                            //     order: '[data-order]',
                            //   },
                            //   sortBy: [ 'order' ]
                            // });

                        }

                    }
                }
            }
            if(window.workon_packages_notification && data.notifications)
            {
                PNotify.removeAll();
                for(var i in data.notifications) {
                    new PNotify({
                        title:  data.notifications[i][0],
                        text: data.notifications[i][1]
                    });
                }

            }
            if(data.remove)
            {
                if(data.remove[0] == "#")
                {
                    if($(data.remove[0]).length)
                    {
                        $(data.remove[0]).remove();
                    }
                }
            }
        }
        else if(typeof data === "string")
        {


        }
        if(window.workon_packages_loading == true)
        {
            $('body').removeLoading();
        }
        $(document).trigger('workon.form_data_received', [data]);
    }

    if(window.workon_packages_modal == true)
    {
        $(document).on('workon.modal_loaded', '[data-modal]', function(self, content)
        {

        });
    }

    $(document).on('submit', '[data-form-ajax]', function(self, id)
    {
        self = $(this);
        id = self.attr('id');
        var data = self.serializeArray();
        if(window.workon_packages_loading == true)
        {
            $('body').addLoading();
        }
        $.post(self.attr('action'), data, function(data)
        {
            window.workon_packages_form_auto_fill_data(data);
            $(self).trigger('workon.form_ajax_success', [data]);
            $(self).trigger('workon.form_ajax_done', [data]);
        })
        return false;
    });

    if(window.workon_packages_modal == true)
    {

        $(document).on('submit', '[data-form-modal]', function(self, id)
        {
            self = $(this);
            id = self.attr('id');
            var data = self.serializeArray();
            if(window.workon_packages_loading == true)
            {
                $('body').addLoading();
            }
            $.post(self.attr('action'), data, function(data, $data)
            {
                try
                {
                    $data = $(data);
                    if($data.find('[data-form-modal]').length)
                    {
                        var form = $data.find('[data-form-modal]')
                        self.replaceWith(form);
                        window.workon_packages_form_apply_packages_on_insert(form);
                        self.trigger('workon.form_modal_failed', [data, $data]);
                        self.trigger('workon.form_ajax_failed', [data, $data ]);
                        if(window.workon_packages_loading == true)
                        {
                            $('body').removeLoading();
                        }
                    }
                    else
                    {
                        window.workon_packages_form_auto_fill_data(data);
                        $.magnificPopup.close();
                        self.trigger('workon.form_modal_success', [data]);
                        self.trigger('workon.form_ajax_success', [data]);
                    }
                }
                catch(e)
                {
                    console.log(e)
                    self.trigger('workon.form_modal_success', [data]);
                    self.trigger('workon.form_ajax_success', [data]);
                }

                self.trigger('workon.form_modal_done', [data]);
                self.trigger('workon.form_ajax_done', [data]);

            })
            return false;
        });
    }

    $(document).on('click', '[data-update-post]', function(e, self, pk)
    {
        self = $(this);
        if(window.workon_packages_loading == true)
        {
            self.addLoading();
        }
        $.post($(this).data('update-post'), $.unserialize($(this).data('update-post')), function(data)
        {
            window.workon_packages_form_auto_fill_data(data);
            self.trigger('workon.update_post_success', [data]);
            self.trigger('workon.update_post_done', [data]);
            if(window.workon_packages_loading == true)
            {
                self.removeLoading();
            }
        });
        return false;
    });

    $(document).on('click', '[data-form-update]', function(e, self, pk)
    {
        self = $(this);
        if(window.workon_packages_loading == true)
        {
            $('body').addLoading();
        }
        $.post($(this).data('form-update'), $.unserialize($(this).data('form-update')), function(data)
        {
            window.workon_packages_form_auto_fill_data(data);
            self.trigger('workon.form_update_success', [data]);
            self.trigger('workon.form_update_done', [data]);
        });
        return false;
    });

    $(document).on('click', '[data-form-remove]', function(e, self)
    {
        self = $(this);
        if(window.workon_packages_loading == true)
        {
            $('body').addLoading();
        }
        $.get($(this).data('form-remove'), null, function(data)
        {
            window.workon_packages_form_auto_fill_data(data);
            var removed = self.parents('[id]').eq(0)
            self.trigger('workon.form_remove_success', [data, removed]);
            self.trigger('workon.form_remove_done', [data, removed]);
            removed.remove();
        });
    });
});