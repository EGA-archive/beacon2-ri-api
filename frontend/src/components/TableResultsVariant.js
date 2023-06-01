import './TableResultsVariant.css'
import { useState, useEffect } from 'react';

function TableResultsIndividuals(props) {

    const [resultsJSON, setResultsJSON] = useState([])

    useEffect(() => {
        props.results.forEach(element => {
            console.log(element)
            resultsJSON.push(JSON.stringify(element, null, 2).replace('[', "").replace(']', ""))
           
        })
        console.log(resultsJSON)
    }, [])


    return (<div className='variantsResult'>
      <pre className='preCrossQueries'><p>{resultsJSON}</p></pre>
    </div>)
}

export default TableResultsIndividuals