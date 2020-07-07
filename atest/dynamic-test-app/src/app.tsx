import React, { ChangeEvent, useState, useRef } from "react";

function goesInvisible(event: React.MouseEvent<HTMLButtonElement>) {
    event.persist()
    console.log("Going hidden in 1 second")
    setTimeout(() => {
        //@ts-expect-error
        event.target.style.visibility = "hidden";
        console.log("Went hidden")
    }, 500)
}

export default function Site() {
    const username = useRef("");
    const password  = useRef("");
    const [submit, setSubmit] = useState(false)

    const handleSubmit = () => {
        setSubmit(true)
    }

    function usernameChange(event: ChangeEvent<HTMLInputElement>) {
        username.current = event.target.value
    }
    function passwordChange(event: ChangeEvent<HTMLInputElement>) {
        password.current = event.target.value
    }

    function Body() {
        if(submit) return <PostSubmit/>
        else return <PreSubmit />
    }

    function PreSubmit() {
        document.title = "Login Page"
        return <>
        <h1>Login Page</h1>
        <p>Please input your user name and password and click the login button.</p>
            <form name="login_form" onSubmit={handleSubmit} >
                <table>
                    <tbody>
                        <tr>
                            <td><label htmlFor="username_field">User Name:</label></td>
                            <td><input id="username_field" size={30} type="text" onChange={usernameChange} /></td>
                        </tr>
                        <tr>
                            <td><label htmlFor="password_field">Password:</label></td>
                            <td><input id="password_field" size={30} type="password" onChange={passwordChange} /></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td><input id="login_button" type="submit" value="LOGIN" /></td>
                        </tr>
                    </tbody>
                </table>
            </form>
            <button id="goes_hidden" onClick={event => goesInvisible(event)} >Visible</button>
    </>
    }

    function PostSubmit() {
        if (username.current == "demo" && password.current == "mode") {
            document.title = "Welcome Page"
            return (<>
                <h1>Welcome Page</h1>
                <p>Login succeeded. Now you can <a href=".">logout</a>.</p>
            </>)
        } else {
            document.title = "Error Page"
            return (<>    
                <h1>Error Page</h1>
                <p>Login failed. Invalid user name and/or password.</p>
            </>) 
        }
    }

    return <Body />
}
