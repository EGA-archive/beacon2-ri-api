import './CrossQueries.css'
import axios from 'axios'
import { useState, useEffect } from 'react'
import configData from '../../config.json'
import TableResultsVariant from '../Results/VariantResults/TableResultsVariant'
import TableResultsIndividuals from '../Results/IndividualsResults/TableResultsIndividuals'
import TableResultsBiosamples from '../Results/BiosamplesResults/TableResultsBiosamples'
import { useNavigate } from 'react-router-dom'

function CrossQueries (props) {
  const [valueInitial, setValueInitial] = useState(props.collection)
  const [valueFinal, setValueFinal] = useState('')

  const [error, setError] = useState('')
  const [results, setResults] = useState([])
  const [arrayResults, setArrayResults] = useState([])

  const [showSubmit, setShowSubmit] = useState(true)
  const [trigger, setTrigger] = useState(true)

  const [triggerResults, setTriggerResults] = useState(false)

  const [resultsPerDataset, setResultsDataset] = useState([])
  const [resultsNotPerDataset, setResultsNotPerDataset] = useState([])

  const [beaconsList, setBeaconsList] = useState([])
  const navigate = useNavigate()

  const handleChangeInitial = e => {
    setValueInitial(e.target.value)
  }

  let scope = props.collection
  let id = props.parameter

  const [scope2, setScope2] = useState(scope)

  const [IdValue, setIdValue] = useState(id)
  const handleChangeFinal = e => {
    setValueFinal(e.target.value)
  }

  const handleChangeID = e => {
    setIdValue(e.target.value)
    setScope2('allScopes')
    setTrigger(false)
  }

  const handleClick = () => {
    setShowSubmit(true)
    setResults([])

    setValueFinal('')
    setValueInitial(props.collection)
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

      res.data.response.resultSets.forEach((element, index) => {
        if (element.id && element.id !== '') {
          if (resultsPerDataset.length > 0) {
            resultsPerDataset.forEach(element2 => {
              element2[0].push(element.id)
              element2[1].push(element.exists)
              element2[2].push(element.resultsCount)
              element2[3].push(element.resultsHandover)
            })
          } else {
            let arrayResultsPerDataset = [
              //element.beaconId,
              [element.id],
              [element.exists],
              [element.resultsCount],
              [element.resultsHandover]
            ]
            resultsPerDataset.push(arrayResultsPerDataset)
          }
        }

        if (element.id === undefined || element.id === '') {
          let arrayResultsNoDatasets = [element.beaconId]
          resultsNotPerDataset.push(arrayResultsNoDatasets)
        }

        if (res.data.response.resultSets[index].results) {
          res.data.response.resultSets[index].results.forEach(
            (element2, index2) => {
              let arrayResult = [
                res.data.meta.beaconId,
                res.data.response.resultSets[index].results[index2]
              ]
              results.push(arrayResult)
            }
          )
        }
      })

      let res2 = await axios.get(configData.API_URL + '/info')
      beaconsList.push(res2.data.response)
      setTriggerResults(true)
      // res.data.response.resultSets.forEach((element, index) => {
      //   if (res.data.response.resultSets[index].results.length > 0) {
      //     setResults(res.data.response.resultSets[index].results)

      //     res.data.response.resultSets[index].results.forEach(element => {
      //       arrayResults.push(
      //         JSON.stringify(element, null, 2).replace('[', '').replace(']', '')
      //       )
      //     })
      //   } else {
      //     setResults(null)
      //   }
      // })
    } catch (error) {
      setError('Not found. Please retry')
    }
  }

  useEffect(() => {
    setTrigger(true)
  }, [scope2])

  return (
    <>
      {results.length < 1 && (
        <div className='divCrossQueries'>
          {!error && (
            <form className='crossQueriesForm' onSubmit={handleSubmit}>
              <label className='originCollection'>
                Pick the "origin" collection:
                <select value={valueInitial} onChange={handleChangeInitial}>
                  {scope2 === 'allScopes' && (
                    <option value='select'>Select</option>
                  )}
                  {scope2 === 'allScopes' && (
                    <option value='g_variants'>Variant</option>
                  )}
                  {scope2 === 'allScopes' && (
                    <option value='individuals'>Individuals</option>
                  )}
                  {scope2 === 'allScopes' && (
                    <option value='biosamples'>Biosamples</option>
                  )}
                  {scope2 === 'allScopes' && <option value='runs'>Runs</option>}
                  {scope2 === 'allScopes' && (
                    <option value='analyses'>Analyses</option>
                  )}

                  {scope2 === 'variants' && (
                    <option value='g_variants' selected>
                      Variant
                    </option>
                  )}
                  {scope2 === 'individuals' && (
                    <option value='individuals' selected>
                      Individuals
                    </option>
                  )}
                  {scope2 === 'biosamples' && (
                    <option value='biosamples' selected>
                      Biosamples
                    </option>
                  )}
                  {scope2 === 'runs' && (
                    <option value='runs' selected>
                      Runs
                    </option>
                  )}
                  {scope2 === 'analyses' && (
                    <option value='analyses' selected>
                      Analyses
                    </option>
                  )}
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
                  {/* <option value='runs'>Runs</option>
              <option value='analyses'>Analyses</option> */}
                </select>
              </label>

              {showSubmit && <button className='formButton'>Submit</button>}
              {error !== '' && results === '' && (
                <h5>Not found. Please retry</h5>
              )}
              {results === null && <h5>Not found. Please retry</h5>}
            </form>
          )}
          {error && <h5>{error}</h5>}
          <div>
            <button
              className='goBackCrossQ'
              onClick={() => props.setShowCrossQuery(false)}
            >
              Back
            </button>
            {!showSubmit && (
              <button className='formButton' onClick={handleClick}>
                New search
              </button>
            )}
          </div>
        </div>
      )}
      {results !== null &&
        results !== '' &&
        triggerResults &&
        valueFinal === 'g_variants' && (
          <div className='containerTableResults'>
            <TableResultsVariant
              show={'full'}
              resultsPerDataset={resultsPerDataset}
              resultsNotPerDataset={resultsNotPerDataset}
              results={results}
              beaconsList={beaconsList}
            ></TableResultsVariant>
          </div>
        )}
      {results !== null &&
        results !== '' &&
        triggerResults &&
        valueFinal === 'individuals' && (
          <div className='containerTableResults'>
            <TableResultsIndividuals
              show={'full'}
              resultsPerDataset={resultsPerDataset}
              resultsNotPerDataset={resultsNotPerDataset}
              results={results}
              beaconsList={beaconsList}
            ></TableResultsIndividuals>
          </div>
        )}
      {results !== null &&
        results !== '' &&
        triggerResults &&
        valueFinal === 'biosamples' && (
          <div className='containerTableResults'>
            <TableResultsBiosamples
              show={'full'}
              resultsPerDataset={resultsPerDataset}
              resultsNotPerDataset={resultsNotPerDataset}
              results={results}
              beaconsList={beaconsList}
            ></TableResultsBiosamples>
          </div>
        )}
    </>
  )
}

export default CrossQueries
