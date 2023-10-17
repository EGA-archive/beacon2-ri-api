import '../../App.css'
import './Cohorts.css'
import React, { useState, useEffect } from 'react'
import Select from 'react-select'
import makeAnimated from 'react-select/animated'

function CohortsModule (props) {
  const [results, setResults] = useState(null)
  const [selectedCohortsAux, setSelectedCohortsAux] = useState([])
  const animatedComponents = makeAnimated()
  const onSubmitCohorts = () => {
    setResults('Cohorts')

    props.setShowGraphs(true)
  }
  const handleChangeCohorts = selectedOption => {
    console.log(selectedOption)
    setSelectedCohortsAux([])
    selectedCohortsAux.push(selectedOption)
    props.setSelectedCohorts(selectedCohortsAux)
  }

  return (
    <div className='cohortsModule'>
      <Select
        closeMenuOnSelect={false}
        components={animatedComponents}
        defaultValue={[]}
        isMulti
        options={props.optionsCohorts}
        onChange={handleChangeCohorts}
        autoFocus={true}
        //onToggleCallback={onToggle3}
      />

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
    </div>
  )
}

export default CohortsModule
