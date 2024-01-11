import './TableResultsIndividuals.css'
import '../../Dataset/BeaconInfo.css'
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
function TableResultsIndividuals (props) {
  const [showDatsets, setShowDatasets] = useState(false)

  const [showResults, setShowResults] = useState(false)

  const [arrayBeaconsIds, setArrayBeaconsIds] = useState([])
  const [rows, setRows] = useState([])
  const [ids, setIds] = useState([])

  const [resultsSelected, setResultsSelected] = useState(props.results)
  const [resultsSelectedFinal, setResultsSelectedFinal] = useState([])

  const [openDatasetArray, setOpenDataset] = useState([])

  const [editable, setEditable] = useState([])

  const [trigger, setTrigger] = useState(false)
  const [trigger2, setTrigger2] = useState(false)

  const [triggerArray, setTriggerArray] = useState([])

  const getSelectedRowsToExport = ({ apiRef }) => {
    const selectedRowIds = selectedGridRowsSelector(apiRef)
    if (selectedRowIds.size > 0) {
      return Array.from(selectedRowIds.keys())
    }

    return gridFilteredSortedRowIdsSelector(apiRef)
  }

  const handleClickDatasets = e => {
    console.log(e)

    openDatasetArray[e] = true
    console.log(openDatasetArray)
    triggerArray[e] = true
    console.log(triggerArray)
    setTrigger(!trigger)
  }

  const columns = [
    {
      field: 'id',
      headerName: 'Row',
      width: 100,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'IndividualId',
      headerName: 'Individual ID',
      width: 150,
      headerClassName: 'super-app-theme--header',
      renderCell: params => (
        <Link to={`/individuals/cross-queries/${params.row.IndividualId}`}>
          {params.row.IndividualId}
        </Link>
      )
    },
    {
      field: 'Beacon',
      headerName: 'Beacon ID',
      width: 340,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'ethnicity',
      headerName: 'ethnicity',
      width: 240,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'geographicOrigin',
      headerName: 'geographicOrigin',
      width: 250,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'interventionsOrProcedures',
      headerName: 'interventionsOrProcedures',
      width: 350,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'measures',
      headerName: 'measures',
      width: 350,
      headerClassName: 'super-app-theme--header',
      cellClass: 'pre'
    },
    {
      field: 'sex',
      headerName: 'sex',
      width: 200,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'diseases',
      headerName: 'diseases',
      width: 350,
      headerClassName: 'super-app-theme--header'
    }
    //   { field: 'pedigrees', headerName: 'pedigrees', width: 150 },
    // { field: 'treatments', headerName: 'treatments', width: 150 },
    //{ field: 'interventionsOrProcedures', headerName: 'interventionsOrProcedures', width: 150 },
    // { field: 'exposures', headerName: 'exposures', width: 150 },
    // { field: 'karyotypicSex', headerName: 'karyotypicSex', width: 150 },
  ]

  const handleSeeResults = ()=> {
 
    setResultsSelectedFinal(resultsSelected)
    console.log(resultsSelected)
    setShowResults(true)
    setShowDatasets(false)
    setTrigger(true)
  }

  useEffect(() => {
    setRows([])
    setIds([])

    resultsSelected.forEach((element, index) => {
      arrayBeaconsIds.push(element[0])
    })
    resultsSelectedFinal.forEach((element, index) => {
      if (element[1] !== undefined) {
        let eth_id = ''
        let eth_label = ''
        let stringEth = ''

        if (element[1].ethnicity !== '' && element[1].ethnicity !== undefined) {
          if (element[1].ethnicity.id !== undefined) {
            eth_id = element[1].ethnicity.id
          }

          eth_label = element[1].ethnicity.label
          stringEth = `${eth_id} / ${eth_label} `
        } else {
          stringEth = ''
        }

        let sex_id = ''
        let sex_label = ''
        let stringSex = ''

        if (element[1].sex !== '') {
          sex_id = element[1].sex.id
          sex_label = element[1].sex.label
          stringSex = `${element[1].sex.label} / ${element[1].sex.id}`
        } else {
          stringSex = ''
        }

        let geographic_id = ''
        let geographic_label = ''
        let stringGeographic = ''

        if (
          element[1].geographicOrigin !== '' &&
          element[1].geographicOrigin !== undefined
        ) {
          geographic_id = element[1].geographicOrigin.id
          geographic_label = element[1].geographicOrigin.label
          stringGeographic = `${geographic_id} / ${geographic_label}`
        } else {
          stringGeographic = ''
        }

        let measuresJson = []
        if (element[1].measures !== '' && element[1].measures !== undefined) {
          if (typeof element[1].measures === 'object') {
            element[1].measures.forEach(element2 => {
              measuresJson.push(
                JSON.stringify(element2, null, 2)
                  .replaceAll('[', '')
                  .replaceAll(']', '')
                  .replaceAll('{', '')
                  .replaceAll('}', '')
                  .replaceAll(',', '')
                  .replaceAll(' ,', '')
                  .replaceAll(', ', '')
                  .replaceAll('"', '')
              )
            })
            measuresJson = measuresJson.toString()
            measuresJson = measuresJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            measuresJson = measuresJson.replaceAll(',', '')
          } else {
            measuresJson = JSON.stringify(element[1].measures, null, 2)
              .replaceAll('[', '')
              .replaceAll(']', '')
              .replaceAll('{', '')
              .replaceAll('}', '')
              .replaceAll(',', '')
              .replaceAll(' ,', '')
              .replaceAll(', ', '')
              .replaceAll('"', '')

            measuresJson = measuresJson.toString()
            measuresJson = measuresJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            measuresJson = measuresJson.replaceAll(',', '')
          }
        }

        let interventionsProcedures = []

        if (
          element[1].interventionsOrProcedures !== '' &&
          element[1].interventionsOrProcedures !== undefined
        ) {
          if (typeof element[1].interventionsOrProcedures === 'object') {
            element[1].interventionsOrProcedures.forEach(element2 => {
              interventionsProcedures.push(
                JSON.stringify(element2, null, 2)
                  .replaceAll('[', '')
                  .replaceAll(']', '')
                  .replaceAll('{', '')
                  .replaceAll('}', '')
                  .replaceAll(',', '')
                  .replaceAll(' ,', '')
                  .replaceAll(', ', '')
                  .replaceAll('"', '')
              )
            })
            interventionsProcedures = interventionsProcedures.toString()
            interventionsProcedures = interventionsProcedures
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            interventionsProcedures = interventionsProcedures.replaceAll(
              ',',
              ''
            )
          } else {
            interventionsProcedures = JSON.stringify(
              element[1].interventionsOrProcedures,
              null,
              2
            )
              .replaceAll('[', '')
              .replaceAll(']', '')
              .replaceAll('{', '')
              .replaceAll('}', '')
              .replaceAll(',', '')
              .replaceAll(' ,', '')
              .replaceAll(', ', '')
              .replaceAll('"', '')
            interventionsProcedures = interventionsProcedures.toString()
            interventionsProcedures = interventionsProcedures
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            interventionsProcedures = interventionsProcedures.replaceAll(
              ',',
              ''
            )
          }
        }

        let diseases = []

        if (element[1].diseases !== '' && element[1].diseases !== undefined) {
          if (typeof element[1].diseases === 'object') {
            element[1].diseases.forEach(element2 => {
              diseases.push(
                JSON.stringify(element2, null, 2)
                  .replaceAll('[', '')
                  .replaceAll(']', '')
                  .replaceAll('{', '')
                  .replaceAll('}', '')
                  .replaceAll(',', '')
                  .replaceAll(' ,', '')
                  .replaceAll(', ', '')
                  .replaceAll('"', '')
              )
            })
            diseases = diseases.toString()
            diseases = diseases.replaceAll(', ', ',').replaceAll(' ,', ',')
            diseases = diseases.replaceAll(',', '')
          } else {
            diseases = JSON.stringify(element[1].diseases, null, 2)
              .replaceAll('[', '')
              .replaceAll(']', '')
              .replaceAll('{', '')
              .replaceAll('}', '')
              .replaceAll(',', '')
              .replaceAll(' ,', '')
              .replaceAll(', ', '')
              .replaceAll('"', '')
            diseases = diseases.toString()
            diseases = diseases.replaceAll(', ', ',').replaceAll(' ,', ',')
            diseases = diseases.replaceAll(',', '')
          }
        }

        rows.push({
          id: index,
          IndividualId: element[1].id,
          Beacon: element[0],
          ethnicity: stringEth,
          geographicOrigin: stringGeographic,
          interventionsOrProcedures: interventionsProcedures,
          measures: measuresJson,
          sex: stringSex,
          diseases: diseases
        })

        if (index === resultsSelectedFinal.length - 1) {
          setEditable(rows.map(o => ({ ...o })))
          setTrigger2(true)
        }
      }
    })
  }, [trigger, resultsSelectedFinal])

  useEffect(() => {
    console.log(props.resultsPerDataset)
    console.log(props.beaconsList)
    let count = 0

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

    setShowDatasets(true)
  }, [])

  return (
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

export default TableResultsIndividuals
