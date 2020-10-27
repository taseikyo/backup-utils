// ==UserScript==
// @name        字体样式美化
// @namespace   http://daysv.github.com
// @description 使得字体更加好看^_^
// @version     3
// @include     *
// @grant       none
// https://greasyfork.org/zh-CN/scripts/12877-字体样式美化/

var css = document.createElement('style');
var text = document.createTextNode('a:hover{color: #39F  !important;text-shadow:-5px 3px 18px #39F !important;-webkit-transition: all 0.3s ease-out;};a{-webkit-transition: all 0.3s ease-out;};*{text-decoration:none!important;font-weight:500!important;}*:not(i):not([class*="hermit"]):not([class*="btn"]):not([class*="button"]):not([class*="ico"]):not(i){font-family: "Microsoft Yahei", "Microsoft Yahei" !important; }*{text-shadow:0.005em 0.005em 0.025em #999999 !important;}');
css.appendChild(text);
document.getElementsByTagName('head') [0].appendChild(css);