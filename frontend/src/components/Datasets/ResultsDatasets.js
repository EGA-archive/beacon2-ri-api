
import './ResultsDatasets.css'
import axios from "axios";
import { useState, useEffect } from 'react';
import configData from "../../config.json";

function ResultsDatasets(props) {

    const [resp, setResponse] = useState([])

    const [trigger, setTrigger] = useState(false)


    useEffect(() => {

        const apiCall = async () => {

            try {
                let res = await axios.get(configData.API_URL +'/info')
                res.data.responses.forEach(element => {
                    resp.push(element)
                });
                setTrigger(true)
                resp.reverse()
            } catch (error) {
                console.log(error)
            }
        }
        apiCall()

    }, [props.trigger])

    return (

        <div className='resultsRecord'>

            {resp.map((result) => {
                return (
                    <div className="datasetCard">
                        <div className='tittle'>
                            <div className="tittle2">
                                <img className="logoBeacon" src={result.response.organization.logoUrl} alt={result.meta.beaconId} />
                                <h1>{result.response.name}</h1>
                            </div>
                            <h2>{result.response.organization.name}</h2>
                        </div>
                        <hr className='line'></hr>
                        {!result.response.description.includes('<a href') && <p>{result.response.description}</p>}
                        {result.response.description.includes('<a href') && <p dangerouslySetInnerHTML={{__html: result.response.description}}/>}
                        <div className="linksBeacons">
                            {result.meta.beaconId === 'org.ega-archive.ga4gh-approval-beacon-test' &&
                                <a href="https://beacon-apis-demo.ega-archive.org/api" target="_blank" rel="noreferrer" >Beacon API</a>}
                            {result.meta.beaconId === 'es.elixir.bsc.beacon' &&
                                <a href="https://beacons.bsc.es/beacon/v2.0.0/" target="_blank" rel="noreferrer" >Beacon API</a>}
                            {result.meta.beaconId === 'org.progenetix' &&
                                <a href="https://beaconplus.progenetix.org/" target="_blank" rel="noreferrer">Beacon API</a>}
                            {result.meta.beaconId !== 'es.elixir.bsc.beacon' && result.meta.beaconId !== 'org.progenetix'  && result.meta.beaconId !== 'org.ega-archive.ga4gh-approval-beacon-test' &&
                                <a href={result.response.alternativeUrl} target="_blank" rel="noreferrer">Beacon API</a>}
                            {result.meta.beaconId === 'es.elixir.bsc.beacon' &&
                                <a href="https://www.bsc.es/" target="_blank" rel="noreferrer">Visit us</a>}
                            {result.meta.beaconId !== 'es.elixir.bsc.beacon' &&
                                <a href={result.response.organization.welcomeUrl} target="_blank" rel="noreferrer">Visit us</a>}
                            {result.meta.beaconId !== 'es.elixir.bsc.beacon' &&
                                <a href={result.response.organization.contactUrl} target="_blank" rel="noreferrer">Contact us</a>}
                            {result.meta.beaconId === 'es.elixir.bsc.beacon' &&
                                <a href="mailto:info@bsc.es" target="_blank" rel="noreferrer">Contact us</a>}
                        </div>
                    </div>
                )

            })}

        </div>
    )

}

export default ResultsDatasets;