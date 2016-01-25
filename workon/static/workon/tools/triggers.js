var NAVIGATOR_IS_MOBILE = (/android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase()));

if (!String.prototype.endsWith) {
  String.prototype.endsWith = function(searchString, position) {
    var subjectString = this.toString();
    if (typeof position !== 'number' || !isFinite(position) || Math.floor(position) !== position || position > subjectString.length) {
      position = subjectString.length;
    }
    position -= searchString.length;
    var lastIndex = subjectString.indexOf(searchString, position);
    return lastIndex !== -1 && lastIndex === position;
  };
}




$(document).ready(function(menuTo, select)
{
    $('[data-share]').each(function(i, self)
    {
        self = $(this);
        self.tooltipster({
            trigger: 'click',
            interactive: true,
            content: self.next().find('.share')
        });
    });
});


