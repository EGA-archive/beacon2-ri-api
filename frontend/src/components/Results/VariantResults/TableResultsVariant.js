import './TableResultsVariant.css'
import '../IndividualsResults/TableResultsIndividuals.css'
import '../../Dataset/BeaconInfo'
import { useState, useEffect } from 'react'

function TableResultsVariant (props) {
  const [showDatsets, setShowDatasets] = useState(false)

  const [showResults, setShowResults] = useState(false)

  const [arrayBeaconsIds, setArrayBeaconsIds] = useState([])
  const [rows, setRows] = useState([])
  const [ids, setIds] = useState([])

  const [resultsJSON, setResultsJSON] = useState([])

  const [stringDataToCopy, setStringDataToCopy] = useState('')

  const [resultsSelected, setResultsSelected] = useState(props.results)
  const [resultsSelectedFinal, setResultsSelectedFinal] = useState([])

  const [openDatasetArray, setOpenDataset] = useState([])
  const [openDatasetArray2, setOpenDataset2] = useState([])

  const [editable, setEditable] = useState([])

  const [trigger, setTrigger] = useState(false)
  const [trigger2, setTrigger2] = useState(false)

  const [triggerArray, setTriggerArray] = useState([])
  const [triggerArray2, setTriggerArray2] = useState([])

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

  const handleSeeResults = e => {
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
    // console.log(props.resultsPerDataset)
    // let count = 0
    // props.beaconsList.forEach((element2, index2) => {
    //   count = getOccurrence(arrayBeaconsIds, element2.meta.beaconId)
    //   if (count > 0) {
    //     beaconsArrayResults.push([element2, count, true])
    //   } else {
    //     beaconsArrayResults.push([element2, count, false])
    //   }
    // })
    // beaconsArrayResults.forEach(element => {
    //   if (element[2] === true) {
    //     beaconsArrayResultsOrdered.push(element)
    //   }
    // })
    // beaconsArrayResults.forEach(element => {
    //   if (element[2] === false) {
    //     beaconsArrayResultsOrdered.push(element)
    //   }
    // })
    // console.log(beaconsArrayResults)

    setShowDatasets(true)
  }, [])

  return (
    <div className='containerBeaconResults'>
      {showDatsets === true &&
        props.beaconsList.map(result => {
          return (
            <>
              {props.show !== 'full' && (
                <>
                  {props.resultSets === 'MISS' &&
                    props.resultsPerDataset.map((element, index) => {
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
                                    <h7>
                                      {datasetObject.replaceAll('_', ' ')}
                                    </h7>
                                  </div>
                                )
                              })}
                            </div>
                          </div>
                        </>
                      )
                    })}

                  {props.resultSets !== 'MISS' &&
                    props.resultSets !== 'HIT' &&
                    props.resultsPerDataset.map((element, index) => {
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
                                    {props.resultSets !== 'NONE' && (
                                      <h7>
                                        {datasetObject.replaceAll('_', ' ')}
                                      </h7>
                                    )}

                                    {element[1][indexDataset] === true &&
                                      props.show === 'boolean' && (
                                        <h6>FOUND</h6>
                                      )}
                                    {element[1][indexDataset] === false &&
                                      props.show === 'boolean' && (
                                        <h5>NOT FOUND</h5>
                                      )}
                                    {props.show === 'count' &&
                                      element[2][indexDataset] !== 0 &&
                                      element[2][indexDataset] !== 1 && (
                                        <h6>
                                          {element[2][indexDataset]} RESULTS
                                        </h6>
                                      )}
                                    {props.show === 'count' &&
                                      element[2][indexDataset] === 0 && (
                                        <h5>
                                          {element[2][indexDataset]} RESULTS
                                        </h5>
                                      )}
                                    {props.show === 'count' &&
                                      element[2][indexDataset] === 1 && (
                                        <h6>
                                          {element[2][indexDataset]} RESULT
                                        </h6>
                                      )}
                                  </div>
                                )
                              })}
                            </div>
                          </div>
                        </>
                      )
                    })}
                  {props.resultSets === 'HIT' &&
                    props.resultsPerDataset.map((element, index) => {
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
                                    <h7>
                                      {datasetObject.replaceAll('_', ' ')}
                                    </h7>

                                    {element[1][indexDataset] === true &&
                                      props.show === 'boolean' && (
                                        <h6>FOUND</h6>
                                      )}
                                    {element[1][indexDataset] === false &&
                                      props.show === 'boolean' && (
                                        <h5>NOT FOUND</h5>
                                      )}
                                    {props.show === 'count' &&
                                      element[2][indexDataset] !== 0 &&
                                      element[2][indexDataset] !== 1 && (
                                        <h6>
                                          {element[2][indexDataset]} RESULTS
                                        </h6>
                                      )}
                                    {props.show === 'count' &&
                                      element[2][indexDataset] === 0 && (
                                        <h5>
                                          {element[2][indexDataset]} RESULTS
                                        </h5>
                                      )}
                                    {props.show === 'count' &&
                                      element[2][indexDataset] === 1 && (
                                        <h5>
                                          {element[2][indexDataset]} RESULT
                                        </h5>
                                      )}
                                  </div>
                                )
                              })}
                            </div>
                          </div>
                        </>
                      )
                    })}

                  {props.resultSets !== 'MISS' &&
                    props.resultsNotPerDataset.map((element, index) => {
                      return (
                        <>
                          {props.show === 'boolean' && (
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

                                <div className='resultSetsContainer'>
                                  <>
                                    <h6>FOUND </h6>
                                  </>
                                </div>
                              </div>
                            </div>
                          )}
                          {props.show === 'boolean' && (
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
                                <div className='resultSetsContainer'>
                                  <>
                                    <h5 className='buttonResults'>NOT FOUND</h5>
                                  </>
                                </div>
                              </div>
                            </div>
                          )}

                          {props.show === 'count' && (
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
                                <div className='resultSetsContainer'>
                                  <>
                                    {element[2] !== 0 && (
                                      <h6 className='buttonResults'>
                                        {element[2]} results
                                      </h6>
                                    )}
                                    {element[2] === 0 && (
                                      <h5 className='buttonResults'>
                                        {element[2]} results
                                      </h5>
                                    )}
                                  </>
                                </div>
                                <button
                                  className='buttonResults'
                                  onClick={() => {
                                    handleSeeResults(result.id)
                                  }}
                                ></button>
                              </div>
                            </div>
                          )}
                        </>
                      )
                    })}
                  {props.resultSets !== 'HIT' &&
                    props.resultsNotPerDataset.map((element, index) => {
                      return (
                        <>
                          {element[1] === true && props.show === 'boolean' && (
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

                                <div className='resultSetsContainer'>
                                  <>
                                    <h6>FOUND </h6>
                                  </>
                                </div>
                              </div>
                            </div>
                          )}
                          {element[1] === false && props.show === 'boolean' && (
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
                                <div className='resultSetsContainer'>
                                  <>
                                    <h5 className='buttonResults'>NOT FOUND</h5>
                                  </>
                                </div>
                              </div>
                            </div>
                          )}

                          {props.show === 'count' && (
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
                                <div className='resultSetsContainer'>
                                  <>
                                    {element[2] !== 0 && (
                                      <h6 className='buttonResults'>
                                        {element[2]} results
                                      </h6>
                                    )}
                                    {element[2] === 0 && (
                                      <h5 className='buttonResults'>
                                        {element[2]} results
                                      </h5>
                                    )}
                                  </>
                                </div>
                                <button
                                  className='buttonResults'
                                  onClick={() => {
                                    handleSeeResults(result.id)
                                  }}
                                ></button>
                              </div>
                            </div>
                          )}
                        </>
                      )
                    })}
                </>
              )}
              {props.show === 'full' && (
                <div className='datasetCardResults'>
                  <div className='tittleResults'>
                    <div className='tittle4'>
                      <img
                        className='logoBeacon'
                        src={result.organization.logoUrl}
                        alt={result.id}
                      />
                      <h2>{result.organization.name}</h2>
                    </div>
                    <div className='seeResultsContainer'>
                      <button
                        className='buttonResults'
                        onClick={() => {
                          handleSeeResults(result.id)
                        }}
                      >
                        {props.show === 'full' && <h7>See results</h7>}
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </>
          )
        })}

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
