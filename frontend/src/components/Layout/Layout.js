import '../../App.css'
import './Layout.css'
import FilteringTerms from '../FilteringTerms/FilteringTerms'
import filtersConfig from '../../config-examples-cancer.json'
import filtersConfig2 from '../../config-examples-covid.json'
import VariantsResults from '../GenomicVariations/VariantsResults'

import BiosamplesResults from '../Biosamples/BiosamplesResults'

import React, { useState, useEffect } from 'react'

import configData from '../../config.json'

import axios from 'axios'

import IndividualsResults from '../Individuals/IndividualsResults'
import AnalysesResults from '../Analyses/AnalysesResults'
import RunsResults from '../Runs/RunsResults'
import FilterContent from '../FiltersComponent/FiltersComponent'
import BeaconInfo from '../Dataset/BeaconInfo'

function Layout (props) {
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('tab1')
  const [placeholder, setPlaceholder] = useState(
    'filtering term comma-separated, ID><=value'
  )

  const [results, setResults] = useState(null)
  const [query, setQuery] = useState('')
  const [queryAux, setQueryAux] = useState(null)
  const [filtersTab1, setFiltersTab1] = useState(filtersConfig.filters)
  const [filtersTab2, setFiltersTab2] = useState(filtersConfig2.filters)
  const [exampleQ, setExampleQ] = useState([])

  const [isNetwork, setIsNetwork] = useState(false)
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
  const [inputValuesTab1, setInputValuesTab1] = useState({})
  const [inputValuesTab2, setInputValuesTab2] = useState({})
  const [checkedOptionsTab1, setCheckedOptionsTab1] = useState({})
  const [checkedOptionsTab2, setCheckedOptionsTab2] = useState({})
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
  const handleInputChange = (e, identifier, tab) => {
    const { value } = e.target
    if (tab === 'tab1') {
      setInputValuesTab1(prevState => ({
        ...prevState,
        [identifier]: value
      }))
    } else if (tab === 'tab2') {
      setInputValuesTab2(prevState => ({
        ...prevState,
        [identifier]: value
      }))
    }
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
  const handleInclude = e => {
    if (ID !== '' && valueFree !== '' && operator !== '') {
      if (query !== null && query !== '') {
        setQuery(query + ',' + `${ID}${operator}${valueFree}`)
      }
      if (query === null || query == '') {
        setQuery(`${ID}${operator}${valueFree}`)
      }
    }
  }

  const handleOption = (e, array, optionIndex, tab) => {
    const updatedInputValues =
      tab === 'tab1' ? { ...inputValuesTab1 } : { ...inputValuesTab2 }
    const updatedCheckedOptions =
      tab === 'tab1' ? { ...checkedOptionsTab1 } : { ...checkedOptionsTab2 }
    const filterIndex = e.target.getAttribute('data-filter-index')
    const elementLabel = e.target.getAttribute('data-element-label') // Get the element label from the checkbox
    const optionId = `option-${filterIndex}-${optionIndex}-${elementLabel}` // Construct the correct key

    updatedCheckedOptions[optionId] = e.target.checked // Update the checked state

    if (tab === 'tab1') {
      setCheckedOptionsTab1(updatedCheckedOptions)
    } else {
      setCheckedOptionsTab2(updatedCheckedOptions)
    }

    let start, end, variantType, referenceBases, alternateBases, assemblyId
    const title = []
    const value = []

    array.forEach(element => {
      title.push(element.schemaField)
      const inputValue =
        updatedInputValues[
          `${optionIndex}-${element.label}-${element.schemaField}`
        ]
      value.push(inputValue || element.value)

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
        case 'assemblyId':
          assemblyId = inputValue || element.value
          break
        default:
          break
      }
    })

    const specialQuery =
      start && end && variantType && referenceBases && alternateBases
        ? `${start}-${end}:${variantType}:${referenceBases}>${alternateBases}${
            assemblyId ? `&assemblyId:${assemblyId}` : ''
          }`
        : null

    const arrayQuery = title
      .map((titleQuery, indexQuery) =>
        titleQuery === 'geneId' || titleQuery === 'aminoacidChange'
          ? `${titleQuery}:${value[indexQuery]}`
          : `${titleQuery}=${value[indexQuery]}`
      )
      .join('&')

    const addQuery = specialQuery || arrayQuery

    if (e.target.checked) {
      setQuery(prevQuery => {
        if (!prevQuery) return addQuery
        return `${prevQuery},${addQuery}`
      })
    } else {
      setQuery(prevQuery => {
        const updatedQueries = prevQuery.split(',').filter(query => {
          if (specialQuery) {
            return query !== specialQuery
          } else {
            return !title.some((titleQuery, indexQuery) => {
              const valueQuery = `${titleQuery}=${value[indexQuery]}`
              const colonQuery = `${titleQuery}:${value[indexQuery]}`
              const mixQuery = `${titleQuery}:${value[indexQuery]}&${titleQuery}:${value[indexQuery]}`
              const combinedQuery = `${titleQuery}:${value[indexQuery]}&${
                title[indexQuery + 1]
              }:${value[indexQuery + 1]}`
              return (
                query === valueQuery ||
                query === colonQuery ||
                query === mixQuery ||
                query === combinedQuery
              )
            })
          }
        })
        return updatedQueries.join(',')
      })
    }

    if (tab === 'tab1') {
      setInputValuesTab1(updatedInputValues)
    } else {
      setInputValuesTab2(updatedInputValues)
    }
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

  const handleReset = () => {
    // Clear the query state
    setQuery('')
    setShowAlphanum(false)
    // Clear the state for input values and checked options

    setCheckedOptionsTab1({})
    setCheckedOptionsTab2({})

    // Uncheck all checkboxes manually
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
        let res2 = await axios.get(configData.API_URL + '/info')

        if (res2.data.meta.isAggregated) {
          setIsNetwork(true)
        }
        setTimeOut(true)

        if (res.data.response.filteringTerms !== undefined) {
          res.data.response.filteringTerms.forEach(element => {
            filteringTerms.push(element)
          })

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

  const search = e => {
    const newQuery = e.target.value

    // Update the query state
    setQuery(newQuery)

    const queryTerms = newQuery.split(',').map(term => term.trim())

    // Update the checked state for "tab1" checkboxes
    const updatedCheckedOptionsTab1 = { ...checkedOptionsTab1 }
    Object.keys(updatedCheckedOptionsTab1).forEach(key => {
      const optionValue = key.split('-').slice(3).join('-')
      updatedCheckedOptionsTab1[key] = queryTerms.some(term =>
        term.includes(optionValue)
      )
    })
    setCheckedOptionsTab1(updatedCheckedOptionsTab1)

    // Update the checked state for "tab2" checkboxes
    const updatedCheckedOptionsTab2 = { ...checkedOptionsTab2 }
    Object.keys(updatedCheckedOptionsTab2).forEach(key => {
      const optionValue = key.split('-').slice(3).join('-')
      updatedCheckedOptionsTab2[key] = queryTerms.some(term =>
        term.includes(optionValue)
      )
    })
    setCheckedOptionsTab2(updatedCheckedOptionsTab2)
  }

  const handleShowFilterEx = () => {
    setShowFilters(true)
  }

  useEffect(() => {
    const initializeInputValues = filters => {
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
      return initialInputValues
    }

    setInputValuesTab1(initializeInputValues(filtersTab1))
    setInputValuesTab2(initializeInputValues(filtersTab2))
  }, [filtersTab1, filtersTab2])

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
            <h1 className='version'>v0.5.6</h1>
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
            </div>
            <div className='buttonsDiv'>
              <button className='searchButton' type='submit'>
                <img
                  className='searchIcon'
                  src='./magnifier.png'
                  alt='searchIcon'
                ></img>
                <span className='buttonText'>Search</span>
              </button>
              <button
                className='clearButton'
                onClick={handleReset}
                type='button'
              >
                <img
                  className='clearIcon'
                  src='./eraser.png'
                  alt='eraserIcon'
                ></img>
                <span className='buttonText'>Clear</span>
              </button>
            </div>
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
            <button className='buttonAlphanum' onClick={handleInclude}>
              <ion-icon name='add-circle'></ion-icon>
            </button>
          </div>
        </tr>
      )}
      {showFilters && (
        <div className='layout-container'>
          <div className='tabs'>
            <div
              className={`tab ${activeTab === 'tab1' ? 'active' : ''}`}
              onClick={() => setActiveTab('tab1')}
            >
              CANCER
            </div>
            <div
              className={`tab ${activeTab === 'tab2' ? 'active' : ''}`}
              onClick={() => setActiveTab('tab2')}
            >
              COVID
            </div>
          </div>
          <div className='tab-content'>
            {activeTab === 'tab1' && (
              <FilterContent
                filters={filtersTab1}
                handleOption={(e, array, optionIndex) =>
                  handleOption(e, array, optionIndex, 'tab1')
                }
                handleOptionAlphanum={handleOptionAlphanum}
                handleInputChange={(e, key) =>
                  handleInputChange(e, key, 'tab1')
                }
                inputValues={inputValuesTab1}
                checkedOptions={checkedOptionsTab1}
                activeTab={activeTab}
              />
            )}
            {activeTab === 'tab2' && (
              <FilterContent
                filters={filtersTab2}
                handleOption={(e, array, optionIndex) =>
                  handleOption(e, array, optionIndex, 'tab2')
                }
                handleOptionAlphanum={handleOptionAlphanum}
                handleInputChange={(e, key) =>
                  handleInputChange(e, key, 'tab2')
                }
                inputValues={inputValuesTab2}
                checkedOptions={checkedOptionsTab2}
                activeTab={activeTab}
              />
            )}
          </div>
          <button
            className='buttonAllFilters'
            onClick={handleSeeFilteringTerms}
          >
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
              isNetwork={isNetwork}
            />
          </div>
        )}
        {isSubmitted && results === 'Individuals' && !triggerQuery && (
          <div>
            <IndividualsResults
              isNetwork={isNetwork}
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
              isNetwork={isNetwork}
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
              isNetwork={isNetwork}
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
              isNetwork={isNetwork}
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
              isNetwork={isNetwork}
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
              isNetwork={isNetwork}
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
              isNetwork={isNetwork}
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
              isNetwork={isNetwork}
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
              isNetwork={isNetwork}
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
              isNetwork={isNetwork}
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

        {results === null && !showFilteringTerms && isNetwork && (
          <BeaconInfo trigger={trigger} />
        )}

        {timeOut === true && error && showFilteringTerms && <h5>{error}</h5>}
      </div>
    </div>
  )
}

export default Layout
