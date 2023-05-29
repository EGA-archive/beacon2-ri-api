import './CrossQueries.css';
import axios from "axios";
import { useState, useEffect } from 'react';

function CrossQueries() {
    const [valueInitial, setValueInitial] = useState('')
    const [valueFinal, setValueFinal] = useState('')
    const [IdValue, setIdValue] = useState('')
    const [error, setError] = useState('')
    const [results, setResults] = useState('')
    const [arrayResults, setArrayResults] = useState([])

    const handleChangeInitial = (e) => {
        setValueInitial(e.target.value)
    }

    const handleChangeFinal = (e) => {
        setValueFinal(e.target.value)
    }

    const handleChangeID = (e) => {
        setIdValue(e.target.value)
    }


    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            let res = await axios.get(`http://localhost:5050/api/${valueInitial}/${IdValue}/${valueFinal}`)
            console.log(res)

            if (res.data.response.resultSets[0].results.length > 0) {
                setResults(res.data.response.resultSets[0].results)
                
                res.data.response.resultSets[0].results.forEach(element => {
                    arrayResults.push(JSON.stringify(element, null, 2).replace('[', "").replace(']', ""))
                });
            } else {
                setResults(null)
            }


        } catch (error) {
            setError(error)
            console.log(error)
        }
    }


    return (<div className='divCrossQueries'>
        <form className="crossQueriesForm" onSubmit={handleSubmit}>
            <label className="originCollection">
                Pick the "origin" collection:
                <select value={valueInitial} onChange={handleChangeInitial}>
                    <option value="select">Select</option>
                    <option value="g_variants">Variant</option>
                    <option value="individuals">Individuals</option>
                    <option value="biosamples">Biosamples</option>
                    <option value="runs">Runs</option>
                    <option value="analyses">Analyses</option>
                </select>
            </label>
            <label>
                ID:
                <input className="inputId" type="text" value={IdValue} onChange={handleChangeID} />
            </label>
            <label>
                Pick the collection you want to see for the written ID:
                <select value={valueFinal} onChange={handleChangeFinal}>
                    <option value="select">Select</option>
                    <option value="g_variants">Variant</option>
                    <option value="individuals">Individuals</option>
                    <option value="biosamples">Biosamples</option>
                    <option value="runs">Runs</option>
                    <option value="analyses">Analyses</option>
                </select>
            </label>

            <button className="formButton">Submit</button>

        </form>

        {error !== '' && <h5>ERROR! Please retry</h5>}
        
        {results === null && <h5>No results found</h5>}
        {results !== null && results !== '' && arrayResults.map((result) => {
            <p>{result}</p>
        })}


    </div>

    )


}

export default CrossQueries;