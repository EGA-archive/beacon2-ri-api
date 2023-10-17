import '../../App.css'

import FilteringTerms from '../FilteringTerms/FilteringTerms'
import { NavLink } from 'react-router-dom'

import ResultsDatasets from '../Dataset/BeaconInfo'
import VariantsResults from '../GenomicVariations/VariantsResults'
import HorizontalExpansion from '../QueryExpansion/HorizontalExpansion'
import BiosamplesResults from '../Biosamples/BiosamplesResults'

import React, { useState, useEffect } from 'react'


import Switch from '@mui/material/Switch'
import MultiSwitch from 'react-multi-switch-toggle'

import configData from '../../config.json'

import axios from 'axios'

import ReactModal from 'react-modal'

import IndividualsResults from '../Individuals/IndividualsResults'
import CohortsModule from '../Cohorts/CohortsModule'

function Layout (props) {
  console.log(props)
  const [error, setError] = useState(null)

  const [placeholder, setPlaceholder] = useState('')

  const [results, setResults] = useState(null)
  const [query, setQuery] = useState(null)
  const [queryAux, setQueryAux] = useState(null)

  const [exampleQ, setExampleQ] = useState([])

  const [expansionSection, setExpansionSection] = useState(false)
  const [arrayFilteringTermsQE, setArrayFilteringTermsQE] = useState([])

  const [resultSet, setResultset] = useState('HIT')

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
  const [filteringTerms, setFilteringTerms] = useState(false)

  const [showVariants, setShowVariants] = useState(false)

  const [showResultsVariants, setShowResultsVariants] = useState(true)

  const [triggerCohorts, setTriggerCohorts] = useState(true)
  const [triggerQuery, setTriggerQuery] = useState(false)
  const [trigger, setTrigger] = useState(false)

  const [showBar, setShowBar] = useState(true)

  const [isOpenModal1, setIsOpenModal1] = useState(false)
  const [isOpenModal2, setIsOpenModal2] = useState(false)
  const [isOpenModal4, setIsOpenModal4] = useState(false)
  const [isOpenModal5, setIsOpenModal5] = useState(false)
  const [isOpenModal6, setIsOpenModal6] = useState(false)

  const [showExtraIndividuals, setExtraIndividuals] = useState(false)
  const [showOptions, setShowOptions] = useState(false)

  const [referenceName, setRefName] = useState('')
  const [referenceName2, setRefName2] = useState('')
  const [start, setStart] = useState('')
  const [start2, setStart2] = useState('')
  const [end, setEnd] = useState('')
  const [variantType, setVariantType] = useState('')
  const [variantType2, setVariantType2] = useState('')
  const [alternateBases, setAlternateBases] = useState('')
  const [alternateBases2, setAlternateBases2] = useState('')
  const [alternateBases3, setAlternateBases3] = useState('')
  const [referenceBases, setRefBases] = useState('')
  const [referenceBases2, setRefBases2] = useState('')
  const [aminoacid, setAminoacid] = useState('')
  const [aminoacid2, setAminoacid2] = useState('')
  const [geneID, setGeneId] = useState('')
  const [assemblyId, setAssemblyId] = useState('')
  const [assemblyId2, setAssemblyId2] = useState('')
  const [assemblyId3, setAssemblyId3] = useState('')

  const [hideForm, setHideForm] = useState(false)

  const [state, setstate] = useState({
    query: '',
    list: []
  })

  const [checked, setChecked] = useState(true)
  const [checked2, setChecked2] = useState(false)

  const [timeOut, setTimeOut] = useState(true)

  const [isSubmitted, setIsSub] = useState(false)

  const [arrayFilteringTerms, setArrayFilteringTerms] = useState([])

  const handleChangeSwitch = e => {
    setDescendantTerm(e.target.checked)
    setChecked(e.target.checked)
  }

  const onToggle = selectedItem => {
    console.log(selectedItem)
    if (selectedItem === 0) {
      setSimilarity('low')
    } else if (selectedItem === 1) {
      setSimilarity('medium')
    } else {
      setSimilarity('high')
    }
  }

  const onToggle2 = selectedItem => {
    console.log(selectedItem)
    if (selectedItem === 0) {
      setResultset('HIT')
    } else if (selectedItem === 1) {
      setResultset('MISS')
    } else if (selectedItem === 2) {
      setResultset('NONE')
    } else {
      setResultset('ALL')
    }
  }

  const handleCloseModal1 = () => {
    setIsOpenModal1(false)
  }

  const handleHelpModal2 = () => {
    setIsOpenModal2(true)
  }

  const handleCloseModal2 = () => {
    setIsOpenModal2(false)
  }

  const handleCloseModal3 = () => {
    setPopUp(false)
  }

  const handleHelpModal4 = () => {
    setIsOpenModal4(true)
  }

  const handleHelpModal5 = () => {
    setIsOpenModal5(true)
  }

  const handleHelpModal6 = () => {
    setIsOpenModal6(true)
  }

  const handleFilteringTerms = async e => {
    setTimeOut(false)
    if (props.collection === 'Individuals') {
      try {
        let res = await axios.get(
          configData.API_URL + '/individuals/filtering_terms?skip=0&limit=0'
        )
        setTimeOut(true)
        console.log(res)
        if (res.data.response.filteringTerms !== undefined) {
          setFilteringTerms(res)
          setResults(null)
        } else {
          setError('No filtering terms now available')
        }
      } catch (error) {
        console.log(error)
      }
    } else if (props.collection === 'Cohorts') {
      try {
        let res = await axios.get(
          configData.API_URL + '/cohorts/filtering_terms?skip=0&limit=0'
        )
        setTimeOut(true)
        if (res.data.response.filteringTerms !== undefined) {
          setFilteringTerms(res)
          setResults(null)
        } else {
          setError('No filtering terms now available')
        }
      } catch (error) {
        console.log(error)
      }
    } else if (props.collection === 'Variant') {
      try {
        let res = await axios.get(
          configData.API_URL + '/g_variants/filtering_terms?skip=0&limit=0'
        )
        setTimeOut(true)
        if (res.data.response.filteringTerms !== undefined) {
          setFilteringTerms(res)
          setResults(null)
        } else {
          setError('No filtering terms now available')
        }
      } catch (error) {
        console.log(error)
        setError('No filtering terms now available')
      }
    } else if (props.collection === 'Analyses') {
      try {
        let res = await axios.get(
          configData.API_URL + '/analyses/filtering_terms?skip=0&limit=0'
        )
        setTimeOut(true)
        if (res.data.response.filteringTerms !== undefined) {
          setFilteringTerms(res)
          setResults(null)
        } else {
          setError('No filtering terms now available')
        }
      } catch (error) {
        console.log(error)
      }
    } else if (props.collection === 'Runs') {
      try {
        let res = await axios.get(
          configData.API_URL + '/runs/filtering_terms?skip=0&limit=0'
        )
        setTimeOut(true)
        if (res.data.response.filteringTerms !== undefined) {
          setFilteringTerms(res)
          setResults(null)
        } else {
          setError('No filtering terms now available')
        }
      } catch (error) {
        console.log(error)
      }
    } else if (props.collection === 'Biosamples') {
      try {
        let res = await axios.get(
          configData.API_URL + '/biosamples/filtering_terms?skip=0&limit=0'
        )
        setTimeOut(true)
        if (res.data.response.filteringTerms !== undefined) {
          setFilteringTerms(res)
          setResults(null)
        } else {
          setError('No filtering terms now available')
        }
      } catch (error) {
        console.log(error)
      }
    }

    setShowFilteringTerms(true)
  }

  const handleExQueries = () => {
    if (props.collection === 'Individuals') {
      setExampleQ([
        'Weight>100',
        'NCIT:C16352',
        'geographicOrigin=%land%',
        'geographicOrigin!England',
        'NCIT:C42331'
      ])
    } else if (props.collection === 'Variant') {
      setExampleQ(['GENO:GENO_0000458'])
    } else if (props.collection === 'Biosamples') {
      setExampleQ(['UBERON:0000178', 'EFO:0009654', 'sampleOriginType:blood'])
    } else if (props.collection === 'Runs') {
      setExampleQ([''])
    } else if (props.collection === 'Analyses') {
      setExampleQ([''])
    }
  }

  const handleExtraSectionIndividuals = e => {
    setShowOptions(!showOptions)
    setShowButton(!showButton)
  }

  const handleChangeStart = e => {
    setStart(e.target.value)
  }
  const handleChangeStart2 = e => {
    setStart2(e.target.value)
  }
  const handleChangeRefN2 = e => {
    setRefName2(e.target.value)
  }
  const handleChangeAlternateB2 = e => {
    setAlternateBases2(e.target.value)
  }
  const handleChangeAssembly2 = e => {
    setAssemblyId2(e.target.value)
  }
  const handleChangeAssembly3 = e => {
    setAssemblyId3(e.target.value)
  }

  const handleChangeAlternateB = e => {
    setAlternateBases(e.target.value)
  }

  const handleChangeAlternateB3 = e => {
    setAlternateBases3(e.target.value)
  }

  const handleChangeReferenceB = e => {
    setRefBases(e.target.value)
  }
  const handleChangeReferenceB2 = e => {
    setRefBases2(e.target.value)
  }

  const handleChangeRefN = e => {
    setRefName(e.target.value)
  }

  const handleChangeEnd = e => {
    setEnd(e.target.value)
  }

  const handleChangeVariantType = e => {
    setVariantType(e.target.value)
  }
  const handleChangeVariantType2 = e => {
    setVariantType2(e.target.value)
  }

  const handleChangeAminoacid = e => {
    setAminoacid(e.target.value)
  }
  const handleChangeAminoacid2 = e => {
    setAminoacid2(e.target.value)
  }

  const handleChangeGeneId = e => {
    setGeneId(e.target.value)
  }

  const handleChangeAssembly = e => {
    setAssemblyId(e.target.value)
  }

  const handleClick = () => {
    setShowBar(!showBar)
    setShowResultsVariants(false)
  }

  const handleHideVariantsForm = e => {
    setHideForm(false)
  }

  const handleQEclick = e => {
    setExpansionSection(true)
  }

  useEffect(() => {
    if (props.collection === 'Individuals') {
      setPlaceholder('filtering term comma-separated, ID><=value')
      setExtraIndividuals(true)
    } else if (props.collection === 'Biosamples') {
      setPlaceholder('filtering term comma-separated')
    } else if (props.collection === 'Cohorts') {
      setShowCohorts(true)
      setExtraIndividuals(false)
      setPlaceholder('Search for any cohort')
    } else if (props.collection === 'Variant') {
      setPlaceholder('filtering term comma-separated')
      setExtraIndividuals(false)
      setShowVariants(true)
    } else if (props.collection === 'Analyses') {
      setPlaceholder('filtering term comma-separated')
      setExtraIndividuals(false)
    } else if (props.collection === 'Runs') {
      setPlaceholder('filtering term comma-separated')
      setExtraIndividuals(false)
    } else if (props.collection === 'Datasets') {
      setPlaceholder('filtering term comma-separated')
      setExtraIndividuals(false)
    } else {
      setPlaceholder('')
    }

    const fetchData = async () => {
      // for query expansion
      try {
        let res = await axios.get(
          configData.API_URL + '/individuals/filtering_terms'
        )
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
      }
    }

    // call the function
    fetchData()
      // make sure to catch any error
      .catch(console.error)
  }, [])

  const onSubmit = async event => {
    event.preventDefault()

    setIsSub(true)

    setQueryAux(query)

    if (queryAux !== query) {
      setTriggerQuery(!triggerQuery)
    }
    console.log(query)

    setExampleQ([])

    if (query === '1' || query === '') {
      setQuery(null)
    }
    if (props.collection === 'Individuals') {
      setResults('Individuals')
    } else if (props.collection === 'Variant') {
      setResults('Variant')
    } else if (props.collection === 'Biosamples') {
      setResults('Biosamples')
    } else if (props.collection === 'Analyses') {
      setResults('Analyses')
    } else if (props.collection === 'Runs') {
      setResults('Runs')
    }
  }

  function search (e) {
    setQuery(e.target.value)
  }

  const handleSubmit = async e => {
    e.preventDefault()
    setPlaceholder('filtering term comma-separated, ID><=value')
    setIsSub(!isSubmitted)
    setExampleQ([])
    setResults('Variant')
  }

  return (
    <div className='container1'>
      <div className='container2'>
        <button className='helpButton' onClick={handleHelpModal2}>
          <img
            className='questionLogo2'
            src='./question.png'
            alt='questionIcon'
          ></img>
        </button>
        <NavLink className='NavlinkVerifier' exact to='/verifier'>
          BEACON VALIDATOR
        </NavLink>

        <div className='logos'>
          {/* <a href="https://www.cineca-project.eu/" target="_blank">
                        <img className="cinecaLogo" src="./CINECA_logo.png" alt='cinecaLogo'></img>
                    </a> */}
          <a href='https://elixir-europe.org/' target='_blank'>
            <img
              className='elixirLogo'
              src='./white-orange-logo.png'
              alt='elixirLogo'
            ></img>
          </a>
        </div>
      </div>

      <div className='Modal1'>
        {popUp && (
          <ReactModal
            isOpen={popUp}
            onRequestClose={handleCloseModal3}
            shouldCloseOnOverlayClick={true}
          >
            <button onClick={handleCloseModal3}>
              <img
                className='closeLogo'
                src='./cancel.png'
                alt='cancelIcon'
              ></img>
            </button>

            <p>
              Please, bear in mind that you might have to log in to get
              information from some datasets.
            </p>
          </ReactModal>
        )}
      </div>
      <nav className='navbar'>
        <div>
          {expansionSection === false && cohorts === false && (
            <button onClick={handleQEclick} className='btn-3'>
              <span className='spanQE'>Query expansion</span>
            </button>
          )}
        </div>
        {expansionSection === true && (
          <HorizontalExpansion
            arrayFilteringTermsQE={arrayFilteringTermsQE}
            query={query}
            setQuery={setQuery}
            setExpansionSection={setExpansionSection}
          />
        )}

        {showBar === true && (
          <div className='container-fluid'>
            {cohorts === false && showBar === true && (
              <div>
                <form className='d-flex' onSubmit={onSubmit}>
                  <input
                    className='formSearch'
                    type='search'
                    placeholder={placeholder}
                    value={query}
                    onChange={e => search(e)}
                    aria-label='Search'
                  />

                  <button className='searchButton' type='submit'>
                    <img
                      className='searchIcon'
                      src='./magnifier.png'
                      alt='searchIcon'
                    ></img>
                  </button>
                </form>
              </div>
            )}
            {props.collection === 'Cohorts' && (
              <CohortsModule
                optionsCohorts={props.optionsCohorts}
                selectedCohorts={props.selectedCohorts}
                setSelectedCohorts={props.setSelectedCohorts}
                setShowGraphs={props.setShowGraphs}
              />
            )}
          </div>
        )}

        <div className='additionalOptions'>
          <div className='example'>
            {cohorts === false && props.collection !== '' && showBar === true && (
              <div className='bulbExample'>
                <button className='exampleQueries' onClick={handleExQueries}>
                  Query Examples
                </button>
                <img
                  className='bulbLogo'
                  src='../light-bulb.png'
                  alt='bulbIcon'
                ></img>
                <div>
                  {exampleQ[0] &&
                    exampleQ.map(result => {
                      return (
                        <div id='exampleQueries'>
                          <button
                            className='exampleQuery'
                            onClick={() => {
                              setPlaceholder(`${result}`)
                              setQuery(`${result}`)
                              setValue(`${result}`)
                            }}
                          >
                            {result}
                          </button>
                        </div>
                      )
                    })}
                </div>
              </div>
            )}
            {props.collection !== '' && showBar === true && (
              <button className='filters' onClick={handleFilteringTerms}>
                Filtering Terms
              </button>
            )}
            <div className='resultSetsDiv'>
              <label>
                <h2>Include Resultset Responses</h2>
              </label>
              <MultiSwitch
                texts={['HIT', 'MISS', 'NONE', 'ALL']}
                selectedSwitch={0}
                bgColor={'white'}
                onToggleCallback={onToggle2}
                fontColor={'black'}
                selectedFontColor={'white'}
                border='0'
                selectedSwitchColor='#e29348'
                borderWidth='1'
                height={'23px'}
                fontSize={'12px'}
                eachSwitchWidth={55}
              ></MultiSwitch>
            </div>
          </div>
        </div>
        {showVariants === true && showBar === true && (
          <button className='modeVariants' onClick={handleClick}>
            <h2 className='modeVariantsQueries'>Change to FORM mode</h2>
          </button>
        )}
        {showVariants === true && showBar === false && (
          <button className='modeVariants' onClick={handleClick}>
            <h2 className='modeVariantsQueries'>Change to BAR mode</h2>
          </button>
        )}
        <hr></hr>
        {showExtraIndividuals && (
          <div className='containerExtraSections'>
            {showButton && (
              <button
                className='arrowButton'
                onClick={handleExtraSectionIndividuals}
              >
                <img
                  className='arrowLogo'
                  src='../arrow-down.png'
                  alt='arrowIcon'
                ></img>
              </button>
            )}
            {!showButton && (
              <button
                className='arrowButton'
                onClick={handleExtraSectionIndividuals}
              >
                <img
                  className='arrowLogo'
                  src='../arrow-up.png'
                  alt='arrowUpIcon'
                ></img>
              </button>
            )}
            {showOptions && (
              <div className='extraSections'>
                <div className='advContainer'>
                  <form className='advSearchForm' onSubmit={onSubmit}>
                    <div>
                      <div className='resultset'>
                        <div className='advSearch-module'>
                          <label>
                            <h2>Similarity</h2>
                          </label>
                          <input
                            id='similarityCheck'
                            type='checkbox'
                            defaultChecked={false}
                            onChange={() => setChecked2(!checked2)}
                          />

                          {checked2 && (
                            <MultiSwitch
                              texts={['Low', 'Medium', 'High']}
                              selectedSwitch={0}
                              bgColor={'white'}
                              onToggleCallback={onToggle}
                              fontColor={'black'}
                              selectedFontColor={'white'}
                              border='0'
                              selectedSwitchColor='#4f85bc'
                              borderWidth='1'
                              height={'23px'}
                              fontSize={'12px'}
                              eachSwitchWidth={60}
                            ></MultiSwitch>
                          )}
                        </div>
                        <div className='advSearch-module'>
                          <label>
                            <h2>Include Descendant Terms</h2>
                          </label>
                          <div className='switchDescendants'>
                            <h3>False</h3>
                            <Switch
                              checked={checked}
                              onChange={handleChangeSwitch}
                              inputProps={{ 'aria-label': 'controlled' }}
                              color='warning'
                              size='small'
                            />
                            <h3>True</h3>
                          </div>
                        </div>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            )}
          </div>
        )}
        {hideForm === true && (
          <button onClick={handleHideVariantsForm}>
            <img
              className='arrowLogo'
              src='../arrow-down.png'
              alt='arrowIcon'
            />
          </button>
        )}
        {showVariants && showBar === false && hideForm === false && (
          <div>
            <form onSubmit={handleSubmit}>
              <div className='variantsContainer'>
                <div className='moduleVariants'>
                  <label className='labelVariantsTittle'>
                    Sequence queries
                  </label>
                  <div>
                    <label className='labelVariants'>AssemblyID*</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={assemblyId}
                      onChange={handleChangeAssembly}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>Reference name*</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={referenceName}
                      onChange={handleChangeRefN}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>
                      Start (single value)*
                    </label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={start}
                      onChange={handleChangeStart}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>referenceBases</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={referenceBases}
                      onChange={handleChangeReferenceB}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>alternateBases*</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={alternateBases}
                      onChange={handleChangeAlternateB}
                    ></input>
                  </div>
                  <div className='DivButtonVariants'>
                    <input
                      className='buttonVariants'
                      type='submit'
                      value='Search'
                    />
                  </div>
                </div>
                <div className='moduleVariants'>
                  <label className='labelVariantsTittle'>Range queries</label>
                  <div>
                    <label className='labelVariants'>AssemblyID*</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={assemblyId2}
                      onChange={handleChangeAssembly2}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>Reference name*</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={referenceName2}
                      onChange={handleChangeRefN2}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>
                      Start (single value)*
                    </label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={start2}
                      onChange={handleChangeStart2}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>End (single value)*</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={end}
                      onChange={handleChangeEnd}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>Variant type:</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={variantType}
                      onChange={handleChangeVariantType}
                    ></input>{' '}
                  </div>
                  <div>
                    <h3>OR</h3>
                    <div className='basesSection'>
                      <div className='referenceBasesContainer'>
                        <label className='labelVariants'>referenceBases:</label>
                        <input
                          className='inputVariants'
                          type='text'
                          value={referenceBases2}
                          onChange={handleChangeReferenceB2}
                        ></input>
                      </div>
                      <div>
                        <label className='labelVariants'>alternateBases:</label>
                        <input
                          className='inputVariants'
                          type='text'
                          value={alternateBases2}
                          onChange={handleChangeAlternateB2}
                        ></input>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h3>OR</h3>
                    <label className='labelVariants'>Aminoacid Change:</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={aminoacid}
                      onChange={handleChangeAminoacid}
                    ></input>
                  </div>
                  <div className='DivButtonVariants'>
                    <input
                      className='buttonVariants'
                      type='submit'
                      value='Search'
                    />
                  </div>
                </div>
                <div className='moduleVariants'>
                  <label className='labelVariantsTittle'>Gene ID queries</label>
                  <div>
                    <label className='labelVariants'>Gene ID*</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={geneID}
                      onChange={handleChangeGeneId}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>AssemblyID</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={assemblyId3}
                      onChange={handleChangeAssembly3}
                    ></input>
                  </div>
                  <div>
                    <label className='labelVariants'>Variant type:</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={variantType2}
                      onChange={handleChangeVariantType2}
                    ></input>
                  </div>
                  <div className='DivButtonVariants'>
                    <input
                      className='buttonVariants'
                      type='submit'
                      value='Search'
                    />
                  </div>
                </div>
              </div>
            </form>
          </div>
        )}
      </nav>

      <div>
        <ReactModal
          isOpen={isOpenModal1}
          onRequestClose={handleCloseModal1}
          shouldCloseOnOverlayClick={true}
        >
          <button onClick={handleCloseModal1}>
            <img
              className='closeLogo'
              src='./cancel.png'
              alt='cancelIcon'
            ></img>
          </button>

          <p>Help for alphanumerical and numerical queries.</p>
        </ReactModal>
        <ReactModal
          isOpen={isOpenModal2}
          onRequestClose={handleCloseModal2}
          shouldCloseOnOverlayClick={true}
        >
          <button onClick={handleCloseModal2}>
            <img
              className='closeLogo'
              src='./cancel.png'
              alt='cancelIcon'
            ></img>
          </button>

          <p>
            "Please use the online validator to check your Beacon API for
            specification compliance before it is included to the network. It
            will check the metadata, defined endpoints and responses over
            Beacon's v2 Schemas."{' '}
          </p>
        </ReactModal>
      </div>

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
          <ResultsDatasets trigger={trigger} />
        )}
        {isSubmitted && results === 'Individuals' && triggerQuery && (
          <div>
            <IndividualsResults
              query={query}
              resultSets={resultSet}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
            />
          </div>
        )}
        {isSubmitted && results === 'Individuals' && !triggerQuery && (
          <div>
            <IndividualsResults
              query={query}
              resultSets={resultSet}
              ID={ID}
              operator={operator}
              valueFree={valueFree}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
            />
          </div>
        )}
        {isSubmitted && results === 'Variant' && triggerQuery && (
          <div>
            <VariantsResults
              query={query}
              resultSets={resultSet}
              showResultsVariants={showResultsVariants}
              setHideForm={setHideForm}
              showBar={showBar}
              aminoacid2={aminoacid2}
              assemblyId2={assemblyId2}
              assemblyId3={assemblyId3}
              alternateBases3={alternateBases3}
              alternateBases2={alternateBases2}
              isSubmitted={isSubmitted}
              variantType2={variantType2}
              start2={start2}
              referenceName2={referenceName2}
              referenceName={referenceName}
              assemblyId={assemblyId}
              start={start}
              end={end}
              variantType={variantType}
              alternateBases={alternateBases}
              referenceBases={referenceBases}
              referenceBases2={referenceBases2}
              aminoacid={aminoacid}
              geneID={geneID}
            />
          </div>
        )}
        {isSubmitted && results === 'Variant' && !triggerQuery && (
          <div>
            <VariantsResults
              query={query}
              resultSets={resultSet}
              showResultsVariants={showResultsVariants}
              setHideForm={setHideForm}
              showBar={showBar}
              aminoacid2={aminoacid2}
              assemblyId2={assemblyId2}
              assemblyId3={assemblyId3}
              alternateBases3={alternateBases3}
              alternateBases2={alternateBases2}
              isSubmitted={isSubmitted}
              variantType2={variantType2}
              start2={start2}
              referenceName2={referenceName2}
              referenceName={referenceName}
              assemblyId={assemblyId}
              start={start}
              end={end}
              variantType={variantType}
              alternateBases={alternateBases}
              referenceBases={referenceBases}
              referenceBases2={referenceBases2}
              aminoacid={aminoacid}
              geneID={geneID}
            />
          </div>
        )}
        {isSubmitted && results === 'Biosamples' && triggerQuery && (
          <div>
            <BiosamplesResults
              query={query}
              resultSets={resultSet}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
            />
          </div>
        )}
        {isSubmitted && results === 'Biosamples' && !triggerQuery && (
          <div>
            <BiosamplesResults
              query={query}
              resultSets={resultSet}
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
            />
          </div>
        )}
        {results === null && timeOut === true && showFilteringTerms && (
          <FilteringTerms
            filteringTerms={filteringTerms}
            collection={props.collection}
            setPlaceholder={setPlaceholder}
            placeholder={placeholder}
            query={query}
            setQuery={setQuery}
          />
        )}
        {timeOut === false}
      </div>
    </div>
  )
}

export default Layout
