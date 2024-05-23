import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import configData from './config.json'
import App from './App'
import reportWebVitals from './reportWebVitals'
import { BrowserRouter } from 'react-router-dom'
import { AuthProviderWrapper } from './components/context/AuthContext'
import { AuthProvider } from 'oidc-react'


const root = ReactDOM.createRoot(document.getElementById('root'))

const oidcConfig = {
  onSignIn: async user => {
    alert('You just signed in!')
    window.location.hash = ''
  },
  authority: 'https://login.elixir-czech.org/oidc',
  clientId: process.env.REACT_APP_CLIENT_ID,
  clientSecret: process.env.REACT_APP_CLIENT_SECRET,
  autoSignIn: false,
  responseType: 'code',
  automaticSilentRenew: true,
  redirectUri:
    process.env.NODE_ENV === 'development' && configData.REDIRECT_URL,
  scope: 'openid profile email ga4gh_passport_v1 offline_access',
  revokeAccessTokenOnSignout: true
}

root.render(
  <BrowserRouter>
    <AuthProvider {...oidcConfig}>
      <AuthProviderWrapper>
        <App />
      </AuthProviderWrapper>
    </AuthProvider>
  </BrowserRouter>
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()


