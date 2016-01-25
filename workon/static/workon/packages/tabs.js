window.workon_packages_tabs = true;

$(document).on('click', '[data-tabs] [href]', function(self)
{
    self = $(this)
    var href = self.attr('href');
    if(href[0] == "#")
    {
        var target = $(href);
        if(target.length)
        {
            self.siblings("[href]").removeClass('active');
            target.siblings("[id]").removeClass('active');
            self.addClass('active');
            target.addClass('active');
            self.trigger('workon.tabs_changed', [ self, target ])
            return false;
        }
    }
})
// $(document).ready(function()
// {
//     // $(window).resize(function()
//     // {
//     //     $tabs.each(function($self, maxHeight) {
//     //         $self = $(this);
//     //         maxHeight = 0;
//     //         $self.find('.tab').height('auto').each(function() {
//     //             maxHeight = Math.max(maxHeight, $(this).height());
//     //         }).height(maxHeight);
//     //     })
//     // });
//     // $(window).resize();

// });