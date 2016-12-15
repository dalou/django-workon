
(function ( $, EMBED_TYPES ) {

    EMBED_TYPES =
    {
        "soundcloud": [
            [
                "(http[s]?\\:\\/\\/w\\.soundcloud\\.com\\/player\\/\\?url=([^\"]+))",
                "<iframe class=\"workon-media\" src=\"https://w.soundcloud.com/player/?url=\\2\" scrolling=\"no\" frameborder=\"no\" allowfullscreen></iframe>"
            ],
            [
                "(http[s]?\\:\\/\\/soundcloud\\.com\\/[\\d\\w\\-_]+/[\\d\\w\\-_]+)",
                "<iframe class=\"workon-media\" src=\"https://w.soundcloud.com/player/?url=\\1\" scrolling=\"no\" frameborder=\"no\" allowfullscreen></iframe>"
            ]
        ],
        "youtube": [
            [
                "(https?://)?(www\\.)?(youtube|youtu|youtube-nocookie)\\.(com|be)/(watch\\?v=|embed/|v/|.+\\?v=)?([^&=%\\?\\s\"]{11})",
                "<iframe class=\"workon-media\" src=\"https://www.youtube.com/embed/\\6?controls=0&amp;showinfo=0\"scrolling=\"no\" frameborder=\"no\" allowfullscreen></iframe>"
            ]
        ],
        'vimeo': [
            [
                "(http[s]?\\:\\/\\/(player\\.)?vimeo\\.com\\/([\\/\\w]+)\\/([\\d]+))",
                '<iframe class="workon-media" src="https://player.vimeo.com/video/\\4" scrolling="no" frameborder="no" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
            ]
        ]
    }

    $.fn.strToEmbed = function(str, authorizedTypes)
    {
        var embed_value = null;

        for(var type in EMBED_TYPES)
        {
            var patterns = EMBED_TYPES[type];
            for(var i in patterns)
            {
                var regex = new RegExp(patterns[i][0], 'gi');
                var result = str.match(regex)
                console.log(str, regex.exec(str))
                if(result)
                {
                    if(
                        !authorizedTypes ||
                        $.inArray(type, authorizedTypes)
                    )
                    {
                        embed_value = result[0].replace(regex, patterns[i][1].replace('\\', '$'));
                    }
                    else
                    {
                        embed_value = null;
                    }
                    break;
                }
            }
        }
        return embed_value;
    }
}( jQuery ));
