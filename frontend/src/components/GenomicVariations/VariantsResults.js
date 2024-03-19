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
  const [logInRequired, setLoginRequired] = useState(false)
  const [messageLoginCount, setMessageLoginCount] = useState('')
  const [messageLoginFullResp, setMessageLoginFullResp] = useState('')
  const [results, setResults] = useState([])
  const [show1, setShow1] = useState(false)
  const [show2, setShow2] = useState(false)
  const [show3, setShow3] = useState(false)

  const [numberResults, setNumberResults] = useState(0)
  const [boolean, setBoolean] = useState(false)
  const [arrayFilter, setArrayFilter] = useState([])
  const [queryArray, setQueryArray] = useState([])
  const [beaconsList, setBeaconsList] = useState([])

  const [limit, setLimit] = useState(0)
  const [skip, setSkip] = useState(0)

  const [showVariantsResults, setShowVariantsResults] = useState(false)

  const { getStoredToken, authenticateUser } = useContext(AuthContext)

  const [resultsPerDataset, setResultsDataset] = useState([])
  const [resultsNotPerDataset, setResultsNotPerDataset] = useState([])

  const [isActive1, setIsActive1] = useState(false)
  const [isActive2, setIsActive2] = useState(false)
  const [isActive3, setIsActive3] = useState(false)

  const [ontologyMultipleScope, setOntologyMultipleScope] = useState([])
  const [ontologyMultipleScopeFinal, setOntologyMultipleScopeFinal] = useState(
    []
  )
  const [optionsScope, setOptionsScope] = useState([])
  const [chosenScope, setChosenScope] = useState('')

  const [triggerSubmit, settriggerSubmit] = useState(false)
  const handleChangeScope = event => {
    console.log(event.target.value)
    setChosenScope(event.target.value)
  }
  let queryStringTerm = ''

  const handleTypeResults1 = () => {
    setShow1(true)
    setShow2(false)
    setShow3(false)
    setIsActive1(true)
    setIsActive2(false)
    setIsActive3(false)
  }

  const handleTypeResults2 = () => {
    setShow2(true)
    setShow1(false)
    setShow3(false)
    setIsActive2(true)
    setIsActive3(false)
    setIsActive1(false)
  }

  const handleTypeResults3 = () => {
    setShow3(true)
    setShow1(false)
    setShow2(false)
    setIsActive3(true)
    setIsActive1(false)
    setIsActive2(false)
  }

  const submitScopeChosen = e => {
    console.log(ontologyMultipleScope)
    let ontologyMultipleScope2 = ontologyMultipleScope.shift()
    console.log(ontologyMultipleScope2)
    ontologyMultipleScope2['scopes'] = chosenScope

    setOntologyMultipleScopeFinal([ontologyMultipleScope2])
  }

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

      var arrayRequestParameters = []
      var requestParametersSequence = {}

      var requestParametersRange = {}

      var requestParametersGene = {}

      if (props.seqModuleArray.length > 0) {
        props.seqModuleArray.forEach(element => {
          if (element.assemblyId !== '') {
            requestParametersSequence['assemblyId'] = element.assemblyId
          }
          if (element.referenceName !== '') {
            requestParametersSequence['referenceName'] = element.referenceName
          }
          if (element.start !== '') {
            requestParametersSequence['start'] = element.start
          }
          if (element.referenceBases !== '') {
            requestParametersSequence['referenceBases'] = element.referenceBases
          }
          if (element.alternateBases !== '') {
            requestParametersSequence['alternateBases'] = element.alternateBases
          }
          if (element.clinicalRelevance !== '') {
            requestParametersSequence['clinicalRelevance'] =
              element.clinicalRelevance
          }

          arrayRequestParameters.push(requestParametersSequence)
          requestParametersSequence = {}
        })
      }
   
      if (props.rangeModuleArray.length > 0) {
        console.log(props.rangeModuleArray)
        props.rangeModuleArray.forEach(element => {
          if (element.assemblyId !== '') {
            requestParametersRange['assemblyId'] = element.assemblyId
          }
          if (element.referenceName !== '') {
            requestParametersRange['referenceName'] = element.referenceName
          }
          if (element.start !== '') {
            requestParametersRange['start'] = element.start
          }
          if (element.end !== '') {
            requestParametersRange['end'] = element.end
          }
          if (element.variantType !== '') {
            requestParametersRange['variantType'] = element.variantType
          }
          if (element.alternateBases !== '') {
            requestParametersRange['alternateBases'] = element.alternateBases
          }

          if (element.referenceBases !== '') {
            requestParametersRange['referenceBases'] = element.referenceBases
          }
          if (element.aminoacid !== '') {
            requestParametersSequence['aminoacidChange'] = element.aminoacid
          }
          if (element.variantMinLength !== '') {
            requestParametersRange['variantMinLength'] =
              element.variantMinLength
          }
          if (element.variantMaxLength !== '') {
            requestParametersRange['variantMaxLength'] =
              element.variantMaxLength
          }
          if (element.clinicalRelevance !== '') {
            requestParametersSequence['clinicalRelevance'] =
              element.clinicalRelevance
          }
          arrayRequestParameters.push(requestParametersRange)
          requestParametersRange = {}
        })
      }

      if (props.geneModuleArray.length > 0) {
        props.geneModuleArray.forEach(element => {
          if (element.geneID !== '') {
            requestParametersGene['geneId'] = element.geneID
          }
          if (element.assemblyId !== '') {
            requestParametersGene['assemblyId'] = element.assemblyId
          }
          if (element.variantType !== '') {
            requestParametersGene['variantType'] = element.variantType
          }
          if (element.variantMinLength !== '') {
            requestParametersGene['variantMinLength'] = element.variantMinLength
          }
          if (element.variantMaxLength !== '') {
            requestParametersGene['variantMaxLength'] = element.variantMaxLength
          }
          if (element.clinicalRelevance !== '') {
            requestParametersSequence['clinicalRelevance'] =
              element.clinicalRelevance
          }
          arrayRequestParameters.push(requestParametersGene)
          requestParametersGene = {}
        })
      }

      if (props.query !== null) {
        if (props.query.includes(',')) {
          queryStringTerm = props.query.split(',')
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
              let alphanumHardCodedScope = 'individuals'
              if (props.query.includes('libraryStrategy=%WES%')){
                alphanumHardCodedScope = 'runs'
              }
              let alphaNumFilter = {
                id: queryArray[index][0],
                operator: queryArray[index][2],
                value: queryArray[index][1],
                scope: alphanumHardCodedScope
              }
              props.filteringTerms.data.response.filteringTerms.forEach(
                element2 => {
                  if (element2.label){
                    if (
                      queryArray[index][0].toLowerCase() ===
                        element2.id.toLowerCase() ||
                      queryArray[index][0].toLowerCase() ===
                        element2.label.toLowerCase()
                    ) {
                      alphaNumFilter = {
                        id: queryArray[index][0],
                        operator: queryArray[index][2],
                        value: queryArray[index][1],
                        scope: element2.scope[0]
                      }
                    }
                  }
                }
              )
              arrayFilter.push(alphaNumFilter)
            } else {
              let filter = {}
              props.filteringTerms.data.response.filteringTerms.forEach(
                element2 => {
                  console.log(element)
                  if (element.toLowerCase() === element2.id.toLowerCase()) {
                    if (element2.scope.length > 1) {
                      ontologyMultipleScope.push({
                        ontology: element2.id,
                        scopes: element2.scope
                      })
                      console.log(ontologyMultipleScope)
                      setOptionsScope(element2.scope)

                      if (chosenScope === '') {
                        filter = { id: element2.id, scope: '' }
                      }
                    } else {
                      if (chosenScope === '') {
                        filter = { id: element2.id, scope: element2.scope[0] }
                      }
                    }
                  } else {
                    let labelToOntology = ''
                    console.log( element.toLowerCase().replaceAll(" ",""))
                 
                    if (element2.label) {
                      console.log(element2.label.toLowerCase().replaceAll(" ",""))
                      if (
                        element.toLowerCase().replaceAll(" ","") === element2.label.toLowerCase().replaceAll(" ","")
                      ) {
                        console.log("HOLI")
                        labelToOntology = element2.id
                      
                        if (element2.scope.length > 1) {
                          ontologyMultipleScope.push({
                            ontology: element2.id,
                            scopes: element2.scope
                          })
                          console.log(ontologyMultipleScope)
                          setOptionsScope(element2.scope)

                          if (chosenScope === '') {
                            filter = { id: element2.id, scope: '' }
                          }
                        } else {
                          filter = {
                            id: labelToOntology,
                            scope: element2.scope[0]
                          }
                        }
                      }
                    }
                  }
                }
              )

              if (Object.keys(filter).length !== 0) {
                arrayFilter.push(filter)
              }
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

            let alphaNumFilter = {
              id: queryArray[0][0],
              operator: queryArray[0][2],
              value: queryArray[0][1],
              scope: 'individuals'
            }
            props.filteringTerms.data.response.filteringTerms.forEach(
              element2 => {
                if (element2.label !== undefined) {
                  if (
                    queryArray[0][0].toLowerCase() ===
                      element2.id.toLowerCase() ||
                    queryArray[0][0].toLowerCase() ===
                      element2.label.toLowerCase()
                  ) {
                    alphaNumFilter = {
                      id: queryArray[0][0],
                      operator: queryArray[0][2],
                      value: queryArray[0][1],
                      scope: element2.scope[0]
                    }
                  }
                }
              }
            )
            arrayFilter.push(alphaNumFilter)
          } else {
            let filter = {}
            props.filteringTerms.data.response.filteringTerms.forEach(
              element => {
                if (props.query === element.id) {
                  if (element.scope.length > 1) {
                    ontologyMultipleScope.push({
                      ontology: element.id,
                      scopes: element.scope
                    })
                    console.log(ontologyMultipleScope)
                    setOptionsScope(element.scope)

                    if (chosenScope === '') {
                      filter = { id: props.query, scope: '' }
                    }
                  } else {
                    filter = { id: props.query, scope: element.scope[0] }
                  }
                } else {
                  let labelToOntology = ''
                  if (element.label) {
                    if (
                      props.query.toLowerCase() === element.label.toLowerCase()
                    ) {
                      labelToOntology = element.id
                      filter = {
                        id: labelToOntology,
                        scope: element.scope[0]
                      }
                    }
                  }
                }
              }
            )

            if (Object.keys(filter).length !== 0) {
              arrayFilter.push(filter)
            }
          }
        }
      }

      try {
        let res = await axios.get(configData.API_URL + '/info')
        console.log(ontologyMultipleScopeFinal)
        if (ontologyMultipleScopeFinal.length > 0) {
          console.log(ontologyMultipleScopeFinal)

          ontologyMultipleScopeFinal.forEach(element => {
            arrayFilter.forEach(element2 => {
              console.log('')
              if (element2.id === element.ontology) {
                element2.scope = element.scopes
              }
            })
          })
          console.log(arrayFilter)
        }
     
        let postPoneQuery = false
        console.log(arrayFilter)
        arrayFilter.forEach(element => {
          if (element.scope === '') {
            postPoneQuery = true
            setTimeOut(true)
          }
        })

        if (postPoneQuery === false) {
          beaconsList.push(res.data.response)
          if (props.query === null) {
            // show all individuals
            var jsonData1 = {}

            if (arrayRequestParameters.length > 0) {
              if (arrayRequestParameters.length === 1) {
                jsonData1 = {
                  meta: {
                    apiVersion: '2.0'
                  },
                  query: {
                    requestParameters: arrayRequestParameters[0],
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
              } else {
                jsonData1 = {
                  meta: {
                    apiVersion: '2.0'
                  },
                  query: {
                    requestParameters: arrayRequestParameters,
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
              }
            } else {
              jsonData1 = {
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
            }

            jsonData1 = JSON.stringify(jsonData1)
            console.log(jsonData1)
            let token = null
            if (auth.userData === null) {
              token = getStoredToken()
            } else {
              token = auth.userData.access_token
            }

            if (token === null) {
              res = await axios.post(
                configData.API_URL + '/g_variants',
                jsonData1
              )
              console.log(jsonData1)
              console.log(res)
            } else {
              const headers = { Authorization: `Bearer ${token}` }

              res = await axios.post(
                configData.API_URL + '/g_variants',
                jsonData1,
                { headers: headers }
              )
            }
            setTimeOut(true)

            if (
              (res.data.responseSummary.numTotalResults < 1 ||
                res.data.responseSummary.numTotalResults === undefined) &&
              props.resultSets !== 'MISS'
            ) {
              setError('No results. Please try another query')
              setNumberResults(0)
              setBoolean(false)
            } else {
              res.data.response.resultSets.forEach((element, index) => {
                if (element.id && element.id !== '') {
                  if (resultsPerDataset.length > 0) {
                    resultsPerDataset.forEach(element2 => {
                      element2[0].push(element.id)
                      element2[1].push(element.exists)
                      element2[2].push(element.resultsCount)
                    })
                  } else {
                    let arrayResultsPerDataset = [
                      //element.beaconId,
                      [element.id],
                      [element.exists],
                      [element.resultsCount]
                    ]
                    resultsPerDataset.push(arrayResultsPerDataset)
                  }
                }

                if (element.id === undefined || element.id === '') {
                  let arrayResultsNoDatasets = [element.beaconId]
                  resultsNotPerDataset.push(arrayResultsNoDatasets)
                }

                if (res.data.response.resultSets[index].results) {
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
            }
          } else {
            var jsonData2 = {}

            if (arrayRequestParameters.length > 0) {
              if (arrayRequestParameters.length === 1) {
                jsonData2 = {
                  meta: {
                    apiVersion: '2.0'
                  },
                  query: {
                    requestParameters: arrayRequestParameters[0],
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
              } else {
                jsonData2 = {
                  meta: {
                    apiVersion: '2.0'
                  },
                  query: {
                    requestParameters: arrayRequestParameters,
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
              }
            } else {
              jsonData2 = {
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
            }
            jsonData2 = JSON.stringify(jsonData2)

            let token = null
            if (auth.userData === null) {
              token = getStoredToken()
            } else {
              token = auth.userData.access_token
            }

            if (token === null) {
              console.log('Querying without token')
              res = await axios.post(
                configData.API_URL + '/g_variants',
                jsonData2
              )
              console.log(jsonData2)

              console.log(res)
            } else {
              console.log('Querying WITH token')
              const headers = { Authorization: `Bearer ${token}` }
              res = await axios.post(
                configData.API_URL + '/g_variants',
                jsonData2,
                { headers: headers }
              )
            }

            setTimeOut(true)

            if (
              (res.data.responseSummary.numTotalResults < 1 ||
                res.data.responseSummary.numTotalResults === undefined) &&
              props.resultSets !== 'MISS'
            ) {
              setError('No results. Please try another query')
              setNumberResults(0)
              setBoolean(false)
            } else {
              res.data.response.resultSets.forEach((element, index) => {
                if (element.id && element.id !== '') {
                  if (resultsPerDataset.length > 0) {
                    resultsPerDataset.forEach(element2 => {
                      element2[0].push(element.id)
                      element2[1].push(element.exists)
                      element2[2].push(element.resultsCount)
                    })
                  } else {
                    let arrayResultsPerDataset = [
                      //element.beaconId,
                      [element.id],
                      [element.exists],
                      [element.resultsCount]
                    ]
                    let found = false
                    resultsPerDataset.forEach(element => {
                      if (element[0] === arrayResultsPerDataset[0]) {
                        found = true
                      }
                    })
                    if (found === false) {
                      resultsPerDataset.push(arrayResultsPerDataset)
                    }
                  }
                }

                if (element.id === undefined || element.id === '') {
                  let arrayResultsNoDatasets = [element.beaconId]
                  resultsNotPerDataset.push(arrayResultsNoDatasets)
                }

                if (res.data.response.resultSets[index].results) {
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
            }
          }

          settriggerSubmit(true)
        }
      } catch (error) {
        console.log(error)
        setError('No results. Please retry')
        setTimeOut(true)
      }
    }
    apiCall()
  }, [ontologyMultipleScopeFinal])
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
      {optionsScope.length > 0 && !triggerSubmit && (
        <div className='scopeDiv'>
          {ontologyMultipleScope.map(element => {
            return (
              <>
                <h10>Please choose a scope for {element.ontology} :</h10>

                <select id='miSelect' onChange={handleChangeScope}>
                  <option value={''}>{''}</option>
                  {optionsScope.map((element, index) => {
                    return <option value={element}>{element}</option>
                  })}
                </select>
                <button onClick={submitScopeChosen} className='doneButton'>
                  <ion-icon name='checkmark-circle-outline'></ion-icon>
                </button>
              </>
            )
          })}
        </div>
      )}

      {triggerSubmit && (
        <div>
          <div>
            {' '}
            {timeOut && error !== 'Connection error. Please retry' && (
              <div>
                <div className='selectGranularity'>
                  <h4>Granularity:</h4>
                  <button className='typeResults' onClick={handleTypeResults1}>
                    <h5
                      className={
                        isActive1 ? 'granularityActive' : 'granularityNoActive'
                      }
                    >
                      Boolean
                    </h5>
                  </button>
                  <button className='typeResults' onClick={handleTypeResults2}>
                    <h5
                      className={
                        isActive2 ? 'granularityActive' : 'granularityNoActive'
                      }
                    >
                      Count
                    </h5>
                  </button>
                  {props.resultSets !== 'MISS' && results.length > 0 && (
                    <button
                      className='typeResults'
                      onClick={handleTypeResults3}
                    >
                      <h5
                        se
                        className={
                          isActive3
                            ? 'granularityActive'
                            : 'granularityNoActive'
                        }
                      >
                        Full response
                      </h5>
                    </button>
                  )}
                </div>
              </div>
            )}
            {timeOut && error === 'Connection error. Please retry' && (
              <h3>&nbsp; {error} </h3>
            )}
            {show3 && logInRequired === false && !error && (
              <div className='containerTableResults'>
                <TableResultsVariant
                  show={'full'}
                  results={results}
                  resultsPerDataset={resultsPerDataset}
                  beaconsList={beaconsList}
                  resultSets={props.resultSets}
                ></TableResultsVariant>
              </div>
            )}
            {show3 && error && <h3>&nbsp; {error} </h3>}
            {show2 && !error && (
              <div className='containerTableResults'>
                <TableResultsVariant
                  show={'count'}
                  resultsPerDataset={resultsPerDataset}
                  resultsNotPerDataset={resultsNotPerDataset}
                  results={results}
                  beaconsList={beaconsList}
                  resultSets={props.resultSets}
                ></TableResultsVariant>
              </div>
            )}
            {show1 && !error && (
              <div className='containerTableResults'>
                <TableResultsVariant
                  show={'boolean'}
                  resultsPerDataset={resultsPerDataset}
                  resultsNotPerDataset={resultsNotPerDataset}
                  results={results}
                  beaconsList={beaconsList}
                  resultSets={props.resultSets}
                ></TableResultsVariant>
              </div>
            )}
            {show2 && error && <h3>&nbsp; {error} </h3>}
            {show1 && error && <h3>&nbsp; {error} </h3>}
          </div>
        </div>
      )}
    </div>
  )
}

export default VariantsResults
