import { NavLink } from 'react-router-dom'
import React, { useState, useEffect } from 'react'
import { AuthContext } from '../context/AuthContext'
import { useContext } from 'react'
import { useAuth } from 'oidc-react'
import OutsideClickHandler from 'react-outside-click-handler'
import './Navbar.css'
import { useNavigate } from 'react-router-dom'
import LoggedIn from '../SignIn/LoggedIn'
import axios from 'axios'

import configData from '../../config.json'

function Navbar () {
  const [selected, setIsSelected] = useState('')
  const [openModal1, setIsOpenModal1] = useState(false)
  const [openMenu, setOpenMenu] = useState(false)
  const {
    isLoggedIn,
    setIsLoggedIn,
    logOutUser,
    authenticateUser,
    getStoredToken,
    userNameToShare,
    setUserNameToShare
  } = useContext(AuthContext)

  const [isNetwork, setIsNetwork] = useState(false)
  const auth = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    let user = localStorage.getItem('userName')
    if (user !== '') {
      setUserNameToShare(user)
    }
    authenticateUser()
    let token = getStoredToken()
    let isAuthenticated = false
    if (token === null) {
      isAuthenticated = auth.userData?.id_token ? true : false
    } else {
      isAuthenticated = true
    }

    if (isAuthenticated || isLoggedIn === true) {
      setIsLoggedIn(true)
    } else {
      setIsLoggedIn(false)
    }
  }, [userNameToShare])

  useEffect(() => {
    const apiCall = async () => {
      try {
        let res2 = await axios.get(configData.API_URL + '/info')

        if (res2.data.meta.isAggregated) {
          setIsNetwork(true)
        }
      } catch (error) {
       
      }
    }

    apiCall()
  }, [])

  const handleHelpModal1 = () => {
    setIsOpenModal1(true)
  }

  const handleMenu = () => {
    setOpenMenu(!openMenu)
  }

  const handleClick = () => {
    setIsLoggedIn(false)
    auth.signOut()
    logOutUser()
    handleMenu()
  }

  return (
    <div className='navB'>
      <LoggedIn />
      <nav className='nav2'>
        {/* <NavLink
          exact
          to='/'
          className={({ isActive }) =>
            isActive ? 'Individuals2' : 'Individuals'
          }
        >
          Individuals
        </NavLink> */}
        {/* <NavLink
          exact
          to='/biosamples'
          className={({ isActive }) =>
            isActive ? 'Biosamples2' : 'Biosamples'
          }
        >
          Biosamples
        </NavLink> */}
        {/* <NavLink
          exact
          to='/genomicVariations'
          className={({ isActive }) => (isActive ? 'Variants2' : 'Variants')}
        >
          Variant
        </NavLink> */}
        {/* <NavLink
          exact
          to='/runs'
          className={({ isActive }) => (isActive ? 'Runs2' : 'Runs')}
        >
          Runs
        </NavLink> */}
        {/* <NavLink
          exact
          to='/analyses'
          className={({ isActive }) => (isActive ? 'Analyses2' : 'Analyses')}
        >
          Analyses
        </NavLink> */}
        {/* <NavLink
          exact
          to='/cohorts'
          className={({ isActive }) => (isActive ? 'Cohorts2' : 'Cohorts')}
        >
          Cohorts
        </NavLink> */}

        <div class='animation nav2'></div>
      </nav>
      <nav className='nav3'>
        {!isLoggedIn && (
          <NavLink
            to='/'
            className={({ isActive }) => (isActive ? 'Home2' : 'Home')}
          >
            <ion-icon name='home-outline'></ion-icon>
          </NavLink>
        )}

        {!isLoggedIn && !isNetwork && (
          <NavLink
            to='/beaconInfo'
            className={({ isActive }) => (isActive ? 'Members2' : 'Members')}
          >
            Beacon Info
          </NavLink>
        )}
        {!isLoggedIn && isNetwork && (
          <NavLink
            to='/beaconInfo'
            className={({ isActive }) => (isActive ? 'Members2' : 'Members')}
          >
            Network members
          </NavLink>
        )}

        {!isLoggedIn && (
          <NavLink
            exact
            to='/sign-in-options'
            className={({ isActive }) => (isActive ? 'Sign-in5' : 'Sign-in6')}
          >
            Log in
          </NavLink>
        )}
        {isLoggedIn && (
          <NavLink
            to='/'
            className={({ isActive }) => (isActive ? 'Home5' : 'Home6')}
          >
            <ion-icon name='home-outline'></ion-icon>
          </NavLink>
        )}

        {isLoggedIn && !isNetwork && (
          <NavLink
            exact
            to='/beaconInfo'
            className={({ isActive }) => (isActive ? 'Members4' : 'Members3')}
          >
            Beacon Info
          </NavLink>
        )}

        {isLoggedIn && isNetwork && (
          <NavLink
            exact
            to='/beaconInfo'
            className={({ isActive }) => (isActive ? 'Members4' : 'Members3')}
          >
            Network Members
          </NavLink>
        )}

        {isLoggedIn && (
          <div className='containerUserName'>
            <NavLink
              exact
              to='/'
              className={({ isActive }) => (isActive ? 'Sign-in3' : 'Sign-in3')}
              onClick={handleClick}
            >
              <img
                className='ls-login-image2'
                src='/../logout.png'
                alt='ls-login-image2'
              />
              Log out
            </NavLink>
            <h5>{userNameToShare}</h5>
          </div>
        )}

        <div class='animation nav3'></div>
      </nav>
      <div className='nav4Container'>
        <nav className='nav4'>
          <button className='buttonMenu' onClick={handleMenu}>
            <img className='menuLogo' src='/../menu.png' alt='menuIcon'></img>
            <img
              className='menuLogoHover'
              src='/../menu2.png'
              alt='menuIconHover'
            ></img>
          </button>

          {openMenu && (
            <div className='divOutsideClickHandle'>
              <OutsideClickHandler
                onOutsideClick={() => {
                  handleMenu()
                }}
              >
                <div className='menuContainer'>
                  <div class='icon'>
                    <img
                      className='arrowUpIcon'
                      src='/../arrow-up2.png'
                      alt='arrowUp2'
                    ></img>
                  </div>
                  <div className='menuNav'>
                    {
                      <NavLink
                        exact
                        to='/'
                        onClick={handleMenu}
                        className='Home3'
                      >
                        <ion-icon name='home-outline'></ion-icon>
                      </NavLink>
                    }
                    {!isNetwork && (
                      <NavLink
                        to='/beaconInfo'
                        onClick={handleMenu}
                        className={({ isActive }) =>
                          isActive ? 'Members2' : 'Members'
                        }
                      >
                        {' '}
                        <h1 className='h1Menu'>Beacon Info</h1>
                      </NavLink>
                    )}
                    {isNetwork && (
                      <NavLink
                        to='/beaconInfo'
                        onClick={handleMenu}
                        className={({ isActive }) =>
                          isActive ? 'Members2' : 'Members'
                        }
                      >
                        {' '}
                        <h1 className='h1Menu'>Network members</h1>
                      </NavLink>
                    )}

                    {!isLoggedIn && (
                      <NavLink
                        exact
                        to='/sign-in-options'
                        onClick={handleMenu}
                        className={({ isActive }) =>
                          isActive ? 'Sign-in5' : 'Sign-in6'
                        }
                      >
                        <h1 className='h1Menu'>Log in</h1>
                      </NavLink>
                    )}

                    {isLoggedIn && (
                      <>
                        <NavLink
                          exact
                          to='/'
                          className={({ isActive }) =>
                            isActive ? 'Sign-in4' : 'Sign-in3'
                          }
                          onClick={handleClick}
                        >
                          <img
                            className='ls-login-image2'
                            src='/../logout.png'
                            alt='ls-login-image2'
                          />
                          <h1 className='h1Menu'>Log out</h1>
                        </NavLink>
                        <h5 className='userNameOpenMenu'>{userNameToShare}</h5>
                      </>
                    )}
                  </div>

                  <div className='menuNav2'>
                    {/* <NavLink
                      exact
                      to='/'
                      onClick={handleMenu}
                      className={({ isActive }) =>
                        isActive ? 'Individuals2' : 'Individuals'
                      }
                    >
                      <h1>Individuals</h1>
                    </NavLink> */}
                    {/* <NavLink
                      exact
                      to='/biosamples'
                      onClick={handleMenu}
                      className={({ isActive }) =>
                        isActive ? 'Biosamples2' : 'Biosamples'
                      }
                    >
                      <h1>Biosamples</h1>
                    </NavLink> */}
                    {/* <NavLink
                      exact
                      to='/genomicVariations'
                      onClick={handleMenu}
                      className={({ isActive }) =>
                        isActive ? 'Variants2' : 'Variants'
                      }
                    >
                      <h1>Variant</h1>
                    </NavLink> */}
                    {/* <NavLink
                      exact
                      to='/runs'
                      onClick={handleMenu}
                      className={({ isActive }) =>
                        isActive ? 'Runs2' : 'Runs'
                      }
                    >
                      <h1>Runs</h1>
                    </NavLink> */}
                    {/* <NavLink
                      exact
                      to='/analyses'
                      onClick={handleMenu}
                      className={({ isActive }) =>
                        isActive ? 'Analyses2' : 'Analyses'
                      }
                    >
                      <h1>Analyses</h1>
                    </NavLink> */}
                    {/* <NavLink
                      exact
                      to='/cohorts'
                      onClick={handleMenu}
                      className={({ isActive }) =>
                        isActive ? 'Cohorts2' : 'Cohorts'
                      }
                    >
                      <h1>Cohorts</h1>
                    </NavLink> */}
                    (
                    <NavLink
                      exact
                      to='/'
                      onClick={handleMenu}
                      className='Home3'
                    >
                      <ion-icon name='home-outline'></ion-icon>
                    </NavLink>
                    )
                    {!isNetwork && (
                      <NavLink
                        to='/beaconInfo'
                        onClick={handleMenu}
                        className={({ isActive }) =>
                          isActive ? 'Members2' : 'Members'
                        }
                      >
                        {' '}
                        <h1 className='h1Menu'>Beacon Info</h1>
                      </NavLink>
                    )}
                    {isNetwork && (
                      <NavLink
                        to='/beaconInfo'
                        onClick={handleMenu}
                        className={({ isActive }) =>
                          isActive ? 'Members2' : 'Members'
                        }
                      >
                        {' '}
                        <h1 className='h1Menu'>Network members</h1>
                      </NavLink>
                    )}
                    {!isLoggedIn && (
                      <NavLink
                        exact
                        to='/sign-in-options'
                        onClick={handleMenu}
                        className={({ isActive }) =>
                          isActive ? 'Sign-in5' : 'Sign-in6'
                        }
                      >
                        <h1 className='h1Menu'>Log in</h1>
                      </NavLink>
                    )}
                    {isLoggedIn && (
                      <>
                        <NavLink
                          exact
                          to='/'
                          className={({ isActive }) =>
                            isActive ? 'Sign-in4' : 'Sign-in3'
                          }
                          onClick={handleClick}
                        >
                          <img
                            className='ls-login-image2'
                            src='/../logout.png'
                            alt='ls-login-image2'
                          />
                          <h1 className='h1Menu'>Log out</h1>
                        </NavLink>

                        <h5 className='userNameSmallScreen'>
                          {userNameToShare}
                        </h5>
                      </>
                    )}
                  </div>
                </div>
              </OutsideClickHandler>
            </div>
          )}
        </nav>
        {isLoggedIn && !openMenu && (
          <h5 className='userName'>{userNameToShare}</h5>
        )}
      </div>
    </div>
  )
}

export default Navbar
