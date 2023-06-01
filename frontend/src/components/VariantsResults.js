import './GenomicVariations.css';
import './Individuals.css';
import '../App.css';
import { useState, useEffect } from 'react';
import axios from "axios";

import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';

import TableResultsVariant from './TableResultsVariant';

function VariantsResults(props) {

    const [error, setError] = useState('')
    const { getStoredToken, authenticateUser } = useContext(AuthContext);
    const [logInRequired, setLoginRequired] = useState(true)
    const [messageLogin, setMessageLogin] = useState('')
    const [results, setResults] = useState([])
    const [show1, setShow1] = useState(false)
    const [show2, setShow2] = useState(false)
    const [show3, setShow3] = useState(false)

    const [numberResults, setNumberResults] = useState(0)
    const [boolean, setBoolean] = useState(false)

    const handleTypeResults1 = () => {
        setShow1(true)
        setShow2(false)
        setShow3(false)
    }

    const handleTypeResults2 = () => {
        setShow2(true)
        setShow1(false)
        setShow3(false)

    }

    const handleTypeResults3 = () => {
        setShow3(true)
        setShow1(false)
        setShow2(false)
    }

    useEffect(() => {
        console.log(props.query)

        const apiCall = async () => {

            authenticateUser()
            const token = getStoredToken()
            console.log(token)
            if (token !== 'undefined') {

                setLoginRequired(false)
            } else {
                setMessageLogin("PLEASE CREATE AN ACCOUNT AND LOG IN FOR QUERYING")
                console.log("ERROR")
            }

            if (token === null) {
                setLoginRequired(true)
                setMessageLogin("PLEASE CREATE AN ACCOUNT AND LOG IN FOR QUERYING")
                console.log("ERROR")
            }

            try {
                if (props.showBar === true) {

                    var jsonData1 = {

                        "meta": {
                            "apiVersion": "2.0"
                        },
                        "query": {
                            "requestParameters": {

                            },
                            "filters": [],
                            "includeResultsetResponses": `${props.resultSets}`,
                            "pagination": {
                                "skip": 0,
                                "limit": 0
                            },
                            "testMode": false,
                            "requestedGranularity": "record",
                        }
                    }
                    jsonData1 = JSON.stringify(jsonData1)

                    const headers = { 'Content-type': 'application/json', 'Authorization': `Bearer ${token}` }
                    const res = await axios.post("https://beacons.bsc.es/beacon-network/v2.0.0/g_variants", jsonData1)
                } else {
                    //   referenceName={referenceName} start={start} end={end} variantType={variantType} alternateBases={alternateBases} referenceBases={referenceBases} aminoacid={aminoacid} geneID={geneID} />
                    //    </div>

                    var requestParameters = {
                    }

                    if (props.referenceName !== '') {
                        requestParameters['referenceName'] = props.referenceName;
                    }
                    if (props.referenceName2 !== '') {
                        requestParameters['referenceName'] = props.referenceName2;
                    }
                    if (props.start !== '') {
                        requestParameters['start'] = props.start;
                    }
                    if (props.start2 !== '') {
                        requestParameters['start'] = props.start2;
                    }
                    if (props.end !== '') {
                        requestParameters['end'] = props.end;
                    }
                    if (props.variantType !== '') {
                        requestParameters['variantType'] = props.variantType;
                    }
                    if (props.variantType2 !== '') {
                        requestParameters['variantType'] = props.variantType2;
                    }
                    if (props.alternateBases !== '') {
                        requestParameters['alternateBases'] = props.alternateBases;
                    }
                    if (props.alternateBases2 !== '') {
                        requestParameters['alternateBases'] = props.alternateBases2;
                    }
                    if (props.referenceBases !== '') {
                        requestParameters['referenceBases'] = props.referenceBases;
                    }
                    if (props.referenceBases2 !== '') {
                        requestParameters['referenceBases'] = props.referenceBases2;
                    }
                    if (props.aminoacid !== '') {
                        requestParameters['aminoacidChange'] = props.aminoacid;
                    }
                    if (props.aminoacid2 !== '') {
                        requestParameters['aminoacidChange'] = props.aminoacid2;
                    }
                    if (props.geneID !== '') {
                        requestParameters['geneId'] = props.geneID;
                    }
                    if (props.assemblyId !== '') {
                        requestParameters['assemblyId'] = props.assemblyId;
                    }
                    if (props.assemblyId2 !== '') {
                        requestParameters['assemblyId'] = props.assemblyId2;
                    }
                    if (props.assemblyId3 !== '') {
                        requestParameters['assemblyId'] = props.assemblyId3;
                    }
                    var jsonData1 = {

                        "meta": {
                            "apiVersion": "2.0"
                        },
                        "query": {
                            "requestParameters": requestParameters,
                            "filters": [],
                            "includeResultsetResponses": 'HIT',
                            "pagination": {
                                "skip": 0,
                                "limit": 0
                            },
                            "testMode": false,
                            "requestedGranularity": "record",
                        }
                    }
                    jsonData1 = JSON.stringify(jsonData1)
                    console.log(jsonData1)
                    //const headers = { 'Content-type': 'application/json', 'Authorization': `Bearer ${token}` }
                    const res = await axios.post("https://ega-archive.org/test-beacon-apis/cineca/g_variants", jsonData1)
                    if (res.data.responseSummary.numTotalResults < 1 || res.data.responseSummary.numTotalResults === undefined) {
                        setError("No results. Please check the query and retry")
                        setNumberResults(0)
                        setBoolean(false)
                    } else {
                        console.log(res.data.responseSummary.numTotalResults)
                        props.setHideForm(true)
                        setNumberResults(res.data.responseSummary.numTotalResults)
                        setBoolean(res.data.responseSummary.exists)
                        console.log(res)
                        res.data.response.resultSets.forEach((element, index) => {

                            let arrayResult = [res.data.response.resultSets[index]]
                            results.push(arrayResult)
                            console.log(arrayResult)
                            console.log(results)
                        })

                    }
                }

            } catch (error) {
                console.log(error)
                setError(error)
            }



        }
        apiCall();
    }, [])

    return (
        <div>
            {logInRequired === true && <div className='variantsResultsError'><h3>{messageLogin}</h3></div>}
                {error !== '' && <h5 className='variantsResultsError'>Please check the query and retry</h5>}
            
            {logInRequired === false &&
                <div>
                    <div className='selectGranularity'>
                        <h4>Granularity:</h4>
                        <button className='typeResults' onClick={handleTypeResults1}><h5>Boolean</h5></button>
                        <button className='typeResults' onClick={handleTypeResults2}><h5>Count</h5></button>
                        <button className='typeResults' onClick={handleTypeResults3}><h5>Full response</h5></button>
                    </div>

                    {show3 && !error && <div>

                        <TableResultsVariant results={results} ></TableResultsVariant>
                    </div>}
                    <div className='resultsContainer'>

                        {show1 && boolean && <p className='p1'>YES</p>}
                        {show1 && !boolean && <p className='p1'>N0</p>}

                        {show2 && numberResults !== 1 && <p className='p1'>{numberResults} &nbsp; Results</p>}
                        {show2 && numberResults === 1 && <p className='p1'>{numberResults} &nbsp; Result</p>}


                    </div>
                </div>}
        </div>


    )
}

export default VariantsResults;