import React, { ChangeEvent, useState, useRef } from 'react';

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
        <div id="progress" style={{ width: '30%', height: '30px', backgroundColor: 'gray' }}>
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

export default function Site() {
    const username = useRef('');
    const password = useRef('');

    const [submit, setSubmit] = useState(false);

    const handleSubmit = () => {
        setSubmit(true);
    };

    function usernameChange(event: ChangeEvent<HTMLInputElement>) {
        username.current = event.target.value;
    }

    function passwordChange(event: ChangeEvent<HTMLInputElement>) {
        password.current = event.target.value;
    }

    function Body() {
        if (submit) return <PostSubmit />;
        else return <PreSubmit />;
    }

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
                <ProgressBar />
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
