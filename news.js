// ==UserScript==

// @name        TongjiEnhance
// @namespace   tongji.1958.cc
// @description Enhance Editing Experiance
// @include     http://tongji.1958.cc:8106/Projects/ProjectsList.aspx
// @version     0.1
// @grant       unsafeWindow
// @require     http://tongji.1958.cc:8106/JavaScript/jquery.js
// ==/UserScript==

var $ = $ || unsafeWindow.$;

var resultID = 0 ;
var __theFormPostData = "";
var __theFormPostCollection = new Array();
var __callbackTextTypes = /^(text|password|hidden|search|tel|url|email|number|range|color|datetime|date|month|week|time|datetime-local)$/i;

function shenhe(vali) {
    var str = "";
    if (vali.length == 6) {
        str = "待定;";
    }
    if (vali.length == 7) {
        str = "退回;";
    }
    switch (vali) {
    case "0":
        {
            str += "未审核";
            break;
        }
    case "1":
        {
            str += "本地审核通过"; break;
        }
    case "2":
        {
            str += "待定"; break;
        }
    case "3":
        {
            str += "本地退回"; break;
        }
    case "10000":
        {
            str += "企业"; break;
        }
    case "11000":
        {
            str += "企业、项目"; break;
        }
    case "11100":
        {
            str += "企业、项目、产品"; break;
        }
    case "11010":
        {
            str += "企业、项目、文字版"; break;
        }
    case "11011":
        {
            str += "企业、项目、文字版、移动"; break;
        }
    case "11110":
        {
            str += "企业、项目、产品、文字"; break;
        }
    case "11001":
        {
            str += "企业、项目、移动"; break;
        }
    case "11111":
        {
            str += "已全部同步"; break;
        }
    }

    return str;
}

function InitCallback() {
    __theFormPostData = "";
    var theForm = document.forms['form1'];
    if (!theForm) {
	theForm = document.form1;
    }
    var formElements = theForm.elements,
        count = formElements.length,
        element;
    for (var i = 0; i < count; i++) {
        element = formElements[i];
        var tagName = element.tagName.toLowerCase();
        if (tagName == "input") {
	    var type = element.type;
	    if ((__callbackTextTypes.test(type) || ((type == "checkbox" || type == "radio") && element.checked))
                && (element.id != "__EVENTVALIDATION")) {
                InitCallbackAddField(element.name, element.value);
	    }
        }
        else if (tagName == "select") {
	    var selectCount = element.options.length;
	    for (var j = 0; j < selectCount; j++) {
                var selectChild = element.options[j];
                if (selectChild.selected == true) {
		    InitCallbackAddField(element.name, element.value);
                }
	    }
        }
        else if (tagName == "textarea") {
	    InitCallbackAddField(element.name, element.value);
        }
    }
    return __theFormPostData;
}

function WebForm_EncodeCallback(parameter) {
    if (encodeURIComponent) {
        return encodeURIComponent(parameter);
    }
    else {
        return escape(parameter);
    }
}

function InitCallbackAddField(name, value) {
    var nameValue = new Object();
    nameValue.name = name;
    nameValue.value = value;
    __theFormPostCollection[__theFormPostCollection.length] = nameValue;
    __theFormPostData += WebForm_EncodeCallback(name) + "=" + WebForm_EncodeCallback(value) + "&";
}

