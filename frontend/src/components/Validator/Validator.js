import './Validator.css'
import { useState, useEffect } from 'react'
import axios from 'axios'
import configData from '../../config.json'

function Validator () {
  const [verifierUrl, setVerifierUrl] = useState('')
  const [response, setResponse] = useState([])
  const [showResults, setShowResults] = useState(false)
  const [errorsFound, setErrorsFound] = useState('')
  const [timeOut, setTimeout] = useState(true)
  const [error, setErrror] = useState('')
  const [stringDataToCopy, setStringDataToCopy] = useState('')

  const handleChangeVerifierUrl = e => {
    setVerifierUrl(e.target.value)
  }

  const copyData = e => {
    navigator.clipboard
      .writeText(stringDataToCopy)
      .then(() => {
        alert('successfully copied')
      })
      .catch(() => {
        alert('something went wrong')
      })
  }

  const submitVerifierUrl = async e => {
    setTimeout(false)
    setErrorsFound('')
    e.preventDefault()
    try {
      if (verifierUrl !== '') {
        let res = await axios.get(
          `https://beacon-network-backend-demo.ega-archive.org/beacon-network/v2.0.0/validate?endpoint=${verifierUrl}`
        )
        let stringData = ''
        res.data.forEach(element => {
          element = JSON.stringify(element, null, 2)
          stringData = stringData + element + '\n'
          stringData = stringData.replace('{', '')
          stringData = stringData.replace('}', '')
          stringData = stringData.replace(/[ '"]+/g, ' ')
        })

        setStringDataToCopy(stringData)

        let isProperty = res.data.some(object => 'code' in object)

        if (isProperty === false) {
          setErrorsFound(true)
        } else {
          setErrorsFound(false)
        }

        setResponse(res.data)

        if (res !== null && res !== undefined) {
          setShowResults(true)
          setTimeout(true)
        }
      } else {
        setErrror('An error occured. Please check the URL and retry.')
        setTimeout(true)
      }
    } catch (error) {
      setErrror('An error occured. Please check the URL and retry.')
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
        {timeOut === false && (
          <div className='loader2'>
            <div id='ld3'>
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
        )}
        {error !== '' && timeOut === true && <h2>{error}</h2>}
        {showResults === true && timeOut === true && error === '' && (
          <div className='copyDiv'>
            <button onClick={copyData}>
              {' '}
              <img className='copyLogo' src='../copy.png' alt='copyIcon'></img>
            </button>
          </div>
        )}

        {showResults === true &&
          timeOut === true &&
          error === '' &&
          response.map((element, index) => {
            return (
              <div className='messageContainer'>
                <div id='copydata'>
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
              </div>
            )
          })}

        {errorsFound === true && error === '' && (
          <h11>
            Congratulations! Validation has finished. No errors detected.
          </h11>
        )}
      </div>
    </div>
  )
}

export default Validator
