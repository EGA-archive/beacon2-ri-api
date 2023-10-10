import './Individuals.css'
import '../../App.css'
import { useState, useEffect } from 'react'
import axios from 'axios'
import { AuthContext } from '../context/AuthContext'
import { useAuth } from 'oidc-react'
import configData from '../../config.json'
import { useContext } from 'react'
import TableResultsIndividuals from '../Results/IndividualsResults/TableResultsIndividuals'

function IndividualsResults (props) {
  const [showLayout, setShowLayout] = useState(false)

  const [beaconsList, setBeaconsList] = useState([])

  const [error, setError] = useState(false)
  const [response, setResponse] = useState(null)
  const [numberResults, setNumberResults] = useState(0)
  const [boolean, setBoolean] = useState(false)
  const [results, setResults] = useState([])
  const [show1, setShow1] = useState(false)
  const [show2, setShow2] = useState(false)
  const [show3, setShow3] = useState(false)

  const [timeOut, setTimeOut] = useState(false)

  const [logInRequired, setLoginRequired] = useState(true)
  const [messageLoginCount, setMessageLoginCount] = useState('')
  const [messageLoginFullResp, setMessageLoginFullResp] = useState('')

  const [limit, setLimit] = useState(0)
  const [skip, setSkip] = useState(0)

  const [skipTrigger, setSkipTrigger] = useState(0)
  const [limitTrigger, setLimitTrigger] = useState(0)

  const [queryArray, setQueryArray] = useState([])
  const [arrayFilter, setArrayFilter] = useState([])

  const { getStoredToken, authenticateUser } = useContext(AuthContext)
  let queryStringTerm = ''

  let res = ''

  const auth = useAuth()
  let isAuthenticated = auth.userData?.id_token ? true : false

  useEffect(() => {
    const apiCall = async () => {
      if (isAuthenticated === false) {
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
        setMessageLoginCount('PLEASE LOG IN FOR GETTING THE NUMBER OF RESULTS')
        setMessageLoginFullResp('PLEASE LOG IN FOR GETTING THE FULL RESPONSE')
      }

      if (props.query !== null) {
        if (props.query.includes(',')) {
          queryStringTerm = props.query.split(',')
          console.log(queryStringTerm)
          queryStringTerm.forEach((element, index) => {
            element = element.trim()
            if (
              element.includes('=') ||
              element.includes('>') ||
              element.includes('<') ||
              element.includes('!') ||
              element.includes('%')
            ) {
              if (element.includes('=')) {
                queryArray[index] = element.split('=')
                queryArray[index].push('=')
              } else if (element.includes('>')) {
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
                id: queryArray[index][0],
                operator: queryArray[index][2],
                value: queryArray[index][1]
              }
              arrayFilter.push(alphaNumFilter)
            } else {
              const filter2 = {
                id: element,
                includeDescendantTerms: props.descendantTerm
              }
              arrayFilter.push(filter2)
            }
          })
        } else {
          if (
            props.query.includes('=') ||
            props.query.includes('>') ||
            props.query.includes('<') ||
            props.query.includes('!') ||
            props.query.includes('%')
          ) {
            if (props.query.includes('=')) {
              queryArray[0] = props.query.split('=')
              queryArray[0].push('=')
            } else if (props.query.includes('>')) {
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
              id: queryArray[0][0],
              operator: queryArray[0][2],
              value: queryArray[0][1]
            }
            arrayFilter.push(alphaNumFilter)
          } else {
            const filter = {
              id: props.query
            }
            arrayFilter.push(filter)
          }
        }
      }

      try {
        let res = await axios.get(configData.API_URL + '/info')

        beaconsList.push(res.data)

        beaconsList.reverse()
        console.log(beaconsList)
        if (props.query === null) {
          // show all individuals

          var jsonData1 = {
            meta: {
              apiVersion: '2.0'
            },
            query: {
              filters: arrayFilter,
              includeResultsetResponses: `${props.resultSets}`,
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
          // console.log(token)
          //const headers = { Authorization: `Bearer ${token}` }

          res = await axios.post(configData.API_URL + '/individuals', jsonData1)

          console.log(res)
          setTimeOut(true)

          if (res.data.responseSummary.numTotalResults < 1) {
            setError('No results. Please check the query and retry')
            setNumberResults(0)
            setBoolean(false)
          } else {
            res.data.response.resultSets.forEach((element, index) => {
              if (res.data.response.resultSets[index].resultsCount > 0) {
                console.log(res.data.response.resultSets[index].results.length)
                res.data.response.resultSets[index].results.forEach(
                  (element2, index2) => {
                    let arrayResult = [
                      res.data.meta.beaconId,
                      res.data.response.resultSets[index].results[index2]
                    ]
                    results.push(arrayResult)
                  }
                )
              }
            })

            setNumberResults(res.data.responseSummary.numTotalResults)
            setBoolean(res.data.responseSummary.exists)
          }
        } else {
          var jsonData2 = {
            meta: {
              apiVersion: '2.0'
            },
            query: {
              filters: arrayFilter,
              includeResultsetResponses: `${props.resultSets}`,
              pagination: {
                skip: skip,
                limit: limit
              },
              testMode: false,
              requestedGranularity: 'record'
            }
          }
          jsonData2 = JSON.stringify(jsonData2)
          console.log(jsonData2)

          //const token = auth.userData.access_token
          //console.log(token)
          //const headers = { Authorization: `Bearer ${token}` }

          //res = await axios.post("https://beacons.bsc.es/beacon-network/v2.0.0/individuals/", jsonData2, { headers: headers })
          res = await axios.post(configData.API_URL + '/individuals', jsonData2)

          console.log(res)
          setTimeOut(true)

          if (
            res.data.responseSummary.numTotalResults < 1 ||
            res.data.responseSummary.numTotalResults === undefined
          ) {
            setError('No results. Please check the query and retry')
            setNumberResults(0)
            setBoolean(false)
          } else {
            console.log(res.data.responseSummary.numTotalResults)
            setNumberResults(res.data.responseSummary.numTotalResults)
            setBoolean(res.data.responseSummary.exists)

            res.data.response.resultSets.forEach((element, index) => {
              if (res.data.response.resultSets[index].resultsCount > 0) {
                console.log(res.data.response.resultSets[index].results.length)
                res.data.response.resultSets[index].results.forEach(
                  (element2, index2) => {
                    let arrayResult = [
                      res.data.meta.beaconId,
                      res.data.response.resultSets[index].results[index2]
                    ]
                    results.push(arrayResult)
                    console.log(arrayResult)
                    console.log(results)
                  }
                )

                console.log(results)
              }
            })
          }
        }
      } catch (error) {
        setError('Error. Please retry')
        setTimeOut(false)
        console.log(error)
      }
    }
    apiCall()
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

  const handleSkipChanges = e => {
    setSkip(Number(e.target.value))
  }

  const handleLimitChanges = e => {
    setLimit(Number(e.target.value))
  }

  const onSubmit = () => {
    setSkipTrigger(skip)
    setLimitTrigger(limit)
    setTimeOut(false)
  }
  return (
    <div>
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

      <div>
        <div>
          {' '}
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
            </div>
          )}
          {show3 && logInRequired === false && !error && (
            <div>
              <TableResultsIndividuals
                results={results}
                beaconsList={beaconsList}
              ></TableResultsIndividuals>
            </div>
          )}
          {show3 && logInRequired === true && <h3>{messageLoginFullResp}</h3>}
          {show3 && error && <h3>&nbsp; {error} </h3>}
          <div className='resultsContainer'>
            {show1 && boolean && <p className='p1'>YES</p>}
            {show1 && !boolean && <p className='p1'>NO</p>}

            {show2 && logInRequired === false && numberResults !== 1 && (
              <p className='p1'>{numberResults} &nbsp; Results</p>
            )}
            {show2 && numberResults === 1 && logInRequired === false && (
              <p className='p1'>{numberResults} &nbsp; Result</p>
            )}
            {show2 && logInRequired === true && <h3>{messageLoginCount}</h3>}
          </div>
        </div>
      </div>
    </div>
  )
}

export default IndividualsResults