function makePostData(id, eventType) {
    var eventArgument;
    var eventTarget = "ASPxPageControl1$popupView$cpPopupView";
    var postID = resultID + 1;
    // if ( __aspxPersistentControlPropertiesStorage == null) {
    // 	postID = 0;
    // } else {
    // 	postID = __aspxPersistentControlPropertiesStorage.ASPxPageControl1_popupView_cpPopupView.activeCallbacks.length;
    // }
    var baseArg = "c" + postID + ":" + id;
    switch(eventType){
    case "View":
	eventArgument = baseArg;
	break;
    case "FirmInfoPass":
	eventArgument = baseArg + "_c1_1";
	break;
    case "ProjPass":
	eventArgument = baseArg + "_c1_2";
	break;
    case "ItemPass":
	eventArgument = baseArg + "_c1_3";
	break;
    case "TextPass":
	eventArgument = baseArg + "_c1_4";
	break;
    case "Refuse":
	eventArgument = baseArg + "_c3_1";
	break;
    case "ItemView":
        eventTarget = "ASPxPageControl1$popupView$cpPopupView$ASPxPageControlViewEdited$popupItems$itPopup";
        eventArgument = baseArg;
        break;
    }
    var theForm = document.forms['form1'];
    if (!theForm) {
	theForm = document.form1;
    }
    var postData = InitCallback() +
	    "__CALLBACKID=" + WebForm_EncodeCallback(eventTarget) +
	    "&__CALLBACKPARAM=" + WebForm_EncodeCallback(eventArgument);
    if (theForm["__EVENTVALIDATION"]) {
        postData += "&__EVENTVALIDATION=" + WebForm_EncodeCallback(theForm["__EVENTVALIDATION"].value);
    }
    return postData;
}

function doPass(id, events) {
    var count = 3;
    function errCount() {
	
    }
    if (events.length == 0) {
	alert("全部通过");
	return 0;
    }
    var event = events.pop();

    var PostData = makePostData(id, event);
    $.post("ProjectsList.aspx", PostData, function(response, status){
	var separatorIndex = response.indexOf("|");
	if (separatorIndex != -1) {
            var validationFieldLength = parseInt(response.substring(0, separatorIndex));
            if (!isNaN(validationFieldLength)) {
                var validationField = response.substring(separatorIndex + 1, separatorIndex + validationFieldLength + 1);
                if (validationField != "") {
                    var validationFieldElement = theForm["__EVENTVALIDATION"];
                    if (!validationFieldElement) {
                        validationFieldElement = document.createElement("INPUT");
                        validationFieldElement.type = "hidden";
                        validationFieldElement.name = "__EVENTVALIDATION";
                        theForm.appendChild(validationFieldElement);
                    }
                    validationFieldElement.value = validationField;
                }
            }
	}
	var resultObj = eval(response.substring(separatorIndex + validationFieldLength + 1));
	var result = false;
	if (resultObj.generalError) {
	    alert("General Error:" + resultObj.generalError);
	} else if (resultObj.error) {
	    switch(event) {
	    case "View":
		result = true;
		break;
	    case "FirmInfoPass":
		result = (resultObj.error.message == "客户信息同步成功");
		break;
	    case "ProjPass":
		result = (resultObj.error.message == "项目信息同步成功");
		break;
	    case "ItemPass":
		result = (resultObj.error.message == "产品数据同步成功");
		break;
	    case "TextPass":
		result = (resultObj.error.message == "项目文字版数据同步成功");
		break;
	    }
	    if(!result) {
		alert("通过信息错误:" + resultObj.error.message);
	    } else {
		resultID = resultObj['id'];
		doPass(id, events);
	    }
	}
    });
    return 1;
}

function runPass(node, id) {
    function afterSyn(qid) {
	$.post("../Editor/valistring.ashx?pid=" + qid, null, function (data) {
            if (data.msg != "0") {
		var dd = shenhe(data);
		node.parentNode.previousSibling.innerHTML = dd;
	    }
	});
    }
    var events = new Array("TextPass", "ItemPass", "ProjPass", "FirmInfoPass");
    return doPass(id, events);
    afterSyn(id);
}
	  	 
