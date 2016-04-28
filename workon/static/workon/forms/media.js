$(document).ready(function() {



    $(document).on('mouseenter', '.workon-media_input', function(self)
    {
        if(this.workon_media_input === true)
        {
            return;
        }
        this.workon_media_input = true;
        self = this;

        $(this).on('click', '.workon-media_input-clear', function(e)
        {
            $(self).find('input[type=checkbox]').eq(0).prop('checked', true);
            $(self).removeClass('image embed');
            $(self).addClass('empty');
            return false;
        })

        $(this).on('workon.media_dropzone_deposed', function(e, media, file, embed)
        {
            console.log('media deposed', media, file, embed)
            if(file)
            {
                $(self).find('.workon-media_input-preview').html('<img class="img-responsive" src="'+file+'"/>').css({
                    backgroundImage: 'url(' + file + ')'
                });
                $(self).find('.workon-media_input-media').addClass('active');
                $(self).find('.workon-media_input-empty').removeClass('active');
                $(self).find('input[type=checkbox]').eq(0).prop('checked', false);
                $(self).find('.workon-media_input-inputs input').attr('name', $(this).data('name'));
                $(self).find('.workon-media_input-inputs textarea').removeAttr('name');
            }
            else if(embed)
            {
                $(self).find('input[type=checkbox]').eq(0).prop('checked', false);

                $(self).find('.workon-media_input-preview').html(embed).css({
                    backgroundImage: ''
                });
                $(self).find('.workon-media_input-media').addClass('active');
                $(self).find('.workon-media_input-empty').removeClass('active');
                $(self).find('.workon-media_input-inputs textarea').val(embed).attr('name', $(this).data('name'));
                $(self).find('.workon-media_input-inputs input').removeAttr('name');
            }
        });




    });
    $('[data-media-dropzone]').mediaDropzone()


});