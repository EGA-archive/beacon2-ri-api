import './SignUpForm.css'
import { NavLink } from 'react-router-dom';
import { Router } from 'react-router-dom';
import { Route, Routes } from 'react-router-dom';
import React, { Component, useState } from 'react';
import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';



export default function SignInForm(){

    const [userName, setUserName] =  useState('')
    const [password, setPassword] = useState('')
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
        e.preventDefault();
        console.log(userName)
        var details = {
            'grant_type': 'password',
            'client_id': 'beacon',
            'client_secret': 'b26ca0f9-1137-4bee-b453-ee51eefbe7ba',
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
        
        const response = await fetch('http://localhost:8080/auth/realms/Beacon/protocol/openid-connect/token', {
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
        
        if (readableResponse.access_token){
            navigate("/")
            setIsLoggedIn(true)
          
        
        } else{
            setError("User not found. Please check the username and the password and retry")
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
                        <NavLink
                           exact
                            to="/sign-up"
                            className={(element) => element.isActive ? 'formTitleLink' : 'formTitleLink-active'}
                        >
                            Sign Up
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
                                    onChange={e => { handleChange2(e) }}
                                />
                            </div>
                      
                            <div className="formField">

                                
                                    <button className="formFieldButton"> Sign In</button>
                            
                                <NavLink to="/sign-up" className="formFieldLink">
                                    Create an account
                                </NavLink>
                            </div>
                        </form>
                    {error !== '' && <h1>{error}</h1>}
                    </div>
                </div>
            </div>

        )
    
}

