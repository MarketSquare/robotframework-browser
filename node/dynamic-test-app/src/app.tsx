import { DraggableData, DraggableEvent } from 'react-draggable';
import Draggable from 'react-draggable';
import React, { ChangeEvent, FocusEvent, useRef, useState } from 'react';

function goesInvisible(event: React.MouseEvent<HTMLButtonElement>) {
    event.persist();
    console.log('Going hidden in 1 second');
    setTimeout(() => {
        //@ts-expect-error TypeScript can't infer that the element has style
        event.target.style.visibility = 'hidden';
        console.log('Went hidden');
    }, 500);
}

function popup(event: React.MouseEvent<HTMLButtonElement>) {
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
                top: '400px',
                left: '0px',
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

function fileUploaded(uploadResultElement: React.RefObject<HTMLElement>, event: ChangeEvent<HTMLInputElement>) {
    const files = event.target.files;
    if (files && files[0].name === 'test_upload_file') {
        uploadResultElement.current!.innerHTML = 'test_upload_file';
    } else {
        uploadResultElement.current!.innerHTML = 'wrong_upload_filename';
    }
}

function testPrompt(promptResultElement: React.RefObject<HTMLElement>) {
    const input = prompt('Enter a value');
    if (input) promptResultElement.current!.innerHTML = input;
    else promptResultElement.current!.innerHTML = 'prompt_not_filled';
}

function DraggableDiv() {
    const onControlledDrag = (e: DraggableEvent, position: DraggableData) => {
        const { x, y } = position;
        setControlledPosition({ x, y });
    };
    const [controlledPosition, setControlledPosition] = useState({ x: 0, y: 0 });
    return (
        <Draggable position={controlledPosition} onDrag={onControlledDrag}>
            <div className="box" id="draggable">
                My position can be changed programmatically. <br />I have a drag handler to sync state.
                <div>
                    x<div id="dragX">{controlledPosition.x}</div>
                </div>
                <div>
                    y<div id="dragY">{controlledPosition.y}</div>
                </div>
            </div>
        </Draggable>
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

    let mouseDelay: number;
    let mouseDownTime: number;
    let click_Count = 0;
    let countKeyPress = 0;

    function eventMouseDown(e: any) {
        mouseDownTime = new Date().getTime();
        mouseButton.current!.innerHTML = '';
        if (e.button == 0) mouseButton.current!.innerHTML = 'left';
        if (e.button == 1) mouseButton.current!.innerHTML = 'middle';
        if (e.button == 2) mouseButton.current!.innerHTML = 'right';
        coordinatesDivX.current!.innerHTML = e.pageX.toString();
        coordinatesDivY.current!.innerHTML = e.pageY.toString();
    }

    function eventMouseUp() {
        const mouseupTime = new Date().getTime();
        mouseDelay = mouseupTime - mouseDownTime;
        click_Count += 1;
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
        return (
            <>
                <h1>Login Page</h1>
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
                <button id="goes_hidden" onClick={goesInvisible}>
                    Visible
                </button>
                <button id="pops_up" onClick={popup}>
                    Pops up a window
                </button>
                <button id="delayed_request" onClick={delayedRequest}>
                    Fires a request in 200ms
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
                <button className="pure-button">Doesn't do anything</button>
                <button className="pure-button">Doesn't do anything</button>
                <button className="pure-button">Doesn't do anything</button>
                <button className="pure-button">Doesn't do anything</button>
                <button className="pure-button">Doesn't do anything</button>
                <button id="clickWithOptions" onMouseDown={eventMouseDown} onMouseUp={eventMouseUp}>
                    Click with Options
                </button>
                <div id="upload_result" ref={uploadResult}></div>
                <div id="mouse_delay_time" ref={mouseDelayDiv}></div>
                <div id="click_count" ref={clickCount}></div>
                <div id="mouse_button" ref={mouseButton}></div>
                <div id="coordinatesX" ref={coordinatesDivX}></div>
                <div id="coordinatesY" ref={coordinatesDivY}></div>
                <div id="countKeyPress" ref={keypresses}></div>

                <input
                    type="file"
                    id="file_chooser"
                    name="file_chooser"
                    onChange={(event) => fileUploaded(uploadResult, event)}
                />
                <a id="file_download" href="index.js" download="test_download_file">
                    Download file{' '}
                </a>
                <ProgressBar />
                <DraggableDiv />
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
