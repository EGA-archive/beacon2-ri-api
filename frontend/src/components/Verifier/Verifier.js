import './Verifier.css'
import { useState, useEffect } from 'react'
import axios from 'axios'

function Verifier () {
  const [verifierUrl, setVerifierUrl] = useState('')
  const [response, setResponse] = useState([])
  const [showResults, setShowResults] = useState(false)

  const handleChangeVerifierUrl = e => {
    setVerifierUrl(e.target.value)
  }

  const submitVerifierUrl = async e => {
    e.preventDefault()
    try {
      let res = await axios.get(
        `https://beacons.bsc.es/beacon-network/v2.0.0/validate?endpoint=${verifierUrl}`
      )
      console.log(res)
      setResponse(res.data)
      console.log(response)
      setShowResults(true)
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <div className='verifierContainer'>
      <h8>Please insert the URL of your Beacon</h8>
      <div>
        <input
          className='inputVerifierUrl'
          type='text'
          value={verifierUrl}
          onChange={handleChangeVerifierUrl}
          placeholder={'https://beacons.bsc.es/beacon/v2.0.0'}
        ></input>
        <button className='submitButton' onClick={submitVerifierUrl}>
          SUBMIT
        </button>
      </div>
      <div className='resultsContainerVerifier'>
        {showResults === true &&
          response.map(element => {
            return (
              <div className='messageContainer'>
                {element.code === undefined && <h1>{element.message}</h1>}
                {element.code && (
                  <div className='errorContainer'>
                    <h10>ERROR!</h10>
                    <div className='errorMessage'>
                      <h9>Code:</h9>
                      <h1>{element.code}</h1>
                      <h9>Location:</h9>
                      <h1>{element.location}</h1>
                      <h9>Message:</h9>
                      <h1>{element.message}</h1>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
      </div>
    </div>
  )
}

export default Verifier
