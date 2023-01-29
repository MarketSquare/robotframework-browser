/*
 This is MIT licensed Anton Medvedevs cool work:
 https://github.com/antonmedv/finder
 Static copy because of ease of installation
 */
let Limit;
(function (a) {
    a[a.All = 0] = "All", a[a.Two = 1] = "Two", a[a.One = 2] = "One"
})(Limit || (Limit = {}));
let config, rootDocument;

export function finder(a, b) {
    if (a.nodeType !== Node.ELEMENT_NODE) throw new Error(`Can't generate CSS selector for non-element node type.`);
    if ("html" === a.tagName.toLowerCase()) return "html";
    const c = {
        root: document.body,
        idName: () => !0,
        className: () => !0,
        tagName: () => !0,
        attr: () => !1,
        seedMinLength: 1,
        optimizedMinLength: 2,
        threshold: 1e3,
        maxNumberOfTries: 1e4
    };
    config = Object.assign(Object.assign({}, c), b), rootDocument = findRootDocument(config.root, c);
    let d = bottomUpSearch(a, Limit.All, () => bottomUpSearch(a, Limit.Two, () => bottomUpSearch(a, Limit.One)));
    if (d) {
        const b = sort(optimize(d, a));
        return 0 < b.length && (d = b[0]), selector(d)
    }
    throw new Error(`Selector was not found.`)
}

function findRootDocument(a, b) {
    return a.nodeType === Node.DOCUMENT_NODE ? a : a === b.root ? a.ownerDocument : a
}

function bottomUpSearch(a, b, c) {
    let d = null, e = [], f = a, g = 0;
    for (; f && f !== config.root.parentElement;) {
        let a = maybe(id(f)) || maybe(...attr(f)) || maybe(...classNames(f)) || maybe(tagName(f)) || [any()];
        const h = index(f);
        if (b === Limit.All) h && (a = a.concat(a.filter(dispensableNth).map(a => nthChild(a, h)))); else if (b === Limit.Two) a = a.slice(0, 1), h && (a = a.concat(a.filter(dispensableNth).map(a => nthChild(a, h)))); else if (b === Limit.One) {
            const [b] = a = a.slice(0, 1);
            h && dispensableNth(b) && (a = [nthChild(b, h)])
        }
        for (let b of a) b.level = g;
        if (e.push(a), e.length >= config.seedMinLength && (d = findUniquePath(e, c), d)) break;
        f = f.parentElement, g++
    }
    return d || (d = findUniquePath(e, c)), d
}

function findUniquePath(a, b) {
    const c = sort(combinations(a));
    if (c.length > config.threshold) return b ? b() : null;
    for (let d of c) if (unique(d)) return d;
    return null
}

function selector(a) {
    let b = a[0], c = b.name;
    for (let d = 1; d < a.length; d++) {
        const e = a[d].level || 0;
        c = b.level === e - 1 ? `${a[d].name} > ${c}` : `${a[d].name} ${c}`, b = a[d]
    }
    return c
}

function penalty(a) {
    return a.map(a => a.penalty).reduce((a, b) => a + b, 0)
}

function unique(candidate) {
    switch (rootDocument.querySelectorAll(selector(candidate)).length) {
        case 0:
            throw new Error(`Can't select any node with this selector: ${selector(candidate)}`);
        case 1:
            return !0;
        default:
            return !1;
    }
}

function id(a) {
    const b = a.getAttribute("id");
    return b && config.idName(b) ? {name: "#" + cssesc(b, {isIdentifier: !0}), penalty: 0} : null
}

function attr(a) {
    const b = Array.from(a.attributes).filter(a => config.attr(a.name, a.value));
    return b.map(a => ({name: "[" + cssesc(a.name, {isIdentifier: !0}) + "=\"" + cssesc(a.value) + "\"]", penalty: .5}))
}

function classNames(a) {
    const b = Array.from(a.classList).filter(config.className);
    return b.map(a => ({name: "." + cssesc(a, {isIdentifier: !0}), penalty: 1}))
}

function tagName(a) {
    const b = a.tagName.toLowerCase();
    return config.tagName(b) ? {name: b, penalty: 2} : null
}

