import '../Individuals/Individuals.css'
import '../../App.css'
import { useState, useEffect } from 'react'
import axios from 'axios'
import { AuthContext } from '../context/AuthContext'
import { useAuth } from 'oidc-react'
import configData from '../../config.json'
import { useContext } from 'react'
import TableResultsBiosamples from '../Results/BiosamplesResults/TableResultsBiosamples'

function BiosamplesResults (props) {
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
  const [updatedArrayFilterVar, setUpdatedArrayFilterVar] = useState([])
  const [queryArray, setQueryArray] = useState([])
  const [beaconsList, setBeaconsList] = useState([])
  const [datasetList, setDatasetList] = useState([])

  const [limit, setLimit] = useState(0)
  const [skip, setSkip] = useState(0)

  const [showVariantsResults, setShowVariantsResults] = useState(false)

  const { getStoredToken, authenticateUser } = useContext(AuthContext)

  const [resultsPerDataset, setResultsDataset] = useState([])
  const [resultsNotPerDataset, setResultsNotPerDataset] = useState([])

  const [isActive1, setIsActive1] = useState(false)
  const [isActive2, setIsActive2] = useState(false)
  const [isActive3, setIsActive3] = useState(false)

  const [pause, setPause] = useState(false)

  const [optionsScope, setOptionsScope] = useState([])
  const [selectedScopes, setSelectedScopes] = useState({})
  const [ontologyMultipleScope, setOntologyMultipleScope] = useState([])
  const [triggerQueryScope, setTriggerQScope] = useState(false)
  const [triggerSubmit, setTriggerSubmit] = useState(false)

  let queryStringTerm = []

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

  const handleChangeScope = (event, idx) => {
    const value = event.target.value
    setSelectedScopes(prevState => ({
      ...prevState,
      [idx]: value
    }))
  }

  const submitScopeChosen = () => {
    // Implement the logic to update element.scope based on selectedScopes
    let updatedArrayFilter = [...arrayFilter]
    updatedArrayFilter.forEach((element, index) => {
      if (selectedScopes[index]) {
        element.scope = [selectedScopes[index]]
      }
    })

    setArrayFilter(updatedArrayFilter)

    setUpdatedArrayFilterVar(updatedArrayFilter)
    setPause(false)
    setTriggerQScope(!triggerQueryScope)
    setOptionsScope([])
    setOntologyMultipleScope([])
  }

  const auth = useAuth()
  let isAuthenticated = auth.userData?.id_token ? true : false
  useEffect(() => {
    setTimeOut(false)
    let collection = ''
    if (props.collection === 'Individuals') {
      collection = 'individual'
    } else if (props.collection === 'Variant') {
      collection = 'variant'
    } else if (props.collection === 'Biosamples') {
      collection = 'biosample'
    }

    const apiCall = async () => {
      if (isAuthenticated === false) {
        authenticateUser()
        const token = getStoredToken()

        if (token !== 'undefined' && token !== null) {
          isAuthenticated = true
        }
      }

      var arrayRequestParameters = []
      // var requestParametersSequence = {}

      // var requestParametersRange = {}

      // var requestParametersGene = {}

      // if (props.seqModuleArray.length > 0) {
      //   props.seqModuleArray.forEach(element => {
      //     if (element.assemblyId !== '') {
      //       requestParametersSequence['assemblyId'] = element.assemblyId
      //     }
      //     if (element.referenceName !== '') {
      //       requestParametersSequence['referenceName'] = element.referenceName
      //     }
      //     if (element.start !== '') {
      //       requestParametersSequence['start'] = element.start
      //     }
      //     if (element.referenceBases !== '') {
      //       requestParametersSequence['referenceBases'] = element.referenceBases
      //     }
      //     if (element.alternateBases !== '') {
      //       requestParametersSequence['alternateBases'] = element.alternateBases
      //     }
      //     if (element.clinicalRelevance !== '') {
      //       requestParametersSequence['clinicalRelevance'] =
      //         element.clinicalRelevance
      //     }

      //     arrayRequestParameters.push(requestParametersSequence)
      //     requestParametersSequence = {}
      //   })
      // }

      // if (props.rangeModuleArray.length > 0) {
      //   console.log(props.rangeModuleArray)
      //   props.rangeModuleArray.forEach(element => {
      //     if (element.assemblyId !== '') {
      //       requestParametersRange['assemblyId'] = element.assemblyId
      //     }
      //     if (element.referenceName !== '') {
      //       requestParametersRange['referenceName'] = element.referenceName
      //     }
      //     if (element.start !== '') {
      //       requestParametersRange['start'] = element.start
      //     }
      //     if (element.end !== '') {
      //       requestParametersRange['end'] = element.end
      //     }
      //     if (element.variantType !== '') {
      //       requestParametersRange['variantType'] = element.variantType
      //     }
      //     if (element.alternateBases !== '') {
      //       requestParametersRange['alternateBases'] = element.alternateBases
      //     }

      //     if (element.referenceBases !== '') {
      //       requestParametersRange['referenceBases'] = element.referenceBases
      //     }

      //     if (element.aminoacid !== '') {
      //       requestParametersRange['aminoacidChange'] = element.aminoacid
      //     }
      //     if (element.variantMinLength !== '') {
      //       requestParametersRange['variantMinLength'] =
      //         element.variantMinLength
      //     }
      //     if (element.variantMaxLength !== '') {
      //       requestParametersRange['variantMaxLength'] =
      //         element.variantMaxLength
      //     }
      //     if (element.clinicalRelevance !== '') {
      //       requestParametersSequence['clinicalRelevance'] =
      //         element.clinicalRelevance
      //     }
      //     arrayRequestParameters.push(requestParametersRange)
      //     requestParametersRange = {}
      //   })
      // }

      // if (props.geneModuleArray.length > 0) {
      //   props.geneModuleArray.forEach(element => {
      //     console.log(element)
      //     if (element.geneID !== '') {
      //       requestParametersGene['geneId'] = element.geneID
      //     }
      //     if (element.assemblyId !== '') {
      //       requestParametersGene['assemblyId'] = element.assemblyId
      //     }
      //     if (element.variantType !== '') {
      //       requestParametersGene['variantType'] = element.variantType
      //     }
      //     if (element.variantMinLength !== '') {
      //       requestParametersGene['variantMinLength'] = element.variantMinLength
      //     }
      //     if (element.variantMaxLength !== '') {
      //       requestParametersGene['variantMaxLength'] = element.variantMaxLength
      //     }
      //     if (element.aminoacid !== '') {
      //       requestParametersGene['aminoacidChange'] = element.aminoacid
      //     }
      //     if (element.clinicalRelevance !== '') {
      //       requestParametersSequence['clinicalRelevance'] =
      //         element.clinicalRelevance
      //     }
      //     arrayRequestParameters.push(requestParametersGene)
      //     requestParametersGene = {}
      //   })
      // }

      var requestParameters = {}

      if (props.query !== null) {
        if (props.query.includes(',')) {
          let queryStringTerm2 = props.query.split(',')
          queryStringTerm2.forEach(element => {
            queryStringTerm.push(element.trim())
          })
        } else {
          if (props.query.includes(':') && !props.query.includes('>')) {
            let arrayParameters = []
            let reqParameters = []
            if (props.query.includes('&')) {
              arrayParameters = props.query.split('&')

              arrayParameters.forEach(element => {
                reqParameters.length = 0
                reqParameters = element.split(':')

                requestParameters[reqParameters[0]] = reqParameters[1]
              })
              arrayRequestParameters.push(requestParameters)
            } else {
              let reqParameters = props.query.split(':')

              requestParameters[reqParameters[0]] = reqParameters[1]
              arrayRequestParameters.push(requestParameters)
            }
          } else if (props.query.includes(':') && props.query.includes('>')) {
            let reqParameters = props.query.split(':')

            let position = []
            if (props.query.includes('-')) {
              position = reqParameters[0].split('-')
            } else {
              position = reqParameters[0]
            }

            let bases = reqParameters[2].split('>')

            requestParameters['start'] = position[0]
            if (position[1]) {
              requestParameters['end'] = position[1]
            }
            requestParameters['variantType'] = reqParameters[1]
            requestParameters['alternateBases'] = bases[1]
            requestParameters['referenceBases'] = bases[0]
            arrayRequestParameters.push(requestParameters)
          } else {
            queryStringTerm.push(props.query.trim())
          }
        }

        let filter = {}
        if (updatedArrayFilterVar.length === 0) {
          queryStringTerm.forEach((term, index) => {
            requestParameters = {}
            if (
              (term.includes('=') ||
                term.includes('>') ||
                term.includes('<') ||
                term.includes('!') ||
                term.includes('%')) &&
              !term.includes(':')
            ) {
              if (term.includes('=')) {
                queryArray[index] = term.split('=')
                queryArray[index].push('=')
              } else if (term.includes('>')) {
                queryArray[index] = term.split('>')
                queryArray[index].push('>')
              } else if (term.includes('<')) {
                queryArray[index] = term.split('<')
                queryArray[index].push('<')
              } else if (term.includes('!')) {
                queryArray[index] = term.split('!')
                queryArray[index].push('!')
              } else {
                queryArray[index] = term.split('%')

                queryArray[index][1] = '%' + queryArray[index][1] + '%'
               
                queryArray[index].push('=')
              }

              let alphanumericFilter = {}
              props.filteringTerms.forEach(element => {
                if (element.label) {
                  if (
                    queryArray[index][1].toLowerCase() ===
                    element.label.toLowerCase()
                  ) {
                    if (queryArray[index][0].toLowerCase() === 'individual') {
                      alphanumericFilter = {
                        id: element.id,
                        scope: ['individuals']
                      }
                    } else if (
                      queryArray[index][0].toLowerCase() === 'genomicvariation'
                    ) {
                      alphanumericFilter = {
                        id: element.id,
                        scope: ['genomicVariation']
                      }
                    } else if (
                      queryArray[index][0].toLowerCase() === 'biosample'
                    ) {
                      alphanumericFilter = {
                        id: element.id,
                        scope: ['biosample']
                      }
                    } else if (
                      queryArray[index][0].toLowerCase() === 'cohort'
                    ) {
                      alphanumericFilter = {
                        id: element.id,
                        scope: ['cohort']
                      }
                    } else if (queryArray[index][0].toLowerCase() === 'run') {
                      alphanumericFilter = {
                        id: element.id,
                        scope: ['run']
                      }
                    } else {
                      alphanumericFilter = {
                        id: element.id,
                        scope: element.scopes
                      }
                    }
                  }
                }
              })

              if (Object.keys(alphanumericFilter).length === 0) {
                props.filteringTerms.forEach(element => {
                  if (
                    queryArray[index][0].toLowerCase() ===
                    element.id.toLowerCase()
                  ) {
                    queryArray[index][3] = element.scopes
                  }
                })

                if (queryArray[index][3] === undefined) {
                  queryArray[index][3] = [collection]
                }

                alphanumericFilter = {
                  id: queryArray[index][0],
                  operator: queryArray[index][2],
                  value: queryArray[index][1],
                  scope: queryArray[index][3]
                }
              }

              arrayFilter.push(alphanumericFilter)
            } else if (term.includes(':') && !term.includes('>')) {
              let arrayParameters = []
              let reqParameters = []
              if (term.includes('&')) {
                arrayParameters = term.split('&')

                arrayParameters.forEach(element => {
                  reqParameters.length = 0
                  reqParameters = element.split(':')

                  requestParameters[reqParameters[0]] = reqParameters[1]
                })
                arrayRequestParameters.push(requestParameters)
              } else {
                let reqParameters = term.split(':')

                requestParameters[reqParameters[0]] = reqParameters[1]
                arrayRequestParameters.push(requestParameters)
              }
            } else if (term.includes(':') && term.includes('>')) {
              let reqParameters = term.split(':')

              let position = []
              if (term.includes('-')) {
                position = reqParameters[0].split('-')
              } else {
                position = reqParameters[0]
              }

              let bases = reqParameters[2].split('>')

              requestParameters['start'] = position[0]
              if (position[1]) {
                requestParameters['end'] = position[1]
              }
              requestParameters['variantType'] = reqParameters[1]
              requestParameters['alternateBases'] = bases[1]
              requestParameters['referenceBases'] = bases[0]
              arrayRequestParameters.push(requestParameters)
            } else {
              props.filteringTerms.forEach(element => {
                if (element.label) {
                  if (
                    term.toLowerCase() === element.label.toLowerCase() ||
                    term.toLowerCase() === element.id.toLowerCase()
                  ) {
                    filter = {
                      id: element.id,
                      scope: element.scopes
                    }
                  }
                } else {
                  if (element.id.toLowerCase() === term.toLowerCase()) {
                    filter = {
                      id: element.id,
                      scope: element.scopes
                    }
                  }
                }
              })

              arrayFilter.push(filter)
            }
          })
        }
      }

      try {
        let res = await axios.get(configData.API_URL + '/info')
        let res2 = await axios.get(configData.API_URL + '/datasets')

        if (res2) {
          datasetList.push(res2.data.response.collections)
        }

        if (updatedArrayFilterVar.length === 0 && props.isNetwork === true) {
          res.data.responses.forEach(element => {
            beaconsList.push(element)
          })
        } else if (updatedArrayFilterVar.length === 0 && props.isNetwork === false){
          beaconsList.push(res.data.response)
        }

        let variablePause = false

        if (props.query === null || props.query === '') {
          // show all individuals
          let jsonData1 = {}

          if (arrayRequestParameters.length > 0) {
            jsonData1 = {
              meta: {
                apiVersion: '2.0'
              },
              query: {
                requestParameters:
                  arrayRequestParameters.length === 1
                    ? arrayRequestParameters[0]
                    : arrayRequestParameters,
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

          let token = null
          if (auth.userData === null) {
            token = getStoredToken()
          } else {
            token = auth.userData.access_token
          }

          if (token === null) {
            res = await axios.post(
              configData.API_URL + '/biosamples',
              jsonData1
            )
          
          } else {
        
            const headers = { Authorization: `Bearer ${token}` }
            console.log('querying with token')
            res = await axios.post(
              configData.API_URL + '/biosamples',
              jsonData1,
              { headers: headers }
            )
          }
          setTimeOut(true)

          if (
            (res.data.responseSummary.numTotalResults === 0 ||
              res.data.responseSummary.exists === false ||
              !res.data.responseSummary) &&
            props.resultSets !== 'MISS'
          ) {
            setNumberResults(0)
            setBoolean(false)
          } else {
            if (props.isNetwork) {
              res.data.response.resultSets.forEach((element, index) => {
                if (element.id && element.id !== '') {
                  if (resultsPerDataset.length > 0) {
                    resultsPerDataset.forEach(element2 => {
                      if (element2[0] === element.beaconId) {
                        element2[1].push(element.id)
                        element2[2].push(element.exists)
                        element2[3].push(element.resultsCount)
                      } else {
                        let arrayResultsPerDataset = [
                          element.beaconId,
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
                    })
                  } else {
                    let arrayResultsPerDataset = [
                      element.beaconId,
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
                        res.data.response.resultSets[index].beaconId,
                        res.data.response.resultSets[index].results[index2]
                      ]
                      results.push(arrayResult)
                    }
                  )
                }
              })
            } else {
              if (props.isNetwork) {
                res.data.response.resultSets.forEach((element, index) => {
                  if (element.id && element.id !== '') {
                    if (resultsPerDataset.length > 0) {
                      resultsPerDataset.forEach(element2 => {
                        if (element2[0] === element.beaconId) {
                          element2[1].push(element.id)
                          element2[2].push(element.exists)
                          element2[3].push(element.resultsCount)
                        } else {
                          let arrayResultsPerDataset = [
                            element.beaconId,
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
                      })
                    } else {
                      let arrayResultsPerDataset = [
                        element.beaconId,
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
                          res.data.response.resultSets[index].beaconId,
                          res.data.response.resultSets[index].results[index2]
                        ]
                        results.push(arrayResult)
                      }
                    )
                  }
                })
              } else {
                res.data.response.resultSets.forEach((element, index) => {
                  if (element.id && element.id !== '') {
                    if (resultsPerDataset.length > 0) {
                      resultsPerDataset.forEach(element2 => {
                        if (element2[0] === res.data.meta.beaconId) {
                          element2[1].push(element.id)
                          element2[2].push(element.exists)
                          element2[3].push(element.resultsCount)
                        } else {
                          let arrayResultsPerDataset = [
                            res.data.meta.beaconId,
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
                      })
                    } else {
                      let arrayResultsPerDataset = [
                        res.data.meta.beaconId,
                        [element.id],
                        [element.exists],
                        [element.resultsCount]
                      ]
                      resultsPerDataset.push(arrayResultsPerDataset)
                    }
                  }

                  if (element.id === undefined || element.id === '') {
                    let arrayResultsNoDatasets = [res.data.meta.beaconId]
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
          }
          setTriggerSubmit(true)
        } else {
         
          let jsonData2 = {}
          variablePause = false

          if (updatedArrayFilterVar.length > 0) {
            updatedArrayFilterVar.forEach((element, index) => {
              if (Array.isArray(element.scope) && !selectedScopes[index]) {
                setPause(true)
                variablePause = true

                let newOptionsScope = [...optionsScope]

                element.scope.forEach(elementScope => {
                  newOptionsScope[index] = newOptionsScope[index] || []
                  newOptionsScope[index].push(elementScope)
                })

                setOptionsScope(newOptionsScope)

                let newOntologyMultipleScope = [...ontologyMultipleScope]
                props.filteringTerms.forEach(element2 => {
                  if (element2.label && element2.id === element.id) {
                    newOntologyMultipleScope.push(element2.label)
                  }
                })
                setOntologyMultipleScope(newOntologyMultipleScope)
              } else if (
                Array.isArray(element.scope) &&
                selectedScopes[index]
              ) {
                element.scope = selectedScopes[index]
              } else {
                element.scope = element.scope
              }
            })
          } else {
            let newOptionsScope = [...optionsScope]
            arrayFilter.forEach((element, index) => {
              if (
                Array.isArray(element.scope) &&
                element.scope.length > 1 &&
                !selectedScopes[index]
              ) {
                setPause(true)
                variablePause = true

                element.scope.forEach(elementScope => {
                  newOptionsScope[index] = newOptionsScope[index] || []
                  newOptionsScope[index].push(elementScope)
                })
                setOptionsScope(newOptionsScope)

                let newOntologyMultipleScope = [...ontologyMultipleScope]

                props.filteringTerms.forEach(element2 => {
                  if (element2.label && element2.id === element.id) {
                    newOntologyMultipleScope[index] =
                      newOntologyMultipleScope[index] || []
                    newOntologyMultipleScope[index].push(element2.label)
                  }
                })

                setOntologyMultipleScope(newOntologyMultipleScope)
              } else if (
                Array.isArray(element.scope) &&
                element.scope.length > 1 &&
                selectedScopes[index]
              ) {
                element.scope = selectedScopes[index]
              } else {
                element.scope = element.scope[0]
              }
            })
          }

          if (!variablePause) {
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
                configData.API_URL + '/biosamples',
                jsonData2
              )
            
            } else {
              console.log('Querying WITH token')
        
              const headers = { Authorization: `Bearer ${token}` }

              res = await axios.post(
                configData.API_URL + '/biosamples',
                jsonData2,
                { headers: headers }
              )
          
            }

            setTimeOut(true)
            setPause(false)
            if (
              (res.data.responseSummary.exists === false ||
                res.data.responseSummary.numTotalResults === 0 ||
                !res.data.responseSummary) &&
              props.resultSets !== 'MISS'
            ) {
              setError('No results')
              setNumberResults(0)
              setBoolean(false)
            } else {
              if (props.isNetwork) {
                res.data.response.resultSets.forEach((element, index) => {
                  if (element.id && element.id !== '') {
                    if (resultsPerDataset.length > 0) {
                      resultsPerDataset.forEach(element2 => {
                        if (element2[0] === element.beaconId) {
                          element2[1].push(element.id)
                          element2[2].push(element.exists)
                          element2[3].push(element.resultsCount)
                        } else {
                          let arrayResultsPerDataset = [
                            element.beaconId,
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
                      })
                    } else {
                      let arrayResultsPerDataset = [
                        element.beaconId,
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
                          res.data.response.resultSets[index].beaconId,
                          res.data.response.resultSets[index].results[index2]
                        ]
                        results.push(arrayResult)
                      }
                    )
                  }
                })
              } else {
                res.data.response.resultSets.forEach((element, index) => {
                  if (element.id && element.id !== '') {
                    if (resultsPerDataset.length > 0) {
                      resultsPerDataset.forEach(element2 => {
                        if (element2[0] === res.data.meta.beaconId) {
                          element2[1].push(element.id)
                          element2[2].push(element.exists)
                          element2[3].push(element.resultsCount)
                        } else {
                          let arrayResultsPerDataset = [
                            res.data.meta.beaconId,
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
                      })
                    } else {
                      let arrayResultsPerDataset = [
                        res.data.meta.beaconId,
                        [element.id],
                        [element.exists],
                        [element.resultsCount]
                      ]
                      resultsPerDataset.push(arrayResultsPerDataset)
                    }
                  }

                  if (element.id === undefined || element.id === '') {
                    let arrayResultsNoDatasets = [res.data.meta.beaconId]
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

            setTriggerSubmit(true)
            updatedArrayFilterVar.length = 0
            setUpdatedArrayFilterVar([])
          } else {
            setTimeOut(true)
          }
        }
      } catch (error) {
        setError(error.message)
        setTimeOut(true)
        setTriggerSubmit(true)
      }
    }
    apiCall()
  }, [triggerQueryScope])

  useEffect(() => {
    if (props.granularity === 'boolean') {
      handleTypeResults1()
    } else if (props.granularity === 'count') {
      handleTypeResults2()
    } else if (props.granularity === 'record') {
      handleTypeResults3()
    }
  }, [])
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
      {pause && (
        <div className='scopeDiv'>
          {ontologyMultipleScope.map((element, idx) => (
            <div className='scopeSelection' key={idx}>
              <h10>Please choose a scope for {element}:</h10>
              <select id='miSelect' onChange={e => handleChangeScope(e, idx)}>
                <option value={''}>{''}</option>
                {(optionsScope[idx] || []).map((scopeOption, index) => (
                  <option value={scopeOption} key={index}>
                    {scopeOption}
                  </option>
                ))}
              </select>
              <button
                onClick={() => submitScopeChosen(idx)}
                className='doneButton'
              >
                <ion-icon name='checkmark-circle-outline'></ion-icon>
              </button>
            </div>
          ))}
        </div>
      )}

      {triggerSubmit && (
        <div>
          <div>
            {/* {timeOut && error === '' && (
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
            )} */}

            {show3 && logInRequired === false && (
              <div className='containerTableResults'>
                <TableResultsBiosamples
                  error={error}
                  show={'full'}
                  results={results}
                  resultsPerDataset={resultsPerDataset}
                  beaconsList={beaconsList}
                  datasetList={datasetList}
                  resultSets={props.resultSets}
                ></TableResultsBiosamples>
              </div>
            )}

            {show2 && (
              <div className='containerTableResults'>
                <TableResultsBiosamples
                  error={error}
                  show={'count'}
                  resultsPerDataset={resultsPerDataset}
                  resultsNotPerDataset={resultsNotPerDataset}
                  results={results}
                  beaconsList={beaconsList}
                  datasetList={datasetList}
                  resultSets={props.resultSets}
                ></TableResultsBiosamples>
              </div>
            )}
            {show1 && (
              <div className='containerTableResults'>
                <TableResultsBiosamples
                  error={error}
                  show={'boolean'}
                  resultsPerDataset={resultsPerDataset}
                  resultsNotPerDataset={resultsNotPerDataset}
                  results={results}
                  beaconsList={beaconsList}
                  datasetList={datasetList}
                  resultSets={props.resultSets}
                ></TableResultsBiosamples>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default BiosamplesResults
