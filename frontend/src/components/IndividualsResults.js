import './Individuals.css';
import '../App.css';
import { useState, useEffect } from 'react';
import axios from "axios";

import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';

import TableResultsIndividuals from './TableResultsIndividuals';

function IndividualsResults(props) {

    const [showLayout, setShowLayout] = useState(false)

    const [beaconId, setBeaconId] = useState('')

    const [error, setError] = useState(false)
    const [response, setResponse] = useState(null)
    const [numberResults, setNumberResults] = useState(0)
    const [boolean, setBoolean] = useState(false)
    const [results, setResults] = useState([])
    const [show1, setShow1] = useState(false)
    const [show2, setShow2] = useState(false)
    const [show3, setShow3] = useState(false)
    const [label, setLabel] = useState([])
    const [ident, setId] = useState([])
    const [operator, setOperator] = useState([])
    const [timeOut, setTimeOut] = useState(false)

    const [logInRequired, setLoginRequired] = useState(true)
    const [messageLogin, setMessageLogin] = useState('')

    const [limit, setLimit] = useState(0)
    const [skip, setSkip] = useState(0)

    const [skipTrigger, setSkipTrigger] = useState(0)
    const [limitTrigger, setLimitTrigger] = useState(0)

    const { getStoredToken, authenticateUser } = useContext(AuthContext);

    const [queryArray, setQueryArray] = useState([])
    const [arrayFilter, setArrayFilter] = useState([])

    const [checked, setChecked] = useState(false)

    const API_ENDPOINT = "https://beacons.bsc.es/beacon-network/v2.0.0/individuals/"

    let queryStringTerm = ''

    let keyTerm = []
    let resultsAux = []
    let obj = {}
    let res = ""


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
           
            }

            if (token === null) {
                setLoginRequired(true)
                setMessageLogin("PLEASE CREATE AN ACCOUNT AND LOG IN FOR QUERYING")
            }

            if (props.query !== null) {

                if (props.query.includes(',')) {
                    console.log("holi")
                    queryStringTerm = props.query.split(',')
                    console.log(queryStringTerm)
                    queryStringTerm.forEach((element, index) => {
                        element = element.trim()
                        if (element.includes('=') || element.includes('>') || element.includes('<') || element.includes('!') || element.includes('%')) {

                            if (element.includes('=')) {
                                queryArray[index] = element.split('=')
                                queryArray[index].push('=')
                            }
                            else if (element.includes('>')) {
                                queryArray[index] = element.split('>')
                                queryArray[index].push('>')
                            } else if (element.includes('<')) {
                                queryArray[index] = element.split('<')
                                queryArray[index].push('<')
                            } else if (element.includes('!')) {
                                queryArray[index] = element.split('!')
                                queryArray[index].push('!')
                            } else {
                                queryArray[index] = element.split('%')
                                queryArray[index].push('%')
                            }

                            console.log(queryArray)
                            const alphaNumFilter = {
                                "id": queryArray[index][0],
                                "operator": queryArray[index][2],
                                "value": queryArray[index][1],
                            }
                            arrayFilter.push(alphaNumFilter)

                        } else {

                            const filter2 = {
                                "id": element,
                                "includeDescendantTerms": props.descendantTerm
                            }
                            arrayFilter.push(filter2)
                        }
                    })
                } else {

                    if (props.query.includes('=') || props.query.includes('>') || props.query.includes('<') || props.query.includes('!') || props.query.includes('%')) {
                        if (props.query.includes('=')) {
                            queryArray[0] = props.query.split('=')
                            queryArray[0].push('=')
                        }
                        else if (props.query.includes('>')) {
                            queryArray[0] = props.query.split('>')
                            queryArray[0].push('>')
                        } else if (props.query.includes('<')) {
                            queryArray[0] = props.query.split('<')
                            queryArray[0].push('<')
                        } else if (props.query.includes('!')) {
                            queryArray[0] = props.query.split('!')
                            queryArray[0].push('!')
                        } else {
                            queryArray[0] = props.query.split('%')
                            queryArray[0].push('%')
                        }

                        const alphaNumFilter = {
                            "id": queryArray[0][0],
                            "operator": queryArray[0][2],
                            "value": queryArray[0][1],
                        }
                        arrayFilter.push(alphaNumFilter)

                    } else {
                        const filter = {
                            "id": props.query
                        }
                        arrayFilter.push(filter)
                    }


                }


            }

            try {
                console.log(props.operator)
                if (props.value !== '' && props.operator !== '' && props.ID !== '') {

                    console.log("holiii")
                    //alphanumerical query

                    const alphaNumFilter = {
                        "id": `${props.ID}`,
                        "operator": `${props.operator}`,
                        "value": `${props.value}`,
                    }

                    arrayFilter.push(alphaNumFilter)


                }

                if (props.query === null) {

                    // show all individuals

                    var jsonData1 = {

                        "meta": {
                            "apiVersion": "2.0"
                        },
                        "query": {
                            "filters": arrayFilter,
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
                    console.log(jsonData1)

                    const headers = { 'Content-type': 'application/json', 'Authorization': `Bearer ${token}` }


                    //   const headers = { 'Content-type': 'application/json', "Access-Control-Allow-Origin": "*" }
                    //res = await axios.post("https://beacons.bsc.es/beacon-network/v2.0.0/individuals/", jsonData1, { headers: headers })
                    res = await axios.post("https://beacons.bsc.es/beacon-network/v2.0.0/individuals", jsonData1)

                    // res = await axios.post("http://localhost:5050/api/individuals", jsonData1, { headers: headers })
                    console.log(res)
                    setTimeOut(true)

                    if (res.data.responseSummary.numTotalResults < 1) {
                        setError("No results. Please check the query and retry")
                        setNumberResults(0)
                        setBoolean(false)
                    }
                    else {

                        res.data.response.resultSets.forEach((element, index) => {

                            if (res.data.response.resultSets[index].resultsCount > 0) {

                                console.log(res.data.response.resultSets[index].results.length)
                                res.data.response.resultSets[index].results.forEach((element2, index2) => {
                                    let arrayResult = [res.data.response.resultSets[index].beaconId, res.data.response.resultSets[index].results[index2]]
                                    results.push(arrayResult)
                                })
                            }

                        })
            
                        setNumberResults(res.data.responseSummary.numTotalResults)
                        setBoolean(res.data.responseSummary.exists)
                    }


                } else {

                    var jsonData2 = {

                        "meta": {
                            "apiVersion": "2.0"
                        },
                        "query": {
                            "filters": arrayFilter,
                            "includeResultsetResponses": `${props.resultSets}`,
                            "pagination": {
                                "skip": skip,
                                "limit": limit
                            },
                            "testMode": false,
                            "requestedGranularity": "record",
                        }
                    }
                    jsonData2 = JSON.stringify(jsonData2)
                    console.log(jsonData2)

                    res = await axios.post("https://beacons.bsc.es/beacon-network/v2.0.0/individuals", jsonData2)
                    console.log(res)
                    setTimeOut(true)

                    if (res.data.responseSummary.numTotalResults < 1 || res.data.responseSummary.numTotalResults === undefined) {
                        setError("No results. Please check the query and retry")
                        setNumberResults(0)
                        setBoolean(false)
                    } else {
                        console.log(res.data.responseSummary.numTotalResults)
                        setNumberResults(res.data.responseSummary.numTotalResults)
                        setBoolean(res.data.responseSummary.exists)

                        res.data.response.resultSets.forEach((element, index) => {

                            if (res.data.response.resultSets[index].resultsCount > 0) {

                                console.log(res.data.response.resultSets[index].results.length)
                                res.data.response.resultSets[index].results.forEach((element2, index2) => {
                                    let arrayResult = [res.data.response.resultSets[index].beaconId, res.data.response.resultSets[index].results[index2]]
                                    results.push(arrayResult)
                                    console.log(arrayResult)
                                })

                                console.log(results)
                            }



                        })


                    }
                }

            } catch (error) {
                console.log(error)

            }
        };
        apiCall();
    }, [])



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

    const handleSkipChanges = (e) => {
        setSkip(Number(e.target.value))
    }

    const handleLimitChanges = (e) => {
        setLimit(Number(e.target.value))

    }

    const onSubmit = () => {
        setSkipTrigger(skip)
        setLimitTrigger(limit)
        setTimeOut(false)

    }
    return (
        <div>
            {logInRequired === false &&

                <div>

                    <div> {timeOut &&
                        <div>
                            <div className='selectGranularity'>
                                <h4>Granularity:</h4>
                                <button className='typeResults' onClick={handleTypeResults1}><h5>Boolean</h5></button>
                                <button className='typeResults' onClick={handleTypeResults2}><h5>Count</h5></button>
                                <button className='typeResults' onClick={handleTypeResults3}><h5>Full response</h5></button>
                            </div>
                        </div>}

                        {show3 && !error && <div>

                            <TableResultsIndividuals results={results} ></TableResultsIndividuals>
                        </div>}

                        {show3 && error && <h3>&nbsp; {error} </h3>}

                        <div className='resultsContainer'>

                            {show1 && boolean && <p className='p1'>YES</p>}
                            {show1 && !boolean && <p className='p1'>N0</p>}

                            {show2 && numberResults !== 1 && <p className='p1'>{numberResults} &nbsp; Results</p>}
                            {show2 && numberResults === 1 && <p className='p1'>{numberResults} &nbsp; Result</p>}


                        </div>
                    </div >
                </div>}
            {logInRequired === true && <h3>{messageLogin}</h3>}
        </div>

    )
}

export default IndividualsResults;