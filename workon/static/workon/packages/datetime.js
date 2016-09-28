!function(e){"use strict";var t={i18n:{bg:{months:["Януари","Февруари","Март","Април","Май","Юни","Юли","Август","Септември","Октомври","Ноември","Декември"],dayOfWeek:["Нд","Пн","Вт","Ср","Чт","Пт","Сб"]},fa:{months:["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"],dayOfWeek:["یکشنبه","دوشنبه","سه شنبه","چهارشنبه","پنجشنبه","جمعه","شنبه"]},ru:{months:["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"],dayOfWeek:["Вск","Пн","Вт","Ср","Чт","Пт","Сб"]},en:{months:["January","February","March","April","May","June","July","August","September","October","November","December"],dayOfWeek:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]},el:{months:["Ιανουάριος","Φεβρουάριος","Μάρτιος","Απρίλιος","Μάιος","Ιούνιος","Ιούλιος","Αύγουστος","Σεπτέμβριος","Οκτώβριος","Νοέμβριος","Δεκέμβριος"],dayOfWeek:["Κυρ","Δευ","Τρι","Τετ","Πεμ","Παρ","Σαβ"]},de:{months:["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],dayOfWeek:["So","Mo","Di","Mi","Do","Fr","Sa"]},nl:{months:["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"],dayOfWeek:["zo","ma","di","wo","do","vr","za"]},tr:{months:["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"],dayOfWeek:["Paz","Pts","Sal","Çar","Per","Cum","Cts"]},fr:{months:["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"],dayOfWeek:["Dim","Lun","Mar","Mer","Jeu","Ven","Sam"]},es:{months:["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],dayOfWeek:["Dom","Lun","Mar","Mié","Jue","Vie","Sáb"]},th:{months:["มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน","กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"],dayOfWeek:["อา.","จ.","อ.","พ.","พฤ.","ศ.","ส."]},pl:{months:["styczeń","luty","marzec","kwiecień","maj","czerwiec","lipiec","sierpień","wrzesień","październik","listopad","grudzień"],dayOfWeek:["nd","pn","wt","śr","cz","pt","sb"]},pt:{months:["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"],dayOfWeek:["Dom","Seg","Ter","Qua","Qui","Sex","Sab"]},ch:{months:["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"],dayOfWeek:["日","一","二","三","四","五","六"]},se:{months:["Januari","Februari","Mars","April","Maj","Juni","Juli","Augusti","September","Oktober","November","December"],dayOfWeek:["Sön","Mån","Tis","Ons","Tor","Fre","Lör"]},kr:{months:["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"],dayOfWeek:["일","월","화","수","목","금","토"]},it:{months:["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno","Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"],dayOfWeek:["Dom","Lun","Mar","Mer","Gio","Ven","Sab"]},da:{months:["January","Februar","Marts","April","Maj","Juni","July","August","September","Oktober","November","December"],dayOfWeek:["Søn","Man","Tir","ons","Tor","Fre","lør"]},no:{months:["Januar","Februar","Mars","April","Mai","Juni","Juli","August","September","Oktober","November","Desember"],dayOfWeek:["Søn","Man","Tir","Ons","Tor","Fre","Lør"]},ja:{months:["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],dayOfWeek:["日","月","火","水","木","金","土"]},vi:{months:["Tháng 1","Tháng 2","Tháng 3","Tháng 4","Tháng 5","Tháng 6","Tháng 7","Tháng 8","Tháng 9","Tháng 10","Tháng 11","Tháng 12"],dayOfWeek:["CN","T2","T3","T4","T5","T6","T7"]},sl:{months:["Januar","Februar","Marec","April","Maj","Junij","Julij","Avgust","September","Oktober","November","December"],dayOfWeek:["Ned","Pon","Tor","Sre","Čet","Pet","Sob"]},cs:{months:["Leden","Únor","Březen","Duben","Květen","Červen","Červenec","Srpen","Září","Říjen","Listopad","Prosinec"],dayOfWeek:["Ne","Po","Út","St","Čt","Pá","So"]}},value:"",lang:"en",format:"Y/m/d H:i",formatTime:"H:i",formatDate:"Y/m/d",startDate:!1,step:60,monthChangeSpinner:!0,closeOnDateSelect:!1,closeOnWithoutClick:!0,closeOnInputClick:!0,timepicker:!0,datepicker:!0,minDate:!1,maxDate:!1,minTime:!1,maxTime:!1,allowTimes:[],opened:!1,initTime:!0,inline:!1,onSelectDate:function(){},onSelectTime:function(){},onChangeMonth:function(){},onChangeDateTime:function(){},onShow:function(){},onClose:function(){},onGenerate:function(){},withoutCopyright:!0,inverseButton:!1,hours12:!1,next:"xdsoft_next",prev:"xdsoft_prev",dayOfWeekStart:0,timeHeightInTimePicker:25,timepickerScrollbar:!0,todayButton:!0,defaultSelect:!0,scrollMonth:!0,scrollTime:!0,scrollInput:!0,lazyInit:!1,mask:!1,validateOnBlur:!0,allowBlank:!0,yearStart:1950,yearEnd:2050,style:"",id:"",fixed:!1,roundTime:"round",className:"",weekends:[],yearOffset:0};Array.prototype.indexOf||(Array.prototype.indexOf=function(e,t){for(var n=t||0,a=this.length;a>n;n++)if(this[n]===e)return n;return-1}),Date.prototype.countDaysInMonth=function(){return new Date(this.getFullYear(),this.getMonth()+1,0).getDate()},e.fn.xdsoftScroller=function(t){return this.each(function(){var n=e(this);if(!e(this).hasClass("xdsoft_scroller_box")){var a=function(e){var t={x:0,y:0};if("touchstart"==e.type||"touchmove"==e.type||"touchend"==e.type||"touchcancel"==e.type){var n=e.originalEvent.touches[0]||e.originalEvent.changedTouches[0];t.x=n.pageX,t.y=n.pageY}else("mousedown"==e.type||"mouseup"==e.type||"mousemove"==e.type||"mouseover"==e.type||"mouseout"==e.type||"mouseenter"==e.type||"mouseleave"==e.type)&&(t.x=e.pageX,t.y=e.pageY);return t},r=0,o=n.children().eq(0),s=n[0].clientHeight,i=o[0].offsetHeight,d=e('<div class="xdsoft_scrollbar"></div>'),u=e('<div class="xdsoft_scroller"></div>'),l=100,c=!1;d.append(u),n.addClass("xdsoft_scroller_box").append(d),u.on("mousedown.xdsoft_scroller",function(a){s||n.trigger("resize_scroll.xdsoft_scroller",[t]);var o=a.pageY,i=parseInt(u.css("margin-top")),c=d[0].offsetHeight;e(document.body).addClass("xdsoft_noselect"),e([document.body,window]).on("mouseup.xdsoft_scroller",function f(){e([document.body,window]).off("mouseup.xdsoft_scroller",f).off("mousemove.xdsoft_scroller",r).removeClass("xdsoft_noselect")}),e(document.body).on("mousemove.xdsoft_scroller",r=function(e){var t=e.pageY-o+i;0>t&&(t=0),t+u[0].offsetHeight>c&&(t=c-u[0].offsetHeight),n.trigger("scroll_element.xdsoft_scroller",[l?t/l:0])})}),n.on("scroll_element.xdsoft_scroller",function(e,t){s||n.trigger("resize_scroll.xdsoft_scroller",[t,!0]),t=t>1?1:0>t||isNaN(t)?0:t,u.css("margin-top",l*t),o.css("marginTop",-parseInt((i-s)*t))}).on("resize_scroll.xdsoft_scroller",function(e,t,a){s=n[0].clientHeight,i=o[0].offsetHeight;var r=s/i,c=r*d[0].offsetHeight;r>1?u.hide():(u.show(),u.css("height",parseInt(c>10?c:10)),l=d[0].offsetHeight-u[0].offsetHeight,a!==!0&&n.trigger("scroll_element.xdsoft_scroller",[t?t:Math.abs(parseInt(o.css("marginTop")))/(i-s)]))}),n.mousewheel&&n.mousewheel(function(e,t,a,r){var d=Math.abs(parseInt(o.css("marginTop")));return n.trigger("scroll_element.xdsoft_scroller",[(d-20*t)/(i-s)]),e.stopPropagation(),!1}),n.on("touchstart",function(e){c=a(e)}),n.on("touchmove",function(e){if(c){var t=a(e),r=Math.abs(parseInt(o.css("marginTop")));n.trigger("scroll_element.xdsoft_scroller",[(r-(t.y-c.y))/(i-s)]),e.stopPropagation(),e.preventDefault()}}),n.on("touchend touchcancel",function(e){c=!1})}n.trigger("resize_scroll.xdsoft_scroller",[t])})},e.fn.datetimepicker=function(n){var a=48,r=57,o=96,s=105,i=17,d=46,u=13,l=27,c=8,f=37,m=38,h=39,g=40,p=9,x=116,v=65,y=67,D=86,T=90,b=89,w=!1,_=e.isPlainObject(n)||!n?e.extend(!0,{},t,n):e.extend({},t),M=0,k=function(e){e.on("open.xdsoft focusin.xdsoft mousedown.xdsoft",function t(n){e.is(":disabled")||e.is(":hidden")||!e.is(":visible")||e.data("xdsoft_datetimepicker")||(clearTimeout(M),M=setTimeout(function(){e.data("xdsoft_datetimepicker")||S(e),e.off("open.xdsoft focusin.xdsoft mousedown.xdsoft",t).trigger("open.xdsoft")},100))})},S=function(t){function n(){var e=_.value?_.value:t&&t.val&&t.val()?t.val():"";return e&&N.isValidDate(e=Date.parseDate(e,_.format))?M.data("changed",!0):e="",e||_.startDate===!1||(e=N.strToDateTime(_.startDate)),e?e:0}var M=e("<div "+(_.id?'id="'+_.id+'"':"")+" "+(_.style?'style="'+_.style+'"':"")+' class="xdsoft_datetimepicker xdsoft_noselect '+_.className+'"></div>'),k=e('<div class="xdsoft_copyright"><a target="_blank" href="http://xdsoft.net/jqplugins/datetimepicker/">xdsoft.net</a></div>'),S=e('<div class="xdsoft_datepicker active"></div>'),O=e('<div class="xdsoft_mounthpicker"><button type="button" class="xdsoft_prev"></button><button type="button" class="xdsoft_today_button"></button><div class="xdsoft_label xdsoft_month"><span></span></div><div class="xdsoft_label xdsoft_year"><span></span></div><button type="button" class="xdsoft_next"></button></div>'),F=e('<div class="xdsoft_calendar"></div>'),I=e('<div class="xdsoft_timepicker active"><button type="button" class="xdsoft_prev"></button><div class="xdsoft_time_box"></div><button type="button" class="xdsoft_next"></button></div>'),C=I.find(".xdsoft_time_box").eq(0),P=e('<div class="xdsoft_time_variant"></div>'),H=e('<div class="xdsoft_scrollbar"></div>'),Y=(e('<div class="xdsoft_scroller"></div>'),e('<div class="xdsoft_select xdsoft_monthselect"><div></div></div>')),W=e('<div class="xdsoft_select xdsoft_yearselect"><div></div></div>');O.find(".xdsoft_month span").after(Y),O.find(".xdsoft_year span").after(W),O.find(".xdsoft_month,.xdsoft_year").on("mousedown.xdsoft",function(t){O.find(".xdsoft_select").hide();var n=e(this).find(".xdsoft_select").eq(0),a=0,r=0;N.currentTime&&(a=N.currentTime[e(this).hasClass("xdsoft_month")?"getMonth":"getFullYear"]()),n.show();for(var o=n.find("div.xdsoft_option"),s=0;s<o.length&&o.eq(s).data("value")!=a;s++)r+=o[0].offsetHeight;return n.xdsoftScroller(r/(n.children()[0].offsetHeight-n[0].clientHeight)),t.stopPropagation(),!1}),O.find(".xdsoft_select").xdsoftScroller().on("mousedown.xdsoft",function(e){e.stopPropagation(),e.preventDefault()}).on("mousedown.xdsoft",".xdsoft_option",function(t){N&&N.currentTime&&N.currentTime[e(this).parent().parent().hasClass("xdsoft_monthselect")?"setMonth":"setFullYear"](e(this).data("value")),e(this).parent().parent().hide(),M.trigger("xchange.xdsoft"),_.onChangeMonth&&_.onChangeMonth.call&&_.onChangeMonth.call(M,N.currentTime,M.data("input"))}),M.setOptions=function(n){if(_=e.extend(!0,{},_,n),n.allowTimes&&e.isArray(n.allowTimes)&&n.allowTimes.length&&(_.allowTimes=e.extend(!0,[],n.allowTimes)),n.weekends&&e.isArray(n.weekends)&&n.weekends.length&&(_.weekends=e.extend(!0,[],n.weekends)),!_.open&&!_.opened||_.inline||t.trigger("open.xdsoft"),_.inline&&(j=!0,M.addClass("xdsoft_inline"),t.after(M).hide()),_.inverseButton&&(_.next="xdsoft_prev",_.prev="xdsoft_next"),_.datepicker?S.addClass("active"):S.removeClass("active"),_.timepicker?I.addClass("active"):I.removeClass("active"),_.value&&(t&&t.val&&t.val(_.value),N.setCurrentTime(_.value)),isNaN(_.dayOfWeekStart)||parseInt(_.dayOfWeekStart)<0||parseInt(_.dayOfWeekStart)>6?_.dayOfWeekStart=0:_.dayOfWeekStart=parseInt(_.dayOfWeekStart),_.timepickerScrollbar||H.hide(),_.minDate&&/^-(.*)$/.test(_.minDate)&&(_.minDate=N.strToDateTime(_.minDate).dateFormat(_.formatDate)),_.maxDate&&/^\+(.*)$/.test(_.maxDate)&&(_.maxDate=N.strToDateTime(_.maxDate).dateFormat(_.formatDate)),O.find(".xdsoft_today_button").css("visibility",_.todayButton?"visible":"hidden"),_.mask){var k=function(e){try{if(document.selection&&document.selection.createRange){var t=document.selection.createRange();return t.getBookmark().charCodeAt(2)-2}if(e.setSelectionRange)return e.selectionStart}catch(n){return 0}},F=function(e,t){if(e="string"==typeof e||e instanceof String?document.getElementById(e):e,!e)return!1;if(e.createTextRange){var n=e.createTextRange();return n.collapse(!0),n.moveEnd(t),n.moveStart(t),n.select(),!0}return e.setSelectionRange?(e.setSelectionRange(t,t),!0):!1},C=function(e,t){var n=e.replace(/([\[\]\/\{\}\(\)\-\.\+]{1})/g,"\\$1").replace(/_/g,"{digit+}").replace(/([0-9]{1})/g,"{digit$1}").replace(/\{digit([0-9]{1})\}/g,"[0-$1_]{1}").replace(/\{digit[\+]\}/g,"[0-9_]{1}");return RegExp(n).test(t)};switch(t.off("keydown.xdsoft"),!0){case _.mask===!0:_.mask=_.format.replace(/Y/g,"9999").replace(/F/g,"9999").replace(/m/g,"19").replace(/d/g,"39").replace(/H/g,"29").replace(/i/g,"59").replace(/s/g,"59");case"string"==e.type(_.mask):C(_.mask,t.val())||t.val(_.mask.replace(/[0-9]/g,"_")),t.on("keydown.xdsoft",function(n){var M=this.value,S=n.which;switch(!0){case S>=a&&r>=S||S>=o&&s>=S||S==c||S==d:var O=k(this),I=S!=c&&S!=d?String.fromCharCode(S>=o&&s>=S?S-a:S):"_";for(S!=c&&S!=d||!O||(O--,I="_");/[^0-9_]/.test(_.mask.substr(O,1))&&O<_.mask.length&&O>0;)O+=S==c||S==d?-1:1;if(M=M.substr(0,O)+I+M.substr(O+1),""==e.trim(M))M=_.mask.replace(/[0-9]/g,"_");else if(O==_.mask.length)break;for(O+=S==c||S==d?0:1;/[^0-9_]/.test(_.mask.substr(O,1))&&O<_.mask.length&&O>0;)O+=S==c||S==d?-1:1;C(_.mask,M)?(this.value=M,F(this,O)):""==e.trim(M)?this.value=_.mask.replace(/[0-9]/g,"_"):t.trigger("error_input.xdsoft");break;case!!~[v,y,D,T,b].indexOf(S)&&w:case!!~[l,m,g,f,h,x,i,p,u].indexOf(S):return!0}return n.preventDefault(),!1})}}_.validateOnBlur&&t.off("blur.xdsoft").on("blur.xdsoft",function(){_.allowBlank&&!e.trim(e(this).val()).length?(e(this).val(null),M.data("xdsoft_datetime").empty()):Date.parseDate(e(this).val(),_.format)?M.data("xdsoft_datetime").setCurrentTime(e(this).val()):(e(this).val(N.now().dateFormat(_.format)),M.data("xdsoft_datetime").setCurrentTime(e(this).val())),M.trigger("changedatetime.xdsoft")}),_.dayOfWeekStartPrev=0==_.dayOfWeekStart?6:_.dayOfWeekStart-1,M.trigger("xchange.xdsoft").trigger("afterOpen.xdsoft")},M.data("options",_).on("mousedown.xdsoft",function(e){return e.stopPropagation(),e.preventDefault(),W.hide(),Y.hide(),!1});var A=I.find(".xdsoft_time_box");A.append(P),A.xdsoftScroller(),M.on("afterOpen.xdsoft",function(){A.xdsoftScroller()}),M.append(S).append(I),_.withoutCopyright!==!0&&M.append(k),S.append(O).append(F),e("body").append(M);var N=new function(){var e=this;e.now=function(){var e=new Date;return _.yearOffset&&e.setFullYear(e.getFullYear()+_.yearOffset),e},e.currentTime=this.now(),e.isValidDate=function(e){return"[object Date]"!==Object.prototype.toString.call(e)?!1:!isNaN(e.getTime())},e.setCurrentTime=function(t){e.currentTime="string"==typeof t?e.strToDateTime(t):e.isValidDate(t)?t:e.now(),M.trigger("xchange.xdsoft")},e.empty=function(){e.currentTime=null},e.getCurrentTime=function(t){return e.currentTime},e.nextMonth=function(){var t=e.currentTime.getMonth()+1;return 12==t&&(e.currentTime.setFullYear(e.currentTime.getFullYear()+1),t=0),e.currentTime.setDate(Math.min(Date.daysInMonth[t],e.currentTime.getDate())),e.currentTime.setMonth(t),_.onChangeMonth&&_.onChangeMonth.call&&_.onChangeMonth.call(M,N.currentTime,M.data("input")),M.trigger("xchange.xdsoft"),t},e.prevMonth=function(){var t=e.currentTime.getMonth()-1;return-1==t&&(e.currentTime.setFullYear(e.currentTime.getFullYear()-1),t=11),e.currentTime.setDate(Math.min(Date.daysInMonth[t],e.currentTime.getDate())),e.currentTime.setMonth(t),_.onChangeMonth&&_.onChangeMonth.call&&_.onChangeMonth.call(M,N.currentTime,M.data("input")),M.trigger("xchange.xdsoft"),t},e.strToDateTime=function(t){if(t&&t instanceof Date&&e.isValidDate(t))return t;var n,a,r=[];return(r=/^(\+|\-)(.*)$/.exec(t))&&(r[2]=Date.parseDate(r[2],_.formatDate))?(n=r[2].getTime()-6e4*r[2].getTimezoneOffset(),a=new Date(N.now().getTime()+parseInt(r[1]+"1")*n)):a=t?Date.parseDate(t,_.format):e.now(),e.isValidDate(a)||(a=e.now()),a},e.strtodate=function(t){if(t&&t instanceof Date&&e.isValidDate(t))return t;var n=t?Date.parseDate(t,_.formatDate):e.now();return e.isValidDate(n)||(n=e.now()),n},e.strtotime=function(t){if(t&&t instanceof Date&&e.isValidDate(t))return t;var n=t?Date.parseDate(t,_.formatTime):e.now();return e.isValidDate(n)||(n=e.now()),n},e.str=function(){return e.currentTime.dateFormat(_.format)}};O.find(".xdsoft_today_button").on("mousedown.xdsoft",function(){M.data("changed",!0),N.setCurrentTime(0),M.trigger("afterOpen.xdsoft")}).on("dblclick.xdsoft",function(){t.val(N.str()),M.trigger("close.xdsoft")}),O.find(".xdsoft_prev,.xdsoft_next").on("mousedown.xdsoft",function(){var t=e(this),n=0,a=!1;!function r(e){N.currentTime.getMonth();t.hasClass(_.next)?N.nextMonth():t.hasClass(_.prev)&&N.prevMonth(),_.monthChangeSpinner&&!a&&(n=setTimeout(r,e?e:100))}(500),e([document.body,window]).on("mouseup.xdsoft",function o(){clearTimeout(n),a=!0,e([document.body,window]).off("mouseup.xdsoft",o)})}),I.find(".xdsoft_prev,.xdsoft_next").on("mousedown.xdsoft",function(){var t=e(this),n=0,a=!1,r=110;!function o(e){var s=C[0].clientHeight,i=P[0].offsetHeight,d=Math.abs(parseInt(P.css("marginTop")));t.hasClass(_.next)&&i-s-_.timeHeightInTimePicker>=d?P.css("marginTop","-"+(d+_.timeHeightInTimePicker)+"px"):t.hasClass(_.prev)&&d-_.timeHeightInTimePicker>=0&&P.css("marginTop","-"+(d-_.timeHeightInTimePicker)+"px"),C.trigger("scroll_element.xdsoft_scroller",[Math.abs(parseInt(P.css("marginTop"))/(i-s))]),r=r>10?10:r-10,!a&&(n=setTimeout(o,e?e:r))}(500),e([document.body,window]).on("mouseup.xdsoft",function s(){clearTimeout(n),a=!0,e([document.body,window]).off("mouseup.xdsoft",s)})});var z=0;M.on("xchange.xdsoft",function(t){clearTimeout(z),z=setTimeout(function(){for(var t="",n=new Date(N.currentTime.getFullYear(),N.currentTime.getMonth(),1,12,0,0),a=0,r=N.now();n.getDay()!=_.dayOfWeekStart;)n.setDate(n.getDate()-1);t+="<table><thead><tr>";for(var o=0;7>o;o++)t+="<th>"+_.i18n[_.lang].dayOfWeek[o+_.dayOfWeekStart>6?0:o+_.dayOfWeekStart]+"</th>";t+="</tr></thead>",t+="<tbody><tr>";var s=!1,i=!1;_.maxDate!==!1&&(s=N.strtodate(_.maxDate),s=new Date(s.getFullYear(),s.getMonth(),s.getDate(),23,59,59,999)),_.minDate!==!1&&(i=N.strtodate(_.minDate),i=new Date(i.getFullYear(),i.getMonth(),i.getDate()));for(var d,u,l,c=[];a<N.currentTime.countDaysInMonth()||n.getDay()!=_.dayOfWeekStart||N.currentTime.getMonth()==n.getMonth();)c=[],a++,d=n.getDate(),u=n.getFullYear(),l=n.getMonth(),c.push("xdsoft_date"),(s!==!1&&n>s||i!==!1&&i>n)&&c.push("xdsoft_disabled"),N.currentTime.getMonth()!=l&&c.push("xdsoft_other_month"),(_.defaultSelect||M.data("changed"))&&N.currentTime.dateFormat(_.formatDate)==n.dateFormat(_.formatDate)&&c.push("xdsoft_current"),r.dateFormat(_.formatDate)==n.dateFormat(_.formatDate)&&c.push("xdsoft_today"),(0==n.getDay()||6==n.getDay()||~_.weekends.indexOf(n.dateFormat(_.formatDate)))&&c.push("xdsoft_weekend"),_.beforeShowDay&&"function"==typeof _.beforeShowDay&&c.push(_.beforeShowDay(n)),t+='<td data-date="'+d+'" data-month="'+l+'" data-year="'+u+'" class="xdsoft_date xdsoft_day_of_week'+n.getDay()+" "+c.join(" ")+'"><div>'+d+"</div></td>",n.getDay()==_.dayOfWeekStartPrev&&(t+="</tr>"),n.setDate(d+1);t+="</tbody></table>",F.html(t),O.find(".xdsoft_label span").eq(0).text(_.i18n[_.lang].months[N.currentTime.getMonth()]),O.find(".xdsoft_label span").eq(1).text(N.currentTime.getFullYear());var f="",m="",l="",h=function(e,t){var n=N.now();n.setHours(e),e=parseInt(n.getHours()),n.setMinutes(t),t=parseInt(n.getMinutes()),c=[],(_.maxTime!==!1&&N.strtotime(_.maxTime).getTime()<n.getTime()||_.minTime!==!1&&N.strtotime(_.minTime).getTime()>n.getTime())&&c.push("xdsoft_disabled"),(_.initTime||_.defaultSelect||M.data("changed"))&&parseInt(N.currentTime.getHours())==parseInt(e)&&(_.step>59||Math[_.roundTime](N.currentTime.getMinutes()/_.step)*_.step==parseInt(t))&&(_.defaultSelect||M.data("changed")?c.push("xdsoft_current"):_.initTime&&c.push("xdsoft_init_time")),parseInt(r.getHours())==parseInt(e)&&parseInt(r.getMinutes())==parseInt(t)&&c.push("xdsoft_today"),f+='<div class="xdsoft_time '+c.join(" ")+'" data-hour="'+e+'" data-minute="'+t+'">'+n.dateFormat(_.formatTime)+"</div>"};if(_.allowTimes&&e.isArray(_.allowTimes)&&_.allowTimes.length)for(var a=0;a<_.allowTimes.length;a++)m=N.strtotime(_.allowTimes[a]).getHours(),l=N.strtotime(_.allowTimes[a]).getMinutes(),h(m,l);else for(var a=0,o=0;a<(_.hours12?12:24);a++)for(o=0;60>o;o+=_.step)m=(10>a?"0":"")+a,l=(10>o?"0":"")+o,h(m,l);P.html(f);var g="",a=0;for(a=parseInt(_.yearStart,10)+_.yearOffset;a<=parseInt(_.yearEnd,10)+_.yearOffset;a++)g+='<div class="xdsoft_option '+(N.currentTime.getFullYear()==a?"xdsoft_current":"")+'" data-value="'+a+'">'+a+"</div>";for(W.children().eq(0).html(g),a=0,g="";11>=a;a++)g+='<div class="xdsoft_option '+(N.currentTime.getMonth()==a?"xdsoft_current":"")+'" data-value="'+a+'">'+_.i18n[_.lang].months[a]+"</div>";Y.children().eq(0).html(g),e(M).trigger("generate.xdsoft")},10),t.stopPropagation()}).on("afterOpen.xdsoft",function(){if(_.timepicker){var e;if(P.find(".xdsoft_current").length?e=".xdsoft_current":P.find(".xdsoft_init_time").length&&(e=".xdsoft_init_time"),e){var t=C[0].clientHeight,n=P[0].offsetHeight,a=P.find(e).index()*_.timeHeightInTimePicker+1;a>n-t&&(a=n-t),C.trigger("scroll_element.xdsoft_scroller",[parseInt(a)/(n-t)])}else C.trigger("scroll_element.xdsoft_scroller",[0])}});var J=0;F.on("click.xdsoft","td",function(n){n.stopPropagation(),J++;var a=e(this),r=N.currentTime;return a.hasClass("xdsoft_disabled")?!1:(r.setDate(1),r.setFullYear(a.data("year")),r.setMonth(a.data("month")),r.setDate(a.data("date")),M.trigger("select.xdsoft",[r]),t.val(N.str()),(J>1||_.closeOnDateSelect===!0||0===_.closeOnDateSelect&&!_.timepicker)&&!_.inline&&M.trigger("close.xdsoft"),_.onSelectDate&&_.onSelectDate.call&&_.onSelectDate.call(M,N.currentTime,M.data("input")),M.data("changed",!0),M.trigger("xchange.xdsoft"),M.trigger("changedatetime.xdsoft"),void setTimeout(function(){J=0},200))}),P.on("click.xdsoft","div",function(t){t.stopPropagation();var n=e(this),a=N.currentTime;return n.hasClass("xdsoft_disabled")?!1:(a.setHours(n.data("hour")),a.setMinutes(n.data("minute")),M.trigger("select.xdsoft",[a]),M.data("input").val(N.str()),!_.inline&&M.trigger("close.xdsoft"),_.onSelectTime&&_.onSelectTime.call&&_.onSelectTime.call(M,N.currentTime,M.data("input")),M.data("changed",!0),M.trigger("xchange.xdsoft"),void M.trigger("changedatetime.xdsoft"))}),M.mousewheel&&S.mousewheel(function(e,t,n,a){return _.scrollMonth?(0>t?N.nextMonth():N.prevMonth(),!1):!0}),M.mousewheel&&C.unmousewheel().mousewheel(function(e,t,n,a){if(!_.scrollTime)return!0;var r=C[0].clientHeight,o=P[0].offsetHeight,s=Math.abs(parseInt(P.css("marginTop"))),i=!0;return 0>t&&o-r-_.timeHeightInTimePicker>=s?(P.css("marginTop","-"+(s+_.timeHeightInTimePicker)+"px"),i=!1):t>0&&s-_.timeHeightInTimePicker>=0&&(P.css("marginTop","-"+(s-_.timeHeightInTimePicker)+"px"),i=!1),C.trigger("scroll_element.xdsoft_scroller",[Math.abs(parseInt(P.css("marginTop"))/(o-r))]),e.stopPropagation(),i});var j=!1;M.on("changedatetime.xdsoft",function(){if(_.onChangeDateTime&&_.onChangeDateTime.call){var e=M.data("input");_.onChangeDateTime.call(M,N.currentTime,e),e.trigger("change")}}).on("generate.xdsoft",function(){_.onGenerate&&_.onGenerate.call&&_.onGenerate.call(M,N.currentTime,M.data("input")),j&&(M.trigger("afterOpen.xdsoft"),j=!1)}).on("click.xdsoft",function(e){e.stopPropagation()});var L=0;t.mousewheel&&t.mousewheel(function(e,n,a,r){return _.scrollInput?!_.datepicker&&_.timepicker?(L=P.find(".xdsoft_current").length?P.find(".xdsoft_current").eq(0).index():0,L+n>=0&&L+n<P.children().length&&(L+=n),P.children().eq(L).length&&P.children().eq(L).trigger("mousedown"),!1):_.datepicker&&!_.timepicker?(S.trigger(e,[n,a,r]),t.val&&t.val(N.str()),M.trigger("changedatetime.xdsoft"),!1):void 0:!0});var E=function(){var t=M.data("input").offset(),n=t.top+M.data("input")[0].offsetHeight-1,a=t.left,r="absolute";_.fixed?(n-=e(window).scrollTop(),a-=e(window).scrollLeft(),r="fixed"):(n+M[0].offsetHeight>e(window).height()+e(window).scrollTop()&&(n=t.top-M[0].offsetHeight+1),0>n&&(n=0),a+M[0].offsetWidth>e(window).width()&&(a=t.left-M[0].offsetWidth+M.data("input")[0].offsetWidth)),M.css({left:a,top:n,position:r})};M.on("open.xdsoft",function(){var t=!0;_.onShow&&_.onShow.call&&(t=_.onShow.call(M,N.currentTime,M.data("input"))),t!==!1&&(M.show(),E(),e(window).off("resize.xdsoft",E).on("resize.xdsoft",E),_.closeOnWithoutClick&&e([document.body,window]).on("mousedown.xdsoft",function n(){M.trigger("close.xdsoft"),e([document.body,window]).off("mousedown.xdsoft",n)}))}).on("close.xdsoft",function(e){var t=!0;_.onClose&&_.onClose.call&&(t=_.onClose.call(M,N.currentTime,M.data("input"))),t===!1||_.opened||_.inline||M.hide(),e.stopPropagation()}).data("input",t);var R=0;M.data("xdsoft_datetime",N),M.setOptions(_),N.setCurrentTime(n()),t.data("xdsoft_datetimepicker",M).on("open.xdsoft focusin.xdsoft mousedown.xdsoft",function(e){t.is(":disabled")||t.is(":hidden")||!t.is(":visible")||t.data("xdsoft_datetimepicker").is(":visible")&&_.closeOnInputClick||(clearTimeout(R),R=setTimeout(function(){t.is(":disabled")||t.is(":hidden")||!t.is(":visible")||(j=!0,N.setCurrentTime(n()),M.trigger("open.xdsoft"))},100))}).on("keydown.xdsoft",function(t){var n=(this.value,t.which);switch(!0){case!!~[u].indexOf(n):var a=e("input:visible,textarea:visible");return M.trigger("close.xdsoft"),a.eq(a.index(this)+1).focus(),!1;case!!~[p].indexOf(n):return M.trigger("close.xdsoft"),!0}})},O=function(t){var n=t.data("xdsoft_datetimepicker");n&&(n.data("xdsoft_datetime",null),n.remove(),t.data("xdsoft_datetimepicker",null).off("open.xdsoft focusin.xdsoft focusout.xdsoft mousedown.xdsoft blur.xdsoft keydown.xdsoft"),e(window).off("resize.xdsoft"),e([window,document.body]).off("mousedown.xdsoft"),t.unmousewheel&&t.unmousewheel())};return e(document).off("keydown.xdsoftctrl keyup.xdsoftctrl").on("keydown.xdsoftctrl",function(e){e.keyCode==i&&(w=!0)}).on("keyup.xdsoftctrl",function(e){e.keyCode==i&&(w=!1)}),this.each(function(){var t;if(t=e(this).data("xdsoft_datetimepicker")){if("string"===e.type(n))switch(n){case"show":e(this).select().focus(),t.trigger("open.xdsoft");break;case"hide":t.trigger("close.xdsoft");break;case"destroy":O(e(this));break;case"reset":this.value=this.defaultValue,this.value&&t.data("xdsoft_datetime").isValidDate(Date.parseDate(this.value,_.format))||t.data("changed",!1),t.data("xdsoft_datetime").setCurrentTime(this.value)}else t.setOptions(n);return 0}"string"!==e.type(n)&&(!_.lazyInit||_.open||_.inline?S(e(this)):k(e(this)))})},e.fn.datetimepicker.defaults=t}(jQuery),function(e){"function"==typeof define&&define.amd?define(["jquery"],e):"object"==typeof exports?module.exports=e:e(jQuery)}(function(e){function t(t){var r,o=t||window.event,s=[].slice.call(arguments,1),i=0,d=0,u=0,l=0,c=0;return t=e.event.fix(o),t.type="mousewheel",o.wheelDelta&&(i=o.wheelDelta),o.detail&&(i=-1*o.detail),o.deltaY&&(u=-1*o.deltaY,i=u),o.deltaX&&(d=o.deltaX,i=-1*d),void 0!==o.wheelDeltaY&&(u=o.wheelDeltaY),void 0!==o.wheelDeltaX&&(d=-1*o.wheelDeltaX),l=Math.abs(i),(!n||n>l)&&(n=l),c=Math.max(Math.abs(u),Math.abs(d)),(!a||a>c)&&(a=c),r=i>0?"floor":"ceil",i=Math[r](i/n),d=Math[r](d/a),u=Math[r](u/a),s.unshift(t,i,d,u),(e.event.dispatch||e.event.handle).apply(this,s)}var n,a,r=["wheel","mousewheel","DOMMouseScroll","MozMousePixelScroll"],o="onwheel"in document||document.documentMode>=9?["wheel"]:["mousewheel","DomMouseScroll","MozMousePixelScroll"];if(e.event.fixHooks)for(var s=r.length;s;)e.event.fixHooks[r[--s]]=e.event.mouseHooks;e.event.special.mousewheel={setup:function(){if(this.addEventListener)for(var e=o.length;e;)this.addEventListener(o[--e],t,!1);else this.onmousewheel=t},teardown:function(){if(this.removeEventListener)for(var e=o.length;e;)this.removeEventListener(o[--e],t,!1);else this.onmousewheel=null}},e.fn.extend({mousewheel:function(e){return e?this.bind("mousewheel",e):this.trigger("mousewheel")},unmousewheel:function(e){return this.unbind("mousewheel",e)}})}),Date.parseFunctions={count:0},Date.parseRegexes=[],Date.formatFunctions={count:0},Date.prototype.dateFormat=function(e){if("unixtime"==e)return parseInt(this.getTime()/1e3);null==Date.formatFunctions[e]&&Date.createNewFormat(e);var t=Date.formatFunctions[e];return this[t]()},Date.createNewFormat=function(format){var funcName="format"+Date.formatFunctions.count++;Date.formatFunctions[format]=funcName;for(var code="Date.prototype."+funcName+" = function() {return ",special=!1,ch="",i=0;i<format.length;++i)ch=format.charAt(i),special||"\\"!=ch?special?(special=!1,code+="'"+String.escape(ch)+"' + "):code+=Date.getFormatCode(ch):special=!0;eval(code.substring(0,code.length-3)+";}")},Date.getFormatCode=function(e){switch(e){case"d":return"String.leftPad(this.getDate(), 2, '0') + ";case"D":return"Date.dayNames[this.getDay()].substring(0, 3) + ";case"j":return"this.getDate() + ";case"l":return"Date.dayNames[this.getDay()] + ";case"S":return"this.getSuffix() + ";case"w":return"this.getDay() + ";case"z":return"this.getDayOfYear() + ";case"W":return"this.getWeekOfYear() + ";case"F":return"Date.monthNames[this.getMonth()] + ";case"m":return"String.leftPad(this.getMonth() + 1, 2, '0') + ";case"M":return"Date.monthNames[this.getMonth()].substring(0, 3) + ";case"n":return"(this.getMonth() + 1) + ";case"t":return"this.getDaysInMonth() + ";case"L":return"(this.isLeapYear() ? 1 : 0) + ";case"Y":return"this.getFullYear() + ";case"y":return"('' + this.getFullYear()).substring(2, 4) + ";case"a":return"(this.getHours() < 12 ? 'am' : 'pm') + ";case"A":return"(this.getHours() < 12 ? 'AM' : 'PM') + ";case"g":return"((this.getHours() %12) ? this.getHours() % 12 : 12) + ";case"G":return"this.getHours() + ";case"h":return"String.leftPad((this.getHours() %12) ? this.getHours() % 12 : 12, 2, '0') + ";case"H":return"String.leftPad(this.getHours(), 2, '0') + ";case"i":return"String.leftPad(this.getMinutes(), 2, '0') + ";case"s":return"String.leftPad(this.getSeconds(), 2, '0') + ";case"O":return"this.getGMTOffset() + ";case"T":return"this.getTimezone() + ";case"Z":return"(this.getTimezoneOffset() * -60) + ";default:return"'"+String.escape(e)+"' + "}},Date.parseDate=function(e,t){if("unixtime"==t)return new Date(isNaN(parseInt(e))?0:1e3*parseInt(e));null==Date.parseFunctions[t]&&Date.createParser(t);var n=Date.parseFunctions[t];return Date[n](e)},Date.createParser=function(format){var funcName="parse"+Date.parseFunctions.count++,regexNum=Date.parseRegexes.length,currentGroup=1;Date.parseFunctions[format]=funcName;for(var code="Date."+funcName+" = function(input) {\nvar y = -1, m = -1, d = -1, h = -1, i = -1, s = -1, z = -1;\nvar d = new Date();\ny = d.getFullYear();\nm = d.getMonth();\nd = d.getDate();\nvar results = input.match(Date.parseRegexes["+regexNum+"]);\nif (results && results.length > 0) {",regex="",special=!1,ch="",i=0;i<format.length;++i)ch=format.charAt(i),special||"\\"!=ch?special?(special=!1,regex+=String.escape(ch)):(obj=Date.formatCodeToRegex(ch,currentGroup),currentGroup+=obj.g,regex+=obj.s,obj.g&&obj.c&&(code+=obj.c)):special=!0;code+="if (y > 0 && z > 0){\nvar doyDate = new Date(y,0);\ndoyDate.setDate(z);\nm = doyDate.getMonth();\nd = doyDate.getDate();\n}",code+="if (y > 0 && m >= 0 && d > 0 && h >= 0 && i >= 0 && s >= 0)\n{return new Date(y, m, d, h, i, s);}\nelse if (y > 0 && m >= 0 && d > 0 && h >= 0 && i >= 0)\n{return new Date(y, m, d, h, i);}\nelse if (y > 0 && m >= 0 && d > 0 && h >= 0)\n{return new Date(y, m, d, h);}\nelse if (y > 0 && m >= 0 && d > 0)\n{return new Date(y, m, d);}\nelse if (y > 0 && m >= 0)\n{return new Date(y, m);}\nelse if (y > 0)\n{return new Date(y);}\n}return null;}",Date.parseRegexes[regexNum]=new RegExp("^"+regex+"$"),eval(code)},Date.formatCodeToRegex=function(e,t){switch(e){case"D":return{g:0,c:null,s:"(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)"};case"j":case"d":return{g:1,c:"d = parseInt(results["+t+"], 10);\n",s:"(\\d{1,2})"};case"l":return{g:0,c:null,s:"(?:"+Date.dayNames.join("|")+")"};case"S":return{g:0,c:null,s:"(?:st|nd|rd|th)"};case"w":return{g:0,c:null,s:"\\d"};case"z":return{g:1,c:"z = parseInt(results["+t+"], 10);\n",s:"(\\d{1,3})"};case"W":return{g:0,c:null,s:"(?:\\d{2})"};case"F":return{g:1,c:"m = parseInt(Date.monthNumbers[results["+t+"].substring(0, 3)], 10);\n",
s:"("+Date.monthNames.join("|")+")"};case"M":return{g:1,c:"m = parseInt(Date.monthNumbers[results["+t+"]], 10);\n",s:"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"};case"n":case"m":return{g:1,c:"m = parseInt(results["+t+"], 10) - 1;\n",s:"(\\d{1,2})"};case"t":return{g:0,c:null,s:"\\d{1,2}"};case"L":return{g:0,c:null,s:"(?:1|0)"};case"Y":return{g:1,c:"y = parseInt(results["+t+"], 10);\n",s:"(\\d{4})"};case"y":return{g:1,c:"var ty = parseInt(results["+t+"], 10);\ny = ty > Date.y2kYear ? 1900 + ty : 2000 + ty;\n",s:"(\\d{1,2})"};case"a":return{g:1,c:"if (results["+t+"] == 'am') {\nif (h == 12) { h = 0; }\n} else { if (h < 12) { h += 12; }}",s:"(am|pm)"};case"A":return{g:1,c:"if (results["+t+"] == 'AM') {\nif (h == 12) { h = 0; }\n} else { if (h < 12) { h += 12; }}",s:"(AM|PM)"};case"g":case"G":case"h":case"H":return{g:1,c:"h = parseInt(results["+t+"], 10);\n",s:"(\\d{1,2})"};case"i":return{g:1,c:"i = parseInt(results["+t+"], 10);\n",s:"(\\d{2})"};case"s":return{g:1,c:"s = parseInt(results["+t+"], 10);\n",s:"(\\d{2})"};case"O":return{g:0,c:null,s:"[+-]\\d{4}"};case"T":return{g:0,c:null,s:"[A-Z]{3}"};case"Z":return{g:0,c:null,s:"[+-]\\d{1,5}"};default:return{g:0,c:null,s:String.escape(e)}}},Date.prototype.getTimezone=function(){return this.toString().replace(/^.*? ([A-Z]{3}) [0-9]{4}.*$/,"$1").replace(/^.*?\(([A-Z])[a-z]+ ([A-Z])[a-z]+ ([A-Z])[a-z]+\)$/,"$1$2$3")},Date.prototype.getGMTOffset=function(){return(this.getTimezoneOffset()>0?"-":"+")+String.leftPad(Math.floor(Math.abs(this.getTimezoneOffset())/60),2,"0")+String.leftPad(Math.abs(this.getTimezoneOffset())%60,2,"0")},Date.prototype.getDayOfYear=function(){var e=0;Date.daysInMonth[1]=this.isLeapYear()?29:28;for(var t=0;t<this.getMonth();++t)e+=Date.daysInMonth[t];return e+this.getDate()},Date.prototype.getWeekOfYear=function(){var e=this.getDayOfYear()+(4-this.getDay()),t=new Date(this.getFullYear(),0,1),n=7-t.getDay()+4;return String.leftPad(Math.ceil((e-n)/7)+1,2,"0")},Date.prototype.isLeapYear=function(){var e=this.getFullYear();return 0==(3&e)&&(e%100||e%400==0&&e)},Date.prototype.getFirstDayOfMonth=function(){var e=(this.getDay()-(this.getDate()-1))%7;return 0>e?e+7:e},Date.prototype.getLastDayOfMonth=function(){var e=(this.getDay()+(Date.daysInMonth[this.getMonth()]-this.getDate()))%7;return 0>e?e+7:e},Date.prototype.getDaysInMonth=function(){return Date.daysInMonth[1]=this.isLeapYear()?29:28,Date.daysInMonth[this.getMonth()]},Date.prototype.getSuffix=function(){switch(this.getDate()){case 1:case 21:case 31:return"st";case 2:case 22:return"nd";case 3:case 23:return"rd";default:return"th"}},String.escape=function(e){return e.replace(/('|\\)/g,"\\$1")},String.leftPad=function(e,t,n){var a=new String(e);for(null==n&&(n=" ");a.length<t;)a=n+a;return a},Date.daysInMonth=[31,28,31,30,31,30,31,31,30,31,30,31],Date.monthNames=["January","February","March","April","May","June","July","August","September","October","November","December"],Date.dayNames=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],Date.y2kYear=50,Date.monthNumbers={Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11},Date.patterns={ISO8601LongPattern:"Y-m-d H:i:s",ISO8601ShortPattern:"Y-m-d",ShortDatePattern:"n/j/Y",LongDatePattern:"l, F d, Y",FullDateTimePattern:"l, F d, Y g:i:s A",MonthDayPattern:"F d",ShortTimePattern:"g:i A",LongTimePattern:"g:i:s A",SortableDateTimePattern:"Y-m-d\\TH:i:s",UniversalSortableDateTimePattern:"Y-m-d H:i:sO",YearMonthPattern:"F, Y"};

window.workon_packages_datetime = true;

$(document).ready(function()
{
    window.workon_packages_datetime_apply = function($elms)
    {
        $elms = $elms ? $elms : $('[data-workon-date-input]');
        $elms.each(function(i, self)
        {
            if(self.workon_datetime === true) { return; }
            $(self).datetimepicker($(self).data('workon-date-input'));
            self.workon_datetime = true;
        });
    }
    window.workon_packages_datetime_apply();

    $(document).on('mousedown', '[data-workon-date-input]', function(e)
    {
        workon_packages_datetime_apply($(e.target));
    });
});