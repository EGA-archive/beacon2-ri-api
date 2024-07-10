import './BeaconInfo.css'
import axios from 'axios'
import { useState, useEffect } from 'react'
import configData from '../../config.json'

function BeaconInfo (props) {
  const [resp, setResponse] = useState([])
  const [isNetwork, setIsNetwork] = useState(false)
  const [trigger, setTrigger] = useState(false)
  const [error, setError] = useState(null)
  useEffect(() => {
    const apiCall = async () => {
      try {
        if (props.isNetwork) {
          let res = await axios.get(configData.API_URL + '/info')
          res.data.responses.forEach(element => {
            resp.push(element)
          })
          resp.forEach((element, index) => {
            if (
              element.meta.beaconId ===
              'org.ega-archive.ga4gh-approval-beacon-test'
            ) {
              resp.splice(index, 1)
              resp.push(element)
              resp.reverse()
            }
          })
        } else {
          let res = await axios.get(configData.API_URL + '/info')
          resp.push(res.data)
        }

        setTrigger(true)
      } catch (error) {}
    }
    apiCall()
  }, [props.trigger])

  useEffect(() => {
    const fetchData = async () => {
      try {
        let res2 = await axios.get(configData.API_URL + '/info')

        if (res2.data.meta.isAggregated) {
          setIsNetwork(true)

          res2.data.responses.forEach(element => {
            resp.push(element)
          })
          resp.forEach((element, index) => {
            if (
              element.meta.beaconId ===
              'org.ega-archive.ga4gh-approval-beacon-test'
            ) {
              resp.splice(index, 1)
              resp.push(element)
              resp.reverse()
            }
          })
        } else {
          resp.push(res2.data.responses)
        }
      } catch (error) {
        setError('No Beacons information available, sorry')
      }
    }

    // call the function
    fetchData()
  }, [])
  return (
    <div>
      {resp[0] !== undefined && !isNetwork && !error && (
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
                  href='https://beacon-apis-demo.ega-archive.org/api'
                  target='_blank'
                >
                  Beacon API
                </a>
              )}
              {resp[0].meta.beaconId !==
                'org.ega-archive.ga4gh-approval-beacon-test' && (
                <a href={resp[0].response.alternativeUrl} target='_blank'>
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
      {resp[0] !== undefined && isNetwork && !error && (
        <div className='resultsRecord'>
          {resp.map(result => {
            return (
              <>
                {result.response && (
                  <div className='datasetCard'>
                    <div className='tittle'>
                      <div className='tittle2'>
                        {result.response.organization.logoUrl !== '' &&
                          result.response.name !== 'NAGENpediatrics Beacon' && (
                            <img
                              className='logoBeacon'
                              src={result.response.organization.logoUrl}
                              alt={result.meta.beaconId}
                            />
                          )}
                        {result.response.name === 'NAGENpediatrics Beacon' && (
                          <img
                            className='logoBeaconNasertic'
                            src={result.response.organization.logoUrl}
                            alt={result.meta.beaconId}
                          />
                        )}
                        <h1>{result.response.name}</h1>
                      </div>
                      <h2>{result.response.organization.name}</h2>
                    </div>
                    <hr className='line'></hr>
                    {!result.response.description.includes('<a href') && (
                      <p>{result.response.description}</p>
                    )}
                    {result.response.description.includes('<a href') && (
                      <p
                        dangerouslySetInnerHTML={{
                          __html: result.response.description
                        }}
                      />
                    )}
                    <div className='linksBeacons'>
                      {result.meta.beaconId ===
                        'org.ega-archive.ga4gh-approval-beacon-test' && (
                        <a
                          href='https://beacon-apis-demo.ega-archive.org/api'
                          target='_blank'
                          rel='noreferrer'
                        >
                          Beacon API
                        </a>
                      )}
                      {result.meta.beaconId === 'es.elixir.bsc.beacon' && (
                        <a
                          href='https://beacons.bsc.es/beacon/v2.0.0/'
                          target='_blank'
                          rel='noreferrer'
                        >
                          Beacon API
                        </a>
                      )}
                      {result.meta.beaconId === 'org.progenetix' && (
                        <a
                          href='https://beaconplus.progenetix.org/'
                          target='_blank'
                          rel='noreferrer'
                        >
                          Beacon API
                        </a>
                      )}
                      {result.meta.beaconId !== 'es.elixir.bsc.beacon' &&
                        result.meta.beaconId !== 'org.progenetix' &&
                        result.meta.beaconId !==
                          'org.ega-archive.ga4gh-approval-beacon-test' && (
                          <a
                            href={result.response.alternativeUrl}
                            target='_blank'
                            rel='noreferrer'
                          >
                            Beacon API
                          </a>
                        )}
                      {result.meta.beaconId === 'es.elixir.bsc.beacon' && (
                        <a
                          href='https://www.bsc.es/'
                          target='_blank'
                          rel='noreferrer'
                        >
                          Visit us
                        </a>
                      )}
                      {result.meta.beaconId !== 'es.elixir.bsc.beacon' && (
                        <a
                          href={result.response.organization.welcomeUrl}
                          target='_blank'
                          rel='noreferrer'
                        >
                          Visit us
                        </a>
                      )}
                      {result.meta.beaconId !== 'es.elixir.bsc.beacon' && (
                        <a
                          href={result.response.organization.contactUrl}
                          target='_blank'
                          rel='noreferrer'
                        >
                          Contact us
                        </a>
                      )}
                      {result.meta.beaconId === 'es.elixir.bsc.beacon' && (
                        <a
                          href='mailto:info@bsc.es'
                          target='_blank'
                          rel='noreferrer'
                        >
                          Contact us
                        </a>
                      )}
                    </div>
                  </div>
                )}
              </>
            )
          })}
        </div>
      )}
      {error && <h5>{error}</h5>}
    </div>
  )
}

export default BeaconInfo
