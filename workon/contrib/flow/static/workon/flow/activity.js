flow = $.extend(flow,
{
    ACTIVITY_DELAY: window.FLOW_ACTIVITY_DELAY, // in MS
    _activity_interval: null,
    _active: true,
    set_active: function(active)
    {
        //console.log('change _active', active)
        if(active != this._active)
        {
            if(active == true) {

                clearTimeout(flow._activity_interval);
                flow._activity_interval = setTimeout(function() { flow.set_active(false); }, flow.ACTIVITY_DELAY);
            }
            this._active = active;
            this._dispatch('activity_changed', active);
        }
    },
    is_active: function(active)
    {
        return this._active;
    },
    _focused: false,
    set_focused: function(focused)
    {
        if(focused != this._focused)
        {
            this._focused = focused;
            this._dispatch('focus_changed', focused);
        }
    },
    is_focused: function(focused)
    {
        return this._focused;
    },
});

flow.on('activity_changed', function()
{
    if(flow.is_active())
    {
        flow._disconnected_receive();
    }
});

flow.on('flow_connected', function(delay)
{
    flow.set_focused(true);

    $(window).mousemove(function() { flow.set_active(true); });
    flow._activity_interval = setTimeout(function() { console.log('first timeout', flow._active); flow.set_active(false); }, flow.ACTIVITY_DELAY);
    $(window).focus(function()
    {
        flow.set_focused(true);
        flow._disconnected_receive(100);
    }).blur(function()
    {
        flow.set_focused(false);
    });
});

