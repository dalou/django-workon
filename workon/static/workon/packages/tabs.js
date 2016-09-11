window.workon_packages_tabs = true;


function workon_tabs_active(href)
{
    workon_tabs_hash_active(href);
}

function workon_tabs_hash_active(hash)
{
    var trigger = $('[data-tabs] [href$="'+hash+'"]');
    if(trigger.length)
    {
        var target = $('[data-tabs="'+hash.replace( /^#/, '')+'"]');
        if(!target.length) target = $('[data-tabs-id="'+hash.replace( /^#/, '__')+'"]');
        if(!target.length) target = $(hash.replace( /^#/, '#__' ));
        if(!target.length) target = $(hash);

        if(target.length)
        {
            trigger.parents('[data-tabs]').eq(0).find('.active').removeClass('active');
            target.siblings("[id],[data-tabs]").removeClass('active');
            trigger.addClass('active');
            target.addClass('active');
            trigger.trigger('workon.tabs_changed', [ trigger, target ]);

            var parent = target.parents("[data-tabs]").eq(0);
            if(parent.length)
            {
                workon_tabs_hash_active('#'+parent.data('tabs'));
            }
        }
    }
}

$(document).on('click', '[data-tabs] [href]', function(e, self)
{
    self = $(this)
    var href = self.attr('href').split('#', 2);
    if(href.length == 2)
    {
        var hash = '#'+href[1];
        workon_tabs_hash_active(hash);
        document.location.hash = hash;
        return false;
    }
})
$(document).ready(function()
{

    var hash = document.location.hash;
    if(hash) {
        workon_tabs_hash_active(hash);
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