function GetTooltip(node, id) {
    var parser = new DOMParser();
    var PostData = makePostData(id, "View");
    $.post("ProjectsList.aspx", PostData, function(response, status){
	var separatorIndex = response.indexOf("|");
	if (separatorIndex != -1) {
            var validationFieldLength = parseInt(response.substring(0, separatorIndex));
            if (!isNaN(validationFieldLength)) {
                var validationField = response.substring(separatorIndex + 1, separatorIndex + validationFieldLength + 1);
                if (validationField != "") {
                    var validationFieldElement = theForm["__EVENTVALIDATION"];
                    if (!validationFieldElement) {
                        validationFieldElement = document.createElement("INPUT");
                        validationFieldElement.type = "hidden";
                        validationFieldElement.name = "__EVENTVALIDATION";
                        theForm.appendChild(validationFieldElement);
                    }
                    validationFieldElement.value = validationField;
                }
            }
	}
	var resultObj = eval(response.substring(separatorIndex + validationFieldLength + 1));
	if (resultObj.generalError) {
	    alert("General Error:" + resultObj.generalError);
	} else if (resultObj.error) {
	    alert("Error:" + resultObj.error.message);
	} else {
	    resultID = resultObj.id;
	    var Message = resultObj.result;
            var wrapper = parser.parseFromString(Message, "text/html");
	    var CompanyName = evaluateXPath(wrapper.documentElement, "/html/body/table/tbody/tr[2]/td/div[1]/table[1]/tbody/tr[1]/td[4]")[0].innerHTML.trim();
            var CompanyType = evaluateXPath(wrapper.documentElement, "/html/body/table/tbody/tr[2]/td/div[1]/table[1]/tbody/tr[2]/td[4]")[0].innerHTML.trim();
            var CompanyIntro = evaluateXPath(wrapper.documentElement, "/html/body/table/tbody/tr[2]/td/div[1]/table[1]/tbody/tr[12]/td[2]")[0].textContent.trim();
            var ProjName = evaluateXPath(wrapper.documentElement, "/html/body/table/tbody/tr[2]/td/div[2]/table[1]/tbody/tr[1]/td[4]")[0].innerHTML.trim();
	    var ProjIntro = evaluateXPath(wrapper.documentElement, "/html/body/table/tbody/tr[2]/td/div[3]")[0].childNodes[0].nodeValue.trim();
	    var ProjType = evaluateXPath(wrapper.documentElement, "/html/body/table/tbody/tr[2]/td/div[2]/table[1]/tbody/tr[3]/td[4]")[0].innerHTML.trim();
            var CompanyPopup = CompanyName + "   " + CompanyType + "   " + CompanyIntro;
            //var FirstPopup = String.format("nhpup.popup(\'{0}\')", CompanyPopup);
            //            node.childNodes[3].setAttribute("onmouseover", FirstPopup);
            node.childNodes[3].setAttribute("title", CompanyPopup);
            var ProjPopup = ProjName + "   " + ProjType + "   " + ProjIntro;
            //var SecondPopup = String.format("nhpup.popup(\'{0}\')", ProjPopup);
            //	    node.childNodes[4].setAttribute("onmouseover", SecondPopup);
            node.childNodes[4].setAttribute("title", ProjPopup);
            // var CompanyTooltip = [CompanyName, CompanyType, CompanyIntro];
	    // var ProjTooltip = [ProjName, ProjType, ProjIntro];
            // Item Name:/html/body/table/tbody/tr[2]/td/div[4]/table[1]/tbody/tr/td/table[1]/tbody/tr[2]/td

            var ItemPopup = document.createElement("div");
            ItemPopup.setAttribute("visibility", "hidden");
            var ItemInfo = evaluateXPath(wrapper.documentElement, "/html/body/table/tbody/tr[2]/td/div[4]/table[1]/tbody/tr/td/table[1]/tbody/tr/td[1]");
            ItemInfo.shift();
            ItemInfo.forEach(function(x) {
                var id = x.innerHTML;
                GetItemInfo(ItemPopup, id);
            });
            node.childNodes[5].appendChild(ItemPopup);
            node.childNodes[5].setAttribute("onmouseover", "");
            ///html/body/table/tbody/tr[2]/td/div[4]/table[1]/tbody/tr/td/table[1]/tbody/tr[2]/td[1]
            // console.log(CompanyTooltip);
            // console.log(ProjTooltip);
            // console.log(wrapper.documentElement);
	}
    });
}

function CheckPopUp(node) {
    node = node.parentNode;
    var id = node.childNodes[2].innerHTML;
    if(node.childNodes[3].hasAttribute("title") &&node.childNodes[4].hasAttribute("title") &&
       node.childNodes[5].hasAttribute("onmouseover")) {
        return 0;
    } else {
        GetTooltip(node, id);
        return 1;
    }
}

