import './GenomicVariations.css';

import { useState, useEffect } from 'react';
import axios from "axios";

import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';

import TableResultsIndividuals from './TableResultsIndividuals';

function VariantsResults(props) {

    const [error, setError] = useState('')
    const { getStoredToken, authenticateUser } = useContext(AuthContext);
    const [logInRequired, setLoginRequired] = useState(true)
    const [messageLogin, setMessageLogin] = useState('')

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
                    if (props.start !== '') {
                        requestParameters['start'] = props.start;
                    }
                    if (props.end !== '') {
                        requestParameters['end'] = props.end;
                    }
                    if (props.variantType !== '') {
                        requestParameters['variantType'] = props.variantType;
                    }
                    if (props.alternateBases !== '') {
                        requestParameters['alternateBases'] = props.alternateBases;
                    }
                    if (props.referenceBases !== '') {
                        requestParameters['referenceBases'] = props.referenceBases;
                    }
                    if (props.aminoacid !== '') {
                        requestParameters['aminoacidChange'] = props.aminoacid;
                    }
                    if (props.geneID !== '') {
                        requestParameters['geneId'] = props.geneID;
                    }
                    if (props.assemblyId !== '') {
                        requestParameters['assemblyId'] = props.assemblyId;
                    }
                    var jsonData1 = {

                        "meta": {
                            "apiVersion": "2.0"
                        },
                        "query": {
                            "requestParameters":requestParameters,
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






                }




            } catch (error) {
                setError(error)
            }



        }
        apiCall();
    }, [])

    return (
        <div>{logInRequired === true && <h3>{messageLogin}</h3>}
            {error !== '' && <h3>Error! Please check the query and retry</h3>}
        </div>

    )
}

export default VariantsResults;