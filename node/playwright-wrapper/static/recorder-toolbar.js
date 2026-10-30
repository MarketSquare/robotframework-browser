// Copyright 2020-     Robot Framework Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// The Robot Framework recorder toolbar, injected into the page under test.
//
// The host sits in an `x-pw-glass` element: Playwright's injected recorder
// ignores every event whose composed path holds one (`_ignoreOverlayEvent`),
// so a toolbar click is never recorded, and never becomes the last Action
// that Playwright attributes the next navigation to. Only `contextmenu` is not
// checked there, so it is stopped before it reaches the recorder. The shadow
// root is closed to keep the page's scripts out of the toolbar.

(function () {
    function installToolbar(TAG) {
        // Sub-frames must not get their own toolbar.
        if (window.top !== window) return;
        if (window.__rfbToolbarRender) return;

        const POSITION_KEY = 'rfb.toolbar.position';
        const COLLAPSED_KEY = 'rfb.toolbar.collapsed';
        const SIZE_KEY = 'rfb.toolbar.size';
        // Mirrors NAME_LIMIT in Browser/recorder/names.py.
        const NAME_LIMIT = 200;

        const read = (key, fallback) => {
            try {
                const raw = window.sessionStorage.getItem(key);
                return raw === null ? fallback : JSON.parse(raw);
            } catch {
                return fallback;
            }
        };
        const write = (key, value) => {
            try {
                window.sessionStorage.setItem(key, JSON.stringify(value));
            } catch {
                /* storage disabled - layout simply does not persist */
            }
        };

        const LOGO =
            '<svg class="logo" role="img" aria-label="Browser library" viewBox="422 465 1664 1219" xmlns="http://www.w3.org/2000/svg"><rect fill="#b82e24" x="562" y="759" width="349.9" height="687.3" transform="rotate(-15,736.9,1102.7)"/><rect fill="#d63a2e" x="900" y="668.4" width="350.6" height="687.3" transform="rotate(-15,1075.3,1012.1)"/><path fill="#fff" d="m 955.4,1004.6 c 11.1,9.5 26.1,12.9 40.2,9.1 8.4,-2.2 15.9,-7 21.6,-13.7 l 80.5,-92.6 c 0.5,-0.6 1,-1.2 1.5,-1.8 15.3,-18.7 12.6,-46.3 -6.1,-61.6 -18.7,-15.3 -46.3,-12.6 -61.6,6.1 l -80.2,92.5 c -15.9,18.2 -14,45.9 4.2,61.9 l -0.1,0 z"/><path fill="#fff" stroke="#000" stroke-width="14.17" d="m 1217.5,659.5 v -0 c 0,0 -120.8,-69.8 -120.8,-69.8 -18.3,-10.6 -40,-13.5 -60.4,-8.1 L 558,709.8 c -20.4,5.5 -37.8,18.8 -48.4,37.1 l -69.6,121 c -10.5,18.3 -13.4,40 -8,60.3 l 128.2,478.3 c 5.5,20.4 18.8,37.8 37.1,48.4 l 120.7,69.8 c 18.3,10.4 40,13.2 60.4,7.8 l 478.3,-128.2 c 20.4,-5.4 37.8,-18.7 48.4,-36.9 l 69.7,-120.8 c 10.6,-18.3 13.5,-40 8,-60.4 L 1254.6,707.9 c -5.4,-20.4 -18.8,-37.9 -37.1,-48.4 z m 76.4,533.5 c 2.1,8 1,16.6 -3.1,23.7 l -53.4,92.5 c -4.2,7.2 -11,12.4 -19,14.6 l -447.2,119.8 c -8,2.1 -16.6,1 -23.7,-3.1 l -92.2,-53.5 c -7.2,-4.2 -12.4,-11 -14.6,-19 L 521,921.3 c -2.1,-8 -1,-16.6 3.1,-23.7 l 53.1,-92.4 c 4.2,-7.2 11,-12.4 19,-14.6 l 447.3,-119.9 c 8,-2.1 16.6,-1 23.7,3.1 l 92.5,53.4 c 7.2,4.2 12.4,11 14.6,19 l 119.6,446.9 z"/><path fill="#fff" d="m 703.4,1091.8 c 23.4,-6.3 37.2,-30.3 31,-53.6 -4.7,-17.6 5.7,-35.7 23.3,-40.4 17.6,-4.7 35.7,5.7 40.4,23.3 l 0,0.1 c 6.3,23.4 30.3,37.2 53.7,30.9 23.4,-6.3 37.2,-30.3 30.9,-53.7 -18,-62.3 -82,-99.3 -144.9,-83.7 -64.7,16 -104.2,81.4 -88.1,146.1 h 0 c 6.3,23.4 30.3,37.2 53.6,31 z"/><path fill="#fff" d="m 1177.3,1267.3 -392.7,105.2 c -23.4,6.3 -47.5,-7.6 -53.8,-31 v 0 c -19,-71 72.5,-157.2 204.3,-192.5 131.8,-35.3 254.2,-6.4 273.2,64.6 v 0 c 6.3,23.4 -7.6,47.5 -31,53.8 z"/><rect fill="#1d8d22" x="1041.9" y="583.9" width="440.9" height="866.1" transform="rotate(15,1262.3,1017)"/><rect fill="#2ead33" x="1467.7" y="698.2" width="441.8" height="866.1" transform="rotate(15,1688.6,1131.2)"/><path d="m 1562.5,1047.5 c 6.1,17.4 20.4,30.6 38.1,35.3 10.6,2.9 21.8,2.4 32.2,-1.3 L 1779,1031.1 c 0.9,-0.3 1.9,-0.6 2.8,-1 28.5,-10.7 42.9,-42.5 32.1,-71 -10.7,-28.5 -42.5,-42.9 -71,-32.1 l -145.9,50.4 c -28.8,9.9 -44.2,41.3 -34.4,70.2 z"/><path stroke="#fff" stroke-width="14.17" d="m 2065.9,836.2 v -0.1 l -87.8,-152.3 c -13.3,-23 -35.1,-39.9 -60.8,-46.9 L 1314.6,475.5 c -25.7,-6.8 -53.1,-3.2 -76.2,10 l -152.2,88.1 c -23,13.3 -39.8,35.1 -46.7,60.8 L 878.1,1237.1 c -6.9,25.7 -3.3,53.1 10,76.2 l 87.8,152.2 c 13.4,22.9 35.3,39.7 61,46.5 l 602.7,161.5 c 25.7,6.9 53,3.4 76.1,-9.8 l 152.1,-88 c 23.1,-13.2 40,-35.2 46.8,-61 l 161.4,-602.5 c 7,-25.7 3.4,-53.1 -10,-76.2 z m -252.7,630.3 c -2.7,10.1 -9.3,18.7 -18.4,23.9 l -116.6,67.3 c -9.1,5.2 -19.8,6.6 -29.9,3.9 l -563.5,-151 c -10.1,-2.7 -18.7,-9.3 -23.9,-18.4 l -66.9,-116.5 c -5.2,-9.1 -6.6,-19.8 -3.9,-29.9 L 1141,682.9 c 2.7,-10.1 9.3,-18.7 18.4,-23.9 l 116.2,-67.3 c 9.1,-5.2 19.8,-6.6 29.9,-3.9 l 563.6,151 c 10.1,2.7 18.7,9.3 23.9,18.4 l 67.3,116.5 c 5.2,9.1 6.6,19.8 3.9,29.9 -123,452.9 -41.2,151.5 -151,562.9 z"/><path d="m 1232.6,984 c 29.4,7.9 59.7,-9.6 67.6,-39 6,-22.2 28.7,-35.3 50.9,-29.4 22.2,5.9 35.4,28.7 29.4,50.9 l -0,0.1 c -7.9,29.4 9.6,59.7 39.1,67.6 29.4,7.9 59.7,-9.6 67.6,-39.1 19.6,-79.3 -26.9,-160 -105.4,-182.6 -80.7,-23.3 -164.9,23.2 -188.2,103.9 h 0.1 c -7.9,29.5 9.6,59.7 39,67.6 z"/><path d="M 1696.9,1258.7 1202.1,1126.1 c -29.5,-7.9 -59.8,9.6 -67.7,39.1 v 0 c -23.9,89.5 91.3,198 257.4,242.5 166.1,44.5 320.3,8.1 344.2,-81.3 v 0 c 7.9,-29.5 -9.6,-59.8 -39.1,-67.7 z"/></svg>';
        const icon = (body) =>
            `<svg class="icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${body}</svg>`;
        const ICONS = {
            close: icon('<path d="M4 4l8 8M12 4l-8 8"/>'),
            minimize: icon('<path d="M3.5 8h9"/>'),
            expand: icon('<path d="M3.5 8h9M8 3.5v9"/>'),
            record: icon('<circle cx="8" cy="8" r="4.5" fill="currentColor" stroke="none"/>'),
            pause: icon('<path d="M5.5 3.5v9M10.5 3.5v9"/>'),
            resume: icon('<path d="M5 3.2l7.5 4.8L5 12.8z" fill="currentColor"/>'),
            bin: icon('<path d="M2.5 4.5h11M6.5 4.5V3h3v1.5M4 4.5l.7 9h6.6l.7-9M6.8 7v4.5M9.2 7v4.5"/>'),
            undo: icon('<path d="M5.5 3.5L2.5 6.5l3 3"/><path d="M2.5 6.5h7a3.5 3.5 0 010 7H7"/>'),
            save: icon('<path d="M3 8.5l3.2 3.2L13 4.8"/>'),
            highlight: icon('<rect x="2.5" y="2.5" width="11" height="11" rx="1.5" stroke-dasharray="2.2 1.8"/>'),
            target: icon('<circle cx="8" cy="8" r="5"/><path d="M8 1.5v3M8 11.5v3M1.5 8h3M11.5 8h3"/>'),
        };
        // Inline and important, so no page style hides them - such as the common
        // `:not(:defined) { visibility: hidden }`, which matches both elements.
        const glass = document.createElement('x-pw-glass');
        glass.style.setProperty('display', 'contents', 'important');
        const host = document.createElement(TAG);
        // `right`, `bottom` and the rest undo the user agent's popover styles (below).
        host.style.cssText =
            'position:fixed;z-index:2147483647;top:0;left:0;right:auto;bottom:auto;margin:0;padding:0;' +
            'border:0;background:transparent;overflow:visible;width:auto;height:auto;max-width:none;max-height:none';
        host.style.setProperty('display', 'block', 'important');
        host.style.setProperty('visibility', 'visible', 'important');
        // A modal of the page (Radix and others) sets `pointer-events: none` on body.
        host.style.setProperty('pointer-events', 'auto', 'important');
        glass.appendChild(host);
        const root = host.attachShadow({ mode: 'closed' });
        root.innerHTML = `
    <style>
      /* The dark palette of robotframework-browser.org (app/assets/css/tokens.css). */
      :host { --paper: #1c2227; --chrome: #232a30; --plate: #12171a; --line: #38424a;
              --line-strong: #4e5a63; --ink: #e2e1d7; --dim: #a3afb5; --faint: #8b979d;
              --red: #ff6b5e; --red-soft: #2e1b19; --teal: #00c0b5; --amber: #ffb86b;
              /* Robot Framework syntax colours, as in the site's code blocks. */
              --tok-keyword: var(--teal); --tok-argument: #e6d7ad; --tok-variable: var(--amber); }
      * { box-sizing: border-box; font: 12px/1.4 'IBM Plex Sans', system-ui, sans-serif; }
      /* Content-driven width: the panel grows to the widest recorded Keyword Call line
         (the .calls list below is white-space: pre, so its max-content width is
         exactly that), clamped so it neither goes back to cramped nor swallows
         the page. resize: horizontal lets the user override that within the
         same clamps; overflow: hidden is required for resize to take effect and
         also keeps the rounded corners clean. Extra bottom padding keeps the
         native resize grip clear of the button rows below. */
      .panel { width: max-content; min-width: 320px; max-width: min(80vw, 900px);
               resize: horizontal; overflow: hidden; padding-bottom: 8px;
               background: var(--paper); color: var(--ink); border: 1px solid var(--line);
               border-radius: 7px; color-scheme: dark;
               box-shadow: 0 1px 2px rgb(0 0 0 / 45%), 0 10px 28px -18px rgb(0 0 0 / 85%); }
      .head { display: flex; align-items: center; gap: 6px; padding: 6px 8px;
              background: var(--chrome); border-bottom: 1px solid var(--line);
              cursor: move; user-select: none; }
      .logo { width: 27px; height: 20px; flex: none; }
      /* Stop lives in the header so it is reachable in both states and both
         modes - it ends the whole session, unlike the body's state-specific rows. */
      .head button { flex: none; width: 24px; height: 22px; padding: 0; }
      /* Shown only while minimized, so the main action stays one click away. */
      .head button.quick { width: auto; padding: 0 8px; font-weight: 600; }
      .head button.quick.rec { animation: glow 1.4s ease-in-out infinite; }
      @keyframes glow { 50% { box-shadow: 0 0 0 4px rgb(255 107 94 / 55%); } }
      /* Minimized: only the header, without the resize grip's spare room. */
      .panel.collapsed { padding-bottom: 0; resize: none; }
      .panel.collapsed .head { border-bottom: 0; }
      @media (prefers-reduced-motion: reduce) { .head button.quick.rec { animation: none; } }
      .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--faint); flex: none; }
      .dot.rec { background: var(--red); animation: pulse 1.4s ease-in-out infinite; }
      .dot.paused { background: var(--amber); }
      @keyframes pulse { 50% { opacity: .25; } }
      @media (prefers-reduced-motion: reduce) { .dot.rec { animation: none; } }
      .title { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .title.rec, .title.rec * { font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas,
                                 'DejaVu Sans Mono', monospace; }
      .count { color: var(--dim); }
      button { background: transparent; color: var(--ink); border: 1px solid var(--line-strong);
               border-radius: 4px; padding: 4px 8px; cursor: pointer;
               display: inline-flex; align-items: center; justify-content: center; gap: 6px; }
      button:disabled { opacity: .5; cursor: default; }
      .icon { width: 14px; height: 14px; flex: none; }
      button:hover { background: var(--ink); border-color: var(--ink); color: var(--paper); }
      button.primary { background: var(--red); border-color: var(--red); color: var(--paper); }
      button.primary:hover { filter: brightness(1.1); }
      button.danger { color: var(--red); border-color: var(--red); }
      button.danger:hover { background: var(--red-soft); color: var(--red); }
      @supports (corner-shape: bevel) { button { corner-shape: bevel; } }
      :focus-visible { outline: 2px solid var(--red); outline-offset: 2px; }
      ::selection { background: var(--red); color: var(--paper); }
      .body { padding: 8px; display: flex; flex-direction: column; gap: 8px; }
      .calls { max-height: 220px; overflow: auto; background: var(--plate); border: 1px solid var(--line);
               border-radius: 4px; margin: 0; padding: 6px 6px 6px 28px;
               font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace;
               font-size: 11px; }
      .calls * { font-family: inherit; font-size: inherit; }
      .args { font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace;
              font-size: 11px; }
      .calls li::marker { color: var(--faint); }
      .calls:empty::after { content: 'no keyword calls yet'; color: var(--faint); }
      .calls li, .call-line { white-space: pre; }
      .call-line { font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace;
                   font-size: 11px; }
      .call-line * { font-family: inherit; font-size: inherit; }
      .cell { margin-left: 3ch; }
      .assign { margin-right: 3ch; color: var(--tok-variable); }
      .tok-keyword { color: var(--tok-keyword); }
      .tok-argument { color: var(--tok-argument); }
      .tok-variable { color: var(--tok-variable); }
      /* A picked selector is a comment row of the keyword. */
      .tok-comment, .tok-comment .tok-argument, .tok-comment .tok-variable { color: var(--faint); font-style: italic; }
      .cell.pick { cursor: pointer; text-decoration: underline dotted var(--teal); }
      .cell.pick:hover { background: rgb(0 192 181 / 20%); }
      .notice { color: var(--amber); }
      .picking { background: var(--amber); color: var(--plate); font-weight: bold; border-radius: 4px; padding: 6px; }
      .args div, .offer label, .dialog label { display: block; }
      input[type=checkbox] { accent-color: var(--red); }
      .offer { background: var(--chrome); border: 1px solid var(--line); border-radius: 4px; padding: 6px;
               display: flex; flex-direction: column; gap: 6px; }
      #offerList { overflow-x: auto; }
      .busy button { opacity: .5; pointer-events: none; }
      .row { display: flex; gap: 6px; }
      .row > button { flex: 1; }
      /* Pause is a quiet, icon-only button; Resume, its replacement, asks to be pressed. */
      .row > button.icon-only { flex: none; width: 34px; padding: 4px 0; }
      .row > button.resume { color: var(--amber); border-color: var(--amber); }
      .hint { color: var(--dim); }
      .err { color: var(--red); }
      [hidden] { display: none !important; }
      /* The host is moved with a transform, which makes it the containing block
         of fixed descendants; --x/--y undo that offset so the glass pane covers
         the whole viewport. */
      .modal { position: fixed; left: calc(-1 * var(--x, 0px)); top: calc(-1 * var(--y, 0px));
               width: 100vw; height: 100vh; background: rgb(0 0 0 / 35%);
               display: flex; align-items: center; justify-content: center; }
      .dialog.starting > :not(.status) { opacity: .5; pointer-events: none; }
      .status { display: flex; align-items: center; gap: 8px; color: var(--dim); }
      .spinner { width: 12px; height: 12px; border: 2px solid var(--line-strong); border-top-color: var(--red);
                 border-radius: 50%; animation: spin .8s linear infinite; }
      @keyframes spin { to { transform: rotate(360deg); } }
      .dialog { background: var(--paper); color: var(--ink); padding: 16px; border-radius: 7px;
                border: 1px solid var(--line); color-scheme: dark;
                width: 320px; display: flex; flex-direction: column; gap: 10px; }
      input, textarea { padding: 6px 8px; border-radius: 4px; border: 1px solid var(--line-strong);
              background: var(--plate); color: var(--ink); font: inherit; }
      textarea { resize: vertical; white-space: pre; }
      /* The marked part stays visible when the focus moves on, which the native
         selection of a textarea does not: a layer behind the transparent
         textarea repeats its text, with the marked part highlighted. */
      .marked { display: grid; }
      .marked > * { grid-area: 1 / 1; margin: 0; }
      .marks { padding: 6px 8px; border: 1px solid transparent; border-radius: 4px; background: var(--plate);
               white-space: pre; overflow: hidden; color: transparent; }
      .marks mark { background: rgb(255 107 94 / 45%); color: transparent; border-radius: 2px; }
      /* The same mark on the part an offer would replace. */
      .call-line mark { background: rgb(255 107 94 / 45%); color: inherit; border-radius: 2px; }
      .marked textarea { background: transparent; }
      /* Record Selector: the selector, coloured like the site's code, under a
         transparent textarea that takes the typing. */
      #selectorBox { display: flex; flex-direction: column; gap: 8px; }
      .gens { gap: 0; }
      .gens > button { border-radius: 0; }
      .gens > button:first-child { border-radius: 4px 0 0 4px; }
      .gens > button:last-child { border-radius: 0 4px 4px 0; }
      #selHighlight[aria-pressed=true], .gens > button[aria-pressed=true] { background: var(--chrome); border-color: var(--teal); color: var(--teal); }
      .sel > *, .sel textarea { font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas,
                                'DejaVu Sans Mono', monospace; font-size: 11px; white-space: pre-wrap;
                                word-break: break-all; }
      .sel .marks { color: var(--tok-argument); }
      /* The coloured tokens must set the text exactly as the textarea does, or the
         caret drifts away from it: the universal font rule above applies to them too. */
      .sel .marks * { font: inherit; letter-spacing: inherit; }
      .sel textarea { color: transparent; caret-color: var(--ink); resize: none; min-height: 3.4em; }
      /* Focus shows on the field's own border, not as an outline over its neighbours. */
      .sel textarea:focus-visible { outline: none; border-color: var(--red); box-shadow: inset 0 0 0 1px var(--red); }
      .tok-sep { color: var(--faint); }
      .match-one { color: var(--teal); }
      .match-many { color: var(--amber); }
    </style>
    <div class="panel" id="panel">
      <div class="head" id="head">
        ${LOGO}
        <span class="dot" id="dot"></span>
        <span class="title" id="title">Idle</span>
        <span class="count" id="count"></span>
        <button class="primary quick" id="headNew" title="Name a new keyword and start recording it" hidden>${ICONS.record}Start</button>
        <button class="primary quick rec" id="headSave" title="Save this keyword and stop recording it. The session stays open for the next one." hidden>${ICONS.save}Save</button>
        <button id="headReselect" title="Pick another element" aria-label="Pick another element" hidden>${ICONS.target}</button>
        <button class="primary quick" id="headUse" title="Use this selector" hidden>${ICONS.save}Use</button>
        <button class="quick" id="headCancel" title="Back to recording, without a selector" hidden>Cancel</button>
        <button class="quick" id="headPick" title="Pick an element on the page and add its selector to the keyword as a comment" hidden>${ICONS.target}Pick</button>
        <button id="collapse" title="Minimize the toolbar">${ICONS.minimize}</button>
        <button id="stop" title="End the recording session. The keyword being recorded is saved; the test continues.">${ICONS.close}</button>
      </div>
      <div class="body" id="body">
        <div class="picking" id="picking" hidden></div>
        <ol class="calls" id="calls"></ol>
        <div class="hint" id="hint"></div>
        <div class="notice" id="notice" hidden></div>
        <div class="offer" id="offer" hidden>
          <div id="offerText"></div>
          <div id="offerList"></div>
          <div class="row"><button id="offerSkip" title="Keep the other occurrences as they are">Skip</button><button class="primary" id="offerApply" title="Use the argument for the checked occurrences too">Replace</button></div>
        </div>
        <div class="args" id="args"></div>
        <div class="err" id="err" hidden></div>
        <div class="notice" id="argHint" hidden></div>
        <div id="selectorBox" hidden>
          <div class="hint" id="selHint"></div>
          <div class="row gens" id="selGens"></div>
          <div class="marked sel" id="selEditor"><div class="marks" id="selMarks" aria-hidden="true"></div><textarea id="selInput" rows="2" spellcheck="false" autocomplete="off" aria-label="Selector"></textarea></div>
          <div id="selCount"></div>
          <div class="row" id="selRow">
            <button id="selCancel" title="Back to recording, without a selector" hidden>Cancel</button>
            <button class="icon-only" id="selHighlight" aria-pressed="true" title="Highlight the elements the selector finds" aria-label="Highlight the matches">${ICONS.highlight}</button>
            <button id="selReselect" title="Pick another element">${ICONS.target}Reselect</button>
            <button class="primary" id="selUse" title="Return this selector">${ICONS.save}Use</button>
          </div>
        </div>
        <div class="row" id="idleRow">
          <button class="primary" id="new" title="Name a new keyword and start recording it">${ICONS.record}Record keyword</button>
        </div>
        <div class="row" id="recRow" hidden>
          <button class="danger" id="discard" title="Drop this keyword - nothing of it is saved">${ICONS.bin}Discard</button>
          <button id="undo" title="Remove the Keyword Calls of the last recorded action">${ICONS.undo}Undo</button>
          <button class="icon-only" id="pause" title="Pause recording - actions are not recorded until you resume" aria-label="Pause recording">${ICONS.pause}</button>
          <button class="resume" id="resume" title="Resume recording - actions are recorded again" hidden>${ICONS.resume}Resume</button>
          <button class="primary" id="finish" title="Save this keyword and stop recording it. The session stays open for the next one.">${ICONS.save}Save</button>
        </div>
      </div>
    </div>
    <div class="modal" id="modal" hidden>
      <div class="dialog" id="nameDialog">
        <div>Name of the keyword to record</div>
        <input id="nameInput" placeholder="e.g. Login As Admin" autocomplete="off" maxlength="${NAME_LIMIT}">
        <div class="err" id="modalErr" hidden></div>
        <div class="status" id="starting" hidden><span class="spinner"></span>Starting recording…</div>
        <div class="row">
          <button id="cancel" title="Close without recording">Cancel</button>
          <button class="primary" id="ok" title="Start recording this keyword">${ICONS.record}Start recording</button>
        </div>
      </div>
    </div>
    <div class="modal" id="argModal" hidden>
      <div class="dialog">
        <div>Mark the part that becomes an argument (or leave it unmarked for the whole value)</div>
        <div class="marked"><div class="marks" id="argMarks" aria-hidden="true"></div><textarea id="argValue" rows="3" readonly></textarea></div>
        <input id="argName" placeholder="argument name, e.g. email or \${email}" autocomplete="off" maxlength="${NAME_LIMIT + 3}">
        <label title="Without a default, every caller must pass a value"><input type="checkbox" id="argDefault" checked> Use the marked value as default</label>
        <div class="err" id="argErr" hidden></div>
        <div class="row"><button id="argCancel" title="Close without making an argument">Cancel</button><button class="primary" id="argOk" title="Make the marked part an argument of the keyword">Make argument</button></div>
      </div>
    </div>`;

        const $ = (id) => root.getElementById(id);
        const panel = $('panel');

        // -- page quiet time --------------------------------------------------- //
        // Playwright holds a click and a navigation back for 500 ms. Each command
        // says how long the page has had neither, so Python waits only as long
        // as such an Action can still arrive.
        const navigation = performance.getEntriesByType('navigation')[0];
        let lastPageActivity = (navigation && navigation.domInteractive) || performance.now();
        const notePageClick = (event) => {
            if (event.isTrusted && !event.composedPath().includes(glass)) lastPageActivity = performance.now();
        };
        const PAGE_CLICK_EVENTS = ['click', 'dblclick', 'auxclick'];
        PAGE_CLICK_EVENTS.forEach((type) => window.addEventListener(type, notePageClick, true));

        // Every command carries an id; the state names the last one Python
        // answered (`answered`), with `error` saying whether it was refused.
        const instance = Math.random().toString(36).slice(2, 10);
        let sentCount = 0;
        const send = (command) => {
            if (!window.__rfbCommand) return null;
            const id = `${instance}-${++sentCount}`;
            window.__rfbCommand({ ...command, id, quietMs: Math.round(performance.now() - lastPageActivity) });
            return id;
        };
        const answered = (id) => !!id && (window.__rfbToolbarState || {}).answered === id;

        // -- size -------------------------------------------------------------- //
        // A manually-chosen *width* is restored as an explicit inline style, which
        // wins over the CSS `width: max-content` rule (inline beats stylesheet),
        // so it also wins over future auto-growth from longer Keyword Calls - matching
        // what a user who has already resized the panel expects. Only width is
        // persisted: `resize: horizontal`, not `both`, is used deliberately -
        // a manually-chosen *height* would leave dead space below the header
        // once the panel collapses, since the body (and with it the panel's
        // content-driven height) simply disappears; width has no such
        // collapse-time surprise.
        const size = read(SIZE_KEY, null);
        if (size && typeof size.width === 'number') {
            panel.style.width = `${size.width}px`;
        }
        // The width before a press near the native resize grip (the bottom-right
        // corner), or null. A button reaching into that corner is clicked, not
        // resized, so only a changed width is kept.
        let widthBeforeResize = null;
        panel.addEventListener('pointerdown', (event) => {
            const rect = panel.getBoundingClientRect();
            const nearGrip = rect.right - event.clientX <= 16 && rect.bottom - event.clientY <= 16;
            widthBeforeResize = nearGrip ? rect.width : null;
        });
        const endResize = () => {
            if (widthBeforeResize === null) return;
            const width = panel.getBoundingClientRect().width;
            if (width !== widthBeforeResize) write(SIZE_KEY, { width: Math.round(width) });
            widthBeforeResize = null;
        };
        window.addEventListener('pointerup', endResize);
        window.addEventListener('pointercancel', endResize);
        // A release over the toolbar does not reach window (see the host's listeners).
        root.addEventListener('pointerup', endResize);

        // -- placement ------------------------------------------------------- //
        // Top left: the top right is where Playwright's overlay grows and
        // Chromium shows its translate prompt.
        const position = read(POSITION_KEY, { x: 12, y: 12 });
        // `position` may lie past an edge (the toolbar then sits at that edge,
        // and stays there when it grows or shrinks); `shown` is where it is drawn.
        const shown = { x: 0, y: 0 };
        const place = () => {
            // Flush with every edge of the viewport, scrollbars excluded.
            const viewWidth = document.documentElement.clientWidth || window.innerWidth;
            const viewHeight = document.documentElement.clientHeight || window.innerHeight;
            const x = Math.min(Math.max(position.x, 0), Math.max(viewWidth - panel.offsetWidth, 0));
            const y = Math.min(Math.max(position.y, 0), Math.max(viewHeight - panel.offsetHeight, 0));
            shown.x = x;
            shown.y = y;
            host.style.transform = `translate(${x}px, ${y}px)`;
            host.style.setProperty('--x', `${x}px`);
            host.style.setProperty('--y', `${y}px`);
        };
        place();

        let drag = null;
        $('head').addEventListener('pointerdown', (event) => {
            // The header doubles as the drag handle; its buttons must still click.
            if (event.button !== 0 || event.target.closest('button')) return;
            // Start from where the toolbar is drawn, so a drop past an edge
            // does not make the next drag wait until the pointer is back.
            position.x = shown.x;
            position.y = shown.y;
            drag = { x: event.clientX - position.x, y: event.clientY - position.y };
            $('head').setPointerCapture(event.pointerId);
        });
        $('head').addEventListener('pointermove', (event) => {
            if (!drag) return;
            position.x = event.clientX - drag.x;
            position.y = event.clientY - drag.y;
            place();
        });
        $('head').addEventListener('pointerup', () => {
            if (drag) write(POSITION_KEY, position);
            drag = null;
        });
        // A pointer the browser took away (touch gesture, pen) must end the drag
        // too, or the next hover over the header would move the toolbar.
        $('head').addEventListener('lostpointercapture', () => {
            drag = null;
        });

        // -- collapse -------------------------------------------------------- //
        let collapsed = read(COLLAPSED_KEY, false);
        // The quick buttons in the header: Start while idle, Save while recording,
        // only when minimized and only when the body would offer the same.
        const updateQuickButtons = () => {
            const state = window.__rfbToolbarState || {};
            // A minimized selector panel offers its two decisions in the header.
            const selector = state.mode === 'selector' ? state : state.picker || null;
            const decide = collapsed && !!selector && selector.phase === 'picked';
            $('headReselect').hidden = !decide;
            $('headUse').hidden = !decide;
            // While a recording picks, only the pick can be ended from the header (and ✕).
            $('headCancel').hidden = !(collapsed && !!state.picker && state.mode !== 'selector');
            const offered = collapsed && !state.fixedName && state.mode !== 'selector' && !state.picker;
            $('headNew').hidden = !offered || state.state === 'recording';
            $('headSave').hidden = !offered || state.state !== 'recording';
            $('headNew').disabled = !!state.pending;
            $('headSave').disabled = !!state.pending;
        };
        const applyCollapsed = () => {
            $('body').hidden = collapsed;
            panel.classList.toggle('collapsed', collapsed);
            $('collapse').innerHTML = collapsed ? ICONS.expand : ICONS.minimize;
            $('collapse').title = collapsed ? 'Expand the toolbar' : 'Minimize the toolbar';
        };
        applyCollapsed();
        $('collapse').addEventListener('click', () => {
            collapsed = !collapsed;
            write(COLLAPSED_KEY, collapsed);
            applyCollapsed();
            updateQuickButtons();
            place();
        });

        // -- commands -------------------------------------------------------- //
        // A `new` command is only answered by a later poll, so the modal stays
        // open until then: a rejected name (duplicate, unusable) comes back
        // *inside* it, with what was typed still there to correct.
        let nameSent = null;
        const setStarting = (id) => {
            nameSent = id;
            const starting = id !== null;
            $('ok').disabled = starting;
            $('nameInput').disabled = starting;
            $('nameDialog').classList.toggle('starting', starting);
            $('starting').hidden = !starting;
        };
        const openModal = () => {
            setStarting(null);
            $('nameInput').value = '';
            $('modalErr').hidden = true;
            $('modal').hidden = false;
            $('nameInput').focus();
        };
        const closeModal = () => {
            setStarting(null);
            $('modal').hidden = true;
        };
        $('new').addEventListener('click', openModal);
        $('headNew').addEventListener('click', openModal);
        $('cancel').addEventListener('click', closeModal);
        $('ok').addEventListener('click', () => {
            if (nameSent !== null) return;
            const name = $('nameInput').value.trim();
            if (!name) {
                $('modalErr').textContent = 'Keyword name must not be empty.';
                $('modalErr').hidden = false;
                return;
            }
            const id = send({ cmd: 'new', name });
            if (id === null) return;
            $('modalErr').hidden = true;
            setStarting(id);
        });
        $('stop').addEventListener('click', () => send({ cmd: 'stop' }));
        $('undo').addEventListener('click', () => send({ cmd: 'undo' }));
        $('discard').addEventListener('click', () => send({ cmd: 'discard' }));
        $('finish').addEventListener('click', () => send({ cmd: 'finish' }));
        $('pause').addEventListener('click', () => send({ cmd: 'pause' }));
        $('resume').addEventListener('click', () => send({ cmd: 'resume' }));
        $('headSave').addEventListener('click', () => send({ cmd: 'finish' }));

        // -- keyword arguments -------------------------------------------------- //
        // `raw` is the literal cell text the offsets refer to (the rendered text
        // differs for escapes); Python rejects the command if it changed meanwhile.
        let argTarget = null;
        // Like the name modal, the dialog stays open until Python answered, so
        // a rejected name is shown here and can be corrected.
        let argSent = null;
        // While Python is finishing a keyword nothing may be sent.
        const isPending = () => !!(window.__rfbToolbarState && window.__rfbToolbarState.pending);
        // The hint is owned by the toolbar itself (render never touches it except
        // to clear it on a real state change), unlike #err which mirrors the state.
        const setHint = (text) => {
            $('argHint').textContent = text;
            $('argHint').hidden = !text;
        };
        // The selection of a textarea outlives its focus, so the marks can always
        // follow it. Text nodes only: the value comes from the page under test.
        const showMarks = () => {
            const input = $('argValue');
            const marks = $('argMarks');
            const { value, selectionStart: from, selectionEnd: to } = input;
            marks.textContent = '';
            const marked = document.createElement('mark');
            marked.textContent = value.slice(from, to);
            // The final newline keeps a trailing empty line as tall as in the textarea.
            marks.append(value.slice(0, from), marked, `${value.slice(to)}\n`);
            marks.scrollTop = input.scrollTop;
            marks.scrollLeft = input.scrollLeft;
        };
        ['select', 'selectionchange', 'keyup', 'mouseup', 'scroll'].forEach((type) =>
            $('argValue').addEventListener(type, showMarks),
        );
        // A selection dragged past the textarea ends outside it.
        root.addEventListener('pointerup', () => {
            if (!$('argModal').hidden) showMarks();
        });

        const openArgModal = (call, value, raw) => {
            if (isPending()) return;
            if (raw === null || raw === undefined) {
                setHint('This value already contains an argument.');
                return;
            }
            setHint('');
            argTarget = { call, value, raw };
            argSent = null;
            $('argOk').disabled = false;
            $('argValue').value = raw;
            $('argValue').setSelectionRange(0, 0);
            showMarks();
            $('argName').value = '';
            $('argDefault').checked = true;
            showArgError('');
            $('argModal').hidden = false;
            $('argValue').focus();
        };
        const closeArgModal = () => {
            $('argModal').hidden = true;
            argTarget = null;
            argSent = null;
        };
        const showArgError = (text) => {
            $('argErr').textContent = text || '';
            $('argErr').hidden = !text;
        };
        // Mirrors `argument_name_error` in names.py for instant feedback; Python
        // checks again and also rejects built-in and taken names.
        const argumentNameError = (name) => {
            if (!name) return 'Argument name must not be empty.';
            if (name.replace(/^\$\{(.*)\}$/, '$1').length > NAME_LIMIT)
                return `Argument name must not be longer than ${NAME_LIMIT} characters.`;
            const plain = /^[A-Za-z_][A-Za-z0-9_]*$/;
            if (name.startsWith('${')) {
                const inner = /^\$\{(.*)\}$/.exec(name);
                return inner && plain.test(inner[1])
                    ? null
                    : 'Write the argument as a variable like ${email}, or just email.';
            }
            return plain.test(name)
                ? null
                : "Argument name must start with a letter or '_' and contain only letters, digits and '_'.";
        };
        $('argCancel').addEventListener('click', closeArgModal);
        $('argOk').addEventListener('click', () => {
            if (!argTarget || argSent || isPending()) return;
            const name = $('argName').value.trim();
            const error = argumentNameError(name);
            showArgError(error);
            if (error) return;
            const input = $('argValue');
            // Selection offsets are UTF-16 code units; Python indexes by code point.
            const points = (text) => Array.from(text).length;
            // A textarea reads "\r\n" and a lone "\r" as "\n"; map its offsets back to the raw value.
            const rawOffset = (offset) => {
                const raw = argTarget.raw;
                let index = 0;
                for (let unit = 0; unit < offset && index < raw.length; unit++) {
                    index += raw[index] === '\r' && raw[index + 1] === '\n' ? 2 : 1;
                }
                return index;
            };
            const from = rawOffset(input.selectionStart ?? 0);
            const to = rawOffset(input.selectionEnd ?? 0);
            let start = points(argTarget.raw.slice(0, from));
            let end = points(argTarget.raw.slice(0, to));
            if (from === to) {
                start = 0;
                end = points(argTarget.raw);
            }
            argSent = send({
                cmd: 'argument',
                call: argTarget.call,
                value: argTarget.value,
                start,
                end,
                name,
                useDefault: $('argDefault').checked,
                raw: argTarget.raw,
            });
            $('argOk').disabled = argSent !== null;
        });
        // -- event isolation ------------------------------------------------- //
        // Keyboard events are composed, so typing in the toolbar would reach the
        // page's key handlers (shortcuts, typeahead) retargeted to the host. A
        // capture listener on window runs before any listener of the document
        // and stops them there; the text still gets typed (default action), and
        // the toolbar's own keys are handled here, as its inputs no longer see them.
        // `contextmenu` is stopped the same way: Playwright's recorder would
        // record a right click on the toolbar, as it skips `x-pw-glass` for every
        // other event but not for this one.
        const toolbarKeys = {
            nameInput: (event) => {
                if (event.key === 'Enter') $('ok').click();
            },
            argName: (event) => {
                if (event.key === 'Enter') $('argOk').click();
            },
            selInput: (event) => {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    $('selUse').click();
                }
            },
        };
        // A click on a glass pane closes its dialog, as in any modal - but only if
        // the press started there too: a text selection or a textarea resize
        // that ends outside the dialog is not a click on the pane.
        const closeOnPaneClick = (pane, close) => {
            let pressedOnPane = false;
            pane.addEventListener('pointerdown', (event) => {
                pressedOnPane = event.target === pane;
            });
            pane.addEventListener('click', (event) => {
                if (event.target === pane && pressedOnPane) close();
            });
        };
        closeOnPaneClick($('modal'), () => {
            if (nameSent === null) closeModal();
        });
        closeOnPaneClick($('argModal'), closeArgModal);
        // Escape closes the open dialog wherever the focus is inside the toolbar.
        const escapeDialog = () => {
            if (!$('argModal').hidden) closeArgModal();
            else if (!$('modal').hidden && nameSent === null) closeModal();
            else if (selectorState()) {
                dropEdit();
                sendSelector({ cmd: 'cancel' });
            }
        };
        const toolbarInput = {
            argName: () => {
                const name = $('argName').value.trim();
                showArgError(name ? argumentNameError(name) : '');
            },
            selInput: () => editSelector(),
        };
        const ISOLATED_EVENTS = [
            'contextmenu',
            'focusin',
            'focusout',
            'keydown',
            'keyup',
            'keypress',
            'beforeinput',
            'input',
            'compositionstart',
            'compositionupdate',
            'compositionend',
            'paste',
            'copy',
            'cut',
        ];
        // A focus event of the page whose other side is the toolbar counts too: a
        // page modal's focus trap would otherwise pull the focus back from it.
        const fromToolbar = (event) =>
            event.composedPath().includes(glass) || (!!event.relatedTarget && glass.contains(event.relatedTarget));
        const isolate = (event) => {
            if (!fromToolbar(event)) return;
            event.stopImmediatePropagation();
            if (event.type === 'keydown' && event.key === 'Escape') {
                escapeDialog();
                return;
            }
            const focused = root.activeElement;
            const handlers = { keydown: toolbarKeys, input: toolbarInput }[event.type];
            const handler = handlers && focused ? handlers[focused.id] : undefined;
            if (handler) handler(event);
        };
        ISOLATED_EVENTS.forEach((type) => window.addEventListener(type, isolate, true));
        // Pointer, mouse and wheel events must reach the toolbar's own listeners
        // first, so they are stopped on the way back up, at the host: the page's
        // document and window listeners never see them. A page modal would
        // otherwise close on a toolbar click ("click outside") or block its
        // scrolling. Playwright's recorder listens in the capture phase and
        // skips them through `x-pw-glass`.
        const BUBBLING_EVENTS = [
            'pointerdown',
            'pointerup',
            'pointermove',
            'mousedown',
            'mouseup',
            'click',
            'dblclick',
            'auxclick',
            'touchstart',
            'touchend',
            'touchmove',
            'wheel',
        ];
        BUBBLING_EVENTS.forEach((type) => host.addEventListener(type, (event) => event.stopPropagation()));
        const currentOffer = () => (window.__rfbToolbarState && window.__rfbToolbarState.offer) || null;
        $('offerApply').addEventListener('click', () => {
            const offer = currentOffer();
            if (!offer || isPending()) return;
            const chosen = [...$('offerList').querySelectorAll('input:checked')].map((i) => [
                Number(i.dataset.c),
                Number(i.dataset.v),
            ]);
            send({ cmd: 'replace', argument: offer.argument, occurrences: chosen });
        });
        $('offerSkip').addEventListener('click', () => {
            const offer = currentOffer();
            if (offer && !isPending()) send({ cmd: 'replace', argument: offer.argument, occurrences: [] });
        });

        // -- Record Selector ------------------------------------------------- //
        // The selector in colour: engines teal, frame and chain separators faint,
        // the rest like a value. Text nodes only: selectors come from the page.
        const selectorTokens = (selector) =>
            selector.split(/( >>> | >> )/).map((part) => {
                if (part === ' >>> ' || part === ' >> ') return [['tok-sep', part]];
                const engine = /^(internal:[a-z-]+=|[a-z-]+=)/.exec(part);
                return engine
                    ? [
                          ['tok-keyword', engine[0]],
                          ['tok-argument', part.slice(engine[0].length)],
                      ]
                    : [['tok-argument', part]];
            });
        const showSelectorMarks = () => {
            const marks = $('selMarks');
            marks.textContent = '';
            selectorTokens($('selInput').value).forEach((tokens) =>
                tokens.forEach(([kind, text]) => {
                    const span = document.createElement('span');
                    span.className = kind;
                    span.textContent = text;
                    marks.appendChild(span);
                }),
            );
            // A trailing newline keeps the layer as tall as the textarea.
            marks.append('\n');
            marks.scrollTop = $('selInput').scrollTop;
        };
        $('selInput').addEventListener('scroll', showSelectorMarks);
        // The selector panel serves Record Selector (`mode: selector`) and the Pick
        // button of a recording (`picker`), whose commands are prefixed `pick-`.
        // Cancel ends Record Selector, but only the pick of a recording.
        const selectorState = () => {
            const state = window.__rfbToolbarState || {};
            return state.mode === 'selector' ? state : state.picker || null;
        };
        const sendSelector = (command) => {
            const standalone = (window.__rfbToolbarState || {}).mode === 'selector';
            if (standalone) return send(command.cmd === 'cancel' ? { cmd: 'stop' } : command);
            return send({ ...command, cmd: `pick-${command.cmd}` });
        };
        // Each change is counted and highlighted on the page once typing pauses.
        let editTimer = null;
        const sendEdit = () => {
            if (editTimer === null) return;
            clearTimeout(editTimer);
            editTimer = null;
            sendSelector({ cmd: 'edit', selector: $('selInput').value });
        };
        // A pending edit belongs to the selector shown when it was typed.
        const dropEdit = () => {
            if (editTimer !== null) clearTimeout(editTimer);
            editTimer = null;
        };
        const editSelector = () => {
            showSelectorMarks();
            $('selCount').textContent = '';
            $('selCount').hidden = true;
            if (editTimer !== null) clearTimeout(editTimer);
            editTimer = setTimeout(sendEdit, 1000);
        };
        $('selReselect').addEventListener('click', () => {
            dropEdit();
            sendSelector({ cmd: 'reselect' });
        });
        $('selHighlight').addEventListener('click', () => {
            sendEdit();
            sendSelector({ cmd: 'highlight', on: $('selHighlight').getAttribute('aria-pressed') !== 'true' });
        });
        $('selCancel').addEventListener('click', () => {
            dropEdit();
            sendSelector({ cmd: 'cancel' });
        });
        $('selUse').addEventListener('click', () => {
            sendEdit();
            sendSelector({ cmd: 'use' });
        });
        $('headPick').addEventListener('click', () => send({ cmd: 'pick' }));
        $('headReselect').addEventListener('click', () => {
            dropEdit();
            sendSelector({ cmd: 'reselect' });
        });
        $('headCancel').addEventListener('click', () => {
            dropEdit();
            sendSelector({ cmd: 'cancel' });
        });
        $('headUse').addEventListener('click', () => {
            sendEdit();
            sendSelector({ cmd: 'use' });
        });
        const GENERATOR_LABELS = { playwright: 'Playwright', css: 'CSS' };
        let shownVersion = null;
        // `keyword` is the keyword being recorded, or null for Record Selector.
        const renderSelector = (state, keyword) => {
            const picking = state.phase === 'picking';
            $('title').classList.toggle('rec', keyword !== null);
            $('count').textContent = '';
            if (keyword === null) {
                $('dot').className = picking ? 'dot rec' : 'dot';
                $('title').textContent = state.label ? `Record Selector - ${state.label}` : 'Record Selector';
                $('stop').title = 'Cancel - Record Selector fails';
            } else {
                $('dot').className = 'dot rec';
                $('title').textContent = `${keyword} - pick a selector`;
            }
            $('selHint').textContent = picking
                ? 'Click an element in the page to pick it.'
                : 'Edit the selector if needed, then use it.';
            const gens = $('selGens');
            gens.textContent = '';
            const unavailable = state.unavailable || {};
            (Array.isArray(state.generators) ? state.generators : []).forEach((name) => {
                const button = document.createElement('button');
                button.textContent = GENERATOR_LABELS[name] || name;
                button.setAttribute('aria-pressed', String(name === state.generator));
                button.disabled = !picking && name in unavailable;
                button.title = button.disabled ? String(unavailable[name]) : `Use the ${button.textContent} selector`;
                button.addEventListener('click', () => sendSelector({ cmd: 'generator', name }));
                gens.appendChild(button);
            });
            $('selEditor').hidden = picking;
            $('selRow').hidden = false;
            $('selReselect').hidden = picking;
            $('selHighlight').hidden = picking;
            $('selHighlight').setAttribute('aria-pressed', String(state.highlight !== false));
            $('selHighlight').title =
                state.highlight !== false
                    ? 'Highlighting the matches - click to stop'
                    : 'Not highlighting - click to highlight the matches';
            $('selUse').hidden = picking;
            $('selCancel').hidden = keyword === null;
            if (state.version !== shownVersion) {
                shownVersion = state.version;
                dropEdit();
                $('selInput').value = state.selector || '';
                showSelectorMarks();
            }
            const count = state.count;
            const counter = $('selCount');
            counter.className = '';
            counter.textContent = '';
            if (!picking && count && count.selector === $('selInput').value) {
                if (typeof count.error === 'string') {
                    counter.className = 'err';
                    counter.textContent = count.error;
                } else if (count.count === 1) {
                    counter.className = 'match-one';
                    counter.textContent = '1 match';
                } else if (count.count === 0) {
                    counter.className = 'err';
                    counter.textContent = 'No match';
                } else {
                    counter.className = 'match-many';
                    counter.textContent = `${count.count} matches`;
                }
            }
            counter.hidden = !counter.textContent;
            $('notice').textContent = state.notice || '';
            $('notice').hidden = !state.notice;
            $('err').textContent = state.error || '';
            $('err').hidden = !state.error;
            updateQuickButtons();
        };

        // -- render ---------------------------------------------------------- //
        // Node sends a state only when it changed, so every render rebuilds.
        let offerKey = null;
        let offerChecked = {};
        window.__rfbToolbarRender = (state) => {
            if (!state) return;
            // A page that swaps its body without navigating (Turbo, htmx, a
            // framework re-bootstrap) takes the toolbar with it.
            if (!glass.isConnected) attach();
            window.__rfbToolbarState = state;
            renderBody(state);
            // The panel's content-driven width can change with every render (a
            // longer Keyword Call just got added); re-clamp so growth never pushes it
            // past the right edge of the viewport.
            place();
            answerDialogs(state);
        };
        // A value as Robot reads it: `argument` and `variable` tokens, coloured.
        const appendTokens = (container, tokens) => {
            (Array.isArray(tokens) ? tokens : []).forEach(([kind, text]) => {
                const token = document.createElement('span');
                token.className = kind === 'variable' ? 'tok-variable' : 'tok-argument';
                token.textContent = text ?? '';
                container.appendChild(token);
            });
            return container;
        };
        // Wraps every occurrence of `text` in the tokens of `cell` in a mark, also
        // where an occurrence spans tokens. Text nodes only: values come from the page.
        const markText = (cell, text) => {
            if (!text) return;
            const tokens = [...cell.children];
            const whole = tokens.map((token) => token.textContent).join('');
            const ranges = [];
            for (let at = whole.indexOf(text); at !== -1; at = whole.indexOf(text, at + text.length))
                ranges.push([at, at + text.length]);
            if (!ranges.length) return;
            let offset = 0;
            tokens.forEach((token) => {
                const own = token.textContent;
                const start = offset;
                offset += own.length;
                const cuts = new Set([0, own.length]);
                ranges.forEach(([from, to]) => {
                    if (from > start && from < offset) cuts.add(from - start);
                    if (to > start && to < offset) cuts.add(to - start);
                });
                const points = [...cuts].sort((a, b) => a - b);
                token.textContent = '';
                points.slice(1).forEach((end, i) => {
                    const piece = own.slice(points[i], end);
                    const inside = ranges.some(([from, to]) => start + points[i] >= from && start + end <= to);
                    if (!inside) {
                        token.append(piece);
                        return;
                    }
                    const mark = document.createElement('mark');
                    mark.textContent = piece;
                    token.appendChild(mark);
                });
            });
        };
        // One Keyword Call as the file shows it: cells three character widths apart.
        // `onPick(valueIndex, value)` makes the selectable values clickable;
        // `marked` ({value, text}) highlights `text` in that value.
        const callLine = (container, call, onPick, marked = null) => {
            if (call.assign) {
                const assign = document.createElement('span');
                assign.className = 'assign';
                assign.textContent = call.assign;
                container.appendChild(assign);
            }
            const kw = document.createElement('span');
            kw.className = call.comment ? 'tok-comment' : 'tok-keyword';
            kw.textContent = call.keyword ?? '';
            container.appendChild(kw);
            (call.values || []).forEach((value, valueIndex) => {
                const cell = document.createElement('span');
                const pick = !!onPick && !!value.selectable;
                cell.className = pick ? 'cell pick' : call.comment ? 'cell tok-comment' : 'cell';
                appendTokens(cell, value.tokens);
                if (marked && marked.value === valueIndex) markText(cell, marked.text);
                if (pick) {
                    cell.title = 'Make this value an argument';
                    cell.addEventListener('click', () => onPick(valueIndex, value));
                }
                container.appendChild(cell);
            });
            return container;
        };
        const RECORDER_PARTS = ['picking', 'calls', 'hint', 'offer', 'args', 'argHint', 'idleRow', 'recRow'];
        const renderBody = (state) => {
            const selectorMode = state.mode === 'selector';
            const picker = !selectorMode && state.state === 'recording' ? state.picker : null;
            $('selectorBox').hidden = !selectorMode && !picker;
            $('headPick').hidden = selectorMode || !!picker || state.state !== 'recording' || !!state.pending;
            if (selectorMode || picker) {
                RECORDER_PARTS.forEach((id) => {
                    $(id).hidden = true;
                });
                renderSelector(selectorMode ? state : picker, selectorMode ? null : state.name || 'Keyword');
                return;
            }
            $('stop').title = 'End the recording session. The keyword being recorded is saved; the test continues.';
            $('hint').hidden = false;
            $('args').hidden = false;
            setHint('');
            const recording = state.state === 'recording';
            const calls = Array.isArray(state.calls) ? state.calls : [];
            const keywords = Array.isArray(state.keywords) ? state.keywords : [];
            const argumentList = Array.isArray(state.arguments) ? state.arguments : [];
            const paused = recording && !!state.paused;
            $('dot').className = paused ? 'dot paused' : recording ? 'dot rec' : 'dot';
            $('title').textContent = recording ? state.name || 'Recording' : 'Idle';
            $('title').classList.toggle('rec', recording || state.pending === 'new');
            // Nothing is recorded while idle, so an empty call list would only confuse.
            $('calls').hidden = !recording;
            $('count').textContent = recording ? `(${calls.length})` : '';
            const list = $('calls');
            const oldTop = list.scrollTop;
            const wasAtBottom = list.scrollTop + list.clientHeight >= list.scrollHeight - 4;
            const oldCount = list.children.length;
            list.textContent = '';
            calls.forEach((call, callIndex) => {
                const onPick = recording ? (valueIndex, value) => openArgModal(callIndex, valueIndex, value.raw) : null;
                list.appendChild(callLine(document.createElement('li'), call, onPick));
            });
            // Keep the reader's place; follow new calls only if already at the end.
            list.scrollTop = calls.length > oldCount && wasAtBottom ? list.scrollHeight : oldTop;
            $('picking').textContent = state.picking
                ? 'Pick locator is on - nothing is being recorded. Turn it off in the Playwright toolbar to continue.'
                : '';
            $('picking').hidden = !state.picking;
            $('notice').textContent = state.notice || '';
            $('notice').hidden = !state.notice;
            const offer = recording ? state.offer : null;
            $('offer').hidden = !offer;
            if (offer) {
                $('offerText').textContent = `Also use \${${offer.argument ?? ''}} for "${offer.text ?? ''}" in:`;
                const identity = JSON.stringify([offer.argument, offer.text, offer.occurrences]);
                if (identity !== offerKey) {
                    offerKey = identity;
                    offerChecked = {};
                }
                const box = $('offerList');
                box.textContent = '';
                (offer.occurrences || []).forEach(([c, v]) => {
                    const label = document.createElement('label');
                    const check = document.createElement('input');
                    check.type = 'checkbox';
                    const id = `${c},${v}`;
                    check.checked = offerChecked[id] !== false;
                    check.addEventListener('change', () => {
                        offerChecked[id] = check.checked;
                    });
                    check.dataset.c = String(c);
                    check.dataset.v = String(v);
                    label.appendChild(check);
                    label.append(' ');
                    if (calls[c])
                        label
                            .appendChild(
                                callLine(document.createElement('span'), calls[c], null, {
                                    value: v,
                                    text: offer.text,
                                }),
                            )
                            .classList.add('call-line');
                    box.appendChild(label);
                });
            }
            const args = $('args');
            args.textContent = '';
            if (recording) {
                argumentList.forEach((arg) => {
                    const line = document.createElement('div');
                    const tokens = [['variable', `\${${arg.name}}`]];
                    if (arg.useDefault) tokens.push(['argument', `=${arg.default ?? ''}`]);
                    args.appendChild(appendTokens(line, tokens));
                });
            }
            $('panel').classList.toggle('busy', !!state.pending);
            const pendingLabel =
                { new: 'starting', pause: 'pausing', resume: 'resuming' }[state.pending] || 'finishing';
            if (state.pending) $('title').textContent = `${state.name || 'Keyword'} - ${pendingLabel}…`;
            else if (paused) $('title').textContent = `${state.name || 'Recording'} - paused`;
            $('idleRow').hidden = recording;
            $('recRow').hidden = !recording;
            // A fixed-name recording writes exactly one keyword: no New, no Finish.
            $('new').hidden = !!state.fixedName;
            $('finish').hidden = !!state.fixedName;
            $('pause').hidden = paused;
            $('resume').hidden = !paused;
            updateQuickButtons();
            $('hint').textContent = paused
                ? 'Paused - nothing is recorded until you resume.'
                : recording
                  ? `writing to ${state.target}`
                  : `${keywords.length} keyword(s) recorded into ${state.target}`;
            $('err').textContent = state.error || '';
            $('err').hidden = !state.error;
        };
        const answerDialogs = (state) => {
            if (answered(nameSent)) {
                if (state.error) {
                    // Rejected: keep the dialog and the typed name, let them retry.
                    $('modalErr').textContent = state.error;
                    $('modalErr').hidden = false;
                    setStarting(null);
                    $('nameInput').focus();
                } else if (state.state === 'recording' || !state.pending) {
                    // Accepted: the dialog shows "Starting" until the keyword records.
                    closeModal();
                }
            }
            if (answered(argSent)) {
                if (state.error) {
                    showArgError(state.error);
                    argSent = null;
                    $('argOk').disabled = false;
                    $('argName').focus();
                } else {
                    closeArgModal();
                }
            }
        };

        window.__rfbToolbarRemove = () => {
            // Nothing re-injects the toolbar once polling has stopped, so removing
            // it here is enough - no "stay away" flag is needed.
            window.removeEventListener('pointerup', endResize);
            window.removeEventListener('pointercancel', endResize);
            ISOLATED_EVENTS.forEach((type) => window.removeEventListener(type, isolate, true));
            PAGE_CLICK_EVENTS.forEach((type) => window.removeEventListener(type, notePageClick, true));
            overlayWatch.disconnect();
            window.removeEventListener('pointerup', release);
            window.removeEventListener('pointercancel', release);
            window.removeEventListener('blur', release);
            following.abort();
            glass.remove();
            delete window.__rfbToolbarRender;
            delete window.__rfbToolbarState;
            delete window.__rfbToolbarRemove;
            delete window.__rfbToolbarConnected;
        };

        // Playwright draws its highlight and Pick locator overlay in the top layer
        // (a manual popover), above every z-index, and brings it to the front each
        // time it installs it. The toolbar is a manual popover too and follows it
        // to the front: the top layer paints the popover opened last on top.
        const popover = typeof host.showPopover === 'function';
        if (popover) host.setAttribute('popover', 'manual');
        const toFront = () => {
            if (!popover || !host.isConnected) return;
            const focused = root.activeElement;
            const selection =
                focused && typeof focused.selectionStart === 'number'
                    ? [focused.selectionStart, focused.selectionEnd]
                    : null;
            try {
                if (host.matches(':popover-open')) host.hidePopover();
                host.showPopover();
            } catch {
                /* not in a document that supports it - stays a fixed element */
            }
            if (focused && root.activeElement !== focused) {
                focused.focus({ preventScroll: true });
                if (selection) focused.setSelectionRange(selection[0], selection[1]);
            }
        };
        // Playwright brings its overlay to the front several times a second while
        // it highlights. Re-showing the toolbar in the middle of a press would cut
        // a resize, a drag or a text selection, and typing would lose its
        // composition; so the toolbar follows only once the press or the typing ends.
        let pressed = false;
        let behind = false;
        const interacting = () => pressed || ['INPUT', 'TEXTAREA'].includes(root.activeElement?.tagName ?? '');
        const followToFront = () => {
            if (interacting()) behind = true;
            else toFront();
        };
        const catchUp = () => {
            if (!behind || interacting()) return;
            behind = false;
            toFront();
        };
        const release = () => {
            pressed = false;
            catchUp();
        };
        root.addEventListener('pointerdown', () => {
            pressed = true;
        });
        root.addEventListener('pointerup', release);
        root.addEventListener('lostpointercapture', release);
        window.addEventListener('pointerup', release);
        window.addEventListener('pointercancel', release);
        // A press released outside the window reports no pointerup.
        window.addEventListener('blur', release);
        // Listeners on Playwright's panes, removed with the toolbar.
        const following = new AbortController();
        root.addEventListener('focusout', () => setTimeout(catchUp));
        const followed = new WeakSet();
        const followPlaywright = () => {
            document.querySelectorAll('x-pw-glass').forEach((pane) => {
                if (pane === glass || followed.has(pane)) return;
                followed.add(pane);
                pane.addEventListener(
                    'toggle',
                    (event) => {
                        if (event.newState === 'open') followToFront();
                    },
                    { signal: following.signal },
                );
            });
        };
        const overlayWatch = new MutationObserver(followPlaywright);
        overlayWatch.observe(document.documentElement, { childList: true });
        followPlaywright();
        const attach = () => {
            if (!document.body) return;
            document.body.appendChild(glass);
            toFront();
        };
        window.__rfbToolbarConnected = () => glass.isConnected;
        if (document.body) attach();
        else document.addEventListener('DOMContentLoaded', attach);
    }

    installToolbar('rfb-recorder-toolbar');
})();
