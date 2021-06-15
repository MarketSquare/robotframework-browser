/*
 This is MIT licensed Anton Medvedevs cool work:
 https://github.com/antonmedv/finder
 Static copy because of ease of installation
 */
var Limit;
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

function unique(a) {
    switch (rootDocument.querySelectorAll(selector(a)).length) {
        case 0:
            throw new Error(`Can't select any node with this selector: ${selector(a)}`);
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

const BROWSER_LIBRARY_ID = "browser-library-selector-recorder";
const BROWSER_LIBRARY_TEXT_ID = "browser-library-selector-recorder-target-text";

function addElement () {
  const newDiv = document.createElement("div");
  newDiv.style.display = "flex";
  newDiv.style.flexDirection = "column";
  newDiv.style.border = "2px solid blue";
  newDiv.style.borderRadius = "5px";
  newDiv.style.background = "white";
  newDiv.style.color = "black";
  newDiv.style.zIndex = "9000";
  newDiv.style.position = "fixed";
  newDiv.style.top = "16px";
  newDiv.style.left = "16px";
  newDiv.style.padding = "8px";
  newDiv.id = BROWSER_LIBRARY_ID;
  const header = document.createElement("h5");
  header.textContent = "Selector recorder";
  newDiv.appendChild(header);
  const targetSpan = document.createElement("span");
  targetSpan.id = BROWSER_LIBRARY_TEXT_ID;
  targetSpan.textContent = "NOTSET";
  newDiv.appendChild(targetSpan);
  const desc = document.createElement("span");
  desc.textContent = "Click focus to page and press (s) to record a selector.";
  newDiv.appendChild(desc);
  document.body.appendChild(newDiv);
}

window.selectorRecorderFindSelector = function() {
    return new Promise((resolve) => {
        let currentTarget = "NOTSET";

        function updateTexts() {
            document.getElementById(BROWSER_LIBRARY_TEXT_ID).textContent = currentTarget;
        }

        function mouseMoveListener(e) {
            console.log(e.pageY);
            const target = document.elementFromPoint(e.pageX, e.pageY);
            if (target) {
                currentTarget = finder(target);
                updateTexts();
            }
            const elem = document.getElementById(BROWSER_LIBRARY_ID);
            if (e.pageY < 120) {
                elem.style.top = null;
                elem.style.bottom = "16px";
            } else {
                elem.style.top = "16px";
                elem.style.bottom = null;
            }
        }

        function keydownListener(e) {
            const keyName = e.key;
            console.log(keyName);
            if (keyName === 's' || keyName === 'S') {
                document.removeEventListener('mousemove', mouseMoveListener);
                document.removeEventListener('keydown', keydownListener);
                document.getElementById(BROWSER_LIBRARY_ID).remove();
                clearInterval(intervalTimer);
                resolve(currentTarget);
            }
        }

        document.addEventListener('keydown', keydownListener);
        document.addEventListener('mousemove', mouseMoveListener);
        addElement();
        const intervalTimer = setInterval(updateTexts, 150);
    });
}
