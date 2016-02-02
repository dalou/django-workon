function graphOptionsIter(object) {
    if (typeof(object) === 'object') {
        for(var prop in object){
            if (typeof(object[prop]) === 'string') {
                var str = object[prop];
                var fct_type = '{function}::';
                if(str.substr(0, fct_type.length) == fct_type) {
                    var fct_str = str.substr(fct_type.length, str.length);
                    object[prop] = new Function(fct_str);
                }
            }
            else {
                graphOptionsIter(object[prop]);
            }
        }
    }
}
function showAreaGraph($graph, options)
{
    options = $graph.data('highchart')
    graphOptionsIter(options);
    var chartsName = $graph.data('series-name') ? $graph.data('series-name') : '';
    //var chartsCatsData = $graph.data('series-data');
    if(options.height) {
        $graph.css({ height: options.height }, 200);
    }
    if(!('chart' in options)) {
        options['chart'] = {};
    }
    if(options.chart.type == "text") {

    }
    else {
        options.credits = { enabled: false };
        options.chart['renderTo'] = $graph[0];
        new Highcharts.Chart(options);
    }
    // $('tspan:contains(Highcharts.com)').remove();
}

function hexToRGBOpacity(h, opacity) {
    return 'rgba('+hexToR(h)+','+hexToG(h)+','+hexToB(h)+','+opacity+')';
}
function hexToR(h) {return parseInt((cutHex(h)).substring(0,2),16)}
function hexToG(h) {return parseInt((cutHex(h)).substring(2,4),16)}
function hexToB(h) {return parseInt((cutHex(h)).substring(4,6),16)}
function cutHex(h) {return (h.charAt(0)=="#") ? h.substring(1,7):h}

function traceGraphs() {
    $('[data-highchart]').each(function(id, $this) {
        id = $(this).data('chart')

        if(window.workon_packages_loading)
        {
            $(this).addLoading();
        }
        showAreaGraph($(this));
        if(window.workon_packages_loading)
        {
            $(this).removeLoading();
        }
    })
}
// $(window).resize(function() {
//     traceGraphs();
// });
$(document).ready(function() {
    setTimeout(function() {
        traceGraphs();
    }, 500);
    $('[data-highchart]').addClass('app loading')
});