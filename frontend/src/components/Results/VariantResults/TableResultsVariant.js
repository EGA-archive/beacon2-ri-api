import './TableResultsVariant.css'
import '../IndividualsResults/TableResultsIndividuals.css'
import '../../Dataset/BeaconInfo.css'
import { useState, useEffect } from 'react'

function TableResultsVariant (props) {
  const [showDatsets, setShowDatasets] = useState(false)

  const [showResults, setShowResults] = useState(false)

  const [arrayBeaconsIds, setArrayBeaconsIds] = useState([])
  const [rows, setRows] = useState([])
  const [ids, setIds] = useState([])

  const [resultsJSON, setResultsJSON] = useState([])

  const [stringDataToCopy, setStringDataToCopy] = useState('')

  const [beaconsArrayResults, setBeaconsArrayResults] = useState([])

  const [beaconsArrayResultsOrdered, setBeaconsArrayResultsOrdered] = useState(
    []
  )

  const [resultsSelected, setResultsSelected] = useState(props.results)
  const [resultsSelectedFinal, setResultsSelectedFinal] = useState([])

  const [openDatasetArray, setOpenDataset] = useState([])

  const [editable, setEditable] = useState([])

  const [trigger, setTrigger] = useState(false)
  const [trigger2, setTrigger2] = useState(false)

  const [triggerArray, setTriggerArray] = useState([])

  const copyData = e => {
    navigator.clipboard
      .writeText(stringDataToCopy)
      .then(() => {
        alert('successfully copied')
      })
      .catch(() => {
        alert('something went wrong')
      })
    console.log('COPY DONE')
  }

  const handleClickDatasets = e => {
  
    openDatasetArray[e] = true
    triggerArray[e] = true
    setTrigger(!trigger)
  }
  const handleSeeResults = ()=> {
 
    setResultsSelectedFinal(resultsSelected)
    setShowResults(true)
    setShowDatasets(false)
    setTrigger(true)
  }

  useEffect(() => {
    props.results.forEach((element, index) => {
      resultsJSON.push([
        JSON.stringify(element[1], null, 2).replace('[', '').replace(']', '')
      ])

      arrayBeaconsIds.push(element[0])
    })
    setTrigger2(true)
    setStringDataToCopy(resultsJSON)
  }, [trigger, resultsSelectedFinal])

  useEffect(() => {
   
    setShowDatasets(true)
  }, [])

  return (
    <div className='containerResultsVariants'>
      <div className='containerBeaconResults'>
        {showDatsets === true &&
           props.beaconsList.map(result => {
            return (
              <>
                {props.show && (
                  <>
                    {props.resultsPerDataset.map((element, index) => {
                      return (
                        <>
                          <div className='datasetCardResults'>
                            <div className='tittleResults'>
                              <div className='tittle4'>
                                <img
                                  className='logoBeacon'
                                  src={result.organization.logoUrl}
                                  alt={result.id}
                                />
                                <h4>{result.organization.name}</h4>
                              </div>
  
                              {element[0].map((datasetObject, indexDataset) => {
                                return (
                                  <div className='resultSetsContainer'>
                                    <button
                                      className='resultSetsButton'
                                      onClick={() =>
                                        handleClickDatasets([index, indexDataset])
                                      }
                                    >
                                      <h7>
                                        {datasetObject.replaceAll('_', ' ')}
                                      </h7>
                                    </button>
                                    {openDatasetArray[[index, indexDataset]] ===
                                      true &&
                                      triggerArray[[index, indexDataset]] ===
                                        true &&
                                      element[1][indexDataset] === true &&
                                      props.show === 'boolean' && <h6>FOUND</h6>}
                                    {openDatasetArray[[index, indexDataset]] ===
                                      true &&
                                      triggerArray[[index, indexDataset]] ===
                                        true &&
                                      element[1][indexDataset] === false &&
                                      props.show === 'boolean' && (
                                        <h5>NOT FOUND</h5>
                                      )}
                                    {props.show === 'count' &&
                                      triggerArray[[index, indexDataset]] ===
                                        true && (
                                        <h6>
                                          {element[2][indexDataset]} RESULTS
                                        </h6>
                                      )}
                                    {props.show === 'full' &&
                                      element[1][indexDataset] === true && (
                                        <button
                                          className='buttonResults'
                                          onClick={() => {
                                            handleSeeResults(
                                              
                                            )
                                          }}
                                        >
                                          <h7 className="seeResultsButton"> SEE RESULTS</h7>
                                        </button>
                                      )}
                                  </div>
                                )
                              })}
                            </div>
                          </div>
                        </>
                      )
                    })}
                  </>
                )}
              </>
            )
          })}
      </div>
      {showDatsets === false && showResults === true && trigger === true && (
        <div className='containerBeaconResultsVariants'>
          <div className='copyDivVariants'>
            <button className='buttonCopy' onClick={copyData}>
              <h7>COPY ALL RESULTS</h7>
              <img className='copyLogo' src='../copy.png' alt='copyIcon'></img>
            </button>
          </div>

          {resultsJSON.map(element => {
            return (
              <pre className='resultsVariants'>
                <p>{element}</p>
              </pre>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default TableResultsVariant