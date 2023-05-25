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
                <NavLink exact
                    to="/"
                    className={({ isActive }) => (isActive ? 'Individuals2' : 'Individuals')}
                >Individuals</NavLink>
                <NavLink exact
                    to="/biosamples"
                    className={({ isActive }) => (isActive ? 'Biosamples2' : 'Biosamples')}
                >Biosamples</NavLink>
                <NavLink exact
                    to="/genomicVariations"
                    className={({ isActive }) => (isActive ? 'Variants2' : 'Variants')}
                >Variant</NavLink>
                <NavLink exact
                    to="/runs"
                    className={({ isActive }) => (isActive ? 'Runs2' : 'Runs')}
                >Runs</NavLink>
                <NavLink exact
                    to="/analyses"
                    className={({ isActive }) => (isActive ? 'Analyses2' : 'Analyses')}
                >Analyses</NavLink>
                <NavLink exact
                    to="/cohorts"
                    className={({ isActive }) => (isActive ? 'Cohorts2' : 'Cohorts')}
                >Cohorts</NavLink>
                <NavLink exact
                    to="/cross-queries"
                    className={({ isActive }) => (isActive ? 'Cross-queries2' : 'Cross-queries')}
                >Cross queries</NavLink>
                <div class="animation nav2"></div>
            </nav>
            <nav className='nav3'>
                <NavLink 
                    to={{pathname:"/members",
                    state: {title:'from home page'}  
                    }}
                    className={({ isActive }) => (isActive ? 'Members2' : 'Members')}
                >Network members</NavLink>
                {!isLoggedIn &&
                    <NavLink exact
                        to="/sign-in"
                        className={({ isActive }) => (isActive ? 'Sign-in2' : 'Sign-in')}
                    >Sign in</NavLink>}
                {isLoggedIn &&
                    <NavLink exact
                        to="/sign-in"
                        className={({ isActive }) => (isActive ? 'Sign-in2' : 'Sign-in')}
                    onClick={logOut}>Log out</NavLink>}

                <div class="animation nav3"></div>
            </nav>

        </div>


    )
}


export default Navbar;