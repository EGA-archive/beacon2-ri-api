import './TableResultsBiosamples.css'
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
function TableResultsBiosamples (props) {
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
      field: 'BiosampleId',
      headerName: 'Biosample ID',
      width: 150,
      headerClassName: 'super-app-theme--header',
      renderCell: params => (
        <Link to={`cross-queries/${params.row.BiosampleId}`}>
          {params.row.BiosampleId}
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
      field: 'individualId',
      headerName: 'Individual ID',
      width: 150,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'biosampleStatus',
      headerName: 'Biosample status',
      width: 240,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'collectionDate',
      headerName: 'Collection date',
      width: 250,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'collectionMoment',
      headerName: 'Collection moment',
      width: 350,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'sampleOriginType',
      headerName: 'Sample origin type',
      width: 350,
      headerClassName: 'super-app-theme--header',
      cellClass: 'pre'
    },
    {
      field: 'sampleOriginDetail',
      headerName: 'Sample origin detail',
      width: 200,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'obtentionProcedure',
      headerName: 'Obtention procedure',
      width: 300,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'tumorProgression',
      headerName: 'Tumor progression',
      width: 350,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'tumorGrade',
      headerName: 'Tumor Grade',
      width: 200,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'pathologicalStage',
      headerName: 'Pathological stage',
      width: 350,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'pathologicalTnmFinding',
      headerName: 'Pathological TNM findings',
      width: 300,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'histologicalDiagnosis',
      headerName: 'Histological diagnosis',
      width: 350,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'diagnosticMarkers',
      headerName: 'Diagnostic markers',
      width: 300,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'phenotypicFeatures',
      headerName: 'Phenotypic features',
      width: 300,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'measurements',
      headerName: 'Measurements',
      width: 300,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'sampleProcessing',
      headerName: 'Sample processing',
      width: 300,
      headerClassName: 'super-app-theme--header'
    },
    {
      field: 'sampleStorage',
      headerName: 'Sample storage',
      width: 300,
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

        let pathologicalStageJson = []

        if (
          element[1].pathologicalStage !== '' &&
          element[1].pathologicalStage !== undefined
        ) {
          if (typeof element[1].pathologicalStage === 'object') {
            element[1].pathologicalStage.forEach(element2 => {
              pathologicalStageJson.push(
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
            pathologicalStageJson = pathologicalStageJson.toString()
            pathologicalStageJson = pathologicalStageJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            pathologicalStageJson = pathologicalStageJson.replaceAll(',', '')
          } else {
            pathologicalStageJson = JSON.stringify(
              element[1].pathologicalStage,
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
            pathologicalStageJson = pathologicalStageJson.toString()
            pathologicalStageJson = pathologicalStageJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            pathologicalStageJson = pathologicalStageJson.replaceAll(',', '')
          }
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

        let histologicalDiagnosisJson = []

        if (
          element[1].histologicalDiagnosis !== '' &&
          element[1].histologicalDiagnosis !== undefined
        ) {
          if (typeof element[1].histologicalDiagnosis === 'object') {
            element[1].histologicalDiagnosis.forEach(element2 => {
              histologicalDiagnosisJson.push(
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
            histologicalDiagnosisJson = histologicalDiagnosisJson.toString()
            histologicalDiagnosisJson = histologicalDiagnosisJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            histologicalDiagnosisJson = histologicalDiagnosisJson.replaceAll(
              ',',
              ''
            )
          } else {
            histologicalDiagnosisJson = JSON.stringify(
              element[1].histologicalDiagnosis,
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
            histologicalDiagnosisJson = histologicalDiagnosisJson.toString()
            histologicalDiagnosisJson = histologicalDiagnosisJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            histologicalDiagnosisJson = histologicalDiagnosisJson.replaceAll(
              ',',
              ''
            )
          }
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

        let sampleStorageJson = []

        if (
          element[1].sampleStorage !== '' &&
          element[1].sampleStorage !== undefined
        ) {
          if (typeof element[1].sampleStorage === 'object') {
            element[1].sampleStorage.forEach(element2 => {
              sampleStorageJson.push(
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
            sampleStorageJson = sampleStorageJson.toString()
            sampleStorageJson = sampleStorageJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            sampleStorageJson = sampleStorageJson.replaceAll(',', '')
          } else {
            sampleStorageJson = JSON.stringify(
              element[1].sampleStorage,
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
            sampleStorageJson = sampleStorageJson.toString()
            sampleStorageJson = sampleStorageJson
              .replaceAll(', ', ',')
              .replaceAll(' ,', ',')
            sampleStorageJson = sampleStorageJson.replaceAll(',', '')
          }
        }

        var myObjRows = new Object()
        myObjRows.id = index
        if (element[1].id !== '') {
          myObjRows.BiosampleId = element[1].id
        }
        if (element[1].individualId !== '') {
          myObjRows.individualId = element[1].individualId
        }
        myObjRows.Beacon = element[0]

        if (stringBiosampleStatus !== '') {
          myObjRows.biosampleStatus = stringBiosampleStatus
        }
        if (stringSampleOriginType !== '') {
          myObjRows.sampleOriginType = stringSampleOriginType
        }
        if (stringSampleOriginDetail !== '') {
          myObjRows.sampleOriginDetail = stringSampleOriginDetail
        }
        if (collectionDateJson !== '') {
          myObjRows.collectionDate = collectionDateJson
        }
        if (collectionMomentJson !== '') {
          myObjRows.collectionMoment = collectionMomentJson
        }
        if (obtentionProcedureJson !== '') {
          myObjRows.obtentionProcedure = obtentionProcedureJson
        }
        if (tumorProgressionJson !== '') {
          myObjRows.tumorProgression = tumorProgressionJson
        }
        if (tumorGradeJson !== '') {
          myObjRows.tumorGrade = tumorGradeJson
        }

        if (pathologicalStageJson !== '') {
          myObjRows.pathologicalStage = pathologicalStageJson
        }

        if (pathologicalTnmFindingJson !== '') {
          myObjRows.pathologicalTnmFinding = pathologicalTnmFindingJson
        }

        if (histologicalDiagnosisJson !== '') {
          myObjRows.histologicalDiagnosis = histologicalDiagnosisJson
        }
        if (diagnosticMarkersJson !== '') {
          myObjRows.diagnosticMarkers = diagnosticMarkersJson
        }
        if (phenotypicFeaturesJson !== '') {
          myObjRows.phenotypicFeatures = phenotypicFeaturesJson
        }
        if (measurementsJson !== '') {
          myObjRows.measurements = measurementsJson
        }
        if (sampleProcessingJson !== '') {
          myObjRows.sampleProcessing = sampleProcessingJson
        }
        if (sampleStorageJson !== '') {
          myObjRows.sampleStorage = sampleStorageJson
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
                                            {datasetObject.replaceAll('_', ' ')}
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
                                          element[3][indexDataset] !== 0 &&
                                          element[3][indexDataset] !== 1 && (
                                            <h6>
                                              {element[3][indexDataset]} RESULTS
                                            </h6>
                                          )}
                                        {props.show === 'count' &&
                                          element[3][indexDataset] === 0 && (
                                            <h5>
                                              {element[3][indexDataset]} RESULTS
                                            </h5>
                                          )}
                                        {props.show === 'count' &&
                                          element[3][indexDataset] === 1 && (
                                            <h5>
                                              {element[3][indexDataset]} RESULT
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
                                          element[3][indexDataset] !== 0 &&
                                          element[3][indexDataset] !== 1 && (
                                            <h6>
                                              {element[3][indexDataset]} RESULTS
                                            </h6>
                                          )}
                                        {props.show === 'count' &&
                                          element[3][indexDataset] === 0 && (
                                            <h5>
                                              {element[3][indexDataset]} RESULTS
                                            </h5>
                                          )}
                                        {props.show === 'count' &&
                                          element[3][indexDataset] === 1 && (
                                            <h5>
                                              {element[3][indexDataset]} RESULT
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
                                        result[0].response.organization.logoUrl
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
                                        result[0].response.organization.logoUrl
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
                                        result[0].response.organization.logoUrl
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
                                      handleSeeResults(result[0].meta.beaconId)
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
                                        result[0].response.organization.logoUrl
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
                                        result[0].response.organization.logoUrl
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
                                        result[0].response.organization.logoUrl
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
                                      handleSeeResults(result[0].meta.beaconId)
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

export default TableResultsBiosamples
