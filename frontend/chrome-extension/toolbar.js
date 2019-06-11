const url = chrome.extension.getURL('toolbar.html');
console.log("Ok injected file worked","url",url);

const iframe = "<iframe id='main' src='"+url+"' style='border:0px;height:100%;position:absolute;top:0;left:0;width:100%' ></iframe>"

$('html').append(iframe);

$('body').css({
    '-webkit-transform':'translateY(50px)'
})