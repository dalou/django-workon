(function ($) {

    // Register callbacks to perform after inline has been added
    WorkonAdmin.after_inline = function () {
        var functions = {};
        var register = function (fn_name, fn_callback) {
            functions[fn_name] = fn_callback;
        };

        var run = function (inline_prefix, row) {
            for (var fn_name in functions) {
                functions[fn_name](inline_prefix, row);
            }
        };

        return {
            register: register,
            run: run
        };
    }();


    WorkonAdmin.date_picker = (function () {
        var lang = document.documentElement.getAttribute('lang');
        var picker_lang_map = {
            'pt-br': 'pt-BR',
            'zh-cn': 'zh-CN',
            'zh-tw': 'zh-TW'
        };
        if (lang.length > 2) {
            var picker_lang = picker_lang_map[lang];
            if (picker_lang) {
                lang = picker_lang
            } else {
                lang = lang.substr(0, 2);
            }
        }
        if ($.fn.datepicker) {
            $.extend($.fn.datepicker.defaults, {
                format: 'yyyy-mm-dd',
                autoclose: true,
                todayBtn: 'linked',
                todayHighlight: true,
                language: lang
            });
        }

        function update() {
            var selector = arguments[0];
            if ($.fn.datepicker) {
                $(selector ? selector : '.input-group.date').datepicker({
                    //weekStart: 1,
                });
            }
        }

        return {
            update: update
        }
    })();

    // Backwards compatiblity
    SuitAfterInline = WorkonAdminInline = WorkonAdmin.after_inline;

    /**
     * Fixed submit buttons.
     */
    $.fn.workon_admin_fixed = function () {
        $(this).each(function () {
            // extra_offset: 70 (60 Footer height + 10 top offset)
            var $fixed_item = $(this),
                item_pos = $fixed_item.offset(),
                extra_offset = 50;
            $(window).bind('scroll.sl resize.sl load.sl', function (e) {
                var $win = $(this),
                    item_height = $fixed_item.height(),
                    scroll_top = $win.scrollTop()
                    ;
                if (scroll_top + $win.height() - item_height - extra_offset < item_pos.top) {
                    if (!$fixed_item.hasClass('fixed')) {
                        $fixed_item.addClass('fixed');
                    }
                } else {
                    $fixed_item.removeClass('fixed');
                }
            });

            $(window).trigger('scroll.sl');
        });
    };


    /**
     * Search filters - submit only changed fields
     */
    $.fn.workon_admin_search_filters = function () {
        $(this).change(function () {
            var $field = $(this);
            var $option = $field.find('option:selected');
            var select_name = $option.data('name');
            if (select_name) {
                $field.attr('name', select_name);
            } else {
                $field.removeAttr('name');
            }
            // Handle additional values for date filters
            var additional = $option.data('additional');
            if (additional) {
                var hidden_id = $field.data('name') + '_add';
                var $hidden = $('#' + hidden_id);
                if (!$hidden.length) {
                    $hidden = $('<input/>').attr('type', 'hidden').attr('id', hidden_id);
                    $field.after($hidden);
                }
                additional = additional.split('=');
                $hidden.attr('name', additional[0]).val(additional[1])
            }
        });
        $(this).trigger('change');
    };

    /**
     * Linked select - shows link to related item after Select
     */
    $.fn.workon_admin_linked_select = function () {

        var get_link_name = function ($select) {
            var text = $select.find('option:selected').text();
            return text && $select.val() ? text + '' : '';
        };

        var get_url = function ($add_link, $select) {
            var value = $select.val();
            return $add_link.attr('href').split('?')[0] + '../' + value + '/';
        };

        var add_link = function ($select) {
            var $add_link = $select.next().find('a').first();
            if ($add_link.hasClass('add-another')) {
                var $input_group = $add_link.parent().parent();
                var $link = $input_group.parent().find('.linked-select-link');
                if (!$link.length) {
                    $link = $('<a/>').addClass('linked-select-link btn btn-default');
                    $link.append($('<span class="glyphicon glyphicon-link"/>'));
                    $input_group.append($('<span class="input-group-btn"/>').append($link));
                }
                $link.attr('title', get_link_name($select))
                    .attr('href', get_url($add_link, $select));
            }
        };

        $(this).each(function () {
            add_link($(this));
        });

        $(document).on('change', this.selector, function () {
            add_link($(this));
        });
    };

    /**
     * Content tabs
     */
    $.fn.workon_admin_form_tabs = function () {

        var $tabs = $(this);
        var tab_prefix = $tabs.data('tab-prefix');
        if (!tab_prefix)
            return;

        var $tab_links = $tabs.find('a');

        function tab_contents($link) {
            return $('.' + tab_prefix + '-' + $link.attr('href').replace('#', ''));
        }

        function activate_tabs() {
            // Init tab by error, by url hash or init first tab
            if (window.location.hash) {
                var found_error;
                $tab_links.each(function () {
                    var $link = $(this);
                    if (tab_contents($link).find('.error').length != 0) {
                        $link.addClass('error');
                        $link.trigger('click');
                        found_error = true;
                    }
                });
                !found_error && $($tabs).find('a[href=' + window.location.hash + ']').click();
            } else {
                $tab_links.first().trigger('click');
            }
        }

        $tab_links.click(function () {
            var $link = $(this);
            $link.parent().parent().find('.active').removeClass('active');
            $link.parent().addClass('active');
            $('.' + tab_prefix).removeClass('show').addClass('hide');
            tab_contents($link).removeClass('hide').addClass('show')
        });

        activate_tabs();
    };

    /**
     * Avoids double-submit issues in the change_form.
     */
    $.fn.workon_admin_form_debounce = function () {
        var $form = $(this),
            $saveButtons = $form.find('.submit-row button'),
            submitting = false;

        $form.submit(function () {
            if (submitting) {
                return false;
            }

            submitting = true;
            $saveButtons.addClass('disabled');

            setTimeout(function () {
                $saveButtons.removeClass('disabled');
                submitting = false;
            }, 5000);
        });
    };

    $(function ()
    {
        $(".nano").nanoScroller();

        //$(document).on('click', 'li.dock-tooltip', function() {return false;})

        $(".panel-footer select").select2();

        $('.select2').each(function() {
            $(this).attr('style', $(this).attr('style').replace('width', 'min-width'))
        });

        $(document).on('mouseover', '#result_list tbody tr td, #result_list tbody tr th', function()
        {
            var header = $(this).parents('table').eq(0).find('thead th').eq($(this).index()).find('.text');
            if(header.data('tooltip'))
            {
                header.trigger('mouseover')
            }
        });
        $(document).on('mouseout', '#result_list tbody tr td, #result_list tbody tr th', function()
        {
            var header = $(this).parents('table').eq(0).find('thead th').eq($(this).index()).find('.text');
            if(header.data('tooltip'))
            {
                header.trigger('mouseout')
            }
        });


        $(document).on('mouseover', 'li.dock-tooltip > a', function(content, options)
        {
            if(this.workon_tooltip === true) { return; }
            this.workon_tooltip = true;
            var position = $(this).parent().data('tooltip-position');
            $(this).tooltipster({
                theme: 'tooltipster-default tooltipster-dock',
                position: position ? position:'right',
                interactive: true,
                contentAsHTML: true,
                trigger: 'hover',
                content: $(this).parent().find('>.dock-menu'),
                delay: 0,//10000 * $('.tooltipster-dock').length,
                autoClose: !$(this).parent().hasClass('dock-tooltip2')
            }).tooltipster('show')

        });

        $(document).on('click', '.inline-related >.panel-heading span.delete', function(e) {
            e.stopPropagation();
        })

        $(document).on('click', '.inline-related >.panel-heading', function(e, self, $fieldset) {
            self = $(this);
            $fieldset = self.next();
            if(!$fieldset.is(':visible')) {

                $fieldset.slideDown()

                self.find('.field-original_address').show()
                self.find('[data-geolocation-input]').each(function () {
                    if(this.geolocationinput) {
                        google.maps.event.trigger(this.geolocationinput, 'resize');
                    }
                })
            }
            else {
                $fieldset.slideUp()
            }
        });

        $('.inline-related').each(function(i, self) {
            if(i == 0) return;

            self = $(this).find('.panel-heading').css({
                cursor: 'pointer'
            })
            //self.find('> fieldset').slideUp()

        });

        // $('#sidebar').on('mousewheel', function() {

        //     var st = $(this).scrollTop();
        //     var hg = $(this).scrollHeight();
        //     console.log(st, hg)
        //     if(st==0)
        //     {
        //         $('#sidebar').addClass('on-top').removeClass('on-bottom')
        //     }
        //     else
        //     {
        //         $('#sidebar').addClass('on-bottom').removeClass('on-top')
        //     }
        // })

        // Fixed submit buttons
        $('.submit-row').workon_admin_fixed();

        // Show link to related item after Select
        $('.linked-select').workon_admin_linked_select();

        // Handle change list filter null values
        $('.search-filter').workon_admin_search_filters();

        // Menu toggle
        $("#menu-toggle").click(function (e) {
            e.preventDefault();
            $("#wrapper").toggleClass("toggled");
        });

        // $(window).resize(function() {
        //     $('#content').css({ top: 70 + ($('#navbar').height()-50) })
        // });
        // $('#content').css({ top: 70 + ($('#navbar').height()-50) })

        $('p.datetime input').addClass('form-control')

        // DatePicker
        WorkonAdmin.date_picker.update();

        $('#nav-expander').click(function()
        {
            $('html').toggleClass('nav-expanded')
        })
        $('#nav-expander-overlay').click(function()
        {
            $('html').removeClass('nav-expanded')
        })

        $('#nav-search-expander').click(function()
        {
            $('html').toggleClass('nav-search-expanded')
        })

        if($('#changelist-search').length) {
            $('#nav-search-form').remove()
        }


        var $tabs = $('#workon_form_tabs');
        var $mainInfos = $('.main-infos');
        var $topInfos = $('.workon-include');

        $tabs.before($mainInfos).css({ marginTop: 25 })
        $tabs.before($topInfos);

        $(document).scroll(function ()
        {
            var scroll = $(window).scrollTop();
            //var topDist = $("header").position();
            if (scroll > 0) {
                $('html').addClass('nav-scrollon');
                //$('body').css({ paddingTop: 117 });
            } else {
                $('html').removeClass('nav-scrollon');
                //$('body').css({ paddingTop: 117 });
            }
        });
        $(document).scroll();
        $('[data-tabs] [href].active').click();

        // $(window).scroll(function()
        // {
        //     var scrollTop = $(window).scrollTop();
        //     var scrollTotal = $(document).height() - $(window).height();
        //     var actions = $('#changelist-form div.actions, #changelist-form .paginator, #changelist-form div.below-actions, .changelist-save')
        //     if(scrollTop <= scrollTotal / 2) {
        //         $('#changelist-form div.results').before(actions);
        //         $('.below-actions input').css({ marginTop: 43 });
        //     }
        //     else {
        //         $('#changelist-form div.results').after(actions);
        //         $('.below-actions input').css({ marginTop: '' });
        //     }

        // });
        // $(window).scroll();


        $(document).on('mouseenter', 'form input[type=file]', function()
        {
            if(!this.better_file_upload)
            {
                this.better_file_upload = true;

                $(this).on("change", function(e)
                {
                    var files = this.files;
                    var $image = $(this).nextAll('img').eq(0);
                    if(!$image.length)
                    {
                        $image = $('<img />').attr('src', '').css(
                        {
                            width: '100%',
                            maxWidth: 300
                        });
                        $(this).after('<br />').after($image);
                    }
                    if (!files || files.length == 0)
                    {
                        return false;
                    }
                    var file = files[0],
                        imageType = /image.*/,
                        fileIsImage = true;

                    // check if this is an image
                    if ( ! file.type.match(imageType)) {
                        fileIsImage = false;
                    }
                    if ( !fileIsImage ) {

                    } else {
                        $image[0].file = file;
                        var reader = new FileReader();
                        reader.onload = (function(aImg){
                            return function(e){
                                aImg.src = e.target.result;
                            };
                        }($image[0]));

                        var ret = reader.readAsDataURL(file),
                            canvas = document.createElement("canvas");

                        ctx = canvas.getContext("2d");
                        $image[0].onload = function(){
                            ctx.drawImage($image[0], 100, 100);
                        }
                    }
                });

            }
        });


        $('p.file-upload > a').each(function()
        {
            var src = $(this).attr('href');
            if( src.toLowerCase().match(/\.(jpeg|jpg|gif|png)$/) != null )
            {
                $(this).parent().append($('<img style="display:block;"/>').attr('src', src).css({
                    maxWidth: 300
                }));
            }
        });


        $('form').attr('novalidate', '')

    });

}(WorkonAdmin.$));
