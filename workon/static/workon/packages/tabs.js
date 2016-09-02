window.workon_packages_tabs = true;


function workon_tabs_active(href) {
    var target = $(href);
    if(!target.length) target = $('#'+href);
    if(target.length)
    {
        // self.siblings("[href]").removeClass('active');
        self.parents('.tabs').eq(0).find('.active').removeClass('active');
        target.siblings("[id]").removeClass('active');
        self.addClass('active');
        target.addClass('active');
        self.trigger('workon.tabs_changed', [ self, target ]);
        document.location.hash = href;
        return false;
    }
}

$(document).on('click', '[data-tabs] [href]', function(e, self)
{
    self = $(this)
    var href = self.attr('href').split('#', 2);
    if(href.length == 2)
    {
        href = '#'+href[1];
        var target = $('[data-tabs="'+href.replace( /^#/, '')+'"]');
        if(!target.length) target = $('[data-tabs-id="'+href.replace( /^#/, '__')+'"]');
        if(!target.length) target = $(href.replace( /^#/, '#__' ));
        if(!target.length) target = $(href);

        if(target.length)
        {
            self.parents('[data-tabs]').eq(0).find('.active').removeClass('active');
            target.siblings("[id],[data-tabs]").removeClass('active');
            self.addClass('active');
            target.addClass('active');
            self.trigger('workon.tabs_changed', [ self, target ]);

            target.parents("[data-tabs]").each(function()
            {
                console.log(this)
                var tabId = $(this).data('tabs');
                $(this).addClass('active');
                $('[href="#'+tabId+'"]').addClass('active');

            })

            document.location.hash = href;
            return false;
        }
    }
})
$(document).ready(function()
{

    var hash = document.location.hash;
    if(hash) {
        $('[data-tabs] [href$="'+hash+'"]').click();
    }
    // $(window).resize(function()
    // {
    //     $tabs.each(function($self, maxHeight) {
    //         $self = $(this);
    //         maxHeight = 0;
    //         $self.find('.tab').height('auto').each(function() {
    //             maxHeight = Math.max(maxHeight, $(this).height());
    //         }).height(maxHeight);
    //     })
    // });
    // $(window).resize();

});