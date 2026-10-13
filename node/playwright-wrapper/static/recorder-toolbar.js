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
               padding: 6px; white-space: pre; font-family: ui-monospace, monospace;
               font-size: 11px; }
      .calls:empty::after { content: 'no keyword calls yet'; opacity: .5; }
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
        <div class="calls" id="calls"></div>
        <div class="hint" id="hint"></div>
        <div class="err" id="err" hidden></div>
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

        // -- render ---------------------------------------------------------- //
        window.__rfbToolbarRender = (state) => {
            if (!state) return;
            window.__rfbToolbarState = state;
            const recording = state.state === 'recording';
            $('dot').className = recording ? 'dot rec' : 'dot';
            $('title').textContent = recording ? state.name : 'Idle';
            $('count').textContent = recording ? `(${state.calls.length})` : '';
            $('calls').textContent = state.calls.map((c) => c.text).join('\n');
            $('idleRow').hidden = recording;
            $('recRow').hidden = !recording;
            // A fixed-name recording writes exactly one keyword: no New, no Finish.
            $('new').hidden = !!state.fixedName;
            $('finish').hidden = !!state.fixedName;
            $('hint').textContent = recording
                ? `writing to ${state.target}`
                : `${state.keywords.length} keyword(s) recorded into ${state.target}`;
            $('err').textContent = state.error || '';
            $('err').hidden = !state.error;
            // The panel's content-driven width can change with every render (a
            // longer Keyword Call just got added); re-clamp so growth never pushes it
            // past the right edge of the viewport.
            place();
            if (pending) {
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
