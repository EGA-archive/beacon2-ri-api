import './BeaconInfo.css'
import axios from 'axios'
import { useState, useEffect } from 'react'
import configData from '../../config.json'

function BeaconInfo (props) {
  const [resp, setResponse] = useState([])

  const [trigger, setTrigger] = useState(false)

  useEffect(() => {
    const apiCall = async () => {
      try {
        let res = await axios.get(configData.API_URL + '/info')
        resp.push(res.data)
        setTrigger(true)
      } catch (error) {
        console.log(error)
      }
    }
    apiCall()
  }, [props.trigger])

  return (
    <div>
      {resp[0] !== undefined && (
        <div className='resultsRecord'>
          <div className='datasetCard'>
            <div className='tittle'>
              <div className='tittle2'>
                {resp[0].response.organization.logoUrl !== '' && (
                  <img
                    className='logoBeacon'
                    src={resp[0].response.organization.logoUrl}
                    alt={resp[0].meta.beaconId}
                  />
                )}
                <h1>{resp[0].response.name}</h1>
              </div>
              <h2>{resp[0].response.organization.name}</h2>
            </div>
            <hr className='line'></hr>

            {!resp[0].response.description.includes('<a href') && (
              <p className='descriptionBeacon'>
                {resp[0].response.description}
              </p>
            )}
            {resp[0].response.description.includes('<a href') && (
              <p
                className='descriptionBeacon'
                dangerouslySetInnerHTML={{
                  __html: resp[0].response.description
                }}
              />
            )}
            <div className='linksBeacons'>
              {resp[0].meta.beaconId ===
                'org.ega-archive.ga4gh-approval-beacon-test' && (
                <a
                  href='https://ega-archive.org/test-beacon-apis/cineca'
                  target='_blank'
                >
                  Beacon API
                </a>
              )}
              {resp[0].meta.beaconId !==
                'org.ega-archive.ga4gh-approval-beacon-test' &&
                resp.response && (
                  <a href={resp.response.alternativeUrl} target='_blank'>
                    Beacon API
                  </a>
                )}
              {resp[0].meta.beaconId !== '' && (
                <a
                  href={resp[0].response.organization.welcomeUrl}
                  target='_blank'
                >
                  Visit us
                </a>
              )}
              {resp[0].meta.beaconId !== 'es.elixir.bsc.beacon' && (
                <a
                  href={resp[0].response.organization.contactUrl}
                  target='_blank'
                >
                  Contact us
                </a>
              )}
              {resp[0].meta.beaconId === 'es.elixir.bsc.beacon' && (
                <a href='mailto:info@bsc.es' target='_blank'>
                  Contact us
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default BeaconInfo