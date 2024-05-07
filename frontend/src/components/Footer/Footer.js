import './Footer.css'
import { NavLink } from 'react-router-dom'
import { useEffect } from 'react'
import { AuthContext } from '../context/AuthContext'
import { useContext } from 'react'
import { useAuth } from 'oidc-react'

function Footer (props) {
  const {
    isLoggedIn,
    setIsLoggedIn,
    logOutUser,
    authenticateUser,
    getStoredToken,
    userNameToShare,
    setUserNameToShare
  } = useContext(AuthContext)

  const handleClick = () => {
    setIsLoggedIn(false)
    auth.signOut()
    logOutUser()
  }
  const auth = useAuth()

  useEffect(() => {
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
  }, [])

  return (
    <div className='footerContainer'>
      <footer className='footer'>
        <ul className='social-icon'>
          <li className='social-icon__item'>
            <NavLink exact to='/about' className='social-icon__link'>
              <ion-icon name='information-circle-outline'></ion-icon>
            </NavLink>
            <NavLink
              exact
              to='/about'
              className={({ isActive }) =>
                isActive ? 'menu__linkActive' : 'menu__link'
              }
            >
              About
            </NavLink>
          </li>
          <li className='social-icon__item'>
            <NavLink exact to='/validator' className='social-icon__link'>
              <ion-icon name='checkmark-circle-outline'></ion-icon>
            </NavLink>
            <NavLink
              exact
              to='/validator'
              className={({ isActive }) =>
                isActive ? 'menu__linkActive' : 'menu__link'
              }
            >
              Beacon validator
            </NavLink>
          </li>
          {/* <li className='social-icon__item'>
            <a
              className='social-icon__link'
              href='https://github.com/elixir-europe/beacon-network-ui/'
              target='_blank'
              rel='noreferrer'
            >
              <ion-icon name='logo-github'></ion-icon>
            </a>
            <a
              className='menu__link'
              href='https://github.com/elixir-europe/beacon-network-ui/'
              target='_blank'
              rel='noreferrer'
            >
              GitHub
            </a>
          </li> */}
          {/* <li className='social-icon__item'>
            <a
              className='social-icon__link'
              href='https://docs.genomebeacons.org/'
              target='_blank'
              rel='noreferrer'
            >
              <ion-icon name='document-text-outline'></ion-icon>
            </a>
            <a
              className='menu__link'
              href='https://docs.genomebeacons.org/'
              target='_blank'
              rel='noreferrer'
            >
              Documentation
            </a>
          </li> */}
          {/* <li className='social-icon__item'>
            <NavLink exact to='/members' className='social-icon__link'>
              <ion-icon name='globe-outline'></ion-icon>
            </NavLink>
            <NavLink
              exact
              to='/members'
              className={({ isActive }) =>
                isActive ? 'menu__linkActive' : 'menu__link'
              }
            >
              Network members
            </NavLink>
          </li> */}
          {isLoggedIn === false && (
            <li className='social-icon__item'>
              <NavLink
                exact
                to='/sign-in-options'
                className='social-icon__link'
              >
                <ion-icon name='log-in-outline'></ion-icon>
              </NavLink>
              <NavLink
                exact
                to='/sign-in-options'
                className={({ isActive }) =>
                  isActive ? 'menu__linkActive' : 'menu__link'
                }
              >
                Log in
              </NavLink>
            </li>
          )}
          {isLoggedIn === true && (
            <li className='social-icon__item'>
              <NavLink
                exact
                to='/sign-in-options'
                className='social-icon__link'
              >
                <ion-icon name='log-out-outline' ></ion-icon>
              </NavLink>
              <NavLink
                exact
                to='/'
                className={({ isActive }) =>
                  isActive ? 'menu__link' : 'menu__link'
                }
                onClick={handleClick}
              >
                Log out
              </NavLink>
            </li>
          )}
        </ul>
      </footer>
    </div>
  )
}
export default Footer
