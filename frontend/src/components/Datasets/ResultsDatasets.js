
import './ResultsDatasets.css'
import axios from "axios";
import { useState, useEffect } from 'react';

function ResultsDatasets(props) {

    const [resp, setResponse] = useState([])

    const [trigger, setTrigger] = useState(false)


    useEffect(() => {

        const apiCall = async () => {

            try {
                let res = await axios.get('https://beacons.bsc.es/beacon-network/v2.0.0/info')
                console.log(res.data.responses)
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
                        {result.meta.beaconId === 'org.ega-archive.ga4gh-approval-beacon-test' && <p>
                        This Beacon is based on synthetic data hosted at the <a id="descriptionEGA" href='https://ega-archive.org/datasets/EGAD00001003338'>EGA</a>. The dataset contains 2504 samples including genetic data based on 1K Genomes data, and 76 individual attributes and phenotypic data derived from UKBiobank.
                        </p>}
                        {result.meta.beaconId !== 'org.ega-archive.ga4gh-approval-beacon-test' && <p>{result.response.description}</p>}
                        <div className="linksBeacons">
                            {result.meta.beaconId === 'org.ega-archive.ga4gh-approval-beacon-test' &&
                                <a href="https://ega-archive.org/test-beacon-apis/cineca">Beacon API</a>}
                            {result.meta.beaconId === 'es.elixir.bsc.beacon' &&
                                <a href="https://beacons.bsc.es/beacon/v2.0.0/">Beacon API</a>}
                            {result.meta.beaconId === 'org.progenetix' &&
                                <a href="https://beacon.progenetix.org/">Beacon API</a>}

                            {result.meta.beaconId === 'es.elixir.bsc.beacon' &&
                                <a href="https://www.bsc.es/">Visit us</a>}
                            {result.meta.beaconId !== 'es.elixir.bsc.beacon' &&
                                <a href={result.response.organization.welcomeUrl}>Visit us</a>}
                            {result.meta.beaconId !== 'es.elixir.bsc.beacon' &&
                                <a href={result.response.organization.contactUrl}>Contact us</a>}
                            {result.meta.beaconId === 'es.elixir.bsc.beacon' &&
                                <a href="mailto:info@bsc.es">Contact us</a>}
                        </div>
                    </div>
                )

            })}

        </div>
    )

}

export default ResultsDatasets;