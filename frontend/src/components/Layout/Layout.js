import '../../App.css'
import './Layout.css'
import FilteringTerms from '../FilteringTerms/FilteringTerms'
import filtersConfig from '../../config-examples-covid.json'
import VariantsResults from '../GenomicVariations/VariantsResults'

import BiosamplesResults from '../Biosamples/BiosamplesResults'
import BeaconInfo from '../Dataset/BeaconInfo'
import React, { useState, useEffect } from 'react'

import configData from '../../config.json'

import axios from 'axios'

import IndividualsResults from '../Individuals/IndividualsResults'
import AnalysesResults from '../Analyses/AnalysesResults'
import RunsResults from '../Runs/RunsResults'

function Layout (props) {
  const [error, setError] = useState(null)

  const [placeholder, setPlaceholder] = useState(
    'filtering term comma-separated, ID><=value'
  )

  const [results, setResults] = useState(null)
  const [query, setQuery] = useState('')
  const [queryAux, setQueryAux] = useState(null)
  const [filters, setFilters] = useState(filtersConfig.filters)
  const [exampleQ, setExampleQ] = useState([])

  const [showFilters, setShowFilters] = useState(true)
  const [expansionSection, setExpansionSection] = useState(false)
  const [arrayFilteringTermsQE, setArrayFilteringTermsQE] = useState([])

  const [resultSet, setResultset] = useState('HIT')
  const [resultSetAux, setResultsetAux] = useState('HIT')

  const [descendantTerm, setDescendantTerm] = useState('true')

  const [similarity, setSimilarity] = useState('Select')

  const [cohorts, setShowCohorts] = useState(false)

  const [ID, setId] = useState('')
  const [operator, setOperator] = useState('')
  const [valueFree, setValueFree] = useState('')

  const [value, setValue] = useState('')

  const [popUp, setPopUp] = useState(false)

  const [showButton, setShowButton] = useState(true)

  const [showFilteringTerms, setShowFilteringTerms] = useState(false)
  const [filteringTerms, setFilteringTerms] = useState([])
  const [filteringTermsButton, setShowFilteringTermsButton] = useState(false)
  const [showVariants, setShowVariants] = useState(false)

  const [showResultsVariants, setShowResultsVariants] = useState(true)

  const [trigger, setTrigger] = useState(false)
  const [triggerQuery, setTriggerQuery] = useState(false)

  const [showBar, setShowBar] = useState(true)

  const [collection, setCollection] = useState('Individuals')
  const [granularity, setGranularity] = useState('count')

  const [terms, setTerm] = useState([])

  const [showExtraIndividuals, setExtraIndividuals] = useState(false)
  const [inputValues, setInputValues] = useState({})

  // Set initial state with the input values obtained from filters

  const [state, setstate] = useState({
    query: '',
    list: []
  })

  const [showAlphanum, setShowAlphanum] = useState(false)
  const [alphanumSchemaField, setAlphanumSchemaField] = useState('')
  const [alphanumValue, setAlphanumValue] = useState('')
  const [timeOut, setTimeOut] = useState(true)

  const [isSubmitted, setIsSub] = useState(false)

  const [arrayFilteringTerms, setArrayFilteringTerms] = useState([])

  const [countGeneModule, setCountGeneModule] = useState(0)
  const [countSeqModule, setCountSeqModule] = useState(0)
  const [countRangeModule, setCountRangeModule] = useState(0)

  const [rangeModuleArray, setRangeModuleArray] = useState([])
  const [seqModuleArray, setSeqModuleArray] = useState([])
  const [geneModuleArray, setGeneModuleArray] = useState([])

  const [trigger3, setTrigger3] = useState(false)

  const [arrayRequestParameters, setArrayReqParameters] = useState([])

  const handleSeeFilteringTerms = () => {
    setShowFilteringTerms(true)
    setResults(null)
    setTimeOut(true)
  }

  // Function to handle input change and update state
  const handleInputChange = (e, identifier) => {
    const { value } = e.target
    setInputValues(prevState => ({
      ...prevState,
      [identifier]: value
    }))
  }

  const handleIdChanges = e => {
    setId(e.target.value)
  }
  const handleOperatorchange = e => {
    setOperator(e.target.value)
  }

  const handleValueChanges = e => {
    setValueFree(e.target.value)
  }
  const handdleInclude = e => {
    console.log(valueFree)
    console.log(operator)
    if (ID !== '' && valueFree !== '' && operator !== '') {
      if (query !== null && query !== '') {
        setQuery(query + ',' + `${ID}${operator}${valueFree}`)
      }
      if (query === null || query == '') {
        setQuery(`${ID}${operator}${valueFree}`)
      }
    }
  }

  const handleOption = (e, array, optionIndex) => {
    // Update input values first

    const updatedInputValues = { ...inputValues }
    console.log(updatedInputValues)
    // Generate query based on updated input values
    let start, end, variantType, referenceBases, alternateBases
    const title = []
    const value = []

    array.forEach(element => {
      title.push(element.schemaField)
      const inputValue =
        updatedInputValues[
          `${optionIndex}-${element.label}-${element.schemaField}`
        ]
      console.log(inputValue)
      value.push(inputValue || element.value)

      // Update start, end, variantType, referenceBases, alternateBases values if applicable
      switch (element.schemaField) {
        case 'start':
          start = inputValue || element.value
          break
        case 'end':
          end = inputValue || element.value
          break
        case 'variantType':
          variantType = inputValue || element.value
          break
        case 'referenceBases':
          referenceBases = inputValue || element.value
          break
        case 'alternateBases':
          alternateBases = inputValue || element.value
          break
        default:
          break
      }
    })

    const specialQuery =
      start && end && variantType && referenceBases && alternateBases
        ? `${start}-${end}:${variantType}:${referenceBases}>${alternateBases}`
        : null
        
        const arrayQuery = title
        .map((titleQuery, indexQuery) =>
          titleQuery === 'geneId' 
            ? `${titleQuery}:${value[indexQuery]}` 
            : `${titleQuery}=${value[indexQuery]}`
        )
        .join('&');

    if (e.target.checked) {
      setQuery(prevQuery => {
        if (!prevQuery) return specialQuery || arrayQuery
        return `${prevQuery},${specialQuery || arrayQuery}`
      })
    } else {
      setQuery(prevQuery => {
        const updatedQuery = prevQuery
          .split(',')
          .filter(item => item !== (specialQuery || arrayQuery))
          .join(',')
        return updatedQuery || ''
      })
    }

    // Update the input values state after generating the query
    setInputValues(updatedInputValues)
  }

  const handleOptionAlphanum = (schemaField, value) => {
    setShowAlphanum(true)
    setAlphanumSchemaField(schemaField)
    setAlphanumValue(value)
    setId(schemaField)
  }

  const handleChangeSelection1 = e => {
    setGranularity(e.target.value)
  }

  const handleChangeSelection2 = e => {
    console.log(e.target.value)
    if (e.target.value === 'Individuals') {
      setCollection('Individuals')
    }
    if (e.target.value === 'Variant') {
      setCollection('Variant')
    }
    if (e.target.value === 'Biosamples') {
      setCollection('Biosamples')
    }
  }

  const handleReset = e => {
    setQuery('')

    // Uncheck all checkboxes
    const checkboxes = document.querySelectorAll('input[type="checkbox"]')
    checkboxes.forEach(checkbox => {
      checkbox.checked = false
    })
  }

  useEffect(() => {
    setError('')

    const fetchData = async () => {
      try {
        let res = await axios.get(
          configData.API_URL + '/filtering_terms?limit=0'
        )
        setTimeOut(true)
        console.log(res)

        if (res.data.response.filteringTerms !== undefined) {
          res.data.response.filteringTerms.forEach(element => {
            filteringTerms.push(element)
          })

          console.log(filteringTerms)
          setResults(null)
        }
        if (res !== null) {
          res.data.response.filteringTerms.forEach(element => {
            if (element.type !== 'custom') {
              arrayFilteringTerms.push(element.id)
              arrayFilteringTermsQE.push(element)
            }
          })

          setstate({
            query: '',
            list: arrayFilteringTerms
          })
        }
      } catch (error) {
        console.log(error)
        setTimeOut(true)
        setError('No filtering terms now available')
      }
      setShowFilteringTermsButton(true)
    }

    // call the function
    fetchData()
      // make sure to catch any error
      .catch(console.error)
  }, [])

  useEffect(() => {
    if (collection === 'Individuals') {
      setPlaceholder('filtering term comma-separated, ID><=value')
      setExtraIndividuals(true)
    }
    if (collection === 'Variant') {
      setPlaceholder('filtering term comma-separated')
      setExtraIndividuals(true)
      setShowVariants(true)
    }
    if (collection === 'Biosamples') {
      setPlaceholder('filtering term comma-separated, ID><=value')
      setExtraIndividuals(true)
    }
  }, [collection])

  const onSubmit = async event => {
    setShowFilters(false)
    console.log(query)
    console.log(value)
    event.preventDefault()

    setIsSub(true)
    setResultsetAux(resultSet)
    setQueryAux(query)

    setTriggerQuery(!triggerQuery)

    setTriggerQuery(!triggerQuery)

    let arrayRequestParameters2 =
      geneModuleArray + seqModuleArray + rangeModuleArray

    setArrayReqParameters(geneModuleArray + seqModuleArray + rangeModuleArray)
    if (arrayRequestParameters !== arrayRequestParameters2) {
      setTriggerQuery(!triggerQuery)
    }

    setExampleQ([])

    if (query === '1' || query === '') {
      setQuery(null)
    }
    if (collection === 'Individuals') {
      setResults('Individuals')
    } else if (collection === 'Variant') {
      setResults('Variant')
    } else if (collection === 'Biosamples') {
      setResults('Biosamples')
    } else if (collection === 'Analyses') {
      setResults('Analyses')
    } else if (collection === 'Runs') {
      setResults('Runs')
    }
  }

  function search (e) {
    const newQuery = e.target.value
    setQuery(newQuery)

    const queryTerms = newQuery.split(',')
    const queryTermsVariants = queryTerms
      .filter(term => term.includes(':'))
      .map(term => term.split(':'))
    const queryTermsVariants2 = queryTerms
      .filter(term => term.includes('&'))
      .map(term => term.split('&'))

    const checkboxes = document.querySelectorAll('input[name="subscribe"]')
    const checkboxes2 = document.querySelectorAll('input[name="subscribe2"]')

    // Update the status of checkboxes for "subscribe"
    checkboxes.forEach(checkbox => {
      const optionValue = checkbox.value
      checkbox.checked = queryTerms.some(term => term.includes(optionValue))
    })

    // Update the status of checkboxes for "subscribe2"
    checkboxes2.forEach(checkbox2 => {
      const optionValue = checkbox2.value

      // Check against variants with ':'
      const isChecked = queryTermsVariants.some(
        ([prefix, value]) =>
          optionValue.includes(prefix) && optionValue.includes(value)
      )

      // Check against variants with '&'
      const isChecked2 = queryTermsVariants2.some(termsArray =>
        termsArray.every(term => {
          const [key, value] = term.split('=')
          return optionValue.includes(key) && optionValue.includes(value)
        })
      )

      checkbox2.checked = isChecked || isChecked2
    })
  }

  const handleVariantOption = optionsArray => {
    const schemaFields = optionsArray.map(option => option.schemaField)
    const values = optionsArray.map(option => option.value)

    let query = ''

    if (schemaFields.length === 1 && schemaFields[0] === 'geneId') {
      query = `${schemaFields[0]}:${values[0]}`
    } else if (
      schemaFields.length > 1 &&
      !schemaFields.includes('alternateBases') &&
      !schemaFields.includes('referenceBases')
    ) {
      query = `${schemaFields[0]}:${values[0]}&${schemaFields[1]}:${values[1]}`
    } else if (
      schemaFields.includes('alternateBases') ||
      schemaFields.includes('referenceBases')
    ) {
      query = 'hola'
    }

    console.log(query)
    // You can send the query to the backend or handle it as needed
  }

  const handleSubmit = async e => {
    setShowVariants(true)
    e.preventDefault()
    setPlaceholder('filtering term comma-separated, ID><=value')
    setIsSub(!isSubmitted)
    setExampleQ([])
    setTimeOut(true)
    setResults('Variant')
  }

  const handleShowFilterEx = () => {
    setShowFilters(true)
  }

  useEffect(() => {
    const initialInputValues = {}
    filters.forEach((filter, index) => {
      filter.options.forEach((option, indexOption) => {
        option.forEach(element => {
          if (filter.type === 'input') {
            const identifier = `${indexOption}-${element.label}-${element.schemaField}`
            initialInputValues[identifier] = element.label || ''
          }
        })
      })
    })
    setInputValues(initialInputValues)
  }, [filters])

  return (
    <div className='container1'>
      <div className='sectionModules'>
        <div className='container2'>
          <div className='logosVersionContainer'>
            <div className='logos'>
              <a
                href='https://ega-archive.org/'
                className='logoInstitution'
                target='_blank'
                rel='noreferrer'
              >
                <img
                  className='ega-logo'
                  src='../ega-archive.png'
                  alt='EGAarchive'
                ></img>
              </a>
            </div>
            <h1 className='version'>v0.5.4</h1>
          </div>
        </div>
        <div className='containerSelection'>
          <select
            name='select'
            className='selectModule1'
            onChange={handleChangeSelection1}
          >
            <option value='boolean' className='optionClass'>
              Do you have?...{' '}
            </option>
            <option value='count' selected>
              How many?...
            </option>
            <option value='record'>Can you give me details on?...</option>
          </select>
          <select
            name='select2'
            className='selectModule2'
            onChange={handleChangeSelection2}
          >
            <option value='Individuals' selected>
              Individuals
            </option>
            <option value='Variant'>Genomic variants</option>
            <option value='Biosamples'>Biosamples</option>
          </select>
          <h14>having ... </h14>
          <form onSubmit={onSubmit} className='formInput'>
            <div className='textAreaDiv'>
              <textarea
                className='inputSearch'
                type='text'
                placeholder={placeholder}
                value={query}
                onChange={e => search(e)}
              />
              <input
                className='resetButton'
                type='reset'
                value='Clear'
                onClick={handleReset}
              ></input>
            </div>
            <button className='searchButton' type='submit'>
              <img
                className='searchIcon'
                src='./magnifier.png'
                alt='searchIcon'
              ></img>
            </button>
          </form>
        </div>
      </div>
      {showAlphanum && (
        <tr className='termsAlphanum'>
          <div className='alphanumContainer2'>
            <div className='alphaIdModule'>
              <div className='listTerms'>
                <label>
                  <h2>ID</h2>
                </label>

                <input
                  className='IdForm2'
                  type='text'
                  value={alphanumValue}
                  autoComplete='on'
                  placeholder={'write and filter by ID'}
                  onChange={handleIdChanges}
                  aria-label='ID'
                />

                <div id='operator2'>
                  <select
                    className='selectedOperator2'
                    onChange={handleOperatorchange}
                    name='selectedOperator'
                  >
                    <option value=''> </option>
                    <option value='='>= </option>
                    <option value='<'>&lt;</option>
                    <option value='>'>&gt;</option>
                    <option value='!'>!</option>
                    <option value='%'>%</option>
                  </select>
                </div>

                <label id='value2'>
                  <h2>Value</h2>
                </label>
                <input
                  className='ValueForm2'
                  type='text'
                  autoComplete='on'
                  placeholder={'free text/ value'}
                  onChange={handleValueChanges}
                  aria-label='Value'
                />
              </div>
            </div>
            <button className='buttonAlphanum' onClick={handdleInclude}>
              <ion-icon name='add-circle'></ion-icon>
            </button>
          </div>
        </tr>
      )}
      {showFilters && (
        <div className='layout-container'>
          <div className='filterTermsContainer'>
            {filters.map((filter, index) => (
              <div key={index} className='divFilter'>
                <p>{filter.title}</p>
                <ul>
                  {filter.options.map((optionsArray, optionIndex) => (
                    <div key={optionIndex}>
                      {filter.title === 'Variant'
                        ? optionsArray.length > 0 &&
                          optionsArray[0].type !== 'alphanumeric' && (
                            <div className='containerExamples1'>
                              <input
                                type='checkbox'
                                onClick={e =>
                                  handleOption(e, optionsArray, optionIndex)
                                }
                                id={`option${index}-${optionIndex}`}
                                name='subscribe2'
                                value={JSON.stringify(optionsArray)}
                                data-filter-index={index} // Add data attribute for filter index
                                data-option-index={optionIndex} // Add data attribute for option index
                                className='inputExamples'
                              />
                              <div className='containerExamplesDiv2'>
                                {optionsArray[0].subTitle && (
                                  <label className='subTitle'>
                                    {optionsArray[0].subTitle}
                                  </label>
                                )}
                                {optionsArray.map((element, elementIndex) => (
                                  <React.Fragment key={elementIndex}>
                                    {!element.subTitle2 ? (
                                      <div className='label-ontology-div'>
                                        <label className='label'>
                                          {element.label}
                                        </label>
                                        <label className='onHover'>
                                          {element.ontology}
                                        </label>
                                      </div>
                                    ) : filter.type === 'input' ? (
                                      <div className='label-ontology-div2'>
                                        <label>{element.subTitle2}</label>
                                        <input
                                          type='text'
                                          className='label'
                                          value={
                                            inputValues[
                                              `${optionIndex}-${element.label}-${element.schemaField}`
                                            ] || ''
                                          }
                                          onChange={e =>
                                            handleInputChange(
                                              e,
                                              `${optionIndex}-${element.label}-${element.schemaField}`
                                            )
                                          }
                                        />
                                      </div>
                                    ) : (
                                      <div className='label-ontology-div2'>
                                        <label>{element.subTitle2}</label>
                                        <label className='label'>
                                          {element.label}
                                        </label>
                                        <label className='onHover'>
                                          {element.ontology}
                                        </label>
                                      </div>
                                    )}
                                  </React.Fragment>
                                  
                                ))}
                              </div>
                              
                            </div>
                          )
                        : optionsArray.length > 0 &&
                          (optionsArray[0].type === 'alphanumeric' ? (
                            <div>
                              <button
                                className='alphanumButton'
                                onClick={() =>
                                  handleOptionAlphanum(
                                    optionsArray[0].schemaField,
                                    optionsArray[0].value
                                  )
                                }
                              >
                                <img
                                  className='formula'
                                  src='/../formula.png'
                                  alt='formula'
                                />
                                {optionsArray[0].label}
                              </button>
                            </div>
                          ) : (
                            <div className='containerExamples1'>
                              <input
                                type='checkbox'
                                onClick={e =>
                                  handleOption(e, optionsArray, optionIndex)
                                }
                                id={`option${index}-${optionIndex}`}
                                name='subscribe'
                                value={optionsArray[0].value}
                                data-filter-index={index}
                                data-option-index={optionIndex}
                              />
                              <div className='containerExamplesDiv2'>
                                {optionsArray[0].subTitle && (
                                  <label>{optionsArray[0].subTitle}</label>
                                )}
                                {optionsArray.map((element, elementIndex) => (
                                  <React.Fragment key={elementIndex}>
                                    {!element.subTitle2 ? (
                                      <div className='label-ontology-div'>
                                        <label className='label'>
                                          {element.label}
                                        </label>
                                        <label className='onHover'>
                                          {element.ontology}
                                        </label>
                                      </div>
                                    ) : filter.type === 'input' ? (
                                      <div className='label-ontology-div2'>
                                        <label>{element.subTitle2}</label>
                                        <input
                                          type='text'
                                          className='label'
                                          value={
                                            inputValues[
                                              `${optionIndex}-${element.label}-${element.schemaField}`
                                            ] || ''
                                          }
                                          onChange={e =>
                                            handleInputChange(
                                              e,
                                              `${optionIndex}-${element.label}-${element.schemaField}`
                                            )
                                          }
                                        />
                                        <label className='onHover'>
                                          {element.ontology}
                                        </label>
                                      </div>
                                    ) : (
                                      <div className='label-ontology-div2'>
                                        <label>{element.subTitle2}</label>
                                        <label className='label'>
                                          {element.label}
                                        </label>
                                        <label className='onHover'>
                                          {element.ontology}
                                        </label>
                                      </div>
                                    )}
                                  </React.Fragment>
                                ))}
                              </div>
                            </div>
                          ))}
                          
                    </div>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <button className='buttonAllFilters' onClick={handleSeeFilteringTerms}>
            <img className='filterIcon' src='../../filter.png'></img>
            <h4>All filtering terms</h4>
          </button>
        </div>
      )}

      {showFilters === false && (
        <button onClick={handleShowFilterEx} className='buttonShowExamples'>
          Show examples
        </button>
      )}
      <hr></hr>
      <div className='results'>
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
        {results === null && !showFilteringTerms && (
          <BeaconInfo trigger={trigger} />
        )}
        {isSubmitted && results === 'Individuals' && triggerQuery && (
          <div>
            <IndividualsResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
              rangeModuleArray={rangeModuleArray}
              seqModuleArray={seqModuleArray}
              geneModuleArray={geneModuleArray}
              granularity={granularity}
              collection={collection}
            />
          </div>
        )}
        {isSubmitted && results === 'Individuals' && !triggerQuery && (
          <div>
            <IndividualsResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
              rangeModuleArray={rangeModuleArray}
              seqModuleArray={seqModuleArray}
              geneModuleArray={geneModuleArray}
              granularity={granularity}
              collection={collection}
            />
          </div>
        )}
        {isSubmitted && results === 'Analyses' && triggerQuery && (
          <div>
            <AnalysesResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
            />
          </div>
        )}
        {isSubmitted && results === 'Analyses' && !triggerQuery && (
          <div>
            <AnalysesResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
            />
          </div>
        )}
        {isSubmitted && results === 'Runs' && triggerQuery && (
          <div>
            <RunsResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
              rangeModuleArray={rangeModuleArray}
              seqModuleArray={seqModuleArray}
              geneModuleArray={geneModuleArray}
            />
          </div>
        )}
        {isSubmitted && results === 'Runs' && !triggerQuery && (
          <div>
            <RunsResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
              rangeModuleArray={rangeModuleArray}
              seqModuleArray={seqModuleArray}
              geneModuleArray={geneModuleArray}
            />
          </div>
        )}
        {isSubmitted && results === 'Variant' && triggerQuery && (
          <div>
            <VariantsResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
              rangeModuleArray={rangeModuleArray}
              seqModuleArray={seqModuleArray}
              geneModuleArray={geneModuleArray}
              granularity={granularity}
              collection={collection}
            />
          </div>
        )}
        {isSubmitted && results === 'Variant' && !triggerQuery && (
          <div>
            <VariantsResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
              rangeModuleArray={rangeModuleArray}
              seqModuleArray={seqModuleArray}
              geneModuleArray={geneModuleArray}
              granularity={granularity}
              collection={collection}
            />
          </div>
        )}
        {!isSubmitted && results === 'Variant' && !triggerQuery && (
          <div>
            <VariantsResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
              rangeModuleArray={rangeModuleArray}
              seqModuleArray={seqModuleArray}
              geneModuleArray={geneModuleArray}
              granularity={granularity}
              collection={collection}
            />
          </div>
        )}
        {isSubmitted && results === 'Biosamples' && triggerQuery && (
          <div>
            <BiosamplesResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
              rangeModuleArray={rangeModuleArray}
              seqModuleArray={seqModuleArray}
              geneModuleArray={geneModuleArray}
              granularity={granularity}
              collection={collection}
            />
          </div>
        )}
        {isSubmitted && results === 'Biosamples' && !triggerQuery && (
          <div>
            <BiosamplesResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
              rangeModuleArray={rangeModuleArray}
              seqModuleArray={seqModuleArray}
              geneModuleArray={geneModuleArray}
              granularity={granularity}
              collection={collection}
            />
          </div>
        )}
        {results === null && timeOut === true && showFilteringTerms && (
          <FilteringTerms
            filteringTerms={filteringTerms}
            collection={collection}
            setPlaceholder={setPlaceholder}
            placeholder={placeholder}
            query={query}
            setQuery={setQuery}
          />
        )}

        {timeOut === true && error && showFilteringTerms && <h5>{error}</h5>}
      </div>
    </div>
  )
}

export default Layout
