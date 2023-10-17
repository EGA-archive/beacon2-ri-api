import './GenomicVariations.css'
import '../Individuals/Individuals.css'
import '../../App.css'
import { useState, useEffect } from 'react'
import axios from 'axios'
import { useAuth } from 'oidc-react'
import configData from '../../config.json'
import { AuthContext } from '../context/AuthContext'
import { useContext } from 'react'
import TableResultsVariant from '../Results/VariantResults/TableResultsVariant'

function VariantsResults (props) {
  const [error, setError] = useState('')
  const [timeOut, setTimeOut] = useState(false)
  const [logInRequired, setLoginRequired] = useState(true)
  const [messageLoginCount, setMessageLoginCount] = useState('')
  const [messageLoginFullResp, setMessageLoginFullResp] = useState('')
  const [results, setResults] = useState([])
  const [show1, setShow1] = useState(false)
  const [show2, setShow2] = useState(false)
  const [show3, setShow3] = useState(false)

  const [numberResults, setNumberResults] = useState(0)
  const [boolean, setBoolean] = useState(false)
  const [arrayFilter, setArrayFilter] = useState([])

  const [showVariantsResults, setShowVariantsResults] = useState(false)

  const { getStoredToken, authenticateUser } = useContext(AuthContext)

  let queryStringTerm = ''
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
    console.log(error)
    setShow3(true)
    setShow1(false)
    setShow2(false)
  }

  const auth = useAuth()
  let isAuthenticated = auth.userData?.id_token ? true : false

  useEffect(() => {
    const apiCall = async () => {
      if ((isAuthenticated === false)) {
        authenticateUser()
        const token = getStoredToken()

        if (token !== 'undefined' && token !== null) {
          isAuthenticated = true
        }
      }

      if (isAuthenticated) {
        setLoginRequired(false)
      } else {
        setLoginRequired(true)
        //setLoginRequired(false)
        setMessageLoginCount('PLEASE LOG IN FOR GETTING THE NUMBER OF RESULTS')
        setMessageLoginFullResp('PLEASE LOG IN FOR GETTING THE FULL RESPONSE')
      }

      try {
        if (props.showBar === true) {
          setShowVariantsResults(true)
          if (props.query.includes(',')) {
            queryStringTerm = props.query.split(',')

            queryStringTerm.forEach((element, index) => {
              element = element.trim()
              const filter = {
                id: element
              }
              arrayFilter.push(filter)
            })
          } else {
            const filter = {
              id: props.query
            }
            arrayFilter.push(filter)
          }
          console.log(arrayFilter)

          var jsonData1 = {
            meta: {
              apiVersion: '2.0'
            },
            query: {
              filters: arrayFilter,
              includeResultsetResponses: `${props.resultSets}`,
              pagination: {
                skip: 0,
                limit: 10
              },
              testMode: false,
              requestedGranularity: 'record'
            }
          }
          jsonData1 = JSON.stringify(jsonData1)
          console.log(jsonData1)
          // const token = auth.userData.access_token
          // console.log(token)
          //const headers = { 'Authorization': `Bearer ${token}` }
          // const res = await axios.post("https://beacons.bsc.es/beacon-network/v2.0.0/g_variants", jsonData1, {headers: headers})
          // const res = await axios.post(
          // configData.API_URL + '/g_variants',
          //jsonData1
          // )
          const res = await axios.post(
            'https://beacon-apis-demo.ega-archive.org/api/g_variants',
            jsonData1
          )
          setTimeOut(true)
          console.log(res)
          if (res.data.responseSummary.exists === false) {
            setBoolean(false)
            setNumberResults(0)
            setError('No results found. Please retry')
          } else {
            res.data.response.resultSets.forEach((element, index) => {
              res.data.response.resultSets[index].results.forEach(
                (element2, index2) => {
                  let arrayResult = [
                    res.data.response.resultSets[index].id,
                    res.data.response.resultSets[index].results[index2]
                  ]
                  results.push(arrayResult)
                  console.log(arrayResult)
                }
              )
            })
            setBoolean(res.data.responseSummary.exists)
            setNumberResults(res.data.responseSummary.numTotalResults)
          }
        } else {
          setShowVariantsResults(false)
          //   referenceName={referenceName} start={start} end={end} variantType={variantType} alternateBases={alternateBases} referenceBases={referenceBases} aminoacid={aminoacid} geneID={geneID} />
          //    </div>

          var requestParameters = {}

          if (props.referenceName !== '') {
            requestParameters['referenceName'] = props.referenceName
          }
          if (props.referenceName2 !== '') {
            requestParameters['referenceName'] = props.referenceName2
          }
          if (props.start !== '') {
            requestParameters['start'] = props.start
          }
          if (props.start2 !== '') {
            requestParameters['start'] = props.start2
          }
          if (props.end !== '') {
            requestParameters['end'] = props.end
          }
          if (props.variantType !== '') {
            requestParameters['variantType'] = props.variantType
          }
          if (props.variantType2 !== '') {
            requestParameters['variantType'] = props.variantType2
          }
          if (props.alternateBases !== '') {
            requestParameters['alternateBases'] = props.alternateBases
          }
          if (props.alternateBases2 !== '') {
            requestParameters['alternateBases'] = props.alternateBases2
          }
          if (props.referenceBases !== '') {
            requestParameters['referenceBases'] = props.referenceBases
          }
          if (props.referenceBases2 !== '') {
            requestParameters['referenceBases'] = props.referenceBases2
          }
          if (props.aminoacid !== '') {
            requestParameters['aminoacidChange'] = props.aminoacid
          }
          if (props.aminoacid2 !== '') {
            requestParameters['aminoacidChange'] = props.aminoacid2
          }
          if (props.geneID !== '') {
            requestParameters['gene'] = props.geneID
          }
          if (props.assemblyId !== '') {
            requestParameters['assemblyId'] = props.assemblyId
          }
          if (props.assemblyId2 !== '') {
            requestParameters['assemblyId'] = props.assemblyId2
          }
          if (props.assemblyId3 !== '') {
            requestParameters['assemblyId'] = props.assemblyId3
          }
          var jsonData1 = {
            meta: {
              apiVersion: '2.0'
            },
            query: {
              requestParameters: requestParameters,
              filters: [],
              includeResultsetResponses: 'HIT',
              pagination: {
                skip: 0,
                limit: 0
              },
              testMode: false,
              requestedGranularity: 'record'
            }
          }
          jsonData1 = JSON.stringify(jsonData1)
          console.log(jsonData1)

          //const token = auth.userData.access_token
          //console.log(token)
          //const headers = { Authorization: `Bearer ${token}` }
          const res = await axios.post(
            configData.API_URL + '/g_variants',
            jsonData1
          )

          if (
            res.data.responseSummary.numTotalResults < 1 ||
            res.data.responseSummary.numTotalResults === undefined
          ) {
            setError('No results. Please check the query and retry')
            setNumberResults(0)
            setBoolean(false)
          } else {
            console.log(res.data.responseSummary.numTotalResults)
            props.setHideForm(true)
            setNumberResults(res.data.responseSummary.numTotalResults)
            setBoolean(res.data.responseSummary.exists)
            console.log(res)
            res.data.response.resultSets.forEach((element, index) => {
              res.data.response.resultSets[index].results.forEach(
                (element2, index2) => {
                  let arrayResult = [
                    res.data.response.resultSets[index].beaconId,
                    res.data.response.resultSets[index].results[index2]
                  ]
                  results.push(arrayResult)
                  console.log(arrayResult)
                }
              )
            })
          }
        }
      } catch (error) {
        setTimeOut(true)
        console.log(error)
        setError(error)
      }
    }
    apiCall()
  }, [props.showBar])

  return (
    <div>
      {showVariantsResults === true && (
        <div className='resultsOptions'>
          {timeOut === false && (
            <div className='loaderLogo'>
              <div className='loader2'>
                <div id='ld3'>
                  <div></div>
                  <div></div>
                  <div></div>
                </div>
              </div>
            </div>
          )}
          {timeOut && (
            <div>
              <div className='selectGranularity'>
                <h4>Granularity:</h4>
                <button className='typeResults' onClick={handleTypeResults1}>
                  <h5>Boolean</h5>
                </button>
                <button className='typeResults' onClick={handleTypeResults2}>
                  <h5>Count</h5>
                </button>
                <button className='typeResults' onClick={handleTypeResults3}>
                  <h5>Full response</h5>
                </button>
              </div>

              {show3 && logInRequired === false && error === '' && (
                <div>
                  <TableResultsVariant results={results}></TableResultsVariant>
                </div>
              )}
              {show3 && logInRequired === true && (
                <h3>{messageLoginFullResp}</h3>
              )}
              <div className='resultsContainer'>
                {show1 && boolean && <p className='p1'>YES</p>}
                {show1 && !boolean && <p className='p1'>NO</p>}
                {show2 && logInRequired === false && numberResults !== 1 && (
                  <p className='p1'>{numberResults} &nbsp; Results</p>
                )}
                {show2 && logInRequired === false && numberResults === 1 && (
                  <p className='p1'>{numberResults} &nbsp; Result</p>
                )}
                {show2 && logInRequired === true && (
                  <h3>{messageLoginCount}</h3>
                )}
                {show3 && error !== '' && (
                  <h5 className='variantsResultsError'>
                    Please check the query and retry
                  </h5>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default VariantsResults
