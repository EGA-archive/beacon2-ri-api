import '../IndividualsResults/TableResultsIndividuals.css'
import '../../Dataset/BeaconInfo.css'
import './TableResultsBiosamples.css'
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

  const handleSeeResults = () => {
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
      console.log(element)
      if (element[1] !== undefined) {
        console.log(element[0])
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

          biosampleStatus_label = element[1].biosampleStatus.label
          stringBiosampleStatus = `${biosampleStatus_id} / ${biosampleStatus_label} `
        } else {
          stringBiosampleStatus = ''
        }

        let sampleOriginType_id = ''
        let sampleOriginType_label = ''
        let stringSampleOriginType = ''

        if (element[1].sampleOriginType !== '') {
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

        console.log(stringSampleOriginDetail)
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
        console.log(rows)

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
    console.log(arrayBeaconsIds)
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
                                          handleSeeResults()
                                        }}
                                      >
                                        <h7 className='seeResultsButton'>
                                          {' '}
                                          SEE RESULTS
                                        </h7>
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

export default TableResultsBiosamples
