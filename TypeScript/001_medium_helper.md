<img src="../images/001_medium_helper_head.png" alt="logo" height="120" align="right" title="medium-helper" />

# medium-helper
a tampermonkey script to improve **[Medium.com](https://medium.com/)** reading experience

## Features

- expand the reading area (728 -> 960)
- add a table of contents (hide/show according to scroll bar height)
- customize your own settings

## Preview

<img src="../images/001_medium_helper_preview.gif" alt="preview.gif">

## Installation

1. via [greasyfork.org](https://greasyfork.org)
	1. install [Tampermonkey Chrome Extension](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
	2. https://greasyfork.org/zh-CN/scripts/388676-medium-helper

2. via source code
	1. install npm (optional)
	2. install typescript
	3. install [Tampermonkey Chrome Extension](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
	4. install the script

```bash
>> git clone https://github.com/taseikyo/backup-utils.git
>> cd backup-utils
>> tsc 001_medium_helper.ts
```

The target js file is `001_medium_helper.js`, then create new script in Tampermonkey dashboard.

e.g.

```javascript
// ==UserScript==
// @name         medium-helper
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  a simple Medium helper to improve reading experience.
// @author       Lewis Tian (https://github.com/LewisTian)
// @match        https://*.medium.com/*
// @grant        MIT
// ==/UserScript==

"use strict";
/**
 *
 * Copyright (c) 2019 Lewis Tian. Licensed under the MIT license.
 * @authors   Lewis Tian (taseikyo@gmail.com)
 * @date      2019-07-30 10:39:19
 * @desc      a simple Medium helper to improve reading experience.
 *
 */
var CONFIG = {
    ...
};
var main = function () {
    ...
};
var toc = function (node) {
    ...
};
var pretty = function () {
	...
};
pretty();
main();
```