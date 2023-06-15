import './TableResultsVariant.css'
import { useState, useEffect } from 'react';

function TableResultsIndividuals(props) {

    const [resultsJSON, setResultsJSON] = useState([])
    const [results, setResults] = useState('')
    useEffect(() => {
        
        props.results.forEach((element,index) => {

            element.forEach(element2 => {
                console.log(element2)
                element2[1].results.forEach(element3 => {
                    resultsJSON.push([element2[0],JSON.stringify(element3, null, 2).replace('[', "").replace(']', "")])
                })


            })


        })
        console.log(resultsJSON)
    }, [])


    return (
        <div>
            {results !== '' && <div>
                <pre className='preCrossQueries'><p>{resultsJSON}</p></pre>
            </div>}
        </div>
    )
}

export default TableResultsIndividuals