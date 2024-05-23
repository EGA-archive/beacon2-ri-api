import '../IndividualsResults/TableResultsIndividuals.css'
import '../../Dataset/BeaconInfo'
import * as React from 'react'
import { useState, useEffect } from 'react'
import CrossQueries from '../../CrossQueries/CrossQueries'
import { FaBars, FaEye, FaEyeSlash } from 'react-icons/fa' // Import icons from react-icons library
import { FiLayers, FiDownload } from 'react-icons/fi'

function TableResultsBiosamples (props) {
  const [showDatsets, setShowDatasets] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [resultsSelected, setResultsSelected] = useState(props.results)
  const [arrayBeaconsIds, setArrayBeaconsIds] = useState([])
  const [errorMessage, setErrorMessage] = useState('')
  const [resultsSelectedFinal, setResultsSelectedFinal] = useState([])
  const [editable, setEditable] = useState([])
  const [trigger, setTrigger] = useState(false)
  const [trigger2, setTrigger2] = useState(false)
  const [exportMenuVisible, setExportMenuVisible] = useState(false)
  const [showCrossQuery, setShowCrossQuery] = useState(false)
  const [parameterCrossQuery, setParamCrossQuery] = useState('')
  const [filteredData, setFilteredData] = useState(editable)
  const [currentPage, setCurrentPage] = useState(1)
  const [rowsPerPage] = useState(10) // You can make this dynamic if needed

  const [note, setNote] = useState('')
  const [isOpenModal2, setIsOpenModal2] = useState(false)

  const totalPages = Math.ceil(filteredData.length / rowsPerPage)

  const [filterValues, setFilterValues] = useState({
    BiosampleId: '',
    Beacon: '',
    individualId: '',
    biosampleStatus: '',
    sampleOriginType: '',
    sampleOriginDetail: '',
    collectionDate: '',
    collectionMoment: '',
    obtentionProcedure: '',
    tumorProgression: '',
    tumorGrade: '',
    pathologicalStage: '',
    pathologicalTnmFinding: '',
    histologicalDiagnosis: '',
    diagnosticMarkers: '',
    phenotypicFeatures: '',
    measurements: '',
    sampleProcessing: '',
    sampleStorage: ''
    // Add other column names here
  })

  const [menuVisible, setMenuVisible] = useState(false)

  const toggleMenu = () => {
    setMenuVisible(prevState => !prevState)
  }

  const [columnVisibility, setColumnVisibility] = useState({
    BiosampleId: true,
    Beacon: true,
    individualId: true,
    biosampleStatus: true,
    sampleOriginType: false,
    sampleOriginDetail: false,
    collectionDate: true,
    collectionMoment: true,
    obtentionProcedure: false,
    tumorProgression: false,
    tumorGrade: false,
    pathologicalStage: true,
    pathologicalTnmFinding: true,
    histologicalDiagnosis: true,
    diagnosticMarkers: false,
    phenotypicFeatures: false,
    measurements: true,
    sampleProcessing: false,
    sampleStorage: true
    // Add more columns as needed
  })
  const handleNextPage = () => {
    setCurrentPage(prevPage => Math.min(prevPage + 1, totalPages))
  }

  const handlePreviousPage = () => {
    setCurrentPage(prevPage => Math.max(prevPage - 1, 1))
  }

  const handlePageClick = pageNumber => {
    setCurrentPage(pageNumber)
  }
  const showAllColumns = () => {
    const columns = document.querySelectorAll('th')
    const rows = document.querySelectorAll('td')

    // Update column visibility state and remove hidden class for all columns
    columns.forEach(column => {
      column.classList.remove('hidden')
      const columnName = column.dataset.columnName
      setColumnVisibility(prevState => ({
        ...prevState,
        [columnName]: true
      }))
    })

    // Change the icon of all rows to the normal eye
    rows.forEach(row => {
      row.classList.remove('hidden')
    })

    setColumnVisibility(prevState => {
      const updatedVisibility = {}
      Object.keys(prevState).forEach(column => {
        updatedVisibility[column] = true
      })
      return updatedVisibility
    })
  }


  const toggleColumnVisibility = columnName => {
    const columns = document.querySelectorAll('th[data-column-name]')
    const rows = document.querySelectorAll(
      `td[data-column-name="${columnName}"]`
    )

    columns.forEach(column => {
      if (column.dataset.columnName === columnName) {
        column.classList.toggle('hidden')
      }
    })

    rows.forEach(row => {
      row.classList.toggle('hidden')
    })

    setColumnVisibility(prevVisibility => ({
      ...prevVisibility,
      [columnName]: !prevVisibility[columnName]
    }))
  }

  const handleFilterChange = (e, columnName) => {
    const { value } = e.target
    setFilterValues({ ...filterValues, [columnName]: value })

    const updatedFilteredData = editable.filter(row =>
      row[columnName].toLowerCase().includes(value.toLowerCase())
    )

    setFilteredData(updatedFilteredData)
  }

  const toggleExportMenu = () => {
    setExportMenuVisible(prevState => !prevState)
  }

  const exportToCSV = () => {
    // Ensure props.results is not null or undefined
    if (!props.results) return

    // Get all keys from the first row of props.results
    const header = Object.keys(props.results[0])

    // Convert each row to CSV format
    const csv = [
      header.join(','), // Header row
      ...props.results.map(row =>
        header
          .map(fieldName => {
            const value = row[fieldName]
            // Check if the value is an object
            if (typeof value === 'object') {
              // Stringify the object
              return JSON.stringify(value)
            } else {
              // Otherwise, return the value as is
              return value
            }
          })
          .join(',')
      )
    ].join('\n')

    // Create a blob object from the CSV content
    const blob = new Blob([csv], { type: 'text/csv' })

    // Create a URL for the blob object
    const url = window.URL.createObjectURL(blob)

    // Create a temporary <a> element to trigger the download
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'exported_data.csv')

    // Programmatically click the link to start the download
    document.body.appendChild(link)
    link.click()

    // Clean up by revoking the URL and removing the temporary <a> element
    window.URL.revokeObjectURL(url)
    document.body.removeChild(link)
  }

  const exportToJSON = () => {
    // Ensure props.results is not null or undefined
    if (!props.results) return

    // Convert the results to JSON
    const jsonString = JSON.stringify(props.results, null, 2)

    // Create a blob object from the JSON content
    const blob = new Blob([jsonString], { type: 'application/json' })

    // Create a URL for the blob object
    const url = URL.createObjectURL(blob)

    // Create a temporary <a> element to trigger the download
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'exported_data.json')

    // Programmatically click the link to start the download
    document.body.appendChild(link)
    link.click()

    // Clean up by revoking the URL and removing the temporary <a> element
    URL.revokeObjectURL(url)
    document.body.removeChild(link)
  }

  const showNote = e => {
    setNote(e)
    setIsOpenModal2(true)
  }

  const handleShowCrossQuery = e => {
    setShowCrossQuery(true)
    console.log(e.target.innerText)
    setParamCrossQuery(e.target.innerText)
  }

  useEffect(() => {
    if (props.show === 'full') {
      setResultsSelectedFinal(resultsSelected)
      setShowResults(true)
      setShowDatasets(false)
      setTrigger(true)
    }

    if (resultsSelected.length === 0) {
      setErrorMessage('NO RESULTS')
    }
    resultsSelected.forEach((element, index) => {
      arrayBeaconsIds.push(element[0])
    })

    resultsSelectedFinal.forEach((element, index) => {
      if (element[1] !== undefined) {
        let biosampleStatus_id = ''
        let biosampleStatus_label = ''
        let stringBiosampleStatus = ''

        if (
          element[1].biosampleStatus !== '' &&
          element[1].biosampleStatus !== undefined
        ) {
          if (element[1].biosampleStatus.id !== undefined) {
            biosampleStatus_id = element[1].biosampleStatus.id
          }
          if (element[1].biosampleStatus.label !== undefined) {
            biosampleStatus_label = element[1].biosampleStatus.label
          }

          stringBiosampleStatus = `${biosampleStatus_id} / ${biosampleStatus_label} `
        } else {
          stringBiosampleStatus = ''
        }

        let sampleOriginType_id = ''
        let sampleOriginType_label = ''
        let stringSampleOriginType = ''

        if (
          element[1].sampleOriginType !== '' &&
          element[1].sampleOriginType !== undefined
        ) {
          sampleOriginType_id = element[1].sampleOriginType.id
          sampleOriginType_label = element[1].sampleOriginType.label
          stringSampleOriginType = `${element[1].sampleOriginType.label} / ${element[1].sampleOriginType.id}`
        } else {
          stringSampleOriginType = ''
        }

        let sampleOriginDetail_id = ''
        let sampleOriginDetail_label = ''
        let stringSampleOriginDetail = ''

        if (
          element[1].sampleOriginDetail !== '' &&
          element[1].sampleOriginDetail !== undefined
        ) {
          sampleOriginDetail_id = element[1].sampleOriginDetail.id
          sampleOriginDetail_label = element[1].sampleOriginDetail.label
          stringSampleOriginDetail = `${sampleOriginDetail_id} / ${sampleOriginDetail_label}`
        } else {
          stringSampleOriginDetail = ''
        }

        let collectionDateJson = []
        if (
          element[1].collectionDate !== '' &&
          element[1].collectionDate !== undefined
        ) {
          if (typeof element[1].collectionDate === 'string') {
            collectionDateJson = element[1].collectionDate
          } else {
            collectionDateJson = element[1].collectionDate.toString()
          }
        }

        let collectionMomentJson = []
        if (
          element[1].collectionMoment !== '' &&
          element[1].collectionMoment !== undefined
        ) {
          if (typeof element[1].collectionMoment === 'string') {
            collectionMomentJson = element[1].collectionMoment
          }
        }

        let obtentionProcedureJson = []

        if (
          element[1].obtentionProcedure !== '' &&
          element[1].obtentionProcedure !== undefined
        ) {
          if (typeof element[1].obtentionProcedure === 'object') {
            element[1].obtentionProcedure.forEach(element2 => {
              obtentionProcedureJson.push(
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
            obtentionProcedureJson = obtentionProcedureJson.toString()
            obtentionProcedureJson = obtentionProcedureJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            obtentionProcedureJson = obtentionProcedureJson.replaceAll(',', '')
          } else {
            obtentionProcedureJson = JSON.stringify(
              element[1].obtentionProcedure,
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
            obtentionProcedureJson = obtentionProcedureJson.toString()
            obtentionProcedureJson = obtentionProcedureJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            obtentionProcedureJson = obtentionProcedureJson.replaceAll(',', '')
          }
        }

        let tumorProgressionJson = []

        if (
          element[1].tumorProgression !== '' &&
          element[1].tumorProgression !== undefined
        ) {
          if (typeof element[1].tumorProgression === 'object') {
            element[1].tumorProgression.forEach(element2 => {
              tumorProgressionJson.push(
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
            tumorProgressionJson = tumorProgressionJson.toString()
            tumorProgressionJson = tumorProgressionJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            tumorProgressionJson = tumorProgressionJson.replaceAll(',', '')
          } else {
            tumorProgressionJson = JSON.stringify(
              element[1].tumorProgression,
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
            tumorProgressionJson = tumorProgressionJson.toString()
            tumorProgressionJson = tumorProgressionJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            tumorProgressionJson = tumorProgressionJson.replaceAll(',', '')
          }
        }

        let tumorGradeJson = []

        if (
          element[1].tumorGrade !== '' &&
          element[1].tumorGrade !== undefined
        ) {
          if (typeof element[1].tumorGrade === 'object') {
            element[1].tumorGrade.forEach(element2 => {
              tumorGradeJson.push(
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
            tumorGradeJson = tumorGradeJson.toString()
            tumorGradeJson = tumorGradeJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            tumorGradeJson = tumorGradeJson.replaceAll(',', '')
          } else {
            tumorGradeJson = JSON.stringify(element[1].tumorGrade, null, 2)
              .replaceAll('[', '')
              .replaceAll(']', '')
              .replaceAll('{', '')
              .replaceAll('}', '')
              .replaceAll(',', '')
              .replaceAll(' ,', '')
              .replaceAll(', ', '')
              .replaceAll('"', '')
            tumorGradeJson = tumorGradeJson.toString()
            tumorGradeJson = tumorGradeJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            tumorGradeJson = tumorGradeJson.replaceAll(',', '')
          }
        }

        let patho_id = ''
        let patho_label = ''
        let stringPatho = ''

        if (element[1].pathologicalStage) {
          patho_id = element[1].pathologicalStage.id
          patho_label = element[1].pathologicalStage.label
          stringPatho = `${element[1].pathologicalStage.label} / ${element[1].pathologicalStage.id}`
        } else {
          stringPatho = ''
        }

        let pathologicalTnmFindingJson = []

        if (
          element[1].pathologicalTnmFinding !== '' &&
          element[1].pathologicalTnmFinding !== undefined
        ) {
          if (typeof element[1].pathologicalTnmFinding === 'object') {
            element[1].pathologicalTnmFinding.forEach(element2 => {
              pathologicalTnmFindingJson.push(
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
            pathologicalTnmFindingJson = pathologicalTnmFindingJson.toString()
            pathologicalTnmFindingJson = pathologicalTnmFindingJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            pathologicalTnmFindingJson = pathologicalTnmFindingJson.replaceAll(
              ',',
              ''
            )
          } else {
            pathologicalTnmFindingJson = JSON.stringify(
              element[1].pathologicalTnmFinding,
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
            pathologicalTnmFindingJson = pathologicalTnmFindingJson.toString()
            pathologicalTnmFindingJson = pathologicalTnmFindingJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            pathologicalTnmFindingJson = pathologicalTnmFindingJson.replaceAll(
              ',',
              ''
            )
          }
        }

        let histologicalDiagnosis_id = ''
        let histologicalDiagnosis_label = ''
        let stringHistologicalDiagnosis = ''

        if (
          element[1].histologicalDiagnosis !== '' &&
          element[1].histologicalDiagnosis !== undefined
        ) {
          histologicalDiagnosis_id = element[1].histologicalDiagnosis.id
          histologicalDiagnosis_label = element[1].histologicalDiagnosis.label
          stringHistologicalDiagnosis = `${histologicalDiagnosis_id} / ${histologicalDiagnosis_label}`
        } else {
          stringHistologicalDiagnosis = ''
        }

        let diagnosticMarkersJson = []

        if (
          element[1].diagnosticMarkers !== '' &&
          element[1].diagnosticMarkers !== undefined
        ) {
          if (typeof element[1].diagnosticMarkers === 'object') {
            element[1].diagnosticMarkers.forEach(element2 => {
              diagnosticMarkersJson.push(
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
            diagnosticMarkersJson = diagnosticMarkersJson.toString()
            diagnosticMarkersJson = diagnosticMarkersJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            diagnosticMarkersJson = diagnosticMarkersJson.replaceAll(',', '')
          } else {
            diagnosticMarkersJson = JSON.stringify(
              element[1].diagnosticMarkers,
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
            diagnosticMarkersJson = diagnosticMarkersJson.toString()
            diagnosticMarkersJson = diagnosticMarkersJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            diagnosticMarkersJson = diagnosticMarkersJson.replaceAll(',', '')
          }
        }

        let phenotypicFeaturesJson = []

        if (
          element[1].phenotypicFeatures !== '' &&
          element[1].phenotypicFeatures !== undefined
        ) {
          if (typeof element[1].phenotypicFeatures === 'object') {
            element[1].phenotypicFeatures.forEach(element2 => {
              phenotypicFeaturesJson.push(
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
            phenotypicFeaturesJson = phenotypicFeaturesJson.toString()
            phenotypicFeaturesJson = phenotypicFeaturesJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            phenotypicFeaturesJson = phenotypicFeaturesJson.replaceAll(',', '')
          } else {
            phenotypicFeaturesJson = JSON.stringify(
              element[1].phenotypicFeatures,
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
            phenotypicFeaturesJson = phenotypicFeaturesJson.toString()
            phenotypicFeaturesJson = phenotypicFeaturesJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            phenotypicFeaturesJson = phenotypicFeaturesJson.replaceAll(',', '')
          }
        }

        let measurementsJson = []

        if (
          element[1].measurements !== '' &&
          element[1].measurements !== undefined
        ) {
          if (typeof element[1].measurements === 'object') {
            element[1].measurements.forEach(element2 => {
              measurementsJson.push(
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
            measurementsJson = measurementsJson.toString()
            measurementsJson = measurementsJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            measurementsJson = measurementsJson.replaceAll(',', '')
          } else {
            measurementsJson = JSON.stringify(element[1].measurements, null, 2)
              .replaceAll('[', '')
              .replaceAll(']', '')
              .replaceAll('{', '')
              .replaceAll('}', '')
              .replaceAll(',', '')
              .replaceAll(' ,', '')
              .replaceAll(', ', '')
              .replaceAll('"', '')
            measurementsJson = measurementsJson.toString()
            measurementsJson = measurementsJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            measurementsJson = measurementsJson.replaceAll(',', '')
          }
        }

        let sampleProcessingJson = []

        if (
          element[1].sampleProcessing !== '' &&
          element[1].sampleProcessing !== undefined
        ) {
          if (typeof element[1].sampleProcessing === 'object') {
            element[1].sampleProcessing.forEach(element2 => {
              sampleProcessingJson.push(
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
            sampleProcessingJson = sampleProcessingJson.toString()
            sampleProcessingJson = sampleProcessingJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            sampleProcessingJson = sampleProcessingJson.replaceAll(',', '')
          } else {
            sampleProcessingJson = JSON.stringify(
              element[1].sampleProcessing,
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
            sampleProcessingJson = sampleProcessingJson.toString()
            sampleProcessingJson = sampleProcessingJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            sampleProcessingJson = sampleProcessingJson.replaceAll(',', '')
          }
        }

        let sampleStorage_id = ''
        let sampleStorage_label = ''
        let stringSampleStorage = ''

        if (
          element[1].sampleStorage !== '' &&
          element[1].sampleStorage !== undefined
        ) {
          sampleStorage_id = element[1].sampleStorage.id
          sampleStorage_label = element[1].sampleStorage.label
          stringSampleStorage = `${sampleStorage_id} / ${sampleStorage_label}`
        } else {
          stringSampleStorage = ''
        }

        editable.push({
          id: index,
          Beacon: element[0],
          BiosampleId: element[1].id,
          individualId: element[1].individualId,
          biosampleStatus: stringBiosampleStatus,
          sampleOriginType: stringSampleOriginType,
          //  sampleOriginDetail: stringSampleOriginDetail,
          collectionDate: collectionDateJson,
          collectionMoment: collectionMomentJson,
          //  obtentionProcedure: obtentionProcedureJson,
          //  tumorProgression: tumorProgressionJson,
          //tumorGrade: tumorGradeJson,
          pathologicalStage: stringPatho,
          pathologicalTnmFinding: pathologicalTnmFindingJson,
          histologicalDiagnosis: stringHistologicalDiagnosis,
          //    diagnosticMarkers: diagnosticMarkersJson,
          //    phenotypicFeatures: phenotypicFeaturesJson,
          measurements: measurementsJson,
          //  sampleProcessing: sampleProcessingJson,
          sampleStorage: stringSampleStorage
        })

        if (index === resultsSelectedFinal.length - 1) {
          setTrigger2(true)
        }
      }
    })
  }, [trigger, resultsSelectedFinal])

  useEffect(() => {
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
                      {element[1][index] === true &&
                        props.show === 'boolean' && (
                          <h6 className='foundResult'>YES</h6>
                        )}
                      {element[1][index] === false &&
                        props.show === 'boolean' && (
                          <h5 className='NotFoundResult'>No, sorry</h5>
                        )}
                      {props.show === 'count' &&
                        element[2][index] !== 0 &&
                        element[2][index] !== 1 && (
                          <h6 className='foundResult'>
                            {element[2][index]} RESULTS
                          </h6>
                        )}
                      {props.show === 'count' && element[2][index] === 0 && (
                        <h5 className='NotFoundResult'>
                          {element[2][index]} RESULTS
                        </h5>
                      )}
                      {props.show === 'count' && element[2][index] === 1 && (
                        <h6 className='foundResult'>
                          {element[2][index]} RESULT
                        </h6>
                      )}
                    </>
                  )
                })}
            </>
          )
        })}

      {!showCrossQuery &&
        showDatsets === false &&
        showResults === true &&
        trigger2 === true && (
          <div className='table-container'>
            <div className='menu-icon-container'>
              <div className='export-menu'>
                <button className='exportButton' onClick={toggleExportMenu}>
                  <FiDownload />
                </button>
                {exportMenuVisible && (
                  <>
                    <ul className='column-list'>
                      <li onClick={exportToJSON}>Export to JSON</li>
                      <li onClick={exportToCSV}>Export to CSV</li>
                    </ul>
                  </>
                )}
              </div>
              <div className='menu-container'>
                <FaBars onClick={toggleMenu} />
                {menuVisible && (
                  <>
                    <ul className='column-list'>
                      <li onClick={showAllColumns}>
                        Show All Columns
                        <FiLayers />
                      </li>
                      {Object.keys(columnVisibility).map(column => (
                        <li
                          key={column}
                          onClick={() => toggleColumnVisibility(column)}
                        >
                          {column}
                          {columnVisibility[column] ? (
                            <FaEye />
                          ) : (
                            <FaEyeSlash />
                          )}
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            </div>
            <div className='header-container'>
              <table className='tableResults'>
                <thead className='theadResults'>
                  <tr>
                    <th
                      className={`sticky-header ${
                        columnVisibility.BiosampleId ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Biosample Id</span>
                      <button
                        onClick={() => toggleColumnVisibility('BiosampleId')}
                      >
                        {columnVisibility.BiosampleId ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter Biosample ID'
                        onChange={e => handleFilterChange(e, 'BiosampleId')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.individualId ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Individual Id</span>
                      <button
                        onClick={() => toggleColumnVisibility('individualId')}
                      >
                        {columnVisibility.individualId ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter individual Id'
                        onChange={e => handleFilterChange(e, 'individualId')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.Beacon ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Beacon</span>
                      <button onClick={() => toggleColumnVisibility('Beacon')}>
                        {columnVisibility.Beacon ? <FaEye /> : <FaEyeSlash />}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter Beacon'
                        onChange={e => handleFilterChange(e, 'Beacon')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.biosampleStatus ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Biosample Status</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('biosampleStatus')
                        }
                      >
                        {columnVisibility.biosampleStatus ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter biosample status'
                        onChange={e => handleFilterChange(e, 'biosampleStatus')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.sampleOriginType ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Sample Origin Type</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('sampleOriginType')
                        }
                      >
                        {columnVisibility.sampleOriginType ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter sample origin type'
                        onChange={e =>
                          handleFilterChange(e, 'sampleOriginType')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.sampleOriginDetail
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Sample Origin Detail</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('sampleOriginDetail')
                        }
                      >
                        {columnVisibility.sampleOriginDetail ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter sample origin detail'
                        onChange={e =>
                          handleFilterChange(e, 'sampleOriginDetail')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.collectionDate ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Collection Date</span>
                      <button
                        onClick={() => toggleColumnVisibility('collectionDate')}
                      >
                        {columnVisibility.collectionDate ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter case level data'
                        onChange={e => handleFilterChange(e, 'collectionDate')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.collectionMoment ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Collection Moment</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('collectionMoment')
                        }
                      >
                        {columnVisibility.collectionMoment ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter collection moment'
                        onChange={e =>
                          handleFilterChange(e, 'collectionMoment')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.obtentionProcedure
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Obtention Procedure</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('obtentionProcedure')
                        }
                      >
                        {columnVisibility.obtentionProcedure ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter obtention procedure'
                        onChange={e =>
                          handleFilterChange(e, 'obtentionProcedure')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.tumorProgression ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Tumor Progression</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('tumorProgression')
                        }
                      >
                        {columnVisibility.tumorProgression ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter tumor progression'
                        onChange={e =>
                          handleFilterChange(e, 'tumorProgression')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.tumorGrade ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Tumor Grade</span>
                      <button
                        onClick={() => toggleColumnVisibility('tumorGrade')}
                      >
                        {columnVisibility.tumorGrade ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter tumor grade'
                        onChange={e => handleFilterChange(e, 'tumorGrade')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.pathologicalStage
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Pathological Stage</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('pathologicalStage')
                        }
                      >
                        {columnVisibility.pathologicalStage ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter pathological stage'
                        onChange={e =>
                          handleFilterChange(e, 'pathologicalStage')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.pathologicalTnmFinding
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Pathological Tnm Finding</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('pathologicalTnmFinding')
                        }
                      >
                        {columnVisibility.pathologicalTnmFinding ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter pathological Tnm finding'
                        onChange={e =>
                          handleFilterChange(e, 'pathologicalTnmFinding')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.histologicalDiagnosis
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Histological Diagnosis</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('histologicalDiagnosis')
                        }
                      >
                        {columnVisibility.histologicalDiagnosis ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter histological diagnosis'
                        onChange={e =>
                          handleFilterChange(e, 'histologicalDiagnosis')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.diagnosticMarkers
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Diagnostic Markers</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('diagnosticMarkers')
                        }
                      >
                        {columnVisibility.diagnosticMarkers ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter diagnostic markers'
                        onChange={e =>
                          handleFilterChange(e, 'diagnosticMarkers')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.phenotypicFeatures
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Phenotypic Features</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('phenotypicFeatures')
                        }
                      >
                        {columnVisibility.phenotypicFeatures ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter phenotypic features'
                        onChange={e =>
                          handleFilterChange(e, 'phenotypicFeatures')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.measurements ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Measurements</span>
                      <button
                        onClick={() => toggleColumnVisibility('measurements')}
                      >
                        {columnVisibility.measurements ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter measurements'
                        onChange={e => handleFilterChange(e, 'measurements')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.sampleProcessing ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Sample Processing</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('sampleProcessing')
                        }
                      >
                        {columnVisibility.sampleProcessing ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter sample processing'
                        onChange={e =>
                          handleFilterChange(e, 'sampleProcessing')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.sampleStorage ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Sample Storage</span>
                      <button
                        onClick={() => toggleColumnVisibility('sampleStorage')}
                      >
                        {columnVisibility.sampleStorage ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter sample storage'
                        onChange={e => handleFilterChange(e, 'sampleStorage')}
                      />
                    </th>

                    {/* Add more column headers here */}
                  </tr>
                </thead>
              </table>
            </div>
            <div className='body-container'>
              <table className='tableResults'>
                <tbody>
                  {filteredData.map((row, index) => (
                    <tr key={index}>
                      <td
                        className={
                          columnVisibility.BiosampleId ? 'visible' : 'hidden'
                        }
                      >
                        {row.BiosampleId}
                      </td>
                      <td
                        className={
                          columnVisibility.individualId ? 'visible' : 'hidden'
                        }
                      >
                        {row.individualId}
                      </td>
                      <td
                        className={
                          columnVisibility.Beacon ? 'visible' : 'hidden'
                        }
                      >
                        {row.Beacon}
                      </td>
                      <td
                        className={
                          columnVisibility.biosampleStatus
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.biosampleStatus}
                      </td>
                      <td
                        className={
                          columnVisibility.sampleOriginType
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.sampleOriginType}
                      </td>
                      <td
                        className={
                          columnVisibility.sampleOriginDetail
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.sampleOriginDetail}
                      </td>
                      <td
                        className={
                          columnVisibility.collectionDate ? 'visible' : 'hidden'
                        }
                      >
                        {row.collectionDate}
                      </td>
                      <td
                        className={
                          columnVisibility.collectionMoment
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.collectionMoment}
                      </td>
                      <td
                        className={
                          columnVisibility.obtentionProcedure
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.obtentionProcedure}
                      </td>
                      <td
                        className={
                          columnVisibility.tumorProgression
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.tumorProgression}
                      </td>
                      <td
                        className={
                          columnVisibility.tumorGrade ? 'visible' : 'hidden'
                        }
                      >
                        {row.tumorGrade}
                      </td>
                      <td
                        className={
                          columnVisibility.pathologicalStage
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.pathologicalStage}
                      </td>
                      <td
                        className={
                          columnVisibility.pathologicalTnmFinding
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.pathologicalTnmFinding}
                      </td>
                      <td
                        className={
                          columnVisibility.histologicalDiagnosis
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.histologicalDiagnosis}
                      </td>
                      <td
                        className={
                          columnVisibility.diagnosticMarkers
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.diagnosticMarkers}
                      </td>
                      <td
                        className={
                          columnVisibility.phenotypicFeatures
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.phenotypicFeatures}
                      </td>
                      <td
                        className={
                          columnVisibility.measurements ? 'visible' : 'hidden'
                        }
                      >
                        {row.measurements}
                      </td>
                      <td
                        className={
                          columnVisibility.sampleProcessing
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.sampleProcessing}
                      </td>
                      <td
                        className={
                          columnVisibility.sampleStorage ? 'visible' : 'hidden'
                        }
                      >
                        {row.sampleStorage}
                      </td>

                      {/* Render other row cells here */}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      <div className='pagination-controls'>
        <button onClick={handlePreviousPage} disabled={currentPage === 1}>
          Previous
        </button>
        {[...Array(totalPages)].map((_, index) => (
          <button
            key={index}
            onClick={() => handlePageClick(index + 1)}
            className={currentPage === index + 1 ? 'active' : ''}
          >
            {index + 1}
          </button>
        ))}
        <button onClick={handleNextPage} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
      {showCrossQuery && (
        <CrossQueries
          parameter={parameterCrossQuery}
          collection={'individuals'}
          setShowCrossQuery={setShowCrossQuery}
        />
      )}
    </div>
  )
}

export default TableResultsBiosamples