function GetItemInfo(node, id) {
    var parser = new DOMParser();
    var PostData = makePostData(id, "ItemView");
    $.post("ProjectsList.aspx", PostData, function(response, status){
	var separatorIndex = response.indexOf("|");
	if (separatorIndex != -1) {
            var validationFieldLength = parseInt(response.substring(0, separatorIndex));
            if (!isNaN(validationFieldLength)) {
                var validationField = response.substring(separatorIndex + 1, separatorIndex + validationFieldLength + 1);
                if (validationField != "") {
                    var validationFieldElement = theForm["__EVENTVALIDATION"];
                    if (!validationFieldElement) {
                        validationFieldElement = document.createElement("INPUT");
                        validationFieldElement.type = "hidden";
                        validationFieldElement.name = "__EVENTVALIDATION";
                        theForm.appendChild(validationFieldElement);
                    }
                    validationFieldElement.value = validationField;
                }
            }
	}
	var resultObj = eval(response.substring(separatorIndex + validationFieldLength + 1));
	if (resultObj.generalError) {
	    alert("General Error:" + resultObj.generalError);
	} else if (resultObj.error) {
	    alert("Error:" + resultObj.error.message);
	} else {
	    resultID = resultObj.id;
	    var Message = resultObj.result;
            node.innerHTML += Message;
	}
    });
}

function doRefuse(node, id) {
    var PostData = makePostData(id, "Refuse");    
    $.post("ProjectsList.aspx", PostData, function(response, status){
	var separatorIndex = response.indexOf("|");
	if (separatorIndex != -1) {
            var validationFieldLength = parseInt(response.substring(0, separatorIndex));
            if (!isNaN(validationFieldLength)) {
                var validationField = response.substring(separatorIndex + 1, separatorIndex + validationFieldLength + 1);
                if (validationField != "") {
                    var validationFieldElement = theForm["__EVENTVALIDATION"];
                    if (!validationFieldElement) {
                        validationFieldElement = document.createElement("INPUT");
                        validationFieldElement.type = "hidden";
                        validationFieldElement.name = "__EVENTVALIDATION";
                        theForm.appendChild(validationFieldElement);
                    }
                    validationFieldElement.value = validationField;
                }
            }
	}
	var resultObj = eval(response.substring(separatorIndex + validationFieldLength + 1));
	if (resultObj.generalError) {
	    alert("General Error:" + resultObj.generalError);
	} else if (resultObj.error) {
	    alert("Error:" + resultObj.error.message);
	} else {
	    node.parentNode.previousSibling.innerHTML = "退回;";
	}
    });
    
}

function evaluateXPath(aNode, aExpr) {
    var xpe = new XPathEvaluator();
    var nsResolver = xpe.createNSResolver(aNode.ownerDocument == null ?
                                           aNode.documentElement : aNode.ownerDocument.documentElement);
    var result = xpe.evaluate(aExpr, aNode, nsResolver, 0, null);
    var found = [];
    var res;
    while ((res = result.iterateNext()))
	found.push(res);
    return found;
}

// unsafeWindow._theFormPostData = __theFormPostData;
// unsafeWindow.makePostData = makePostData;
// unsafeWindow.doPass = doPass;
// unsafeWindow.runPass = runPass;

if (!String.format) {
    String.format = function(format) {
	var args = Array.prototype.slice.call(arguments, 1);
	return format.replace(/{(\d+)}/g, function(match, number) { 
	    return typeof args[number] != 'undefined'
		? args[number] 
		: match
	    ;
	});
    };
}

//var NodeList = $("[id^='ASPxPageControl1_grid1_DXDataRow']");

var NodeList = document.body.querySelectorAll("[id^='ASPxPageControl1_grid1_DXDataRow']");
for (var i=0; i<NodeList.length; i++) {
    var Item = NodeList[i];
    var id = Item.childNodes[2].innerHTML;
    var passLink = String.format("<a onclick='runPass(this, {0})' href='javascript:void(0);'>通过</a>", id);
    var refuseLink = String.format("<a onclick='doRefuse(this, {0})' href='javascript:void(0);'>退回</a>", id);
    Item.childNodes[9].innerHTML += passLink;
    Item.childNodes[9].innerHTML += refuseLink;
    Item.childNodes[1].setAttribute("onmouseover", "CheckPopUp(this)");
}

