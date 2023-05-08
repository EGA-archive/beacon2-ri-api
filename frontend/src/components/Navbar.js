import { NavLink } from 'react-router-dom';

import React, { useState } from 'react';
import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';
import SignInForm from './SignInForm';
import './Navbar.css';


function Navbar() {

    const [selected, setIsSelected] = useState('')
    const [openModal1, setIsOpenModal1] = useState(false)

    const { isLoggedIn, setIsLoggedIn, logOutUser, authenticateUser, getStoredToken } = useContext(AuthContext);

    const handleHelpModal1 = () => {
        setIsOpenModal1(true)
    }
    const logOut = (e) => {

        logOutUser()
        setIsLoggedIn(false)
        console.log(isLoggedIn)
    }

    return (

        <nav className='nav2'>
            <a href="/">Home</a>
            <a href="/cross-queries">Cross queries</a>
            <a href="/members">Network members</a>
            {!isLoggedIn && <a href="/sign-up">Sign up</a>}
            {!isLoggedIn && <a href="/sign-in">Sign in</a>}
            {isLoggedIn && <a href="/sign-in">Log out</a>}
            <div class="animation start-home"></div>
        </nav>



    )
}


export default Navbar;