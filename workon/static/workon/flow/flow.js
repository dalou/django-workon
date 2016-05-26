
var Notification = window.Notification || window.mozNotification || window.webkitNotification;





var flow =
{
    _ready: false,
    _loaded: false,
    _connected: false,
    _focus: false,
    _listeners: {},
    AUTO_CONNECT: window.FLOW_AUTO_CONNECT,
    DEBUG: window.FLOW_DEBUG,
    DISCONNECTED_ENABLED: window.FLOW_DISCONNECTED_ENABLED,
    DISCONNECTED_RECEIVE_URL: window.FLOW_DISCONNECTED_RECEIVE_URL,
    DISCONNECTED_SEND_URL: window.FLOW_DISCONNECTED_SEND_URL,
    WS_ENABLED: window.FLOW_WS_ENABLED,
    WS_URI: window.FLOW_WS_URI,
    WS_HEARTBEAT: window.FLOW_WS_HEARTBEAT,
    _redis_ws: null,
    _builtin_notification: window.Notification || window.mozNotification || window.webkitNotification,


    authorizeNotification: function()
    {
        Notification.requestPermission(function (permission) {
            // console.log(permission);
        });
    },

    init: function(source)
    {
        console.log('%c FLOW initialisation', 'color: #222', source);
        if(!flow._ready)
        {
            flow._ready = true;
            flow._dispatch('flow_ready');

            if(source)
            {
                $.get(source, null, function(wsdata)
                {
                    //console.log(wsdata)
                    for( var i in wsdata)
                    {
                        var data = wsdata[i];
                        if(flow.DEBUG)
                        {
                            console.log('%c INITIAL ', data.type, 'background: #B1D3D4; color: #222', data.data);
                        }
                        flow._dispatch(data.type, data.data);
                    }
                    flow._loaded = true;
                    flow._dispatch('flow_loaded');
                    if(flow.AUTO_CONNECT)
                    {
                        flow._connect();
                    }
                });
            }
            else
            {
                flow._loaded = true;
                flow._dispatch('flow_loaded');
                flow._dispatch('flow_no_inital');
                if(flow.AUTO_CONNECT)
                {
                    flow._connect();
                }
                if(flow.DEBUG)
                {
                    console.log('%c FLOW has no INITIAL_URL', 'color: #550000');
                }
                return;
            }


        }
    },
    load: function(source, callback)
    {
        if(!source)
        {
             callback(source)

        }
        else
        {
            if(typeof source == "array" || (typeof source[0] == "object" && source[0].type))
            {

                for( var i in source)
                {
                    flow._dispatch(source[i].type, source[i].data);
                }
                if(callback)
                {
                    callback(source)
                }
            }
            else if(typeof source == "object")
            {
               flow._dispatch(source.type, source.data);
               if(callback)
               {
                    callback(source)
               }

            }
            else if(typeof source == "string")
            {
                $.get(source, null, function(wsdata)
                {
                    //console.log(wsdata)
                    for( var i in wsdata)
                    {
                        var data = wsdata[i]
                        if(self.DEBUG)
                        {
                            console.log('%c RECEIVE ', 'background: #bada55; color: #222', data);
                        }
                        flow._dispatch(data.type, data.data);
                    }
                    if(callback)
                    {
                        callback(source)
                    }
                });
            }
        }
    },
    connect: function()
    {
        if(!flow._redis_ws)
        {
            flow._connect();
        }
    },
    _connect: function()
    {
        if(flow.WS_ENABLED && flow.WS_URI)
        {
            flow = this;
            flow._redis_ws = RedisWebSocket(
            {
                uri: flow.WS_URI+'flow?subscribe-user&publish-user&echo',
                receive_message: flow._receive,
                heartbeat_msg: flow.WS_HEARTBEAT,
                on_open: function()
                {
                    setTimeout(function()
                    {
                        flow._connected = true;
                        flow._dispatch('flow_connected');
                    }, 500);
                },
                flow: flow,
            });
        }
        else
        {
            flow._dispatch('flow_ws_disabled');
            if(flow.DEBUG)
            {
                console.log('%c FLOW websocket is disabled ', 'color: #550000');
            }
            if(flow.DISCONNECTED_ENABLED)
            {
                flow._disconnected_receive(2000);
            }
            else
            {
                if(flow.DEBUG)
                {
                    console.log('%c FLOW disconnected is disabled ', 'color: #550000');
                }
            }
        }
    },
    on: function(type, fct)
    {
        var types = type.split(',')
        for(var i in types)
        {
            var type = $.trim(types[i]);
            listeners = flow._listeners[type];
            if(!listeners) {
                flow._listeners[type] = listeners = [];
            }
            listeners.push(fct);
        }
    },
    _disconnected_send: function(msg)
    {
        if(flow.DISCONNECTED_ENABLED && flow.DISCONNECTED_SEND_URL)
        {
            $.get(flow.DISCONNECTED_SEND_URL, {msg:msg}, function(wsdata)
            {
                for(var i in wsdata)
                {
                    flow._receive(wsdata[i]);
                }
            });
        }
    },
    send: function(type, data)
    {
        var typed_data = {}
        typed_data.type = type;
        typed_data.from = "js"
        typed_data.data = data
        var msg = JSON.stringify(typed_data);
        if(flow._connected && flow._redis_ws)
        {
            if(flow.DEBUG)
            {
                console.log('%c SEND ', 'background: #222; color: #bada55', typed_data);
            }
            flow._redis_ws.send_message(msg);
        }
        else
        {
            flow._disconnected_send(msg);
        }
    },
    _disconnected_receive_timeout: null,
    _disconnected_receive: function(timeout)
    {
        if(flow.DISCONNECTED_ENABLED && flow.DISCONNECTED_RECEIVE_URL)
        {
            if(flow._disconnected_receive_timeout)
            {
                clearTimeout(flow._disconnected_receive_timeout);
            }
            flow._disconnected_receive_timeout = setTimeout(function()
            {
                if(flow.is_active())
                {
                    $.get(flow.DISCONNECTED_RECEIVE_URL, null, function(wsdata)
                    {
                        for(var i in wsdata)
                        {
                            flow._receive(wsdata[i]);
                        }
                    });
                    flow._disconnected_receive(flow.is_focused() ? 5000 : 20000);
                }
            }, timeout);
        }
    },
    _receive: function(msg)
    {
        var data = JSON.parse(msg);
        if(data && data.from != "js")
        {
            if(flow.DEBUG)
            {
                console.log('%c RECEIVE ', 'background: #bada55; color: #222', data);
            }
            flow._dispatch(data.type, data.data);
        }
    },

    _dispatch: function(type, data)
    {
        if(flow._listeners[type])
        {
            for(var i in flow._listeners[type])
            {
                flow._listeners[type][i](data)
                //console.log('LISTEN', json.type, json)
            }
        }
        else
        {
            // console.error('LISTEN', type+" has no listeners.", data)
        }
    },

    trigger: function(type, data)
    {
        flow._dispatch(type, data);
    },

    template: function(id, data)
    {
        if(Handlebars) {

            var source   = $('#'+id).html();
            var template = Handlebars.compile(source);
            var html    = template(data);
            return $(html);
        }
        else {
            return $(id);
        }
    },
}
window.flow = flow;











