window.workon_packages_navigation = true;

$(document).ready(function($navs, scrollFct)
{
    $navs = $('[data-navigation]').each(function(i, self, $menu)
    {
        self = $(this);
        $menu = $('<li><a class="item"><span>'+self.data('navigation')+'</span></a></li>');
        $menu.on('click', 'a', function()
        {
            $.smoothScroll({
                scrollTarget: self,
                offset: -50
            });
        });
        $('#main-scroll-nav').append($menu);
        self[0].nav_menu = $menu;
    });

    scrollFct = function(windowHeight, scrollTop, closest, closest_depth)
    {

        windowHeight = $(window).height();
        scrollTop = $(window).scrollTop();
        // var middle = scrollTop + windowHeight/2

        closest_depth = null;
        closest = null;

        // $('#fixed-nav-social').css({ top: middle - $('#fixed-nav-social').height()/2 })
        // $('#fixed-nav').css({ top: middle - $('#fixed-nav').height()/2 })

        $navs.each(function(i, self, top, bottom)
        {
            self = $(this);
            top = self.offset().top;

            var wCenter = ( windowHeight/2 + scrollTop );
            var tCenter = (top + self.height()/2);

            //var depth = Math.abs(wCenter - tCenter)
            var depth = Math.abs((scrollTop - top) + ((scrollTop+windowHeight) - (top + self.height())))

            //console.log(self[0].nav_menu.text(), depth, scrollTop >= top)

            if(!closest_depth || ( depth <= closest_depth )  ) {
                closest = self;
                closest_depth = depth;
            }

        });

        if(closest) {
            closest[0].nav_menu.find('a').addClass('active')
            closest[0].nav_menu.siblings().find('a').removeClass('active');
        }

    }
    $(window).scroll(scrollFct);
    $(window).resize(scrollFct);
    scrollFct();
});