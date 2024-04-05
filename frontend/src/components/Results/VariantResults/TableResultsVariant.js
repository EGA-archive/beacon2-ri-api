import './TableResultsVariant.css'
import '../IndividualsResults/TableResultsIndividuals.css'
import '../../Dataset/BeaconInfo'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  DataGrid,
  GridToolbar,
  selectedGridRowsSelector,
  gridFilteredSortedRowIdsSelector,
  GridToolbarContainer,
  GridToolbarExport
} from '@mui/x-data-grid'
import ReactModal from 'react-modal'

function CustomToolbar () {
  return (
    <GridToolbarContainer>
      <GridToolbarExport />
    </GridToolbarContainer>
  )
}

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

  const columns = [
    {
      field: 'id',
      headerName: 'Row',
      width: 100,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'variantInternalId',
      headerName: 'Variant ID',
      width: 350,
      headerClassName: 'super-app-theme--header'
      // renderCell: params => (
      //   <Link to={`/g_variants/cross-queries/${params.row.variantInternalId}`}>
      //     {params.row.variantInternalId}
      //   </Link>
      // )
    },
    {
      field: 'variation',
      headerName: 'Variation',
      width: 340,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'identifiers',
      headerName: 'identifiers',
      width: 240,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'molecularAttributes',
      headerName: 'Molecular Attributes',
      width: 250,
      headerClassName: 'super-app-theme--header'
    },
    // {
    //   field: 'molecularEffects',
    //   headerName: 'Molecular Effects',
    //   width: 250,
    //   headerClassName: 'super-app-theme--header'
    // },
    {
      field: 'caseLevelData',
      headerName: 'Case Level Data',
      width: 350,
      headerClassName: 'super-app-theme--header'
    },
    // {
    //   field: 'variantLevelData',
    //   headerName: 'Variant Level Data',
    //   width: 350,
    //   headerClassName: 'super-app-theme--header',
    //   cellClass: 'pre'
    // },
    {
      field: 'frequencyInPopulations',
      headerName: 'Frequency in populations',
      width: 350,
      headerClassName: 'super-app-theme--header'
    }
    // { field: 'pedigrees', headerName: 'pedigrees', width: 150 },
    // { field: 'treatments', headerName: 'treatments', width: 150 },
    // {
    // field: 'interventionsOrProcedures',
    // headerName: 'interventionsOrProcedures',
    // width: 150
    //},
    //{ field: 'exposures', headerName: 'exposures', width: 150 },
    //{ field: 'karyotypicSex', headerName: 'karyotypicSex', width: 150 }
  ]

  const showNote = e => {
    setNote(e)
    setIsOpenModal2(true)
  }

  const handleCloseModal2 = () => {
    setIsOpenModal2(false)
  }

  useEffect(() => {
    // props.results.forEach((element, index) => {
    //   resultsJSON.push([
    //     JSON.stringify(element[1], null, 2).replace('[', '').replace(']', '')
    //   ])

    //   arrayBeaconsIds.push(element[0])
    // })
    // setTrigger2(true)
    // setStringDataToCopy(resultsJSON)
    if (props.show === 'full'){
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
        let variationJson = []
        if (element[1].variation !== '' && element[1].variation !== undefined) {
          variationJson = JSON.stringify(element[1].variation, null, 2)
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')

          variationJson = variationJson.toString()
          variationJson = variationJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          variationJson = variationJson.replaceAll(',', '')
        }

        let identifiersJson = []

        if (
          element[1].identifiers !== '' &&
          element[1].identifiers !== undefined
        ) {
          identifiersJson = JSON.stringify(element[1].identifiers, null, 2)
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')
          identifiersJson = identifiersJson.toString()
          identifiersJson = identifiersJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          identifiersJson = identifiersJson.replaceAll(',', '')
        }

        let molecularAttributesJson = []

        if (
          element[1].molecularAttributes !== '' &&
          element[1].molecularAttributes !== undefined
        ) {
          molecularAttributesJson = JSON.stringify(
            element[1].molecularAttributes,
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
          molecularAttributesJson = molecularAttributesJson.toString()
          molecularAttributesJson = molecularAttributesJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          molecularAttributesJson = molecularAttributesJson.replaceAll(',', '')
        }

        let molecularEffectsJson = []

        if (
          element[1].molecularEffects !== '' &&
          element[1].molecularEffects !== undefined
        ) {
          molecularEffectsJson = JSON.stringify(
            element[1].molecularEffects,
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
          molecularEffectsJson = molecularEffectsJson.toString()
          molecularEffectsJson = molecularEffectsJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          molecularEffectsJson = molecularEffectsJson.replaceAll(',', '')
        }

        let caseLevelDataJson = []

        if (
          element[1].caseLevelData !== '' &&
          element[1].caseLevelData !== undefined
        ) {
          caseLevelDataJson = JSON.stringify(element[1].caseLevelData, null, 2)
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')
          caseLevelDataJson = caseLevelDataJson.toString()
          caseLevelDataJson = caseLevelDataJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          caseLevelDataJson = caseLevelDataJson.replaceAll(',', '')
        }

        let variantLevelDataJson = []

        if (
          element[1].variantLevelData !== '' &&
          element[1].variantLevelData !== undefined
        ) {
          variantLevelDataJson = JSON.stringify(
            element[1].variantLevelData,
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
          variantLevelDataJson = variantLevelDataJson.toString()
          variantLevelDataJson = variantLevelDataJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          variantLevelDataJson = variantLevelDataJson.replaceAll(',', '')
        }

        let frequencyInPopulationsJson = []

        if (
          element[1].frequencyInPopulations !== '' &&
          element[1].frequencyInPopulations !== undefined
        ) {
          frequencyInPopulationsJson = JSON.stringify(
            element[1].frequencyInPopulations,
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
          frequencyInPopulationsJson = frequencyInPopulationsJson.toString()
          frequencyInPopulationsJson = frequencyInPopulationsJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          frequencyInPopulationsJson = frequencyInPopulationsJson.replaceAll(
            ',',
            ''
          )
        }

        rows.push({
          id: index,
          variantInternalId: element[1].variantInternalId,
          variation: variationJson,
          identifiers: identifiersJson,
          molecularAttributes: molecularAttributesJson,
          molecularEffects: molecularEffectsJson,
          caseLevelData: caseLevelDataJson,
          variantLevelData: variantLevelDataJson,
          frequencyInPopulations: frequencyInPopulationsJson
        })

        if (index === resultsSelectedFinal.length - 1) {
          setEditable(rows.map(o => ({ ...o })))
          setTrigger2(true)
        }
      }
    })
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
                      element[2][0] !== 1 && <h6 className='foundResult'>{element[2][0]} RESULTS</h6>}
                    {props.show === 'count' && element[2][0] === 0 && (
                      <h5 className='NotFoundResult'>{element[2][0]} RESULTS</h5>
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

export default TableResultsVariant
