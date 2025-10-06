import React, { ChangeEvent, MouseEvent, useRef, useState } from 'react';

function goesInvisible(event: React.MouseEvent<HTMLButtonElement>) {
    event.persist();
    console.log('Going hidden in 1 second');
    setTimeout(() => {
        //@ts-expect-error TypeScript can't infer that the element has style
        event.target.style.visibility = 'hidden';
        console.log('Went hidden');
    }, 500);
}

function popup() {
    window.open('../static/popup.html', 'width=400,height=200,scrollbars=yes');
}

function ProgressBar() {
    const [width, setWidth] = useState(() => 10);
    const enabled = useRef(false);
    function frame() {
        if (enabled.current && width < 100) {
            setWidth(width + 1);
            console.log('width growing');
        }
    }
    React.useEffect(() => {
        const interval = setInterval(frame, 10);
        return () => clearInterval(interval);
    });
    return (
        <div
            id="progress"
            style={{
                position: 'absolute',
                top: '20px',
                left: '500px',
                width: '400px',
                height: '30px',
                backgroundColor: 'gray',
            }}
        >
            <div
                id="progress_bar"
                onClick={() => {
                    enabled.current = true;
                }}
                style={{ width: width + '%', height: '100%', backgroundColor: 'green' }}
            />
            <div style={{ textAlign: 'center', color: 'black' }}> {width}% </div>
        </div>
    );
}

async function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

async function delayedRequest() {
    await sleep(200);
    console.log(await fetch('/api/get/json'));
}

async function delayedRequestBig() {
    await sleep(250);
    console.log(await fetch('/api/get/json/big'));
}

function fileUploaded(uploadResultElement: React.RefObject<HTMLElement>, event: ChangeEvent<HTMLInputElement>) {
    const files = event.target.files;
    let fileNames = '';
    if (files) {
        for (let i = 0; i < files.length; i++) {
            if (i > 0) {
                fileNames = `${fileNames},${files[i].name}`;
            } else {
                fileNames = files[i].name;
            }
        }
        uploadResultElement.current!.innerHTML = fileNames;
    } else {
        uploadResultElement.current!.innerHTML = 'no uploaded file';
    }
}

function testPrompt(promptResultElement: React.RefObject<HTMLElement>) {
    const input = prompt('Enter a value');
    if (input) promptResultElement.current!.innerHTML = input;
    else promptResultElement.current!.innerHTML = 'prompt_not_filled';
}

/**
 * EventLogger — a compact test bench that attaches listeners to the test input and button
 * and logs all events with timestamps to a visual log and a textarea.
 *
 * - Visual log: #event_log (div, scrolls as entries arrive)
 * - Plain text log: #event_log_text (textarea containing one JSON line per event)
 */
