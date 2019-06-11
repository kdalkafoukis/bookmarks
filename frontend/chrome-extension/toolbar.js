const url = chrome.extension.getURL('toolbar.html');
// const height = "50px";
const height = "50px";

console.log("Ok injected file worked","url",url);

const iframe = "<iframe id='main' src='"+url+"' style='border:0px;position:fixed;top:0;width: 100%;height:"+height+";' />"

$('html').append(iframe);

$('body').css({
    '-webkit-transform':'translateY(50px)'
})