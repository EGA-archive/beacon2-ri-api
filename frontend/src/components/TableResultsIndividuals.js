
import './TableResultsIndividuals.css'
import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

function TableResultsIndividuals(props) {

    const columns = [
        { field: 'id', headerName: 'Id', width: 100 , headerClassName: 'super-app-theme--header'},
        { field: 'ethnicity', headerName: 'ethnicity', width: 200 , headerClassName: 'super-app-theme--header'},
        { field: 'geographicOrigin', headerName: 'geographicOrigin', width: 150 , headerClassName: 'super-app-theme--header'},
        { field: 'interventionsOrProcedures', headerName: 'interventionsOrProcedures', width: 200 , headerClassName: 'super-app-theme--header'},
        { field: 'measures', headerName: 'measures', width: 290 , headerClassName: 'super-app-theme--header'},
        { field: 'sex', headerName: 'sex', width: 150 , headerClassName: 'super-app-theme--header'},
        { field: 'diseases', headerName: 'diseases', width: 200, headerClassName: 'super-app-theme--header' },
     //   { field: 'pedigrees', headerName: 'pedigrees', width: 150 },
       // { field: 'treatments', headerName: 'treatments', width: 150 },
        //{ field: 'interventionsOrProcedures', headerName: 'interventionsOrProcedures', width: 150 },
       // { field: 'exposures', headerName: 'exposures', width: 150 },
       // { field: 'karyotypicSex', headerName: 'karyotypicSex', width: 150 },
    ]
    console.log(props.results)
    const rows = []
    props.results.forEach(element => {
        let  eth_id = ''
        let eth_label = ''
        let stringEth = ''

        if (element.ethnicity !== '' && element.ethnicity !== undefined){
            if(element.ethnicity.id !== undefined){
                eth_id = element.ethnicity.id
            }
            
            
          
            eth_label = element.ethnicity.label
            stringEth = eth_id + '/' + eth_label 
        } else{
            stringEth = ''
        }

        let sex_id = ''
        let sex_label = ''
        let stringSex= ''

        if (element.sex !== ''){
            sex_id = element.sex.id
            sex_label = element.sex.label
            stringSex= element.sex.label + '/' + element.sex.id
    
       } else{
           stringSex = ''
       }

   


 
        rows.push({ id: element.id, ethnicity: stringEth ,geographicOrigin: '', interventionsOrProcedures: '', measures: '', sex: stringSex, diseases:''})



    })


    return (
        <DataGrid
            columns={columns}
            rows={rows}
        />
    )

}





export default TableResultsIndividuals;