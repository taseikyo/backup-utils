/**
 * 
 * Copyright (c) 2019 Lewis Tian. Licensed under the MIT license.
 * @authors   Lewis Tian (taseikyo@gmail.com)
 * @date      2019-07-30 10:39:19
 * @link      https://github.com/taseikyo
 * @desc      a simple Medium helper to improve reading experience: 
 *             1. expand the reading area (728 -> 960)
 *             2. add a table of contents (hide/show according to scroll bar height)
 *             3. customize your own settings
 * 
 */


const CONFIG = {
  maxWidth: 960,            // article max-width (728px default -> 960px)
  likeBoxLeftFloat: 5,      // follow/like box left float (50% default -> -5%)
  tocTop: 20,               // toc top float (50% default)
  tocRight: 0,
  scrollTopShow: 300,       // show toc when `scrollTopShow` from top 
  scrollBottomHide: 1600,   // hide toc when scroll to  'See response' area
  highlightedStart: 150,    // highlighted text
  delay: 500
};

const main = () => {
  let root = document.querySelector('#root')
  if (root == null) {
    return
  }
  let article = root.children[0].querySelector('article')
  if (article == null) {
    return
  }
  // hand or bookmark
  let likeBox = <HTMLElement>article.nextSibling
  // maybe there is a picture on the top of text, so we select the last node
  let section = article.querySelector('div')!.querySelector('section')
  let textBody = section!.children[section!.children.length-1].children[0]

  likeBox!.setAttribute('style', `left: -${CONFIG.likeBoxLeftFloat}% `)
  textBody.setAttribute('style', `max-width: ${CONFIG.maxWidth}px !important`)

  for (let i of <any>textBody.children) {
    if (i.nodeName === 'h1' || i.nodeName === 'H1') {
      toc(textBody)
      break
    }
  }

  setTimeout(delayHighlight, CONFIG.delay);
}

/**
 * add toc of the article
 *
 * @node: the arcile text div
 */
const toc = (node: Element) => {
  let anchorRoot = document.createElement('div')
  anchorRoot.className = 'BlogAnchor'

  let p = document.createElement('p')
  let a = document.createElement('a')
  a.href = '#'
  a.innerText = 'Table of contents'
  p.appendChild(a)
  anchorRoot.appendChild(p)

  let anchorBody = document.createElement('div')
  anchorBody.className = 'AnchorContent'
  anchorBody.id = 'AnchorContent'

  for (let i of <any>node.children) {
    if (i.nodeName === 'h1' || i.nodeName === 'H1') {
      let li = document.createElement('li')
      let a = document.createElement('a')
      a.href = `#${i.id}`
      a.innerText = i.innerText
      li.appendChild(a)

      li.setAttribute('style', 'list-style-type: none; padding-right: 10px;')
      anchorBody.appendChild(li)
    }
  }

  let line = document.createElement('hr')
  anchorRoot.appendChild(line)
  anchorRoot.appendChild(anchorBody)

  // set style
  p.setAttribute('style', 'font-weight: bold; font-size: 1.2em;')
  anchorRoot.setAttribute('style', `position: fixed; right: ${CONFIG.tocRight}%; top: ${CONFIG.tocTop}%; background: #f4f7f9; padding: 10px; line-height: 180%;`)

  document.getElementsByTagName('body')[0].appendChild(anchorRoot)
  anchorRoot.style.visibility = 'hidden'

  window.addEventListener('scroll', (evt: Event) => {
    let scrollTop = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;
    if (scrollTop >= document.body.clientHeight - CONFIG.scrollBottomHide) {
      anchorRoot.style.visibility = 'hidden'
    }
    else if(scrollTop >= CONFIG.scrollTopShow) {
      anchorRoot.style.visibility = 'visible'
    } else {
      anchorRoot.style.visibility = 'hidden'
    }
  });
}

/**
 * set highlight text style
 * add margin according CONFIG
 */
const delayHighlight = () => {
	let root = document.querySelector('#root')
  let article = root!.children[0].querySelector('article')
  if (article == null) {
    return
  }

  let highlightedBox = article.querySelector('aside')
  if (highlightedBox) {
  	for (let x of <any>highlightedBox.children) {
	    x.querySelector('h4').setAttribute('style', `margin-inline-start: ${CONFIG.highlightedStart}px; !important;`)
	  }
  }
}

// https://greasyfork.org/zh-CN/scripts/12877-字体样式美化/
const pretty = () => {
  let css = document.createElement('style')
  let text = document.createTextNode('a:hover{color: #39F !important; text-shadow:-5px 3px 18px #39F !important; -webkit-transition: all 0.3s ease-out;}; a{-webkit-transition: all 0.3s ease-out;};*{text-decoration:none!important;font-weight:500!important;}*:not(i):not([class*="hermit"]):not([class*="btn"]):not([class*="button"]):not([class*="ico"]):not(i){font-family: "Microsoft Yahei", "Microsoft Yahei" !important; }*{text-shadow:0.005em 0.005em 0.025em #999999 !important;}')
  css.appendChild(text)
  document.getElementsByTagName('head')[0].appendChild(css)
}

pretty()
main()