import '../../App.css'
import './Cohorts.css'
import React, { useState, useEffect } from 'react'
import Select from 'react-select'
import makeAnimated from 'react-select/animated'
import Cohorts from './Cohorts'

function CohortsModule (props) {
  const [results, setResults] = useState(null)

  const animatedComponents = makeAnimated()
  const [selected, setSelected] = useState(null)

  const [trigger, setTrigger] = useState(false)
  const [newSearch, setNewSearch] = useState(true)

  const onSubmitCohorts = () => {
    setResults('Cohorts')
    props.setShowGraphs(true)
  }
  const handleChangeCohorts = selectedOption => {
    setSelected(selectedOption)
    props.setSelectedCohorts(selectedOption)
  }

  const handleSearchAgain = () => {
    setTrigger(true)
    props.setResponse('')
    props.setTrigger2(!props.trigger2)
  }

  return (
    <div className='cohortsModule'>
      <Select
        options={props.optionsCohorts}
        onChange={handleChangeCohorts}
        autoFocus={true}
      />

      {!props.alreadySelectedCohort && (
        <form className='d-flex2' onSubmit={onSubmitCohorts}>
          {results !== 'Cohorts' && (
            <button className='searchButton2' type='submit'>
              <img
                className='forwardIcon'
                src='./next.png'
                alt='searchIcon'
              ></img>
            </button>
          )}
        </form>
      )}
      {props.alreadySelectedCohort && (
        <button className='searchButton2' onClick={handleSearchAgain}>
          <img className='forwardIcon' src='./next.png' alt='searchIcon'></img>
        </button>
      )}

      {trigger && <Cohorts newSearch={newSearch} setNewSearch={setNewSearch} />}
    </div>
  )
}

export default CohortsModule