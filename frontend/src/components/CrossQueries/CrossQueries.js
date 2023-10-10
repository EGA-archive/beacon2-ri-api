import './CrossQueries.css'
import axios from 'axios'
import { useState, useEffect } from 'react'
import configData from '../../config.json'

function CrossQueries () {
  const [valueInitial, setValueInitial] = useState('')
  const [valueFinal, setValueFinal] = useState('')
  const [IdValue, setIdValue] = useState('')
  const [error, setError] = useState('')
  const [results, setResults] = useState('')
  const [arrayResults, setArrayResults] = useState([])

  const [showSubmit, setShowSubmit] = useState(true)

  const handleChangeInitial = e => {
    setValueInitial(e.target.value)
  }

  const handleChangeFinal = e => {
    setValueFinal(e.target.value)
  }

  const handleChangeID = e => {
    setIdValue(e.target.value)
  }

  const handleClick = () => {
    setShowSubmit(true)
    setResults('')
    setIdValue('')
    setValueFinal('')
    setValueInitial('')
    setError('')
    setArrayResults([])
  }

  const handleSubmit = async e => {
    e.preventDefault()
    setShowSubmit(false)
    try {
      let res = await axios.get(
        configData.API_URL + `/${valueInitial}/${IdValue}/${valueFinal}`
      )
      console.log(res)
      res.data.response.resultSets.forEach((element, index) => {
        if (res.data.response.resultSets[index].results.length > 0) {
          setResults(res.data.response.resultSets[index].results)

          res.data.response.resultSets[index].results.forEach(element => {
            arrayResults.push(
              JSON.stringify(element, null, 2).replace('[', '').replace(']', '')
            )
          })
          console.log(results)
          console.log(arrayResults)
        } else {
          setResults(null)
        }
      })
    } catch (error) {
      setError('Not found. Please retry')
      console.log(error)
    }
  }

  return (
    <div className='divCrossQueries'>
      <form className='crossQueriesForm' onSubmit={handleSubmit}>
        <label className='originCollection'>
          Pick the "origin" collection:
          <select value={valueInitial} onChange={handleChangeInitial}>
            <option value='select'>Select</option>
            <option value='g_variants'>Variant</option>
            <option value='individuals'>Individuals</option>
            <option value='biosamples'>Biosamples</option>
            <option value='runs'>Runs</option>
            <option value='analyses'>Analyses</option>
          </select>
        </label>
        <label>
          ID:
          <input
            className='inputId'
            type='text'
            value={IdValue}
            onChange={handleChangeID}
          />
        </label>
        <label>
          Pick the collection you want to see for the written ID:
          <select value={valueFinal} onChange={handleChangeFinal}>
            <option value='select'>Select</option>
            <option value='g_variants'>Variant</option>
            <option value='individuals'>Individuals</option>
            <option value='biosamples'>Biosamples</option>
            <option value='runs'>Runs</option>
            <option value='analyses'>Analyses</option>
          </select>
        </label>

        {showSubmit && <button className='formButton'>Submit</button>}
        {error !== '' && results === '' && <h5>Not found. Please retry</h5>}
        {results === null && <h5>Not found. Please retry</h5>}
      </form>

      {!showSubmit && (
        <button className='formButton' onClick={handleClick}>
          New search
        </button>
      )}

      {results !== null && results !== '' && (
        <div>
          <pre className='preCrossQueries'>
            <p>{arrayResults}</p>
          </pre>
        </div>
      )}
    </div>
  )
}

export default CrossQueries
