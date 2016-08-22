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
        var target = $(href);
        if(!target.length) target = $(href.replace( /^#/, '#__' ));
        console.log(href, target)
        if(target.length)
        {
            self.parents('[data-tabs]').eq(0).find('.active').removeClass('active');
            target.siblings("[id]").removeClass('active');
            self.addClass('active');
            target.addClass('active');
            self.trigger('workon.tabs_changed', [ self, target ]);
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