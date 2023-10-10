
import React, { useState, createContext, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import configData from '../../config.json'

const AuthContext = createContext()

function AuthProviderWrapper (props) {
  // Store the variables we want to share
  const [user, setUser] = useState(null)
  const [expirationMessage, setExpirationMessage] = useState('')
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const navigate = useNavigate()

  // Functions to store and delete the token received by the backend in the browser
  const getStoredToken = () => {
    return localStorage.getItem('authToken')
  }

  const storeToken = token => {
    localStorage.setItem('authToken', token)
  }

  const refreshTokenFunction = token => {
    console.log(token)
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
    setIsLoggedIn(false)
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
    console.log(token)
    console.log(startTime)

    setCurrentTime(Date.now())

    const currentTime = localStorage.getItem('currentTime')
    console.log(currentTime)
    console.log('AUTHENTICATING')

    if (currentTime - startTime > expirationTime) {
      ///GET NEW REFRESH TOKEN

      if (currentTime - startTime > refreshTime) {
        setExpirationMessage(
          'Session expired due to inactivity. Please log in again'
        )
        console.log("asdasdhas")
      } else {
        setExpirationMessage('')
        console.log('HA PASADO EL EXPIRATION TIME')

        var details = {
          grant_type: 'refresh_token',
          client_id: 'beacon',
          client_secret: 'WGahOcaJcbQ2srhBsNH56NhhDxH5M51f',
          realm: 'Beacon',
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
        console.log(readableResponse)

        storeToken(readableResponse.access_token)
        refreshTokenFunction(readableResponse.refresh_token)

        setExpirationTime(readableResponse.expires_in)
        setExpirationTimeRefresh(readableResponse.refresh_expires_in)

        setStartTime(Date.now())
        const startTime = localStorage.getItem('startTime')
        console.log(startTime)
      }
    }
  }

  return (
    <AuthContext.Provider
      value={{
        setIsLoggedIn,
        isLoggedIn,
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
