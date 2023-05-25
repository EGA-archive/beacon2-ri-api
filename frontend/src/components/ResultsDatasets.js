
import './ResultsDatasets.css'
import axios from "axios";
import { useState, useEffect } from 'react';

function ResultsDatasets(props) {
    
    const [resp, setResponse] = useState([])

  

    useEffect(() => {

        const apiCall = async () => {

            try {
                let res = await axios.get('https://beacons.bsc.es/beacon-network/v2.0.0/info')
                res.data.responses.forEach(element => {
                    resp.push(element)
                });

            } catch (error) {
                console.log(error)
            }
        }
        apiCall()

    }, [])


    return (
        <div className='resultsRecord'>

            {resp.map((result) => {
                return (
                    <div className="datasetCard">
                        <div className='tittle'>
                            <img className="logoBeacon" src={result.response.organization.logoUrl} alt={result.meta.beaconId} />
                            <h1>{result.response.name}</h1>
                            <h2>{result.response.organization.name}</h2>
                        </div>
                        <hr className='line'></hr>
                        <p>{result.response.description}</p>
                        {result.meta.beaconId === 'org.ega-archive.ga4gh-approval-beacon-test' &&
                            <a href="https://ega-archive.org/test-beacon-apis/cineca">Beacon API</a>}
                        {result.meta.beaconId === 'es.elixir.bsc.beacon' &&
                            <a href="https://beacons.bsc.es/beacon/v2.0.0/">Beacon API</a>}
                        {result.meta.beaconId === 'org.progenetix' &&
                            <a href="https://beacon.progenetix.org/">Beacon API</a>}
                        <a href={result.response.organization.welcomeUrl}>Visit us</a>
                        <a href={result.response.organization.contactUrl}>Contact us</a>
                    </div>
                )

            })}

        </div>
    )

}

export default ResultsDatasets;