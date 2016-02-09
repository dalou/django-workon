function workonGraphOptionsIter(object) {
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
                workonGraphOptionsIter(object[prop]);
            }
        }
    }
}
function workonShowAreaGraph($graph, options)
{
    options = $graph.data('highchart')
    console.log(options)
    workonGraphOptionsIter(options);
    var chartsName = $graph.data('series-name') ? $graph.data('series-name') : '';
    //var chartsCatsData = $graph.data('series-data');
    if(options.height)
    {
        $graph.css({ height: options.height }, 200);
    }
    if(!('chart' in options))
    {
        options['chart'] = {};
    }
    if(options.chart.type == "text")
    {

    }
    else
    {
        options.credits = { enabled: false };
        options.chart['renderTo'] = $graph[0];
        new Highcharts.Chart(options);
    }
    // $('tspan:contains(Highcharts.com)').remove();
}

function workonTtraceGraphs()
{
    $('[data-highchart]').each(function(i, self)
    {
        if(window.workon_packages_loading)
        {
            $(this).addLoading();
        }
        workonShowAreaGraph($(this));
        if(window.workon_packages_loading)
        {
            $(this).removeLoading();
        }
    })
}
// $(window).resize(function() {
//     workonTtraceGraphs();
// });
$(document).ready(function()
{
    console.log('HIGHTCHART !', $('[data-highchart]'))
    setTimeout(function()
    {
        workonTtraceGraphs();
    }, 500);
});