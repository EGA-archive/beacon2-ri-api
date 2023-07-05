import './SignUpForm.css'
import { NavLink } from 'react-router-dom';
import { Router } from 'react-router-dom';
import { Route, Routes } from 'react-router-dom';
import React, { Component, useState, useEffect } from 'react';
import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import LoggedIn from './LoggedIn';
import { AuthProvider, useAuth } from 'oidc-react';



export default function SignInForm() {

    const [userName, setUserName] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')

    const navigate = useNavigate();
    const { storeToken, setIsLoggedIn, isLoggedIn, refreshTokenFunction, authenticateUser, expirationMessage, setExpirationTime, setStartTime, setExpirationTimeRefresh } = useContext(AuthContext);

    const auth = useAuth();
    console.log(auth)

    
    const isAuthenticated = auth.userData?.id_token ? true : false;
    if(!isAuthenticated){
    auth.userManager?.signinRedirect();}

 
    

    

    



    return (
        <div className="App">
          <header className="App-header">
            <p>OIDC React</p>
            <LoggedIn />
          </header>
        </div>

    )

}