function any() {
    return {name: "*", penalty: 3}
}

function index(a) {
    const b = a.parentNode;
    if (!b) return null;
    let c = b.firstChild;
    if (!c) return null;
    let d = 0;
    for (; c && (c.nodeType === Node.ELEMENT_NODE && d++, c !== a);) c = c.nextSibling;
    return d
}

function nthChild(a, b) {
    return {name: a.name + `:nth-child(${b})`, penalty: a.penalty + 1}
}

function dispensableNth(a) {
    return "html" !== a.name && !a.name.startsWith("#")
}

function maybe(...a) {
    const b = a.filter(notEmpty);
    return 0 < b.length ? b : null
}

function notEmpty(a) {
    return null !== a && a !== void 0
}

function* combinations(a, b = []) {
    if (0 < a.length) for (let c of a[0]) yield* combinations(a.slice(1, a.length), b.concat(c)); else yield b
}

function sort(a) {
    return Array.from(a).sort((c, a) => penalty(c) - penalty(a))
}

function* optimize(a, b, c = {counter: 0, visited: new Map}) {
    if (2 < a.length && a.length > config.optimizedMinLength) for (let d = 1; d < a.length - 1; d++) {
        if (c.counter > config.maxNumberOfTries) return;
        c.counter += 1;
        const e = [...a];
        e.splice(d, 1);
        const f = selector(e);
        if (c.visited.has(f)) return;
        unique(e) && same(e, b) && (yield e, c.visited.set(f, !0), yield* optimize(e, b, c))
    }
}

function same(a, b) {
    return rootDocument.querySelector(selector(a)) === b
}

