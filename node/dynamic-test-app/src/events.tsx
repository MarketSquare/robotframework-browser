import React from 'react';

/**
 * EventsPage — standalone event testing page
 * - Test input + button
 * - Logs every relevant event with 24h wall time ("HH:MM:SS.mmm") and monotonic time (performance.now())
 * - Visual log + JSON-lines textarea for machine parsing
 * - Deterministic readiness markers for tests:
 *     - window.__eventLoggerReady === 1
 *     - <div id="rf-ready" data-ready="1">
 *     - documentElement[data-eventlogger="1"]
 */
const EventsPage: React.FC = () => {
  React.useEffect(() => {
    document.title = 'Event Test Page';
  }, []);

  return (
    <div style={{ padding: 16, fontFamily: 'system-ui, sans-serif' }}>
      <h1 id="events-heading">Event Test Page</h1>
      <p>Use the input and the button below. All events will be logged with timestamps.</p>
      <EventLogger />
    </div>
  );
};

export default EventsPage;

function EventLogger() {
  const logRef = React.useRef<HTMLDivElement>(null);
  const textRef = React.useRef<HTMLTextAreaElement>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);
  const buttonRef = React.useRef<HTMLButtonElement>(null);
  const [isAttached, setIsAttached] = React.useState(false);

  function formatTime24h(d: Date): string {
    const hh = String(d.getHours()).padStart(2, '0');
    const mm = String(d.getMinutes()).padStart(2, '0');
    const ss = String(d.getSeconds()).padStart(2, '0');
    const ms = String(d.getMilliseconds()).padStart(3, '0');
    return `${hh}:${mm}:${ss}.${ms}`;
  }

  const pushVisual = (text: string) => {
    const root = logRef.current;
    if (!root) return;
    const el = document.createElement('div');
    el.textContent = text;
    root.appendChild(el);
    root.scrollTop = root.scrollHeight;
  };

  const pushText = (obj: Record<string, unknown>) => {
    const ta = textRef.current;
    if (!ta) return;
    ta.value += JSON.stringify(obj) + '\n';
    ta.scrollTop = ta.scrollHeight;
  };

  const buildEventSummary = (e: Event) => {
    const base: Record<string, unknown> = {
      time: formatTime24h(new Date()), // human-readable 24h time
      mono: performance.now(),         // monotonic ms since page load
      type: e.type,
      targetId: (e.target as HTMLElement | null)?.id || '',
    };
    if ('button' in e) {
      const me = e as unknown as MouseEvent;
      base.button = me.button;
      // @ts-ignore
      base.pageX = (me as any).pageX;
      // @ts-ignore
      base.pageY = (me as any).pageY;
    }
    if ('key' in e) {
      const ke = e as unknown as KeyboardEvent;
      base.key = ke.key;
      base.code = ke.code;
      base.altKey = ke.altKey;
      base.ctrlKey = ke.ctrlKey;
      base.metaKey = ke.metaKey;
      base.shiftKey = ke.shiftKey;
      base.repeat = ke.repeat;
    }
    if ('pointerType' in e) {
      const pe = e as unknown as PointerEvent;
      base.pointerType = pe.pointerType;
      base.pointerId = pe.pointerId;
    }
    return base;
  };

  React.useLayoutEffect(() => {
    const input = inputRef.current;
    const button = buttonRef.current;
    if (!input || !button) return;

    const targets: Element[] = [input, button];
    const events = [
      // Mouse
      'click','dblclick','mousedown','mouseup','mouseenter','mouseleave','mouseover','mouseout','mousemove','contextmenu',
      // Focus
      'focus','blur',
      // Keyboard
      'keydown','keypress','keyup',
      // Form/Input
      'input','change','submit',
      // Drag
      'drag','dragstart','dragend','dragenter','dragleave','dragover','drop',
      // Clipboard
      'copy','cut','paste',
      // Touch
      'touchstart','touchend','touchmove','touchcancel',
      // Pointer
      'pointerdown','pointerup','pointermove','pointerenter','pointerleave','pointercancel','pointerover','pointerout',
    ];

    const handler = (e: Event) => {
      const data = buildEventSummary(e);
      // Show both wall-clock and monotonic in the visual log
      pushVisual(`[${data.time} | ${Math.round(data.mono as number)}ms] ${data.type} on #${data.targetId}`);
      // Persist full JSON line
      pushText(data);
    };

    for (const t of targets) {
      for (const ev of events) {
        t.addEventListener(ev, handler as EventListener, { passive: true });
      }
    }

    setIsAttached(true);
    (window as any).__eventLoggerReady = 1;
    document.documentElement.setAttribute('data-eventlogger', '1');
    window.dispatchEvent(new Event('event-logger-ready'));

    return () => {
      for (const t of targets) {
        for (const ev of events) {
          t.removeEventListener(ev, handler as EventListener);
        }
      }
      setIsAttached(false);
      (window as any).__eventLoggerReady = 0;
      document.documentElement.removeAttribute('data-eventlogger');
    };
  }, []);

  const clearLogs = () => {
    if (logRef.current) logRef.current.innerHTML = '';
    if (textRef.current) textRef.current.value = '';
  };

  return (
    <div id="event_logger_section" style={{ marginTop: 12 }}>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <input
          ref={inputRef}
          id="event_test_input"
          type="text"
          placeholder="Type or focus here"
          style={{ padding: 6 }}
        />
        <button ref={buttonRef} id="event_test_button">Test Button</button>
        <button id="event_log_clear" type="button" onClick={clearLogs}>Clear Log</button>
        <span id="event_listeners_status" aria-live="polite">
          {isAttached ? 'Listeners attached' : 'Listeners detached'}
        </span>
        {/* Hidden, deterministic readiness marker */}
        <div id="rf-ready" data-ready={isAttached ? '1' : '0'} style={{ display: 'none' }} />
      </div>

      <div
        id="event_log"
        ref={logRef}
        style={{
          marginTop: 10,
          width: '95%',
          maxWidth: 900,
          height: 280,
          overflowY: 'auto',
          border: '1px solid gray',
          padding: 6,
          fontFamily: 'monospace',
          background: '#f9f9f9',
        }}
      />

      <label htmlFor="event_log_text" style={{ display: 'block', marginTop: 10 }}>
        Raw event log (JSON lines)
      </label>
      <textarea
        id="event_log_text"
        ref={textRef}
        readOnly
        style={{
          width: '95%',
          maxWidth: 900,
          height: 180,
          fontFamily: 'monospace',
          whiteSpace: 'pre',
        }}
      />
    </div>
  );
}
