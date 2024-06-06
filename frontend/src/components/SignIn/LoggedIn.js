import React from 'react'
import { useAuth } from 'oidc-react'
import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

const LoggedIn = () => {
  const auth = useAuth()
  const { isLoggedIn, setIsLoggedIn, logOutUser, setUserNameToShare } =
    useContext(AuthContext)

  if (auth && auth.userData) {
    setIsLoggedIn(true)

    setUserNameToShare(
      localStorage.setItem('userName', auth.userData.profile.name)
    )

    return (
      <div>
        <strong>Logged in! 🎉</strong>
        <br />
      </div>
    )
  }
  return (
    <div>Not logged in! Try to refresh to be redirected to LifeScience.</div>
  )
}

export default LoggedIn
