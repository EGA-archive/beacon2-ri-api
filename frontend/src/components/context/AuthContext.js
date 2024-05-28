import React, { useState, createContext, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import configData from '../../config.json'
import { useAuth } from 'oidc-react';

const AuthContext = createContext()

function AuthProviderWrapper (props) {
  // Store the variables we want to share
  const [user, setUser] = useState(null)
  const [userNameToShare, setUserNameToShare] = useState('')
  const [expirationMessage, setExpirationMessage] = useState('')
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const navigate = useNavigate()
  const auth = useAuth();
  // Functions to store and delete the token received by the backend in the browser
  const getStoredToken = () => {
    return localStorage.getItem('authToken')
  }

  const storeToken = token => {
    localStorage.setItem('authToken', token)
  }

  const refreshTokenFunction = token => {
    localStorage.setItem('refreshToken', token)
  }

  const removeToken = () => {
    localStorage.removeItem('authToken')
  }

  const setExpirationTime = time => {
    localStorage.setItem('expirationTime', time * 1000)
  }

  const setExpirationTimeRefresh = time => {
    localStorage.setItem('refreshExpirationTime', time * 1000)
  }

  const setStartTime = time => {
    localStorage.setItem('startTime', time)
  }

  const setCurrentTime = time => {
    localStorage.setItem('currentTime', time)
  }

  const logOutUser = () => {
    removeToken()
    auth = null
    setIsLoggedIn(false)
    setExpirationMessage('')
    navigate('/')
  }

  // Function to check if the user is already authenticated or not
  const authenticateUser = async () => {
    const storedToken = localStorage.getItem('authToken')

    if (storedToken !== 'undefined' && storedToken !== null) {
      setIsLoggedIn(true)
    }
    const refreshToken = localStorage.getItem('refreshToken')
    const expirationTime = localStorage.getItem('expirationTime')
    const refreshTime = localStorage.getItem('refreshExpirationTime')

    const startTime = localStorage.getItem('startTime')
    const token = localStorage.getItem('authToken')
    setCurrentTime(Date.now())

    const currentTime = localStorage.getItem('currentTime')

    console.log('AUTHENTICATING')

    if (currentTime - startTime > expirationTime) {
      ///GET NEW REFRESH TOKEN

      if (currentTime - startTime > refreshTime) {
        setExpirationMessage(
          'Session expired due to inactivity. Please log in again'
        )
        removeToken()
      } else {
        setExpirationMessage('')
        var details = {
          grant_type: 'refresh_token',
          client_id: process.env.REACT_APP_KEYCLOAK_CLIENT_ID,
          client_secret: process.env.REACT_APP_KEYCLOAK_CLIENT_SECRET,
          realm: process.env.REACT_APP_KEYCLOAK_CLIENT_REALM,
          scope: 'openid',
          requested_token_type:
            'urn:ietf:params:oauth:token-type:refresh_token',
          refresh_token: `${refreshToken}`
        }
       
        var formBody = []
        for (var property in details) {
          var encodedKey = encodeURIComponent(property)
          var encodedValue = encodeURIComponent(details[property])
          formBody.push(encodedKey + '=' + encodedValue)
        }
        formBody = formBody.join('&')

        const response = await fetch(
          configData.KEYCLOAK_URL +
            '/auth/realms/Beacon/protocol/openid-connect/token',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formBody
          }
        )
        const readableResponse = await response.json()

        storeToken(readableResponse.access_token)
        refreshTokenFunction(readableResponse.refresh_token)

        setExpirationTime(readableResponse.expires_in)
        setExpirationTimeRefresh(readableResponse.refresh_expires_in)

        setStartTime(Date.now())
        const startTime = localStorage.getItem('startTime')
       
      }
    }
  }

  return (
    <AuthContext.Provider
      value={{
        setIsLoggedIn,
        isLoggedIn,
        userNameToShare,
        setUserNameToShare,
        getStoredToken,
        setExpirationTime,
        expirationMessage,
        setExpirationTimeRefresh,
        storeToken,
        refreshTokenFunction,
        authenticateUser,
        setStartTime,
        setCurrentTime,
        logOutUser
      }}
    >
      {props.children}
    </AuthContext.Provider>
  )
}

export { AuthProviderWrapper, AuthContext }