function EventLogger() {
    const logRef = React.useRef<HTMLDivElement>(null);
    const textRef = React.useRef<HTMLTextAreaElement>(null);

    // NEW: refs for the actual controls (no querySelector/id lookups)
    const inputRef = React.useRef<HTMLInputElement>(null);
    const buttonRef = React.useRef<HTMLButtonElement>(null);

    // Expose a deterministic “ready” signal for your tests
    const [isAttached, setIsAttached] = React.useState(false);

    function formatTime(d: Date): string {
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
            time: formatTime(new Date()),
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

    // IMPORTANT: useLayoutEffect => attaches before paint
    React.useLayoutEffect(() => {
        const input = inputRef.current;
        const button = buttonRef.current;
        if (!input || !button) return;

        const targets: Element[] = [input, button];
        const events = [
            'click',
            'dblclick',
            'mousedown',
            'mouseup',
            'mouseenter',
            'mouseleave',
            'mouseover',
            'mouseout',
            'mousemove',
            'contextmenu',
            'focus',
            'blur',
            'keydown',
            'keypress',
            'keyup',
            'input',
            'change',
            'submit',
            'drag',
            'dragstart',
            'dragend',
            'dragenter',
            'dragleave',
            'dragover',
            'drop',
            'copy',
            'cut',
            'paste',
            'touchstart',
            'touchend',
            'touchmove',
            'touchcancel',
            'pointerdown',
            'pointerup',
            'pointermove',
            'pointerenter',
            'pointerleave',
            'pointercancel',
            'pointerover',
            'pointerout',
        ];

        const handler = (e: Event) => {
            const data = buildEventSummary(e);
            pushVisual(`[${data.time}] ${data.type} on #${data.targetId}`);
            pushText(data);
        };

        for (const t of targets)
            for (const ev of events) {
                t.addEventListener(ev, handler as EventListener, { passive: true });
            }

        // Mark ready synchronously (your tests can wait on this)
        setIsAttached(true);
        (window as any).__eventLoggerReady = 1; // window flag
        document.documentElement.setAttribute('data-eventlogger', '1'); // HTML attr
        window.dispatchEvent(new Event('event-logger-ready')); // DOM event

        return () => {
            for (const t of targets)
                for (const ev of events) {
                    t.removeEventListener(ev, handler as EventListener);
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
        <div id="event_logger_section" style={{ marginTop: '20px' }}>
            <h2>Event Test Area</h2>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
                {/* NEW: refs instead of ids */}
                <input ref={inputRef} id="event_test_input" type="text" placeholder="Type or focus here" />
                <button ref={buttonRef} id="event_test_button">
                    Test Button
                </button>
                <button id="event_log_clear" type="button" onClick={clearLogs}>
                    Clear Log
                </button>
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
                    marginTop: '10px',
                    width: '80%',
                    maxHeight: '240px',
                    overflowY: 'auto',
                    border: '1px solid gray',
                    padding: '6px',
                    fontFamily: 'monospace',
                    background: '#f9f9f9',
                }}
            />

            <label htmlFor="event_log_text" style={{ display: 'block', marginTop: '10px' }}>
                Raw event log (JSON lines)
            </label>
            <textarea
                id="event_log_text"
                ref={textRef}
                readOnly
                style={{ width: '80%', height: '160px', fontFamily: 'monospace', whiteSpace: 'pre' }}
            />
        </div>
    );
}

export default function Site() {
    const username = useRef('');
    const password = useRef('');

    const [submit, setSubmit] = useState(false);
    const uploadResult = React.createRef<HTMLDivElement>();
    const promptResult = React.createRef<HTMLDivElement>();
    const networkPinger = React.createRef<HTMLDivElement>();
    const mouseDelayDiv = React.createRef<HTMLDivElement>();
    const clickCount = React.createRef<HTMLDivElement>();
    const mouseButton = React.createRef<HTMLDivElement>();
    const coordinatesDivX = React.createRef<HTMLDivElement>();
    const coordinatesDivY = React.createRef<HTMLDivElement>();
    const keypresses = React.createRef<HTMLDivElement>();
    const altKey = React.createRef<HTMLDivElement>();
    const shiftKey = React.createRef<HTMLDivElement>();
    const ctrlKey = React.createRef<HTMLDivElement>();
    const metaKey = React.createRef<HTMLDivElement>();

    let mouseDelay: number;
    let mouseDownTime: number;
    let click_Count = 0;
    let countKeyPress = 0;

    function eventMouseDown(e: MouseEvent<HTMLButtonElement>) {
        mouseDownTime = new Date().getTime();
        mouseButton.current!.innerHTML = '';
        const mouseButtons = ['left', 'middle', 'right'];
        mouseButton.current!.innerHTML = mouseButtons[e.button];
        console.log(`Mouse button: ${mouseButtons[e.button]}, X: ${e.pageX}, Y: ${e.pageY}, Time: ${new Date()}`);
        altKey.current!.innerHTML = e.altKey.toString();
        shiftKey.current!.innerHTML = e.shiftKey.toString();
        ctrlKey.current!.innerHTML = e.ctrlKey.toString();
        metaKey.current!.innerHTML = e.metaKey.toString();
        coordinatesDivX.current!.innerHTML = e.pageX.toString();
        coordinatesDivY.current!.innerHTML = e.pageY.toString();
        if (e.altKey && e.shiftKey) {
            throw new EvalError('You are not allowed to use this site');
        }
    }

    function eventMouseUp() {
        const mouseupTime = new Date().getTime();
        mouseDelay = mouseupTime - mouseDownTime;
        click_Count += 1;
        console.error(`${click_Count.toString()}`);
        console.warn(`${mouseDelay.toString()}`);
        clickCount.current!.innerHTML = click_Count.toString();
        mouseDelayDiv.current!.innerHTML = mouseDelay.toString();
    }

    const handleSubmit = () => {
        setSubmit(true);
    };

    function usernameChange(event: ChangeEvent<HTMLInputElement>) {
        username.current = event.target.value;
        countKeyPress += 1;
        keypresses.current!.innerHTML = countKeyPress.toString();
    }

    function passwordChange(event: ChangeEvent<HTMLInputElement>) {
        password.current = event.target.value;
    }

    function Body() {
        if (submit) return <PostSubmit />;
        else return <PreSubmit />;
    }

    function networkPing() {
        fetch('/api/get/json')
            .then(() => {
                networkPinger.current!.innerText = 'Online';
            })
            .catch(() => {
                networkPinger.current!.innerText = 'no connection';
            });
    }

    React.useEffect(() => {
        const interval = setInterval(networkPing, 500);
        return () => clearInterval(interval);
    }, []);

    function PreSubmit() {
        document.title = 'Login Page';
        const tableStyle = {
            fontSize: 'small',
        };
        return (
            <>
                <h1 id="heading1">Login Page</h1>
                <p>Please input your user name and password and click the login button.</p>
                <form name="login_form" onSubmit={handleSubmit}>
                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    <label htmlFor="username_field">User Name:</label>
                                </td>
                                <td>
                                    <input id="username_field" size={30} type="text" onChange={usernameChange} />
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label htmlFor="password_field">Password:</label>
                                </td>
                                <td>
                                    <input id="password_field" size={30} type="password" onChange={passwordChange} />
                                </td>
                            </tr>
                            <tr>
                                <td></td>
                                <td>
                                    <input id="login_button" type="submit" value="LOGIN" />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </form>
                <textarea id="textarea51" defaultValue="Some initial text" />
                <button id="goes_hidden" onClick={goesInvisible}>
                    Visible
                </button>
                <button id="pops_up" onClick={popup}>
                    Pops up a window
                </button>
                <button id="delayed_request" onClick={delayedRequest}>
                    Fires a request in 200ms
                </button>
                <button id="delayed_request_big" onClick={delayedRequestBig}>
                    Fires a big request in 250ms
                </button>
                <button id="alerts" onClick={() => alert('Am an alert')}>
                    Pops up an alert
                </button>
                <div id="prompt_result" ref={promptResult} />
                <button id="prompts" onClick={() => testPrompt(promptResult)}>
                    Pops up a prompt
                </button>
                <div id="network_pinger" ref={networkPinger}>
                    Online
                </div>
                <button id="ManyClass" className="pure-button another something kala">
                    Doesn't do anything
                </button>
                <button className="pure-button">Doesn't do anything</button>
                <button className="pure-button">Doesn't do anything</button>
                <button className="pure-button">Doesn't do anything</button>
                <button className="pure-button">Doesn't do anything</button>
                <button id="clickWithOptions" onMouseDown={eventMouseDown} onMouseUp={eventMouseUp}>
                    Click with Options
                </button>
                <button style={{ width: '0px', height: '0px', padding: '0px', border: '0px' }} id="no-size"></button>
                <button hidden={true} id="hidden-btn">
                    hidden=true
                </button>
                <button id="hidden-visibility-btn" style={{ visibility: 'hidden' }}>
                    visibility hidden
                </button>
                <button id="hidden-display-btn" style={{ display: 'none' }}>
                    display none
                </button>
                <table style={tableStyle}>
                    <tbody>
                        <tr>
                            <td>
                                <label htmlFor="upload_result">Upload Result:</label>
                            </td>
                            <td>
                                <div id="upload_result" ref={uploadResult} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="mouse_delay_time">Mouse Delay:</label>
                            </td>
                            <td>
                                <div id="mouse_delay_time" ref={mouseDelayDiv} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="mouse_button">Mouse Button:</label>
                            </td>
                            <td>
                                <div id="mouse_button" ref={mouseButton} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="coordinatesX">Coordinates X:</label>
                            </td>
                            <td>
                                <div id="coordinatesX" ref={coordinatesDivX} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="coordinatesY">Coordinates Y:</label>
                            </td>
                            <td>
                                <div id="coordinatesY" ref={coordinatesDivY} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="click_count">Click Count:</label>
                            </td>
                            <td>
                                <div id="click_count" ref={clickCount} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="countKeyPress">Keypresses:</label>
                            </td>
                            <td>
                                <div id="countKeyPress" ref={keypresses} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="alt_key">Alt Key:</label>
                            </td>
                            <td>
                                <div id="alt_key" ref={altKey} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="ctrl_key">Ctrl Key:</label>
                            </td>
                            <td>
                                <div id="ctrl_key" ref={ctrlKey} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="shift_key">Shift Key:</label>
                            </td>
                            <td>
                                <div id="shift_key" ref={shiftKey} />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label htmlFor="meta_key">Meta Key:</label>
                            </td>
                            <td>
                                <div id="meta_key" ref={metaKey} />
                            </td>
                        </tr>
                    </tbody>
                </table>

                <input
                    type="file"
                    id="file_chooser"
                    name="file_chooser"
                    onChange={(event) => fileUploaded(uploadResult, event)}
                />
                <input
                    type="file"
                    id="multi_file_chooser"
                    name="multi_file_chooser"
                    multiple
                    onChange={(event) => fileUploaded(uploadResult, event)}
                />
                <a id="file_download" href="index.js" download="test_download_file">
                    Download file{' '}
                </a>

                <ProgressBar />

                {/* >>> Event Test Area (for Robot Framework Browser / Playwright event tracing) <<< */}
                <EventLogger />
            </>
        );
    }

    function PostSubmit() {
        if (username.current == 'demo' && password.current == 'mode') {
            document.title = 'Welcome Page';
            return (
                <>
                    <h1>Welcome Page</h1>
                    <p>
                        Login succeeded. Now you can <a href=".">logout</a>.
                    </p>
                </>
            );
        } else {
            document.title = 'Error Page';
            return (
                <>
                    <h1>Error Page</h1>
                    <p>Login failed. Invalid user name and/or password.</p>
                </>
            );
        }
    }

    return <Body />;
}
