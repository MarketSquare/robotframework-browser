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
// It lives in a *closed* shadow root. That is load-bearing, not cosmetic:
// Playwright's injected recorder resolves an event's target with
// `composedPath()`, which does not cross a closed shadow boundary, so every
// interaction with this toolbar is attributed to the host element and can be
// filtered out of the recording by tag name alone. An open shadow root, or
// plain DOM, would record the user's own toolbar clicks as keyword calls.

(function () {
    function installToolbar(TAG) {
        // Sub-frames must not get their own toolbar.
        if (window.top !== window) return;
        if (window.__rfbToolbarRender) return;

        const POSITION_KEY = 'rfb.toolbar.position';
        const COLLAPSED_KEY = 'rfb.toolbar.collapsed';
        const SIZE_KEY = 'rfb.toolbar.size';

        const read = (key, fallback) => {
            try {
                const raw = window.sessionStorage.getItem(key);
                return raw === null ? fallback : JSON.parse(raw);
            } catch (e) {
                return fallback;
            }
        };
        const write = (key, value) => {
            try {
                window.sessionStorage.setItem(key, JSON.stringify(value));
            } catch (e) {
                /* storage disabled - layout simply does not persist */
            }
        };

        const LOGO =
            '<svg class="logo" role="img" aria-label="Browser library" viewBox="422 465 1664 1219" xmlns="http://www.w3.org/2000/svg"><rect fill="#b82e24" x="562" y="759" width="349.9" height="687.3" transform="rotate(-15,736.9,1102.7)"/><rect fill="#d63a2e" x="900" y="668.4" width="350.6" height="687.3" transform="rotate(-15,1075.3,1012.1)"/><path fill="#fff" d="m 955.4,1004.6 c 11.1,9.5 26.1,12.9 40.2,9.1 8.4,-2.2 15.9,-7 21.6,-13.7 l 80.5,-92.6 c 0.5,-0.6 1,-1.2 1.5,-1.8 15.3,-18.7 12.6,-46.3 -6.1,-61.6 -18.7,-15.3 -46.3,-12.6 -61.6,6.1 l -80.2,92.5 c -15.9,18.2 -14,45.9 4.2,61.9 l -0.1,0 z"/><path fill="#fff" stroke="#000" stroke-width="14.17" d="m 1217.5,659.5 v -0 c 0,0 -120.8,-69.8 -120.8,-69.8 -18.3,-10.6 -40,-13.5 -60.4,-8.1 L 558,709.8 c -20.4,5.5 -37.8,18.8 -48.4,37.1 l -69.6,121 c -10.5,18.3 -13.4,40 -8,60.3 l 128.2,478.3 c 5.5,20.4 18.8,37.8 37.1,48.4 l 120.7,69.8 c 18.3,10.4 40,13.2 60.4,7.8 l 478.3,-128.2 c 20.4,-5.4 37.8,-18.7 48.4,-36.9 l 69.7,-120.8 c 10.6,-18.3 13.5,-40 8,-60.4 L 1254.6,707.9 c -5.4,-20.4 -18.8,-37.9 -37.1,-48.4 z m 76.4,533.5 c 2.1,8 1,16.6 -3.1,23.7 l -53.4,92.5 c -4.2,7.2 -11,12.4 -19,14.6 l -447.2,119.8 c -8,2.1 -16.6,1 -23.7,-3.1 l -92.2,-53.5 c -7.2,-4.2 -12.4,-11 -14.6,-19 L 521,921.3 c -2.1,-8 -1,-16.6 3.1,-23.7 l 53.1,-92.4 c 4.2,-7.2 11,-12.4 19,-14.6 l 447.3,-119.9 c 8,-2.1 16.6,-1 23.7,3.1 l 92.5,53.4 c 7.2,4.2 12.4,11 14.6,19 l 119.6,446.9 z"/><path fill="#fff" d="m 703.4,1091.8 c 23.4,-6.3 37.2,-30.3 31,-53.6 -4.7,-17.6 5.7,-35.7 23.3,-40.4 17.6,-4.7 35.7,5.7 40.4,23.3 l 0,0.1 c 6.3,23.4 30.3,37.2 53.7,30.9 23.4,-6.3 37.2,-30.3 30.9,-53.7 -18,-62.3 -82,-99.3 -144.9,-83.7 -64.7,16 -104.2,81.4 -88.1,146.1 h 0 c 6.3,23.4 30.3,37.2 53.6,31 z"/><path fill="#fff" d="m 1177.3,1267.3 -392.7,105.2 c -23.4,6.3 -47.5,-7.6 -53.8,-31 v 0 c -19,-71 72.5,-157.2 204.3,-192.5 131.8,-35.3 254.2,-6.4 273.2,64.6 v 0 c 6.3,23.4 -7.6,47.5 -31,53.8 z"/><rect fill="#1d8d22" x="1041.9" y="583.9" width="440.9" height="866.1" transform="rotate(15,1262.3,1017)"/><rect fill="#2ead33" x="1467.7" y="698.2" width="441.8" height="866.1" transform="rotate(15,1688.6,1131.2)"/><path d="m 1562.5,1047.5 c 6.1,17.4 20.4,30.6 38.1,35.3 10.6,2.9 21.8,2.4 32.2,-1.3 L 1779,1031.1 c 0.9,-0.3 1.9,-0.6 2.8,-1 28.5,-10.7 42.9,-42.5 32.1,-71 -10.7,-28.5 -42.5,-42.9 -71,-32.1 l -145.9,50.4 c -28.8,9.9 -44.2,41.3 -34.4,70.2 z"/><path stroke="#fff" stroke-width="14.17" d="m 2065.9,836.2 v -0.1 l -87.8,-152.3 c -13.3,-23 -35.1,-39.9 -60.8,-46.9 L 1314.6,475.5 c -25.7,-6.8 -53.1,-3.2 -76.2,10 l -152.2,88.1 c -23,13.3 -39.8,35.1 -46.7,60.8 L 878.1,1237.1 c -6.9,25.7 -3.3,53.1 10,76.2 l 87.8,152.2 c 13.4,22.9 35.3,39.7 61,46.5 l 602.7,161.5 c 25.7,6.9 53,3.4 76.1,-9.8 l 152.1,-88 c 23.1,-13.2 40,-35.2 46.8,-61 l 161.4,-602.5 c 7,-25.7 3.4,-53.1 -10,-76.2 z m -252.7,630.3 c -2.7,10.1 -9.3,18.7 -18.4,23.9 l -116.6,67.3 c -9.1,5.2 -19.8,6.6 -29.9,3.9 l -563.5,-151 c -10.1,-2.7 -18.7,-9.3 -23.9,-18.4 l -66.9,-116.5 c -5.2,-9.1 -6.6,-19.8 -3.9,-29.9 L 1141,682.9 c 2.7,-10.1 9.3,-18.7 18.4,-23.9 l 116.2,-67.3 c 9.1,-5.2 19.8,-6.6 29.9,-3.9 l 563.6,151 c 10.1,2.7 18.7,9.3 23.9,18.4 l 67.3,116.5 c 5.2,9.1 6.6,19.8 3.9,29.9 -123,452.9 -41.2,151.5 -151,562.9 z"/><path d="m 1232.6,984 c 29.4,7.9 59.7,-9.6 67.6,-39 6,-22.2 28.7,-35.3 50.9,-29.4 22.2,5.9 35.4,28.7 29.4,50.9 l -0,0.1 c -7.9,29.4 9.6,59.7 39.1,67.6 29.4,7.9 59.7,-9.6 67.6,-39.1 19.6,-79.3 -26.9,-160 -105.4,-182.6 -80.7,-23.3 -164.9,23.2 -188.2,103.9 h 0.1 c -7.9,29.5 9.6,59.7 39,67.6 z"/><path d="M 1696.9,1258.7 1202.1,1126.1 c -29.5,-7.9 -59.8,9.6 -67.7,39.1 v 0 c -23.9,89.5 91.3,198 257.4,242.5 166.1,44.5 320.3,8.1 344.2,-81.3 v 0 c 7.9,-29.5 -9.6,-59.8 -39.1,-67.7 z"/></svg>';
        const host = document.createElement(TAG);
        host.style.cssText = 'position:fixed;z-index:2147483647;top:0;left:0';
        const root = host.attachShadow({ mode: 'closed' });
        root.innerHTML = `
    <style>
      /* The dark palette of robotframework-browser.org (app/assets/css/tokens.css). */
      :host { --paper: #1c2227; --chrome: #232a30; --plate: #12171a; --line: #38424a;
              --line-strong: #4e5a63; --ink: #e2e1d7; --dim: #a3afb5; --faint: #8b979d;
              --red: #ff6b5e; --red-soft: #2e1b19; --teal: #00c0b5; --amber: #ffb86b; }
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
      .head button { flex: none; padding: 2px 6px; cursor: pointer; }
      .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--faint); flex: none; }
      .dot.rec { background: var(--red); }
      .title { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .count { color: var(--dim); }
      button { background: transparent; color: var(--ink); border: 1px solid var(--line-strong);
               border-radius: 4px; padding: 4px 8px; cursor: pointer; }
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
      .calls li::marker { color: var(--faint); }
      .calls:empty::after { content: 'no keyword calls yet'; color: var(--faint); }
      .calls li { white-space: pre; }
      .cell { margin-left: 8px; }
      .cell.pick { cursor: pointer; text-decoration: underline dotted var(--teal); }
      .cell.pick:hover { background: rgb(0 192 181 / 20%); }
      .notice { color: var(--amber); }
      .picking { background: var(--amber); color: var(--plate); font-weight: bold; border-radius: 4px; padding: 6px; }
      .args label, .offer label { display: block; }
      input[type=checkbox] { accent-color: var(--red); }
      .offer { background: var(--chrome); border: 1px solid var(--line); border-radius: 4px; padding: 6px;
               display: flex; flex-direction: column; gap: 6px; }
      .busy button { opacity: .5; pointer-events: none; }
      .row { display: flex; gap: 6px; }
      .row > button { flex: 1; }
      .hint { color: var(--dim); }
      .err { color: var(--red); }
      [hidden] { display: none !important; }
      .modal { position: fixed; inset: 0; background: rgb(0 0 0 / 50%);
               display: flex; align-items: center; justify-content: center; }
      .dialog { background: var(--paper); color: var(--ink); padding: 16px; border-radius: 7px;
                border: 1px solid var(--line); color-scheme: dark;
                width: 320px; display: flex; flex-direction: column; gap: 10px; }
      input, textarea { padding: 6px 8px; border-radius: 4px; border: 1px solid var(--line-strong);
              background: var(--plate); color: var(--ink); font: inherit; }
      textarea { resize: vertical; white-space: pre; }
    </style>
    <div class="panel" id="panel">
      <div class="head" id="head">
        ${LOGO}
        <span class="dot" id="dot"></span>
        <span class="title" id="title">Idle</span>
        <span class="count" id="count"></span>
        <button id="stop" title="End the recording session">Stop</button>
        <button id="collapse" title="Collapse">-</button>
      </div>
      <div class="body" id="body">
        <div class="picking" id="picking" hidden></div>
        <ol class="calls" id="calls"></ol>
        <div class="hint" id="hint"></div>
        <div class="notice" id="notice" hidden></div>
        <div class="offer" id="offer" hidden>
          <div id="offerText"></div>
          <div id="offerList"></div>
          <div class="row"><button id="offerSkip">Skip</button><button class="primary" id="offerApply">Replace</button></div>
        </div>
        <div class="args" id="args"></div>
        <div class="err" id="err" hidden></div>
        <div class="notice" id="argHint" hidden></div>
        <div class="row" id="idleRow">
          <button class="primary" id="new">+ New Keyword</button>
        </div>
        <div class="row" id="recRow" hidden>
          <button id="undo">Undo</button>
          <button class="danger" id="discard">Discard</button>
          <button class="primary" id="finish">Finish</button>
        </div>
      </div>
    </div>
    <div class="modal" id="modal" hidden>
      <div class="dialog">
        <div>Name of the keyword to record</div>
        <input id="nameInput" placeholder="e.g. Login As Admin" autocomplete="off">
        <div class="err" id="modalErr" hidden></div>
        <div class="row">
          <button id="cancel">Cancel</button>
          <button class="primary" id="ok">Start recording</button>
        </div>
      </div>
    </div>
    <div class="modal" id="argModal" hidden>
      <div class="dialog">
        <div>Mark the part that becomes an argument (or leave it unmarked for the whole value)</div>
        <textarea id="argValue" rows="3" readonly></textarea>
        <input id="argName" placeholder="argument name, e.g. email" autocomplete="off">
        <div class="err" id="argErr" hidden></div>
        <div class="row"><button id="argCancel">Cancel</button><button class="primary" id="argOk">Make argument</button></div>
      </div>
    </div>`;

        const $ = (id) => root.getElementById(id);
        const panel = $('panel');
        const send = (command) => {
            if (!window.__rfbCommand) return false;
            window.__rfbCommand(command);
            return true;
        };

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
        let resizing = false;
        panel.addEventListener('pointerdown', (event) => {
            const rect = panel.getBoundingClientRect();
            // The native resize grip lives in the bottom-right corner; anywhere
            // else on the panel is ordinary content, not a resize gesture.
            resizing = rect.right - event.clientX <= 16 && rect.bottom - event.clientY <= 16;
        });
        const endResize = () => {
            if (!resizing) return;
            resizing = false;
            write(SIZE_KEY, { width: Math.round(panel.getBoundingClientRect().width) });
        };
        window.addEventListener('pointerup', endResize);
        window.addEventListener('pointercancel', endResize);

        // -- placement ------------------------------------------------------- //
        const position = read(POSITION_KEY, { x: window.innerWidth - 340, y: 12 });
        const place = () => {
            const width = panel.offsetWidth || 320;
            const x = Math.min(Math.max(position.x, 0), Math.max(window.innerWidth - width - 10, 0));
            const y = Math.min(Math.max(position.y, 0), Math.max(window.innerHeight - 60, 0));
            host.style.transform = `translate(${x}px, ${y}px)`;
        };
        place();

        let drag = null;
        $('head').addEventListener('pointerdown', (event) => {
            // The header doubles as the drag handle; its buttons must still click.
            if (event.target.id === 'collapse' || event.target.id === 'stop') return;
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

        // -- collapse -------------------------------------------------------- //
        let collapsed = read(COLLAPSED_KEY, false);
        const applyCollapsed = () => {
            $('body').hidden = collapsed;
            $('collapse').textContent = collapsed ? '+' : '-';
        };
        applyCollapsed();
        $('collapse').addEventListener('click', () => {
            collapsed = !collapsed;
            write(COLLAPSED_KEY, collapsed);
            applyCollapsed();
        });

        // -- commands -------------------------------------------------------- //
        // A `new` command is only answered by a later poll, so the modal cannot be
        // closed when it is sent: a rejected name (duplicate, unusable) must come
        // back *inside* the panel, with what was typed still there to correct.
        let pending = false;
        // The state a poll renders right after the `new` was sent can still be
        // the one from before it - including the error of an earlier rejected
        // name. Only a state that differs from the one at send time, or the
        // second render after it (by then the command has been processed), answers it.
        let sentKey = null;
        let rendersSinceSend = 0;
        const openModal = () => {
            pending = false;
            $('ok').disabled = false;
            $('nameInput').value = '';
            $('modalErr').hidden = true;
            $('modal').hidden = false;
            $('nameInput').focus();
        };
        const closeModal = () => {
            pending = false;
            $('ok').disabled = false;
            $('modal').hidden = true;
        };
        $('new').addEventListener('click', openModal);
        $('cancel').addEventListener('click', closeModal);
        $('ok').addEventListener('click', () => {
            if (pending) return;
            const name = $('nameInput').value.trim();
            if (!name) {
                $('modalErr').textContent = 'Keyword name must not be empty.';
                $('modalErr').hidden = false;
                return;
            }
            if (!send({ cmd: 'new', name })) return;
            pending = true;
            sentKey = lastKey;
            rendersSinceSend = 0;
            $('ok').disabled = true;
        });
        $('stop').addEventListener('click', () => send({ cmd: 'stop' }));
        $('undo').addEventListener('click', () => send({ cmd: 'undo' }));
        $('discard').addEventListener('click', () => send({ cmd: 'discard' }));
        $('finish').addEventListener('click', () => send({ cmd: 'finish' }));

        // -- keyword arguments -------------------------------------------------- //
        // `raw` is the literal cell text the offsets refer to (the rendered text
        // differs for escapes); Python rejects the command if it changed meanwhile.
        let argTarget = null;
        // While Python is finishing a keyword nothing may be sent.
        const isPending = () => !!(window.__rfbToolbarState && window.__rfbToolbarState.pending);
        // The hint is owned by the toolbar itself (render never touches it except
        // to clear it on a real state change), unlike #err which mirrors the state.
        const setHint = (text) => {
            $('argHint').textContent = text;
            $('argHint').hidden = !text;
        };
        const openArgModal = (call, value, raw) => {
            if (isPending()) return;
            if (raw === null || raw === undefined) {
                setHint('This value already contains an argument.');
                return;
            }
            setHint('');
            argTarget = { call, value, raw };
            $('argValue').value = raw;
            $('argName').value = '';
            $('argErr').hidden = true;
            $('argModal').hidden = false;
            $('argValue').focus();
        };
        const closeArgModal = () => {
            $('argModal').hidden = true;
            argTarget = null;
        };
        $('argCancel').addEventListener('click', closeArgModal);
        $('argOk').addEventListener('click', () => {
            if (!argTarget || isPending()) return;
            const name = $('argName').value.trim();
            if (!name) {
                $('argErr').textContent = 'Argument name must not be empty.';
                $('argErr').hidden = false;
                return;
            }
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
            send({
                cmd: 'argument',
                call: argTarget.call,
                value: argTarget.value,
                start,
                end,
                name,
                raw: argTarget.raw,
            });
            closeArgModal();
        });
        // -- keyboard isolation ---------------------------------------------- //
        // Keyboard events are composed, so typing in the toolbar would reach the
        // page's key handlers (shortcuts, typeahead) retargeted to the host. A
        // capture listener on window runs before any listener of the document
        // and stops them there; the text still gets typed (default action), and
        // the toolbar's own keys are handled here, as its inputs no longer see them.
        const toolbarKeys = {
            nameInput: (event) => {
                if (event.key === 'Enter') $('ok').click();
                if (event.key === 'Escape') closeModal();
            },
            argName: (event) => {
                if (event.key === 'Enter') $('argOk').click();
                if (event.key === 'Escape') closeArgModal();
            },
        };
        const KEYBOARD_EVENTS = [
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
        const isolateKeyboard = (event) => {
            if (event.target !== host) return;
            event.stopImmediatePropagation();
            const focused = root.activeElement;
            const handler = event.type === 'keydown' && focused ? toolbarKeys[focused.id] : undefined;
            if (handler) handler(event);
        };
        KEYBOARD_EVENTS.forEach((type) => window.addEventListener(type, isolateKeyboard, true));
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

        // -- render ---------------------------------------------------------- //
        // Polling re-sends the state every 200 ms. Rebuilding the DOM that often
        // would swallow clicks straddling a poll, reset the scroll position and
        // the offer's checkboxes, so an unchanged state renders nothing.
        let lastKey = null;
        let offerKey = null;
        let offerChecked = {};
        window.__rfbToolbarRender = (state) => {
            if (!state) return;
            window.__rfbToolbarState = state;
            const key = JSON.stringify(state);
            if (key !== lastKey) {
                lastKey = key;
                renderBody(state);
            }
            finishRender(state, key);
        };
        const renderBody = (state) => {
            setHint('');
            const recording = state.state === 'recording';
            const calls = Array.isArray(state.calls) ? state.calls : [];
            const keywords = Array.isArray(state.keywords) ? state.keywords : [];
            const argumentList = Array.isArray(state.arguments) ? state.arguments : [];
            $('dot').className = recording ? 'dot rec' : 'dot';
            $('title').textContent = recording ? state.name || 'Recording' : 'Idle';
            $('count').textContent = recording ? `(${calls.length})` : '';
            const list = $('calls');
            const oldTop = list.scrollTop;
            const wasAtBottom = list.scrollTop + list.clientHeight >= list.scrollHeight - 4;
            const oldCount = list.children.length;
            list.textContent = '';
            calls.forEach((call, callIndex) => {
                const item = document.createElement('li');
                const kw = document.createElement('span');
                kw.textContent = call.keyword ?? '';
                item.appendChild(kw);
                (call.values || []).forEach((value, valueIndex) => {
                    const cell = document.createElement('span');
                    const pick = !!value.selectable && recording;
                    cell.className = pick ? 'cell pick' : 'cell';
                    cell.textContent = value.text ?? '';
                    if (pick) {
                        cell.title = 'Make this value an argument';
                        cell.addEventListener('click', () => openArgModal(callIndex, valueIndex, value.raw));
                    }
                    item.appendChild(cell);
                });
                list.appendChild(item);
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
                    label.append(` ${calls[c] ? (calls[c].text ?? '') : ''}`);
                    box.appendChild(label);
                });
            }
            const args = $('args');
            args.textContent = '';
            if (recording) {
                argumentList.forEach((arg) => {
                    const label = document.createElement('label');
                    const check = document.createElement('input');
                    check.type = 'checkbox';
                    check.checked = !!arg.useDefault;
                    check.addEventListener('change', () => {
                        if (isPending()) {
                            check.checked = !check.checked;
                            return;
                        }
                        send({ cmd: 'default', argument: arg.name, use: check.checked });
                    });
                    label.appendChild(check);
                    label.append(` \${${arg.name}} default: ${arg.default ?? ''}`);
                    args.appendChild(label);
                });
            }
            $('panel').classList.toggle('busy', !!state.pending);
            if (state.pending === 'new') $('title').textContent = `${state.name || 'Keyword'} - starting…`;
            else if (state.pending) $('title').textContent = `${state.name || 'Recording'} - finishing…`;
            $('idleRow').hidden = recording;
            $('recRow').hidden = !recording;
            // A fixed-name recording writes exactly one keyword: no New, no Finish.
            $('new').hidden = !!state.fixedName;
            $('finish').hidden = !!state.fixedName;
            $('hint').textContent = recording
                ? `writing to ${state.target}`
                : `${keywords.length} keyword(s) recorded into ${state.target}`;
            $('err').textContent = state.error || '';
            $('err').hidden = !state.error;
        };
        const finishRender = (state, key) => {
            const recording = state.state === 'recording';
            // The panel's content-driven width can change with every render (a
            // longer Keyword Call just got added); re-clamp so growth never pushes it
            // past the right edge of the viewport.
            place();
            if (pending && (key !== sentKey || ++rendersSinceSend >= 2)) {
                if (state.error) {
                    // Rejected: keep the panel and the typed name, let them retry.
                    $('modalErr').textContent = state.error;
                    $('modalErr').hidden = false;
                    pending = false;
                    $('ok').disabled = false;
                } else if (recording) {
                    // Accepted only once the session actually reports recording;
                    // `error === null` alone can still be the pre-command state.
                    closeModal();
                }
            }
        };

        window.__rfbToolbarRemove = () => {
            // Nothing re-injects the toolbar once polling has stopped, so removing
            // it here is enough - no "stay away" flag is needed.
            window.removeEventListener('pointerup', endResize);
            window.removeEventListener('pointercancel', endResize);
            KEYBOARD_EVENTS.forEach((type) => window.removeEventListener(type, isolateKeyboard, true));
            host.remove();
            delete window.__rfbToolbarRender;
            delete window.__rfbToolbarState;
            delete window.__rfbToolbarRemove;
        };

        const attach = () => document.body && document.body.appendChild(host);
        if (document.body) attach();
        else document.addEventListener('DOMContentLoaded', attach);
    }

    installToolbar('rfb-recorder-toolbar');
})();
