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
        <div className="navB">
            <nav className='nav2'>
                <a href="/" className='Individuals'>Individuals</a>
                <a href="/biosamples" className='Biosamples'>Biosamples</a>
                <a href="/genomicVariations" className='Variants'>Variants</a>
                <a href="/runs" className='Runs'>Runs</a>
                <a href="/analyses" className='Analyses'>Analyses</a>
                <a href="/cohorts" className='Cohorts'>Cohorts</a>
                <a href="/cross-queries" className='Cross-queries'>Cross queries</a>
                <div class="animation nav2"></div>
            </nav>
            <nav className='nav3'>
                <a href="/members" className='Members'>Network members</a>
                {!isLoggedIn && <a href="/sign-in" className='Sign-in'>Sign in</a>}
                {isLoggedIn && <a href="/sign-in" className='Sign-in'>Log out</a>}
                <div class="animation nav3"></div>
            </nav>

        </div>


    )
}


export default Navbar;