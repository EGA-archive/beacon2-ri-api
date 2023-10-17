import { NavLink } from 'react-router-dom'

import React, { useState } from 'react'
import { AuthContext } from '../context/AuthContext'
import { useContext } from 'react'
import { useAuth } from 'oidc-react'
import './Navbar.css'

function Navbar () {
  const [selected, setIsSelected] = useState('')
  const [openModal1, setIsOpenModal1] = useState(false)

  const { isLoggedIn, setIsLoggedIn, logOutUser } = useContext(AuthContext)
  const auth = useAuth()

  const isAuthenticated = auth.userData?.id_token ? true : false
  if (isAuthenticated || isLoggedIn === true) {
    setIsLoggedIn(true)
  } else {
    setIsLoggedIn(false)
  }

  const handleHelpModal1 = () => {
    setIsOpenModal1(true)
  }

  const handleClik = () => {
    console.log('hejek')
    setIsLoggedIn(false)
    auth.signOut()
    logOutUser()
  }

  return (
    <div className='navB'>
      <nav className='nav2'>
        <NavLink
          exact
          to='/'
          className={({ isActive }) =>
            isActive ? 'Individuals2' : 'Individuals'
          }
        >
          Individuals
        </NavLink>
        <NavLink
          exact
          to='/biosamples'
          className={({ isActive }) =>
            isActive ? 'Biosamples2' : 'Biosamples'
          }
        >
          Biosamples
        </NavLink>
        <NavLink
          exact
          to='/genomicVariations'
          className={({ isActive }) => (isActive ? 'Variants2' : 'Variants')}
        >
          Variant
        </NavLink>
        <NavLink
          exact
          to='/runs'
          className={({ isActive }) => (isActive ? 'Runs2' : 'Runs')}
        >
          Runs
        </NavLink>
        <NavLink
          exact
          to='/analyses'
          className={({ isActive }) => (isActive ? 'Analyses2' : 'Analyses')}
        >
          Analyses
        </NavLink>
        <NavLink
          exact
          to='/cohorts'
          className={({ isActive }) => (isActive ? 'Cohorts2' : 'Cohorts')}
        >
          Cohorts
        </NavLink>
        <NavLink
          exact
          to='/cross-queries'
          className={({ isActive }) =>
            isActive ? 'Cross-queries2' : 'Cross-queries'
          }
        >
          Cross queries
        </NavLink>
        <div class='animation nav2'></div>
      </nav>
      <nav className='nav3'>
        {!isLoggedIn && (
          <NavLink
            to='/info'
            className={({ isActive }) => (isActive ? 'Members2' : 'Members')}
          >
            Beacon information
          </NavLink>
        )}
        {!isLoggedIn && (
          <NavLink
            exact
            to='/sign-in'
            className={({ isActive }) => (isActive ? 'Sign-in2' : 'Sign-in')}
          >
            {' '}
            <img
              className='ls-login-image'
              src='../ls-login.png'
              alt='ls-login-image'
            />
          </NavLink>
        )}
        {!isLoggedIn && (
          <NavLink
            exact
            to='/sign-in-noLS'
            className={({ isActive }) => (isActive ? 'Sign-in5' : 'Sign-in6')}
          >
            Log in
          </NavLink>
        )}

        {isLoggedIn && (
          <NavLink
            exact
            to='/info'
            className={({ isActive }) => (isActive ? 'Members4' : 'Members3')}
          >
            Beacon information
          </NavLink>
        )}

        {isLoggedIn && (
          <NavLink
            exact
            to='/individuals'
            className={({ isActive }) => (isActive ? 'Sign-in4' : 'Sign-in3')}
            onClick={handleClik}
          >
            <img
              className='ls-login-image2'
              src='../logout.png'
              alt='ls-login-image2'
            />
            Log out
          </NavLink>
        )}

        <div class='animation nav3'></div>
      </nav>
    </div>
  )
}

export default Navbar
