import './TableResultsIndividuals.css'
import '../../Dataset/BeaconInfo'
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
import ReactModal from 'react-modal'
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
  const [openDatasetArray2, setOpenDataset2] = useState([])

  const [editable, setEditable] = useState([])

  const [trigger, setTrigger] = useState(false)
  const [trigger2, setTrigger2] = useState(false)

  const [triggerArray, setTriggerArray] = useState([])
  const [triggerArray2, setTriggerArray2] = useState([])

  const [errorMessage, setErrorMessage] = useState('')
  const [note, setNote] = useState('')
  const [isOpenModal2, setIsOpenModal2] = useState(false)

  const getSelectedRowsToExport = ({ apiRef }) => {
    const selectedRowIds = selectedGridRowsSelector(apiRef)
    if (selectedRowIds.size > 0) {
      return Array.from(selectedRowIds.keys())
    }

    return gridFilteredSortedRowIdsSelector(apiRef)
  }

  const showNote = e => {
    setNote(e)
    setIsOpenModal2(true)
  }

  const columns = [
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
      field: 'ethnicity',
      headerName: 'ethnicity',
      width: 240,
      headerClassName: 'super-app-theme--header'
    },
    // {
    //   field: 'geographicOrigin',
    //   headerName: 'geographicOrigin',
    //   width: 250,
    //   headerClassName: 'super-app-theme--header'
    // },
    {
      field: 'interventionsOrProcedures',
      headerName: 'interventionsOrProcedures',
      width: 350,
      headerClassName: 'super-app-theme--header'
    },
    // {
    //   field: 'measures',
    //   headerName: 'measures',
    //   width: 350,
    //   headerClassName: 'super-app-theme--header',
    //   cellClass: 'pre'
    // },
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
    },
    // { field: 'pedigrees', headerName: 'pedigrees', width: 150 },
    { field: 'treatments', headerName: 'treatments', width: 150 },
    {
      field: 'interventionsOrProcedures',
      headerName: 'interventionsOrProcedures',
      width: 150
    }
    //{ field: 'exposures', headerName: 'exposures', width: 150 },
    //{ field: 'karyotypicSex', headerName: 'karyotypicSex', width: 150 }
  ]

  const handleCloseModal2 = () => {
    setIsOpenModal2(false)
  }

  useEffect(() => {
    if (props.show === 'full') {
      setResultsSelectedFinal(resultsSelected)
      setShowResults(true)
      setShowDatasets(false)
      setTrigger(true)
    }
    setRows([])
    setIds([])
    if (resultsSelected.length === 0) {
      setErrorMessage('NO RESULTS')
    }
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
          interventionsOrProcedures: interventionsProcedures,
          //measures: measuresJson,
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
    props.resultsPerDataset.forEach(element => {
      console.log(element[3])
    })
    setShowDatasets(true)
  }, [])

  return (
    <div className='containerBeaconResults'>
      {showDatsets === true &&
        props.beaconsList.map(result => {
          return (
            <>
              {props.show !== 'full' &&
                props.resultsPerDataset.map((element, index) => {
                  return (
                    <>
                      {element[1][0] === true && props.show === 'boolean' && (
                        <h6 className='foundResult'>FOUND</h6>
                      )}
                      {element[1][0] === false && props.show === 'boolean' && (
                        <h5 className='NotFoundResult'>NOT FOUND</h5>
                      )}
                      {props.show === 'count' &&
                        element[2][0] !== 0 &&
                        element[2][0] !== 1 && (
                          <h6 className='foundResult'>
                            {element[2][0]} RESULTS
                          </h6>
                        )}
                      {props.show === 'count' && element[2][0] === 0 && (
                        <h5 className='NotFoundResult'>
                          {element[2][0]} RESULTS
                        </h5>
                      )}
                      {props.show === 'count' && element[2][0] === 1 && (
                        <h6 className='foundResult'>{element[2][0]} RESULT</h6>
                      )}
                    </>
                  )
                })}
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
