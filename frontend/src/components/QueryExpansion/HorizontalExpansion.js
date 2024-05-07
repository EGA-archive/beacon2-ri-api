import '../../App.css'
import './HorizontalExpansion.css'

import React, { useState, useEffect } from 'react'

import axios from 'axios'

function HorizontalExpansion (props) {
  const [error, setError] = useState(null)

  const [timeOut, setTimeOut] = useState(true)

  const [showQEresults, setShowQEresults] = useState(false)
  const [showQEfirstResults, setShowQEfirstResults] = useState(false)
  const [qeValue, setQEvalue] = useState('')
  const [ontologyValue, setOntologyValue] = useState('')
  const [resultsQEexact, setResultsQEexact] = useState([])

  const [matchesQE, setMatchesQE] = useState([])

  const handleQEchanges = e => {
    setQEvalue(e.target.value.trim())
  }

  const handleOntologyChanges = e => {
    setOntologyValue(e.target.value.trim())
  }
  const handleNewQEsearch = () => {
    setShowQEresults(false)
  }
  const handleSubmitQE = async e => {
    setTimeOut(false)
    try {
      if (ontologyValue !== '' && qeValue !== '') {
        resultsQEexact.splice(0, resultsQEexact.length)
        setError(null)
        const res = await axios.get(
          `https://cineca-query-expansion.text-analytics.ch/catalogue_explorer/HorizontalExpansionOls/?keywords=${qeValue}&ontology=${ontologyValue.toLowerCase()}`
        )
        setTimeOut(true)
        
        let arrayResults = []
        if (res.data.response.ols[qeValue] !== undefined) {
          arrayResults = res.data.response.ols[qeValue].search_term_expansion
        } else {
          arrayResults =
            res.data.response.ols[qeValue.toLowerCase()].search_term_expansion
        }
        if (arrayResults.length < 1) {
          setError(
            'Not found. Please check the keyword and ontologies and retry'
          )
        }
        
        arrayResults.forEach(element => {
          if (element.label.trim().toLowerCase() === qeValue.toLowerCase()) {
            //exact match
            resultsQEexact.push(element)
          }
        })

        if (resultsQEexact.length > 0) {
          setShowQEfirstResults(true)
          matchesQE.splice(0, matchesQE.length)
          resultsQEexact.forEach(element => {
            props.arrayFilteringTermsQE.forEach(element2 => {
              if (
                element.obo_id.toLowerCase().trim() ===
                element2.id.toLowerCase().trim()
              ) {
                setError(null)
                matchesQE.push(element2.id)
                setShowQEresults(true)
              }
            })
          })
        }
      } else {
        setError('Please write the keyword and at least one ontology')
      }
    } catch (error) {
      setError('NOT FOUND')
    }
  }

  const handleForward = () => {
    setShowQEfirstResults(false)
    setShowQEresults(false)
  }
  const handleNext = () => {
    setShowQEfirstResults(false)
    setShowQEresults(true)
  }

  const handleCheckQE = e => {
    if (e.target.checked === true) {
      if (props.query !== null && props.query !== '') {
        props.setQuery(props.query + ',' + e.target.value)
      } else {
        props.setQuery(e.target.value)
      }
    } else if (e.target.checked === false) {
      let varQuery = ''
      if (props.query.includes(',' + e.target.value)) {
        varQuery = props.query.replace(',' + e.target.value, '')
      } else if (props.query.includes(e.target.value + ',')) {
        varQuery = props.query.replace(e.target.value + ',', '')
      } else {
        varQuery = props.query.replace(e.target.value, '')
      }
      props.setQuery(varQuery)
    }
  }

  return (
    <div>
      <button onClick={() => props.setExpansionSection(false)}>
        <img className='hideQE' src='../hide.png' alt='hideIcon'></img>
      </button>
      <div className='expansionContainer2'>
        {showQEresults === false && showQEfirstResults === false && (
          <div className='qeSection'>
            {timeOut === true && (
              <h2 className='qeSubmitH2'>Horizontal query expansion</h2>
            )}
            {timeOut === false && (
              <div className='loaderLogo'>
                <div className='loader2'>
                  <div id='ld3'>
                    <div></div>
                    <div></div>
                    <div></div>
                  </div>
                </div>
              </div>
            )}
            {timeOut === true && (
              <input
                className='QEinput'
                type='text'
                value={qeValue}
                autoComplete='on'
                placeholder={
                  'Type ONE keyword (what you want to search): e.g., melanoma'
                }
                onChange={e => handleQEchanges(e)}
                aria-label='ID'
              />
            )}
            {timeOut === true && (
              <input
                className='QEinput2'
                type='text'
                value={ontologyValue}
                autoComplete='on'
                placeholder={
                  'Type the ontologies to include in the search comma-separated: e.g., mondo,ncit'
                }
                onChange={e => handleOntologyChanges(e)}
                aria-label='ID'
              />
            )}
            {timeOut === true && (
              <button onClick={handleSubmitQE}>
                <h2 className='qeSubmit'>SUBMIT</h2>
              </button>
            )}
          </div>
        )}
        {showQEfirstResults === true && (
          <div className='qeSection'>
            <h2 className='qeSubmitH2'>Horizontal query expansion</h2>

            {ontologyValue.includes(',') && (
              <p className='textQE2'>
                Results found of <b>exactly {qeValue} </b> keyword from{' '}
                <b>{ontologyValue.toUpperCase()}</b> ontologies:
              </p>
            )}
            {!ontologyValue.includes(',') && (
              <p className='textQE2'>
                Results found of <b>exactly {qeValue} </b> keyword from{' '}
                <b>{ontologyValue.toUpperCase()}</b> ontology:
              </p>
            )}
            {resultsQEexact.map((element, index) => {
              return (
                <div>
                  <li className='qeListItem' key={index}>
                    {element.obo_id}
                  </li>
                </div>
              )
            })}
            <button onClick={handleForward} className='forwardButton'>
              RETURN
            </button>
            <button onClick={handleNext} className='nextButton'>
              SEARCH IN FILTERING TERMS
            </button>
          </div>
        )}
        {showQEresults === true && showQEfirstResults === false && (
          <div className='qeSection'>
            <h2 className='qeSubmitH2'>Horizontal query expansion</h2>
            {matchesQE.length > 0 && (
              <p className='textQE'>
                We looked for all the ontology terms derived from the typed
                keyword <b>"{qeValue}" </b> that are part of the Beacon Network{' '}
                <b>filtering terms</b>. You can select them so that they are
                automatically copied to your query. Please be aware that if you
                want to look for individuals{' '}
                <b>with either one ontology or the other </b>you have to do
                different searches <b>for now.</b> In other words, one ontology
                term at a time. If you included all ontologies in a unique
                search you would be looking for individuals with several{' '}
                {qeValue} ontology terms in the same document, which does not
                makes much sense.
              </p>
            )}
            {matchesQE.length === 0 && (
              <h5>
                Unfortunately the keyword is not among the current filtering
                terms
              </h5>
            )}
            {matchesQE.map(element => {
              return (
                <div className='divCheckboxQE'>
                  <label className='labelQE'>
                    <input
                      onChange={handleCheckQE}
                      className='inputCheckbox'
                      type='checkbox'
                      value={element}
                    />
                    {element}
                  </label>
                </div>
              )
            })}
            <button onClick={handleNewQEsearch}>
              <h2 className='newQEsearch'>New QE search</h2>
            </button>
          </div>
        )}
        {error !== null && <h6 className='errorQE'>{error}</h6>}
      </div>
    </div>
  )
}

export default HorizontalExpansion