const regexAnySingleEscape = /[ -,\.\/:-@\[-\^`\{-~]/, regexSingleEscape = /[ -,\.\/:-@\[\]\^`\{-~]/,
    regexExcessiveSpaces = /(^|\\+)?(\\[A-F0-9]{1,6})\x20(?![a-fA-F0-9\x20])/g,
    defaultOptions = {escapeEverything: !1, isIdentifier: !1, quotes: "single", wrap: !1};

function cssesc(a, b = {}) {
    const c = Object.assign(Object.assign({}, defaultOptions), b);
    "single" != c.quotes && "double" != c.quotes && (c.quotes = "single");
    const d = "double" == c.quotes ? "\"" : "'", e = c.isIdentifier, f = a.charAt(0);
    let g = "", h = 0;
    for (const f = a.length; h < f;) {
        const b = a.charAt(h++);
        let i, j = b.charCodeAt(0);
        if (32 > j || 126 < j) {
            if (55296 <= j && 56319 >= j && h < f) {
                const b = a.charCodeAt(h++);
                56320 == (64512 & b) ? j = ((1023 & j) << 10) + (1023 & b) + 65536 : h--
            }
            i = "\\" + j.toString(16).toUpperCase() + " "
        } else i = c.escapeEverything ? regexAnySingleEscape.test(b) ? "\\" + b : "\\" + j.toString(16).toUpperCase() + " " : /[\t\n\f\r\x0B]/.test(b) ? "\\" + j.toString(16).toUpperCase() + " " : "\\" == b || !e && ("\"" == b && d == b || "'" == b && d == b) || e && regexSingleEscape.test(b) ? "\\" + b : b;
        g += i
    }
    return e && (/^-[-\d]/.test(g) ? g = "\\-" + g.slice(1) : /\d/.test(f) && (g = "\\3" + f + " " + g.slice(1))), g = g.replace(regexExcessiveSpaces, function (a, b, c) {
        return b && b.length % 2 ? a : (b || "") + c
    }), !e && c.wrap ? d + g + d : g
}

/* Cool work ends and Browser library work begins */
const BROWSER_LIBRARY_SELECTOR_CLASS = "browser-library-selector-class";
const BROWSER_LIBRARY_MONOSPACED_CLASS = "browser-library-monospaced-class";
const BROWSER_LIBRARY_SYSFONT_CLASS = "browser-library-sysfont-class";
const BROWSER_LIBRARY_ID = "browser-library-selector-recorder";
const BROWSER_LIBRARY_HEADER_ID = "browser-library-selector-recorder-header";
const BROWSER_LIBRARY_TEXT_ID = "browser-library-selector-recorder-target-text";
const BROWSER_LIBRARY_SELECT_BUTTON_ID = "browser-library-select-selector";
const BROWSER_LIBRARY_SELECT_CANCEL_BUTTON_ID = "browser-library-cancel-selector";
const BROWSER_LIBRARY_DESCRIPTION = "browser-library-selector-recorder-description-text";
const BROWSER_LIBRARY_SELECTION = "browser-library-selection-id";
const BROWSER_LIBRARY_SELECTIONS = "browser-library-selections-id";
const BROWSER_LIBRARY_SELECTION_FRAME = "browser-library-selection-frame";
const BROWSER_LIBRARY_SELECTION_PANEL = "browser-library-selection-panel";
const BROWSER_LIBRARY_SELECTION_OK_BUTTON = "browser-library-selection-ok-button";
const BROWSER_LIBRARY_SELECTION_CANCEL_BUTTON = "browser-library-selection-cancel-button";
const BROWSER_LIBRARY_SELECTION_HIGHLIGHT_BUTTON = "browser-library-selection-highlight-button";
const BROWSER_LIBRARY_SELECTION_BUTTON_CLASS = "browser-library-selection-button-class";

function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

function addElement(label) {
    const newDiv = htmlToElement(`
    <div id="${BROWSER_LIBRARY_ID}" class="${BROWSER_LIBRARY_SELECTOR_CLASS}">
        <h5 id="${BROWSER_LIBRARY_HEADER_ID}" class="${BROWSER_LIBRARY_SYSFONT_CLASS}">
        ${"Selector Recorder" + (label && label.length ? " For '" + label + "'" : "")}
        </h5>
        <span id="${BROWSER_LIBRARY_TEXT_ID}" class="${BROWSER_LIBRARY_MONOSPACED_CLASS}">NOTSET</span>
        <span id="${BROWSER_LIBRARY_DESCRIPTION}" class="${BROWSER_LIBRARY_MONOSPACED_CLASS}"></span>
        <span style="max-width: 300px" class="${BROWSER_LIBRARY_SYSFONT_CLASS}">Move mouse and Hover over an element to record a selector.</span>
    </div>
    `)
    const elem = document.body.appendChild(newDiv);
    dragElement(elem, document.getElementById(BROWSER_LIBRARY_HEADER_ID));
    setTimeout(() => elem.focus(), 300);
}

function dragElement(elmnt, header) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    header.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

function elementSelectorFromPointInFrame(x, y) {
    const subelementFromPoint = (parentElement) => {
        const element = parentElement.elementFromPoint(x, y);
        if (!element) {
            return '???';
        }
        if (element.shadowRoot) {
            const parentSelector = finder(element, {root: parentElement})
            const [childSelector, rect] = subelementFromPoint(element.shadowRoot);
            return [childSelector.map(s => parentSelector + " >> " + s), rect];
        }
        const rect = element.getBoundingClientRect();
        const left = parseFloat(window.getComputedStyle(element, null).getPropertyValue('padding-left')) || 0;
        const top = parseFloat(window.getComputedStyle(element, null).getPropertyValue('padding-top')) || 0;
        const selectors = [];
        const selector1 = finder(element, {root: parentElement})
        selectors.push(selector1);
        const selector2 = finder(element, {
            root: parentElement,
            className: (c) => !selector1.includes("." + c),
        });
        if (!selectors.includes(selector2)) selectors.push(selector2);
        const selector3 = finder(element, {
            root: parentElement,
            idName: (id) => !selector1.includes('#' + id)
        });
        if (!selectors.includes(selector3)) selectors.push(selector3);
        const selector4 = finder(element, {
            root: parentElement,
            className: (c) => !selector1.includes("." + c),
            idName: (id) => !selector1.includes('#' + id),
        });
        if (!selectors.includes(selector4)) selectors.push(selector4);
        return [selectors, {
            top: rect.top,
            left: rect.left,
            height: rect.height,
            width: rect.width,
            paddingLeft: left,
            paddingTop: top
        }];
    }
    return subelementFromPoint(document);
}

window.subframeSelectorRecorderFindSelector = function (myid) {

    let currentCssSelector = "NOTSET";

    function mouseMoveListener(e) {
        const cssselector = elementSelectorFromPointInFrame(e.pageX - window.scrollX, e.pageY - window.scrollY);
        if (cssselector && cssselector !== currentCssSelector) {
            window.setRecordedSelector(myid, cssselector);
            currentCssSelector = cssselector;
        }
    }

    document.addEventListener('mousemove', mouseMoveListener);
}

window.selectorRecorderFindSelector = function (label) {
    return new Promise((resolve) => {
        let currentCssSelector = "NOTSET";
        let lastTotalRecord = [];
        let lastDisplayedRecord = "NOTSET";
        let lastTotalRecordTime = new Date().getTime();
        let findingElement = true;
        let updatingTexts = true;

        async function findingElementUpdateText() {
            if (!findingElement) return;
            const selectors = ((await window.getRecordedSelectors()) || []);
            const recorded = selectors.map(i => i[0]);
            const displayed = recorded.map(i => i[0]).join(" >>> ");
            if (lastDisplayedRecord !== displayed) {
                document.getElementById(BROWSER_LIBRARY_TEXT_ID).textContent = displayed;
                lastTotalRecord = recorded;
                lastDisplayedRecord = displayed;
                lastTotalRecordTime = new Date().getTime();
            } else {
                const timediff = new Date().getTime() - lastTotalRecordTime;
                if (timediff > 3000) {
                    findingElement = false;
                    const rect = selectors.map(i => i[1]).reduce((acc, cur) => {
                        return {
                            top: acc.top + cur.top + acc.paddingTop,
                            left: acc.left + cur.left + acc.paddingLeft,
                            width: cur.width,
                            height: cur.height,
                            paddingLeft: cur.paddingLeft,
                            paddingTop: cur.paddingTop
                        }
                    }, {
                        top: 0, left: 0, width: 0, height: 0, paddingTop: 0, paddingLeft: 0
                    });
                    const div = htmlToElement(`<div id="${BROWSER_LIBRARY_SELECTION_FRAME}" style="
position: fixed;
top: ${rect.top - 2}px;
left: ${rect.left - 2}px;
width: ${rect.width + 4}px;
height: ${rect.height+ 4}px;

"><div class="found-element animate-flicker" style="
width: 100%;
height: 100%;

"></div>
<div
style="
position: relative;
display: flex;
flex-wrap: wrap;"
>
<button id="${BROWSER_LIBRARY_SELECT_BUTTON_ID}" class="${BROWSER_LIBRARY_SELECTOR_CLASS}"
>Select</button>
<button id="${BROWSER_LIBRARY_SELECT_CANCEL_BUTTON_ID}" class="${BROWSER_LIBRARY_SELECTOR_CLASS}"
>Cancel</button>
</div>
</div>`);
                    document.body.appendChild(div);
                    const selectButton = document.getElementById(BROWSER_LIBRARY_SELECT_BUTTON_ID);
                    const cancelButton = document.getElementById(BROWSER_LIBRARY_SELECT_CANCEL_BUTTON_ID);
                    selectButton.onclick = () => {
                        cancelButton.remove();
                        selectButton.remove();
                        displaySelection(div);
                    };
                    cancelButton.onclick = () => {
                        div.remove();
                        findingElement = true;
                    };
                }
                document.getElementById(BROWSER_LIBRARY_DESCRIPTION).textContent = `${Math.round(300 - timediff / 10) / 100} s`;
            }
        }

        async function updateTexts() {
            await findingElementUpdateText()
            setTimeout(() => {
            if (updatingTexts) {
                window.requestAnimationFrame(updateTexts);
            }}, 100);
        }

        function displaySelection(focusDiv) {
            const maxit = Math.min(...lastTotalRecord.map(i => i.length));
            const options = [];
            for (let i = 0; i < maxit; i++) {
                const item = lastTotalRecord.map(j => j[i]).join(" >>> ");
                options.push(item);
            }
            const oldElement = document.getElementById(BROWSER_LIBRARY_ID);
            const oldPosition = oldElement.getBoundingClientRect();
            const div = htmlToElement(`<div id="${BROWSER_LIBRARY_SELECTION_PANEL}" class="${BROWSER_LIBRARY_SELECTOR_CLASS}" style="
    display: flex;
    flex-direction: column;
    z-index: 2147483647;
    position: fixed;
    top: ${oldPosition.top}px;
    left: ${oldPosition.left}px;">
<style>
</style>
<span>Select selector pattern to use:</span>
<input id="${BROWSER_LIBRARY_SELECTION}"
       value="${options[0]}"
       name="${BROWSER_LIBRARY_SELECTION}"
       list="${BROWSER_LIBRARY_SELECTIONS}">
<datalist id="${BROWSER_LIBRARY_SELECTIONS}">
${options.map(o => `<option value="${o}"/>`).join("\n")}
</datalist>
<button id="${BROWSER_LIBRARY_SELECTION_OK_BUTTON}" class="${BROWSER_LIBRARY_SELECTION_BUTTON_CLASS} ${BROWSER_LIBRARY_SELECTOR_CLASS}">Take It</button>
<button id="${BROWSER_LIBRARY_SELECTION_HIGHLIGHT_BUTTON}" class="${BROWSER_LIBRARY_SELECTION_BUTTON_CLASS} ${BROWSER_LIBRARY_SELECTOR_CLASS}">Highlight</button>
<button id="${BROWSER_LIBRARY_SELECTION_CANCEL_BUTTON}" class="${BROWSER_LIBRARY_SELECTION_BUTTON_CLASS} ${BROWSER_LIBRARY_SELECTOR_CLASS}">Reselect</button>
</div>`);
            oldElement.style.visibility = 'hidden';
            document.body.appendChild(div);
            const selection = document.getElementById(BROWSER_LIBRARY_SELECTION)
            document.getElementById(BROWSER_LIBRARY_SELECTION_OK_BUTTON).onclick = () => {
                cleanup();
                focusDiv.remove();
                div.remove();
                resolve(selection.value);
            };
            document.getElementById(BROWSER_LIBRARY_SELECTION_CANCEL_BUTTON).onclick = () => {
                oldElement.style.visibility = 'visible';
                focusDiv.remove();
                div.remove();
                findingElement = true;
            };
            document.getElementById(BROWSER_LIBRARY_SELECTION_HIGHLIGHT_BUTTON).onclick = () => {
                window.highlightPWSelector(selection.value);
            }
        }

        async function mouseMoveListener(e) {
            const elem = document.getElementById(BROWSER_LIBRARY_ID);
            const rect = elem.getBoundingClientRect()
            const xmin = rect.left + window.scrollX;
            const xmax = xmin + rect.width;
            const ymin = rect.top + window.scrollY;
            const ymax = ymin + rect.height;
            if (e.pageX >= xmin && e.pageX <= xmax &&
                e.pageY >= ymin && e.pageY <= ymax) {
                return;
            }
            const target = elementSelectorFromPointInFrame(e.pageX - window.scrollX, e.pageY - window.scrollY);
            if (target && target !== currentCssSelector) {
                window.setRecordedSelector(0, target);
                currentCssSelector = target;
                await findingElementUpdateText();
            }
        }

        function cleanup() {
            document.removeEventListener('mousemove', mouseMoveListener);
            document.getElementById(BROWSER_LIBRARY_ID).remove();
            updatingTexts = false;
        }

        document.addEventListener('mousemove', mouseMoveListener);
        const style = htmlToElement(`<style>
#${BROWSER_LIBRARY_SELECTION_FRAME}{
    position: absolute;
    z-index: 2147483646;
}
@keyframes flickerAnimation {
  0%   { opacity:1; }
  50%  { opacity:0; }
  100% { opacity:1; }
}
@-o-keyframes flickerAnimation{
  0%   { opacity:1; }
  50%  { opacity:0; }
  100% { opacity:1; }
}
@-moz-keyframes flickerAnimation{
  0%   { opacity:1; }
  50%  { opacity:0; }
  100% { opacity:1; }
}
@-webkit-keyframes flickerAnimation{
  0%   { opacity:1; }
  50%  { opacity:0; }
  100% { opacity:1; }
}
.animate-flicker {
   -webkit-animation: flickerAnimation 1s infinite;
   -moz-animation: flickerAnimation 1s infinite;
   -o-animation: flickerAnimation 1s infinite;
    animation: flickerAnimation 1s infinite;
}
.found-element{
    border: 2px dashed green;
    box-shadow:0 0 20px green;
}

#${BROWSER_LIBRARY_ID} {
    display: flex;
    flex-direction: column;
    border: 1px solid lightblue;
    border-radius: 15px;
    z-index: 2147483647;
    position: fixed;
    top: 56px;
    left: 99px;
    background: rgba(0, 0, 139, 0.5);
    padding: 12px;
    -webkit-backdrop-filter: blur(5px);
    backdrop-filter: blur(5px);
}

#${BROWSER_LIBRARY_HEADER_ID} {
    cursor: move;
    background: lightgray;
    color: darkblue;
    border-radius: 3px;
    padding: 0px 5px;
    margin: 0px;
    margin-bottom: 10px;
}


.${BROWSER_LIBRARY_SELECTOR_CLASS},
.${BROWSER_LIBRARY_MONOSPACED_CLASS} {
    font-family: monospace;
    font-size: medium;
    font-weight: normal;
}

.${BROWSER_LIBRARY_SYSFONT_CLASS},
button.${BROWSER_LIBRARY_SELECTOR_CLASS} {
    font-family: system-ui, -apple-system, sans-serif !important;
}

.${BROWSER_LIBRARY_SELECTOR_CLASS} {
    color: white;
    -webkit-backdrop-filter: blur(5px);
    backdrop-filter: blur(5px);
    box-shadow: 2px 2px 5px darkblue;
}

#${BROWSER_LIBRARY_SELECT_BUTTON_ID} {
    background: #00008b70;
    padding: 0px 5px;
    border: 1px solid lightblue;
    border-radius: 1rem;
    cursor: pointer;
    margin: 0.5rem;
}

#${BROWSER_LIBRARY_SELECT_BUTTON_ID}:hover {
    color: black;
    background: lightblue;
    border-color: white;
}
#${BROWSER_LIBRARY_SELECT_CANCEL_BUTTON_ID} {
    background: #09090970;
    padding: 0px 5px;
    border: 1px solid lightgray;
    border-radius: 1rem;
    cursor: pointer;
    margin: 0.5rem;
    box-shadow: 2px 2px 5px black;
}
#${BROWSER_LIBRARY_SELECT_CANCEL_BUTTON_ID}:hover {
    background: lightgray;
    border-color: black;
    color: black;
}

#${BROWSER_LIBRARY_SELECTION_PANEL} {
    display: flex;
    flex-direction: column;
    border: 1px solid lightblue;
    border-radius: 15px;
    z-index: 2147483647;
    position: fixed;
    background: rgba(0, 0, 139, 0.5);
    padding: 12px;
    color: white;
    -webkit-backdrop-filter: blur(5px);
    backdrop-filter: blur(5px);
}

#${BROWSER_LIBRARY_SELECTION}:hover {
    background: white;
}

#${BROWSER_LIBRARY_SELECTION} {
    background: #d5d5d5;
    color: black;
    padding: 4px;
    margin: 4px;
    border: 1px solid darkblue;
    font-family: monospace;
    font-size: medium;
    font-weight: normal;
}
.${BROWSER_LIBRARY_SELECTION_BUTTON_CLASS} {
    color: white;
    background: #00008b70;
    border: 1px solid lightblue;
    text-align: center;
    vertical-align: middle;
    margin: 4px 0px;
    box-shadow: 2px 2px 5px black;
    border-radius: 1rem;
    padding: 4px;
}
.${BROWSER_LIBRARY_SELECTION_BUTTON_CLASS}:hover {
    color: black;
    background: lightblue;
    border-color: white;
}

</style>`)
        document.head.appendChild(style);
        addElement(label);
        window.requestAnimationFrame(updateTexts);
    });
}