var $jq = jQuery; // this is safe in WP installations with noConflict mode (which is default)

nhpup = {

    pup: null,      // This is the popup box, represented by a div    
    identifier: "pup",  // Name of ID and class of the popup box
    minMargin: 15,  // Set how much minimal space there should be (in pixels)
                    // between the popup and everything else (borders, mouse)
    default_width: 200, // Will be set to width from css in document.ready
    move: false,   // Move it around with the mouse? we are only ready for that when the mouse event is set up.
                   // Besides, having this turned off intially is resource-friendly.

    /*
     Write message, show popup w/ custom width if necessary,
      make sure it disappears on mouseout
    */
    popup: function(p_msg, p_config)
    {
        // do track mouse moves and update position 
        this.move = true;
        // restore defaults
        this.pup.removeClass()
                .addClass(this.identifier)
                .width(this.default_width);

        // custom configuration
        if (typeof p_config != 'undefined') {
            if ('class' in p_config) {
                this.pup.addClass(p_config['class']);
            }
            if ('width' in p_config) {
                this.pup.width(p_config['width']);
            }
        }

        // Write content and display
        this.pup.html(p_msg).show();

        // Make sure popup goes away on mouse out and we stop the constant 
        //  positioning on mouse moves.
        // The event obj needs to be gotten from the virtual 
        //  caller, since we use onmouseover='nhpup.popup(p_msg)' 
        var t = this.getTarget(arguments.callee.caller.arguments[0]);
        $jq(t).unbind('mouseout').bind('mouseout', 
            function(e){
                nhpup.pup.hide();
                nhpup.move = false;
            }
        );
    },

    // set the target element position
    setElementPos: function(x, y)
    {
        // Call nudge to avoid edge overflow. Important tweak: x+10, because if
        //  the popup is where the mouse is, the hoverOver/hoverOut events flicker
        var x_y = this.nudge(x + 10, y);
        // remember: the popup is still hidden
        this.pup.css('top', x_y[1] + 'px')
                .css('left', x_y[0] + 'px');
    },

    /* Avoid edge overflow */
    nudge: function(x,y)
    {
        var win = $jq(window);

        // When the mouse is too far on the right, put window to the left
        var xtreme = $jq(document).scrollLeft() + win.width() - this.pup.width() - this.minMargin;
        if(x > xtreme) {
            x -= this.pup.width() + 2 * this.minMargin;
        }
        x = this.max(x, 0);

        // When the mouse is too far down, move window up
        if((y + this.pup.height()) > (win.height() +  $jq(document).scrollTop())) {
            y -= this.pup.height() + this.minMargin;
        }

        return [ x, y ];
    },

    /* custom max */
    max: function(a,b)
    {
        if (a>b) return a;
        else return b;
    },

    /*
     Get the target (element) of an event.
     Inspired by quirksmode
    */
    getTarget: function(e)
    {
        var targ;
        if (!e) var e = window.event;
        if (e.target) targ = e.target;
        else if (e.srcElement) targ = e.srcElement;
        if (targ.nodeType == 3) // defeat Safari bug
            targ = targ.parentNode;
        return targ;
    },

    onTouchDevice: function() 
    {
        var deviceAgent = navigator.userAgent.toLowerCase();
        return deviceAgent.match(/(iphone|ipod|ipad|android|blackberry|iemobile|opera m(ob|in)i|vodafone)/) !== null;
    }
};


/* Prepare popup and define the mouseover callback */
jQuery(document).ready(function(){
    // create default popup on the page    
    $jq('body').append('<div id="' + nhpup.identifier + '" class="' + nhpup.identifier + '" style="position:abolute; display:none; z-index:200;"></div>');
    nhpup.pup = $jq('#' + nhpup.identifier);

    // set dynamic coords when the mouse moves
    $jq(document).mousemove(function(e){ 
        if (!nhpup.onTouchDevice()) { // turn off constant repositioning for touch devices (no use for this anyway)
            if (nhpup.move){
                nhpup.setElementPos(e.pageX, e.pageY);
            }
        }
    });
});
