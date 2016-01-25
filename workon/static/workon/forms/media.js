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
            console.log(self)
            $(self).find('input[type=checkbox]').eq(0).prop('checked', true);
            $(self).removeClass('image embed');
            $(self).addClass('empty');
            return false;
        })

        $(this).on('workon.media_dropzone_deposed', function(e, media, file, embed)
        {
            //console.log('media deposed', media, file, embed)
            if(file)
            {
                $(self).find('.workon-media_input-preview').html('<img class="img-responsive" src="'+file+'"/>').css({
                    backgroundImage: 'url(' + file + ')'
                });
                $(self).find('.workon-media_input-media').addClass('active');
                $(self).find('.workon-media_input-empty').removeClass('active');
                $(self).find('input[type=checkbox]').eq(0).prop('checked', false);
            }
            else if(embed)
            {
                $(self).find('input[type=checkbox]').eq(0).prop('checked', false);

                $(self).find('.workon-media_input-preview').html(embed).css({
                    backgroundImage: ''
                });
                $(self).find('.workon-media_input-media').addClass('active');
                $(self).find('.workon-media_input-empty').removeClass('active');
            }
        });




    });



});