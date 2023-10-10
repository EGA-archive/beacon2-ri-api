import './SignInForm.css'
import { NavLink } from 'react-router-dom';
import React, { Component, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../NavBar/Navbar';

export default function SignInFormNoLS() {

    const [userName, setUserName] = useState('dummy_user')
    const [password, setPassword] = useState('dummy_pw')
    const [error, setError] = useState('')

    const navigate = useNavigate();
    const { storeToken, setIsLoggedIn, isLoggedIn, refreshTokenFunction, authenticateUser, expirationMessage, setExpirationTime, setStartTime, setExpirationTimeRefresh } = useContext(AuthContext);


    const handleChange1 = (e) => {
        console.log(e.target.value)
        
        setUserName(e.target.value)

    }

    const handleChange2 = (e) => {

        console.log(e.target.value)
        setPassword(e.target.value)
    }

    const handleSubmit = async (e) => {

        try {


            e.preventDefault();
            console.log(userName)
            var details = {
                'grant_type': 'password',
                'client_id': 'beacon',
                'client_secret': 'WGahOcaJcbQ2srhBsNH56NhhDxH5M51f',
                'username': userName,
                'password': password,
                'realm': 'Beacon',
                'scope': 'openid',
                'requested_token_type': 'urn:ietf:params:oauth:token-type:refresh_token'
            };


            var formBody = [];
            for (var property in details) {
                var encodedKey = encodeURIComponent(property);
                var encodedValue = encodeURIComponent(details[property]);
                formBody.push(encodedKey + "=" + encodedValue);
            }
            formBody = formBody.join("&");


            const response = await fetch('https://beacon-network-demo2.ega-archive.org/auth/realms/Beacon/protocol/openid-connect/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formBody
            })

            const readableResponse = await response.json()
            console.log(readableResponse.access_token)

            storeToken(readableResponse.access_token)
            refreshTokenFunction(readableResponse.refresh_token)


            setExpirationTime(readableResponse.expires_in)
            setExpirationTimeRefresh(readableResponse.refresh_expires_in)

            setStartTime(Date.now())
            //storeToken(response.data.authToken);
            authenticateUser();

            if (readableResponse.access_token) {
                navigate("/")
                setIsLoggedIn(true)
            } else {
                setError("User not found. Please check the username and the password and retry")
            }
        } catch (error) {
            setError("User not found")

        }
    }


    return (
        <div className="login">
            <div className="appAside" />
            <div className="appForm">
                {expirationMessage != '' && <h3>{expirationMessage}</h3>}
                <div className="pageSwitcher">
                    <NavLink

                        to="/sign-in"
                        className={(element) => element.isActive ? 'formTitleLink' : 'formTitleLink-active'}
                    >
                        Sign In
                    </NavLink>

                </div>

                <div className="formCenter">
                    <form onSubmit={handleSubmit} className="formFields">
                        <div className="formField">
                            <label className="formFieldLabel" htmlFor="userName">
                                Username
                            </label>
                            <input
                                type="text"
                                id="userName"
                                className="formFieldInput"
                                placeholder="Enter your username"
                                name="userName"
                                value="dummy_user"
                                onChange={e => { handleChange1(e) }}
                            />
                        </div>
                        <div className="formField">
                            <label className="formFieldLabel" htmlFor="password">
                                Password
                            </label>
                            <input
                                type="password"
                                id="password"
                                className="formFieldInput"
                                placeholder="Enter your password"
                                name="password"
                                value="dummy_pw"
                                onChange={e => { handleChange2(e) }}
                            />
                        </div>

                        <div className="formField">


                            <button className="formFieldButton"> Sign In</button>

                         
                        </div>
                    </form>
                    {error !== '' && <h1>{error}</h1>}
                </div>
            </div>
        </div>

    )

}

