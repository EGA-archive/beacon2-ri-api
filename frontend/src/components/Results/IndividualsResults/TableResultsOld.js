import './TableResultsIndividuals.css'
import * as React from 'react'
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid'

function TableResultsIndividuals (props) {
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
      headerClassName: 'super-app-theme--header'
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

  const rows = []
  const ids = []
  props.results.forEach((element, index) => {
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
                .replace('[', '')
                .replace(']', '')
            )
          })
        } else {
          measuresJson = JSON.stringify(element[1].measures, null, 2)
            .replace('[', '')
            .replace(']', '')
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
                .replace('[', '')
                .replace(']', '')
            )
          })
        } else {
          interventionsProcedures = JSON.stringify(
            element[1].interventionsOrProcedures,
            null,
            2
          )
            .replace('[', '')
            .replace(']', '')
        }
      }

      let diseases = []

      if (element[1].diseases !== '' && element[1].diseases !== undefined) {
        if (typeof element[1].diseases === 'object') {
          element[1].diseases.forEach(element2 => {
            diseases.push(
              JSON.stringify(element2, null, 2)
                .replace('[', '')
                .replace(']', '')
            )
          })
        } else {
          diseases = JSON.stringify(element[1].diseases, null, 2)
            .replace('[', '')
            .replace(']', '')
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
    }
  })

  return <DataGrid getRowHeight={() => 'auto'} columns={columns} rows={rows} />
}

export default TableResultsIndividuals
