import '../IndividualsResults/TableResultsIndividuals.css'
import '../../Datasets/ResultsDatasets.css'
import * as React from 'react'
import {
  DataGrid,
  GridToolbar,
  selectedGridRowsSelector,
  gridFilteredSortedRowIdsSelector,
  GridToolbarContainer,
  GridToolbarExport
} from '@mui/x-data-grid'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function CustomToolbar () {
  return (
    <GridToolbarContainer>
      <GridToolbarExport />
    </GridToolbarContainer>
  )
}
function TableResultsRuns (props) {
  const [showDatsets, setShowDatasets] = useState(false)

  const [showResults, setShowResults] = useState(false)

  const [arrayBeaconsIds, setArrayBeaconsIds] = useState([])
  const [rows, setRows] = useState([])
  const [ids, setIds] = useState([])

  const [beaconsArrayResults, setBeaconsArrayResults] = useState([])

  const [beaconsArrayResultsOrdered, setBeaconsArrayResultsOrdered] = useState(
    []
  )

  const [resultsSelected, setResultsSelected] = useState(props.results)
  const [resultsSelectedFinal, setResultsSelectedFinal] = useState([])

  const [openDatasetArray, setOpenDataset] = useState([])
  const [openDatasetArray2, setOpenDataset2] = useState([])

  const [editable, setEditable] = useState([])

  const [trigger, setTrigger] = useState(false)
  const [trigger2, setTrigger2] = useState(false)

  const [triggerArray, setTriggerArray] = useState([])
  const [triggerArray2, setTriggerArray2] = useState([])

  const getSelectedRowsToExport = ({ apiRef }) => {
    const selectedRowIds = selectedGridRowsSelector(apiRef)
    if (selectedRowIds.size > 0) {
      return Array.from(selectedRowIds.keys())
    }

    return gridFilteredSortedRowIdsSelector(apiRef)
  }

  const handleClickDatasets = e => {
    openDatasetArray[e] = true
    triggerArray[e] = true
    setTrigger(!trigger)
  }

  const handleClickDatasets2 = e => {
    openDatasetArray2[e] = true
    triggerArray2[e] = true
    setTrigger(!trigger)
  }

  let columns = [
    {
      field: 'id',
      headerName: 'Row',
      width: 100,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'runId',
      headerName: 'Run ID',
      width: 150,
      headerClassName: 'super-app-theme--header',
      renderCell: params => (
        <Link to={`cross-queries/${params.row.runId}`}>{params.row.runId}</Link>
      )
    },
    {
      field: 'Beacon',
      headerName: 'Beacon ID',
      width: 340,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'biosampleId',
      headerName: 'Biosample ID',
      width: 150,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'individualId',
      headerName: 'Individual ID',
      width: 150,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'runDate',
      headerName: 'Run date',
      width: 240,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'librarySource',
      headerName: 'Library source',
      width: 250,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'librarySelection',
      headerName: 'Library selection',
      width: 350,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'libraryStrategy',
      headerName: 'Library strategy',
      width: 350,
      headerClassName: 'super-app-theme--header',
      cellClass: 'pre'
    },
    {
      field: 'libraryLayout',
      headerName: 'Library layout',
      width: 200,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'platform',
      headerName: 'Platform',
      width: 200,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'platformModel',
      headerName: 'Platform model',
      width: 200,
      headerClassName: 'super-app-theme--header'
    }
  ]
  const handleSeeResults = e => {
    resultsSelected.forEach(element => {
      if (element[0] === e) {
        resultsSelectedFinal.push(element)
      }
    })
    setShowResults(true)
    setShowDatasets(false)
    setTrigger(true)
  }

  function getOccurrence (array, value) {
    var count = 0
    array.forEach(v => v === value && count++)
    return count
  }

  useEffect(() => {
    setRows([])
    setIds([])

    resultsSelected.forEach((element, index) => {
      arrayBeaconsIds.push(element[0])
    })
    resultsSelectedFinal.forEach((element, index) => {
      if (element[1] !== undefined) {
        let runDateJson = []
        if (element[1].runDate !== '' && element[1].runDate !== undefined) {
          if (typeof element[1].runDate === 'string') {
            runDateJson = element[1].runDate
          } else {
            runDateJson = element[1].runDate.toString()
          }
        }

        let librarySource_id = ''
        let librarySource_label = ''
        let stringLibrarySource = ''

        if (element[1].librarySource !== '') {
          librarySource_id = element[1].librarySource.id
          librarySource_label = element[1].librarySource.label
          stringLibrarySource = `${element[1].librarySource.label} / ${element[1].librarySource.id}`
        } else {
          stringLibrarySource = ''
        }

        let librarySelectionJson = []
        if (
          element[1].librarySelection !== '' &&
          element[1].librarySelection !== undefined
        ) {
          if (typeof element[1].librarySelection === 'string') {
            librarySelectionJson = element[1].librarySelection
          }
        }
        let libraryStrategyJson = []
        if (
          element[1].libraryStrategy !== '' &&
          element[1].libraryStrategy !== undefined
        ) {
          if (typeof element[1].libraryStrategy === 'string') {
            libraryStrategyJson = element[1].libraryStrategy
          }
        }

        let libraryLayoutJson = []

        if (
          element[1].libraryLayout !== '' &&
          element[1].libraryLayout !== undefined
        ) {
          if (typeof element[1].libraryLayout === 'string') {
            libraryLayoutJson = element[1].libraryLayout
          }
        }

        let platformJson = []

        if (element[1].platform !== '' && element[1].platform !== undefined) {
          if (typeof element[1].platform === 'string') {
            platformJson = element[1].platform
          }
        }

        let platformModel_id = ''
        let platformModel_label = ''
        let stringPlatformModel = ''

        if (element[1].platformModel !== '') {
          platformModel_id = element[1].platformModel.id
          platformModel_label = element[1].platformModel.label
          stringPlatformModel = `${element[1].platformModel.label} / ${element[1].platformModel.id}`
        } else {
          stringPlatformModel = ''
        }
        var myObjRows = new Object()
        myObjRows.id = index
        if (element[1].id !== '') {
          myObjRows.runId = element[1].id
        }
        myObjRows.Beacon = element[0]
        if (element[1].biosampleId !== '') {
          myObjRows.biosampleId = element[1].biosampleId
        }
        if (element[1].individualId !== '') {
          myObjRows.individualId = element[1].individualId
        }

        if (runDateJson !== '') {
          myObjRows.runDate = runDateJson
        }
        if (stringLibrarySource !== '') {
          myObjRows.librarySource = stringLibrarySource
        }
        if (librarySelectionJson !== '') {
          myObjRows.librarySelection = librarySelectionJson
        }
        if (libraryStrategyJson !== '') {
          myObjRows.libraryStrategy = libraryStrategyJson
        }
        if (libraryLayoutJson !== '') {
          myObjRows.libraryLayout = libraryLayoutJson
        }
        if (platformJson !== '') {
          myObjRows.platform = platformJson
        }
        if (stringPlatformModel !== '') {
          myObjRows.platformModel = stringPlatformModel
        }

        rows.push(myObjRows)

        if (index === resultsSelectedFinal.length - 1) {
          setEditable(rows.map(o => ({ ...o })))

          setTrigger2(true)
        }
      }
    })
  }, [trigger, resultsSelectedFinal])

  useEffect(() => {
    let count = 0
    props.beaconsList.forEach((element2, index2) => {
      count = getOccurrence(arrayBeaconsIds, element2.meta.beaconId)
      if (count > 0) {
        beaconsArrayResults.push([element2, count, true])
      } else {
        beaconsArrayResults.push([element2, count, false])
      }
    })
    beaconsArrayResults.forEach(element => {
      if (element[2] === true) {
        beaconsArrayResultsOrdered.push(element)
      }
    })
    beaconsArrayResults.forEach(element => {
      if (element[2] === false) {
        beaconsArrayResultsOrdered.push(element)
      }
    })

    setShowDatasets(true)
  }, [])

  return (
    <div className='containerBeaconResults'>
      {showDatsets === true &&
        beaconsArrayResultsOrdered.length > 0 &&
        beaconsArrayResultsOrdered.map(result => {
          return (
            <>
                {props.show !== 'full' && (
                  <>
                    {props.resultSets === 'MISS' &&
                      props.resultsPerDataset.map((element, index) => {
                        return (
                          <>
                            {element[0] === result[0].meta.beaconId && (
                              <div className='datasetCardResults'>
                                <div className='tittleResults'>
                                  <div className='tittle4'>
                                    <img
                                      className='logoBeacon'
                                      src={
                                        result[0].response.organization.logoUrl
                                      }
                                      alt={result[0].meta.beaconId}
                                    />
                                    <h4>
                                      {result[0].response.organization.name}
                                    </h4>
                                  </div>

                                  {element[1].map(
                                    (datasetObject, indexDataset) => {
                                      return (
                                        <div className='resultSetsContainer'>
                                          <h7>
                                            {datasetObject.replaceAll('_', ' ')}
                                          </h7>
                                        </div>
                                      )
                                    }
                                  )}
                                </div>
                              </div>
                            )}
                          </>
                        )
                    })}

                    {props.resultSets !== 'MISS' &&
                      props.resultSets !== 'HIT' &&
                      props.resultsPerDataset.map((element, index) => {
                        return (
                          <>
                            {element[0] === result[0].meta.beaconId && (
                              <div className='datasetCardResults'>
                                <div className='tittleResults'>
                                  <div className='tittle4'>
                                    <img
                                      className='logoBeacon'
                                      src={
                                        result[0].response.organization.logoUrl
                                      }
                                      alt={result[0].meta.beaconId}
                                    />
                                    <h4>
                                      {result[0].response.organization.name}
                                    </h4>
                                  </div>

                                  {element[1].map(
                                    (datasetObject, indexDataset) => {
                                      return (
                                        <div className='resultSetsContainer'>
                                          {props.resultSets !== 'NONE' && (
                                            <h7>
                                              {datasetObject.replaceAll(
                                                '_',
                                                ' '
                                              )}
                                            </h7>
                                          )}

                                          {element[2][indexDataset] === true &&
                                            props.show === 'boolean' && (
                                              <h6>FOUND</h6>
                                            )}
                                          {element[2][indexDataset] === false &&
                                            props.show === 'boolean' && (
                                              <h5>NOT FOUND</h5>
                                            )}
                                          {props.show === 'count' &&
                                            element[3][indexDataset] !== 0 && element[3][indexDataset] !== 1 &&(
                                              <h6>
                                                {element[3][indexDataset]}{' '}
                                                RESULTS
                                              </h6>
                                            )}
                                          {props.show === 'count' &&
                                            element[3][indexDataset] === 0 && (
                                              <h5>
                                                {element[3][indexDataset]}{' '}
                                                RESULTS
                                              </h5>
                                            )}
                                          {props.show === 'count' &&
                                            element[3][indexDataset] === 1 && (
                                              <h5>
                                                {element[3][indexDataset]}{' '}
                                                RESULT
                                              </h5>
                                            )}
                                        </div>
                                      )
                                    }
                                  )}
                                </div>
                              </div>
                            )}
                          </>
                        )
                      })}
                    {props.resultSets === 'HIT' &&
                      result[2] === true &&
                      props.resultsPerDataset.map((element, index) => {
                        return (
                          <>
                            {element[0] === result[0].meta.beaconId && (
                              <div className='datasetCardResults'>
                                <div className='tittleResults'>
                                  <div className='tittle4'>
                                    <img
                                      className='logoBeacon'
                                      src={
                                        result[0].response.organization.logoUrl
                                      }
                                      alt={result[0].meta.beaconId}
                                    />
                                    <h4>
                                      {result[0].response.organization.name}
                                    </h4>
                                  </div>

                                  {element[1].map(
                                    (datasetObject, indexDataset) => {
                                      return (
                                        <div className='resultSetsContainer'>
                                          <h7>
                                            {datasetObject.replaceAll('_', ' ')}
                                          </h7>

                                          {element[2][indexDataset] === true &&
                                            props.show === 'boolean' && (
                                              <h6>FOUND</h6>
                                            )}
                                          {element[2][indexDataset] === false &&
                                            props.show === 'boolean' && (
                                              <h5>NOT FOUND</h5>
                                            )}
                                          {props.show === 'count' &&
                                            element[3][indexDataset] !== 0 &&  element[3][indexDataset] !== 1 && (
                                              <h6>
                                                {element[3][indexDataset]}{' '}
                                                RESULTS
                                              </h6>
                                            )}
                                          {props.show === 'count' &&
                                            element[3][indexDataset] === 0 && (
                                              <h5>
                                                {element[3][indexDataset]}{' '}
                                                RESULTS
                                              </h5>
                                            )}
                                          {props.show === 'count' &&
                                            element[3][indexDataset] === 1 && (
                                              <h5>
                                                {element[3][indexDataset]}{' '}
                                                RESULT
                                              </h5>
                                            )}
                                        </div>
                                      )
                                    }
                                  )}
                                </div>
                              </div>
                            )}
                          </>
                        )
                      })}

                    {props.resultSets !== 'MISS' &&
                      result[2] === true &&
                      props.resultsNotPerDataset.map((element, index) => {
                        return (
                          <>
                            {result[2] === true &&
                              props.show === 'boolean' &&
                              element[0] === result[0].meta.beaconId && (
                                <div className='datasetCardResults'>
                                  <div className='tittleResults'>
                                    <div className='tittle4'>
                                      <img
                                        className='logoBeacon'
                                        src={
                                          result[0].response.organization
                                            .logoUrl
                                        }
                                        alt={result[0].meta.beaconId}
                                      />
                                      <h4>
                                        {result[0].response.organization.name}
                                      </h4>
                                    </div>

                                    <div className='resultSetsContainer'>
                                      <>
                                        <h6>FOUND </h6>
                                      </>
                                    </div>
                                  </div>
                                </div>
                              )}
                            {result[2] === false &&
                              props.show === 'boolean' &&
                              element[0] === result[0].meta.beaconId && (
                                <div className='datasetCardResults'>
                                  <div className='tittleResults'>
                                    <div className='tittle4'>
                                      <img
                                        className='logoBeacon'
                                        src={
                                          result[0].response.organization
                                            .logoUrl
                                        }
                                        alt={result[0].meta.beaconId}
                                      />
                                      <h4>
                                        {result[0].response.organization.name}
                                      </h4>
                                    </div>
                                    <div className='resultSetsContainer'>
                                      <>
                                        <h5 className='buttonResults'>
                                          NOT FOUND
                                        </h5>
                                      </>
                                    </div>
                                  </div>
                                </div>
                              )}

                            {props.show === 'count' &&
                              element[0] === result[0].meta.beaconId && (
                                <div className='datasetCardResults'>
                                  <div className='tittleResults'>
                                    <div className='tittle4'>
                                      <img
                                        className='logoBeacon'
                                        src={
                                          result[0].response.organization
                                            .logoUrl
                                        }
                                        alt={result[0].meta.beaconId}
                                      />
                                      <h4>
                                        {result[0].response.organization.name}
                                      </h4>
                                    </div>
                                    <div className='resultSetsContainer'>
                                      <>
                                        {result[1] !== 0 && (
                                          <h6 className='buttonResults'>
                                            {result[1]} results
                                          </h6>
                                        )}
                                        {result[1] === 0 && (
                                          <h5 className='buttonResults'>
                                            {result[1]} results
                                          </h5>
                                        )}
                                      </>
                                    </div>
                                    <button
                                      className='buttonResults'
                                      onClick={() => {
                                        handleSeeResults(
                                          result[0].meta.beaconId
                                        )
                                      }}
                                    ></button>
                                  </div>
                                </div>
                              )}
                          </>
                        )
                      })}
                    {props.resultSets !== 'HIT' &&
                      result[2] === false &&
                      props.resultsNotPerDataset.map((element, index) => {
                        return (
                          <>
                            {result[2] === true &&
                              props.show === 'boolean' &&
                              element[0] === result[0].meta.beaconId && (
                                <div className='datasetCardResults'>
                                  <div className='tittleResults'>
                                    <div className='tittle4'>
                                      <img
                                        className='logoBeacon'
                                        src={
                                          result[0].response.organization
                                            .logoUrl
                                        }
                                        alt={result[0].meta.beaconId}
                                      />
                                      <h4>
                                        {result[0].response.organization.name}
                                      </h4>
                                    </div>

                                    <div className='resultSetsContainer'>
                                      <>
                                        <h6>FOUND </h6>
                                      </>
                                    </div>
                                  </div>
                                </div>
                              )}
                            {result[2] === false &&
                              props.show === 'boolean' &&
                              element[0] === result[0].meta.beaconId && (
                                <div className='datasetCardResults'>
                                  <div className='tittleResults'>
                                    <div className='tittle4'>
                                      <img
                                        className='logoBeacon'
                                        src={
                                          result[0].response.organization
                                            .logoUrl
                                        }
                                        alt={result[0].meta.beaconId}
                                      />
                                      <h4>
                                        {result[0].response.organization.name}
                                      </h4>
                                    </div>
                                    <div className='resultSetsContainer'>
                                      <>
                                        <h5 className='buttonResults'>
                                          NOT FOUND
                                        </h5>
                                      </>
                                    </div>
                                  </div>
                                </div>
                              )}

                            {props.show === 'count' &&
                              element[0] === result[0].meta.beaconId && (
                                <div className='datasetCardResults'>
                                  <div className='tittleResults'>
                                    <div className='tittle4'>
                                      <img
                                        className='logoBeacon'
                                        src={
                                          result[0].response.organization
                                            .logoUrl
                                        }
                                        alt={result[0].meta.beaconId}
                                      />
                                      <h4>
                                        {result[0].response.organization.name}
                                      </h4>
                                    </div>
                                    <div className='resultSetsContainer'>
                                      <>
                                        {result[1] !== 0 && (
                                          <h6 className='buttonResults'>
                                            {result[1]} results
                                          </h6>
                                        )}
                                        {result[1] === 0 && (
                                          <h5 className='buttonResults'>
                                            {result[1]} results
                                          </h5>
                                        )}
                                      </>
                                    </div>
                                    <button
                                      className='buttonResults'
                                      onClick={() => {
                                        handleSeeResults(
                                          result[0].meta.beaconId
                                        )
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
                {props.show === 'full' && result[2] === true && (
                  <div className='datasetCardResults'>
                    <div className='tittleResults'>
                      <div className='tittle4'>
                        <img
                          className='logoBeacon'
                          src={result[0].response.organization.logoUrl}
                          alt={result[0].meta.beaconId}
                        />
                        <h2>{result[0].response.organization.name}</h2>
                      </div>
                      <div className='seeResultsContainer'>
                        <button
                          className='buttonResults'
                          onClick={() => {
                            handleSeeResults(result[0].meta.beaconId)
                          }}
                        >
                          {result[2] === true && props.show === 'full' && (
                            <h7>See results</h7>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                )}
            </>
          )
        })}

      {showDatsets === false && showResults === true && trigger2 === true && (
        <DataGrid
          getRowHeight={() => 'auto'}
          checkboxSelection
          columns={columns}
          rows={editable}
          slots={{ toolbar: CustomToolbar }}
          slotProps={{
            toolbar: {
              printOptions: { getRowsToExport: getSelectedRowsToExport }
            }
          }}
        />
      )}
    </div>
  )
}

export default TableResultsRuns
