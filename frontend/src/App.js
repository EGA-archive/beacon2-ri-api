import 'devextreme/dist/css/dx.light.css'

import './App.css'
import { Route, Routes } from 'react-router-dom'

import Individuals from './components/Individuals/Individuals'
import GenomicVariations from './components/GenomicVariations/GenomicVariations'
import Biosamples from './components/Biosamples/Biosamples'
import Runs from './components/Runs/Runs'
import Analyses from './components/Analyses/Analyses'
import Cohorts from './components/Cohorts/Cohorts'
import ErrorPage from './pages/ErrorPage'
import Navbar from './components/NavBar/Navbar'
import SignInForm from './components/SignIn/SignInForm'
import CrossQueries from './components/CrossQueries/CrossQueries'
import LoggedIn from './components/SignIn/LoggedIn'
import Validator from './components/Validator/Validator'
import SignInFormNoLS from './components/SignIn/SignInFormNoLS'
import AboutSection from './components/AboutSection/AboutSection'
import SignInOptions from './components/SignInOptions/SignInOptions'
import Footer from './components/Footer/Footer'
import BeaconInfo from './components/Dataset/BeaconInfo'

function App () {
  return (
    <div className='App'>
      <Navbar />
      <Routes>
        <Route path='/' element={<Individuals />} />
        <Route path='/individuals' element={<Individuals />} />
        <Route path='/genomicVariations' element={<GenomicVariations />} />
        <Route path='/biosamples' element={<Biosamples />} />
        <Route path='/runs' element={<Runs />} />
        <Route path='/analyses' element={<Analyses />} />
        <Route path='/cohorts' element={<Cohorts />} />
        <Route path='/beaconInfo' element={<BeaconInfo />} />
        <Route path='/sign-in' element={<SignInForm />} />
        <Route path='/sign-in-noLS' element={<SignInFormNoLS />} />
        <Route path='/sign-in-options' element={<SignInOptions />} />
        <Route path='/loggedOut' element={<LoggedIn />} />
        <Route path='/:scope/cross-queries/:id' element={<CrossQueries />} />
        <Route path='/validator' element={<Validator />} />
        <Route path='/about' element={<AboutSection />} />
        <Route path='*' element={<ErrorPage />} />
      </Routes>

    </div>
  )
}

export default App
