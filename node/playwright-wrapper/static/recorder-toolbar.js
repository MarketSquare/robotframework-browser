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

        const host = document.createElement(TAG);
        host.style.cssText = 'position:fixed;z-index:2147483647;top:0;left:0';
        const root = host.attachShadow({ mode: 'closed' });
        root.innerHTML = `
    <style>
      * { box-sizing: border-box; font: 12px/1.4 system-ui, sans-serif; }
      /* Content-driven width: the panel grows to the widest recorded Keyword Call line
         (the .calls list below is white-space: pre, so its max-content width is
         exactly that), clamped so it neither goes back to cramped nor swallows
         the page. resize: horizontal lets the user override that within the
         same clamps; overflow: hidden is required for resize to take effect and
         also keeps the rounded corners clean. Extra bottom padding keeps the
         native resize grip clear of the button rows below. */
      .panel { width: max-content; min-width: 320px; max-width: min(80vw, 900px);
               resize: horizontal; overflow: hidden; padding-bottom: 8px;
               background: #1e1e1e; color: #eee; border-radius: 6px;
               box-shadow: 0 4px 16px rgba(0,0,0,.45); }
      .head { display: flex; align-items: center; gap: 6px; padding: 6px 8px;
              background: #2d2d2d; cursor: move; user-select: none; }
      /* Stop lives in the header so it is reachable in both states and both
         modes - it ends the whole session, unlike the body's state-specific rows. */
      .head button { flex: none; padding: 2px 6px; cursor: pointer; }
      .dot { width: 8px; height: 8px; border-radius: 50%; background: #888; flex: none; }
      .dot.rec { background: #e51400; }
      .title { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .count { opacity: .6; }
      button { background: #3a3a3a; color: #eee; border: 0; border-radius: 4px;
               padding: 4px 8px; cursor: pointer; }
      button:hover { background: #4a4a4a; }
      button.primary { background: #0a6ebd; }
      button.danger { background: #8b1a1a; }
      .body { padding: 8px; display: flex; flex-direction: column; gap: 8px; }
      .calls { max-height: 220px; overflow: auto; background: #141414; border-radius: 4px;
               margin: 0; padding: 6px 6px 6px 28px; font-family: ui-monospace, monospace;
               font-size: 11px; }
      .calls:empty::after { content: 'no keyword calls yet'; opacity: .5; }
      .calls li { white-space: pre; }
      .cell { margin-left: 8px; }
      .cell.pick { cursor: pointer; text-decoration: underline dotted; }
      .cell.pick:hover { background: #0a6ebd55; }
      .notice { color: #ffd479; }
      .picking { background: #b8860b; color: #fff; font-weight: bold; border-radius: 4px; padding: 6px; }
      .args label, .offer label { display: block; }
      .offer { background: #2a2a2a; border-radius: 4px; padding: 6px;
               display: flex; flex-direction: column; gap: 6px; }
      .busy button { opacity: .5; pointer-events: none; }
      .row { display: flex; gap: 6px; }
      .row > button { flex: 1; }
      .hint { opacity: .6; }
      .err { color: #ff9a9a; }
      [hidden] { display: none !important; }
      .modal { position: fixed; inset: 0; background: rgba(0,0,0,.5);
               display: flex; align-items: center; justify-content: center; }
      .dialog { background: #1e1e1e; color: #eee; padding: 16px; border-radius: 6px;
                width: 320px; display: flex; flex-direction: column; gap: 10px; }
      input { padding: 6px 8px; border-radius: 4px; border: 1px solid #555;
              background: #141414; color: #eee; }
    </style>
    <div class="panel" id="panel">
      <div class="head" id="head">
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
        <input id="argValue" readonly>
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
        $('nameInput').addEventListener('keydown', (event) => {
            if (event.key === 'Enter') $('ok').click();
            if (event.key === 'Escape') closeModal();
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
            const from = input.selectionStart ?? 0;
            const to = input.selectionEnd ?? 0;
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
        $('argName').addEventListener('keydown', (event) => {
            if (event.key === 'Enter') $('argOk').click();
            if (event.key === 'Escape') closeArgModal();
        });
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
