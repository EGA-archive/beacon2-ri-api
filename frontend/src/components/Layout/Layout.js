import '../../App.css'
import './Layout.css'
import FilteringTerms from '../FilteringTerms/FilteringTerms'

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
  const [query, setQuery] = useState(null)
  const [queryAux, setQueryAux] = useState(null)

  const [exampleQ, setExampleQ] = useState([])

  const [expansionSection, setExpansionSection] = useState(false)
  const [arrayFilteringTermsQE, setArrayFilteringTermsQE] = useState([])

  const [resultSet, setResultset] = useState('HIT')
  const [resultSetAux, setResultsetAux] = useState('HIT')

  const [descendantTerm, setDescendantTerm] = useState('true')

  const [similarity, setSimilarity] = useState('Select')

  const [cohorts, setShowCohorts] = useState(false)

  const [ID, setId] = useState('age')
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
  const [granularity, setGranularity] = useState('boolean')

  const [terms, setTerm] = useState([])

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
  const [variantMinLength, setVariantMinLength] = useState('')
  const [variantMaxLength, setVariantMaxLength] = useState('')
  const [variantMinLength2, setVariantMinLength2] = useState('')
  const [variantMaxLength2, setVariantMaxLength2] = useState('')
  const [clinicalRelevance, setClinicalRelevance] = useState('')
  const [clinicalRelevance2, setClinicalRelevance2] = useState('')
  const [clinicalRelevance3, setClinicalRelevance3] = useState('')

  const [sequenceSubmitted, setSequenceSub] = useState(false)
  const [rangeSubmitted, setRangeSub] = useState(false)
  const [rangeSubmitted1, setRangeSub1] = useState(false)
  const [rangeSubmitted2, setRangeSub2] = useState(false)
  const [geneSubmitted, setGeneSub] = useState(false)
  const [geneSubmitted2, setGeneSub2] = useState(false)

  const [hideForm, setHideForm] = useState(false)

  const [state, setstate] = useState({
    query: '',
    list: []
  })

  const [showAlphanum, setShowAlphanum] = useState(false)

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
      console.log('hola')
      if (query !== null) {
        setQuery(query + ',' + `${ID}${operator}${valueFree}`)
      }
      if (query === null) {
        setQuery(`${ID}${operator}${valueFree}`)
      }
    }
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
  const handleChangeVariantMaxLength = e => {
    setVariantMaxLength(e.target.value)
  }
  const handleChangeVariantMinLength = e => {
    setVariantMinLength(e.target.value)
  }
  const handleChangeVariantMaxLength2 = e => {
    setVariantMaxLength2(e.target.value)
  }
  const handleChangeVariantMinLength2 = e => {
    setVariantMinLength2(e.target.value)
  }

  const handleChangeClinicalRelevance = e => {
    setClinicalRelevance(e.target.value)
  }

  const handleChangeClinicalRelevance2 = e => {
    setClinicalRelevance2(e.target.value)
  }
  const handleChangeClinicalRelevance3 = e => {
    setClinicalRelevance3(e.target.value)
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

  const handleRangeModule = e => {
    setRangeSub(true)
    setCountRangeModule(countRangeModule + 1)

    let objectRange = {
      assemblyId: assemblyId2,
      referenceName: referenceName2,
      start: start2,
      end: end,
      variantType: variantType,
      alternateBases: alternateBases2,
      referenceBases: referenceBases2,
      aminoacid: aminoacid,
      variantMinLength: variantMinLength,
      variantMaxLength: variantMaxLength,
      clinicalRelevance: clinicalRelevance2
    }
    console.log(objectRange)
    rangeModuleArray.push(objectRange)

    setAssemblyId2('')
    setRefName2('')
    setStart2('')
    setEnd('')
    setVariantType('')
    setAlternateBases2('')
    setRefBases2('')
    setAminoacid('')
    setVariantMinLength('')
    setVariantMaxLength('')
    setClinicalRelevance2('')
  }

  const handleSeqeModule = e => {
    setSequenceSub(true)
    setCountSeqModule(countSeqModule + 1)

    let objectSeq = {
      assemblyId: assemblyId,
      referenceName: referenceName,
      start: start,
      referenceBases: referenceBases,
      alternateBases: alternateBases,
      clinicalRelevance: clinicalRelevance
    }

    seqModuleArray.push(objectSeq)

    setAssemblyId('')
    setRefName('')
    setStart('')
    setRefBases('')
    setAlternateBases('')
    setClinicalRelevance('')
  }

  const handleGeneModule = e => {
    setGeneSub(true)
    setCountGeneModule(countGeneModule + 1)

    let objectGene = {
      geneID: geneID,
      aminoacid: aminoacid2,
      assemblyId: assemblyId3,
      variantType: variantType2,
      variantMinLength: variantMinLength2,
      variantMaxLength: variantMaxLength2,
      clinicalRelevance: clinicalRelevance3
    }

    geneModuleArray.push(objectGene)

    setGeneId('')
    setAminoacid2('')
    setAssemblyId3('')
    setVariantType2('')
    setVariantMinLength2('')
    setVariantMaxLength2('')
    setClinicalRelevance3('')
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

  const handleOptionDisease = e => {
    if (e.target.checked === true) {
      filteringTerms.forEach(element => {
        if (element.label) {
          if (element.label.toLowerCase() === e.target.value.toLowerCase()) {
            let ontology = element.id
            terms.push([element.label, ontology])
            if (query !== null && query !== '') {
              setQuery(query + ',' + 'disease=' + element.label)
            } else {
              setQuery('disease=' + element.label)
            }
          } else {
            if (query !== null && query !== '') {
              setQuery(query + ',' + 'disease=' + e.target.value)
            } else {
              setQuery('disease=' + e.target.value)
            }
          }
        }
      })
    } else {
      if (query.includes(`,disease=${e.target.value}`)) {
        setQuery(query.replace(`,disease=${e.target.value}`, ''))
      } else if (query.includes(`disease=${e.target.value},`)) {
        setQuery(query.replace(`disease=${e.target.value},`, ''))
      } else {
        setQuery(query.replace(`disease=${e.target.value}`, ''))
      }
    }
  }

  const handleOptionSex = e => {
    if (e.target.checked === true) {
      filteringTerms.forEach(element => {
        if (element.label) {
          if (element.label.toLowerCase() === e.target.value.toLowerCase()) {
            let ontology = element.id
            terms.push([element.label, ontology])
            if (query !== null && query !== '') {
              setQuery(query + ',' + 'sex=' + element.label)
            } else {
              setQuery('sex=' + element.label)
            }
          } else {
            if (query !== null && query !== '') {
              setQuery(query + ',' + 'sex=' + e.target.value)
            } else {
              setQuery('sex=' + e.target.value)
            }
          }
        }
      })
    } else {
      if (query.includes(`,sex=${e.target.value}`)) {
        setQuery(query.replace(`,sex=${e.target.value}`, ''))
      } else if (query.includes(`sex=${e.target.value},`)) {
        setQuery(query.replace(`sex=${e.target.value},`, ''))
      } else {
        setQuery(query.replace(`sex=${e.target.value}`, ''))
      }
    }
  }

  const handleOptionAge = e => {
    setShowAlphanum(true)
  }

  const handleOptionHisto = e => {
    if (e.target.checked === true) {
      filteringTerms.forEach(element => {
        if (element.label) {
          if (element.label.toLowerCase() === e.target.value.toLowerCase()) {
            let ontology = element.id
            terms.push([element.label, ontology])
            if (query !== null && query !== '') {
              setQuery(query + ',' + 'histopathology=' + element.label)
            } else {
              setQuery('histopathology=' + element.label)
            }
          } else {
            if (query !== null && query !== '') {
              setQuery(query + ',' + 'histopathology=' + e.target.value)
            } else {
              setQuery('histopathology=' + e.target.value)
            }
          }
        }
      })
    } else {
      if (query.includes(`,histopathology=${e.target.value}`)) {
        setQuery(query.replace(`,histopathology=${e.target.value}`, ''))
      } else if (query.includes(`histopathology=${e.target.value},`)) {
        setQuery(query.replace(`histopathology=${e.target.value},`, ''))
      } else {
        setQuery(query.replace(`histopathology=${e.target.value}`, ''))
      }
    }
  }

  const handleOptionTreatment = e => {
    if (e.target.checked === true) {
      filteringTerms.forEach(element => {
        if (element.label) {
          if (element.label.toLowerCase() === e.target.value.toLowerCase()) {
            let ontology = element.id
            terms.push([element.label, ontology])
            if (query !== null && query !== '') {
              setQuery(query + ',' + 'treatment=' + element.label)
            } else {
              setQuery('treatment=' + element.label)
            }
          } else {
            if (query !== null && query !== '') {
              setQuery(query + ',' + 'treatment=' + e.target.value)
            } else {
              setQuery('treatment=' + e.target.value)
            }
          }
        }
      })
    } else {
      if (query.includes(`,treatment=${e.target.value}`)) {
        setQuery(query.replace(`,treatment=${e.target.value}`, ''))
      } else if (query.includes(`treatment=${e.target.value},`)) {
        setQuery(query.replace(`treatment=${e.target.value},`, ''))
      } else {
        setQuery(query.replace(`treatment=${e.target.value}`, ''))
      }
    }
  }

  const handleOptionVariant = e => {
    if (e.target.checked) {
      let objectRange = {
        assemblyId: assemblyId2,
        referenceName: referenceName2,
        start: '110173330',
        end: '110173331',
        variantType: 'SNP',
        alternateBases: 'T',
        referenceBases: 'C',
        aminoacid: aminoacid,
        variantMinLength: variantMinLength,
        variantMaxLength: variantMaxLength,
        clinicalRelevance: clinicalRelevance2
      }
      rangeModuleArray.push(objectRange)
      console.log(rangeModuleArray)
      setRangeSub1(true)
    } else {
      setRangeSub1(false)
      setRangeModuleArray([])
    }
  }

  const handleOptionVariant2 = e => {
    if (e.target.checked) {
      let objectRange = {
        assemblyId: assemblyId2,
        referenceName: referenceName2,
        start: '1334544',
        end: '1334545',
        variantType: 'SNP',
        alternateBases: 'A',
        referenceBases: 'T',
        aminoacid: aminoacid,
        variantMinLength: variantMinLength,
        variantMaxLength: variantMaxLength,
        clinicalRelevance: clinicalRelevance2
      }
      let objectRange2 = {
        assemblyId: assemblyId2,
        referenceName: referenceName2,
        start: '3670751',
        end: '3670752',
        variantType: 'SNP',
        alternateBases: 'T',
        referenceBases: 'C',
        aminoacid: aminoacid,
        variantMinLength: variantMinLength,
        variantMaxLength: variantMaxLength,
        clinicalRelevance: clinicalRelevance2
      }
      rangeModuleArray.push(objectRange)
      rangeModuleArray.push(objectRange2)
      console.log(rangeModuleArray)
      setRangeSub2(true)
    } else {
      setRangeSub2(false)
      setRangeModuleArray([])
    }
  }
  const handleOptionVariant3 = e => {
    if (e.target.checked) {
      let objectGene = {
        geneID: 'CTNNB1',
        aminoacid: aminoacid2,
        assemblyId: assemblyId3,
        variantType: variantType2,
        variantMinLength: variantMinLength2,
        variantMaxLength: variantMaxLength2,
        clinicalRelevance: clinicalRelevance3
      }

      geneModuleArray.push(objectGene)
      setGeneSub(true)

      setQuery('treatment=Chemotherapy, ')
    } else {
      setGeneSub(false)
      setGeneModuleArray([])
    }
  }
  const handleOptionVariant4 = e => {
    if (e.target.checked) {
      let objectGene = {
        geneID: 'CSDE1',
        aminoacid: aminoacid2,
        assemblyId: assemblyId3,
        variantType: variantType2,
        variantMinLength: variantMinLength2,
        variantMaxLength: variantMaxLength2,
        clinicalRelevance: clinicalRelevance3
      }

      geneModuleArray.push(objectGene)
      setGeneSub2(true)
    } else {
      setGeneSub2(false)
      setGeneModuleArray([])
    }
  }

  const handleReset = e => {
    setQuery('')
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
    setQuery(e.target.value)
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

  return (
    <div className='container1'>
      <div className='sectionModules'>
        <div className='container2'>
          <div className='logosVersionContainer'>
            <div className='logos'>
              <a
                href='https://eosc4cancer.eu/'
                className='logoInstitution'
                target='_blank'
                rel='noreferrer'
              >
                <img
                  className='eosc4cancer'
                  src='../eosc4cancer.png'
                  alt='eosc4cancer'
                ></img>
              </a>
            </div>
            <h1 className='version'>v0.5.2</h1>
          </div>
        </div>
        <div className='containerSelection'>
          <select
            name='select'
            className='selectModule1'
            onChange={handleChangeSelection1}
          >
            <option value='boolean' selected className='optionClass'>
              Do you have?...{' '}
            </option>
            <option value='count'>How many?...</option>
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
        {rangeSubmitted1 && (
          <div className='moduleAddedVariant'>
            <h4>Range query</h4>
            <h2>alternateBases: T</h2>
            <h2>referenceBases: C</h2>
            <h2>start: 110173330</h2>
            <h2>end: 110173331</h2>
            <h2>type: SNP</h2>
          </div>
        )}
        {rangeSubmitted2 && (
          <div className='containerModulesVariants'>
            <div className='moduleAddedVariant2'>
              <h4>Range query</h4>
              <h2>alternateBases: A</h2>
              <h2>referenceBases: T</h2>
              <h2>start: 1334544</h2>
              <h2>end: 1334545</h2>
              <h2>type: SNP</h2>
            </div>
            <div className='moduleAddedVariant2'>
              <h4>Range query</h4>
              <h2>alternateBases: T</h2>
              <h2>referenceBases: C</h2>
              <h2>start: 3670751</h2>
              <h2>end: 3670752</h2>
              <h2>type: SNP</h2>
            </div>
          </div>
        )}
        {geneSubmitted && (
          <div className='moduleAddedVariant'>
            <h4>Gene query</h4>
            <h2>Gene ID: CTNNB1</h2>
          </div>
        )}
        {geneSubmitted2 && (
          <div className='moduleAddedVariant'>
            <h4>Gene query</h4>
            <h2>Gene ID: CSDE1</h2>
          </div>
        )}
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
                  value={'age'}
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

      <div className='filterTermsContainer'>
        <div className='divFilter'>
          <p>Diseases</p>

          <ul>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionDisease}
                id='subscribeNews'
                name='subscribe'
                value='Colon adenocarcinoma'
              />
              <label className='label'>Colon adenocarcinoma</label>
              <label className='onHover'>NCIT:C4349</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionDisease}
                id='subscribeNews'
                name='subscribe'
                value='Mucinous Adenocarcinoma of the Colon and Rectum'
              />
              <label className='label'>
                Mucinous Adenocarcinoma of the Colon and Rectum
              </label>
              <label className='onHover'>NCIT:C7966</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionDisease}
                id='subscribeNews'
                name='subscribe'
                value='Rectal Adenocarcinoma'
              />
              <label className='label'>Rectal Adenocarcinoma</label>
              <label className='onHover'>NCIT:C9383</label>
            </div>
            <div>
              <img
                className='dictionary'
                src='/../dictionary.png'
                alt='dictionary'
              ></img>
              <button
                className='othersButton'
                onClick={handleSeeFilteringTerms}
              >
                Others
              </button>
            </div>
          </ul>
        </div>
        <div className='divFilter2'>
          <p>Demographics</p>

          <ul>
            <div>
              <img
                className='formula'
                src='/../formula.png'
                alt='formula'
              ></img>
              <button className='ageButton' onClick={handleOptionAge}>
                Age at diagnosis
              </button>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionSex}
                id='subscribeNews'
                name='subscribe'
                value='Female'
              />
              <label className='label'>Female</label>
              <label className='onHover'>NCIT:C16576</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionSex}
                id='subscribeNews'
                name='subscribe'
                value='Male'
              />
              <label className='label'>Male</label>
              <label className='onHover'>NCIT:C20197</label>
            </div>
            <div>
              <img
                className='dictionary'
                src='/../dictionary.png'
                alt='dictionary'
              ></img>
              <button
                className='othersButton'
                onClick={handleSeeFilteringTerms}
              >
                Others
              </button>
            </div>
          </ul>
        </div>
        <div className='divFilter4'>
          <p>Treatment</p>

          <ul>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Radiation Therapy'
              />
              <label className='label'>Radiation Therapy</label>
              <label className='onHover'>NCIT:C15313</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Chemotherapy'
              />
              <label className='label'>Chemotherapy</label>
              <label className='onHover'>NCIT:C15632</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Fluorouracil'
              />
              <label className='label'>Fluorouracil</label>
              <label className='onHover'>NCIT:C505</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Oxaliplatin'
              />
              <label className='label'>Oxaliplatin</label>
              <label className='onHover'>NCIT:C1181</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Zoledronic Acid'
              />
              <label className='label'>Zoledronic Acid</label>
              <label className='onHover'>NCIT:C1699</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Irinotecan'
              />
              <label className='label'>Irinotecan</label>
              <label className='onHover'>NCIT:C62040</label>
            </div>
            <div>
              <img
                className='dictionary'
                src='/../dictionary.png'
                alt='dictionary'
              ></img>
              <button
                className='othersButton'
                onClick={handleSeeFilteringTerms}
              >
                Others
              </button>
            </div>
          </ul>
        </div>
        <div className='divFilter3'>
          <p>Histopathology</p>
          <div className='divHisto'>
            <ul>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Ascending colon'
                />
                <label className='label'>Ascending colon</label>
                <label className='onHover'>ICD10:C18.2</label>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Descending colon'
                />
                <label className='label'>Descending colon</label>
                <label className='onHover'>ICD10:C18.6</label>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Transverse colon'
                />
                <label className='label'>Transverse colon</label>
                <label className='onHover'>ICD10:C18.4</label>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Hepatic flexure'
                />
                <label className='label'>Hepatic flexure</label>
                <label className='onHover'>ICD10:C18.3</label>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Splenic flexure'
                />
                <label className='label'>Splenic flexure</label>
                <label className='onHover'>ICD10:C18.5</label>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Sigmoid colon'
                />
                <label className='label'>Sigmoid colon</label>
                <label className='onHover'>ICD10:C18.7</label>
              </div>
            </ul>
            <ul>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Caecum'
                />
                <label className='label'>Caecum</label>
                <label className='onHover'>ICD10:C18.0</label>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Stage I'
                />
                <label className='label'>Tumor stage I</label>
                <label className='onHover'>NCIT:C27966</label>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Stage II'
                />
                <label className='label'>Tumor stage II</label>
                <label className='onHover'>NCIT:C28054</label>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Stage III'
                />
                <label className='label'>Tumor stage III</label>
                <label className='onHover'>NCIT:C27970</label>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Stage IV'
                />
                <label className='label'>Tumor stage IV</label>
                <label className='onHover'>NCIT:C27971</label>
              </div>
              <div>
                <img
                  className='dictionary'
                  src='/../dictionary.png'
                  alt='dictionary'
                ></img>
                <button
                  className='othersButton'
                  onClick={handleSeeFilteringTerms}
                >
                  Others
                </button>
              </div>
            </ul>
          </div>
        </div>

        <div className='divFilter5'>
          <p>Variant</p>

          <ul>
            <div className='containerMutation'>
              <input
                type='checkbox'
                onClick={handleOptionVariant}
                id='subscribeNews'
                name='subscribe'
                value='Radiation Therapy'
              />
              <label className='tittleVariant'>With mutation:</label>

              <div>
                <div className='mutationDiv'>
                  <label>alternateBases: T</label>
                  <label>referenceBases: C</label>
                  <label>start: 110173330</label>
                  <label>end: 110173331</label>
                  <label>type: SNP</label>
                </div>
              </div>
            </div>
            <div className='containerMutation'>
              <input
                type='checkbox'
                onClick={handleOptionVariant2}
                id='subscribeNews'
                name='subscribe'
                value='Fluorouracil'
              />
              <label className='tittleVariant'>With mutations:</label>
              <div className='mutationDiv'>
                <label>alternateBases: A</label>
                <label>referenceBases: T</label>
                <label>start: 1334544</label>
                <label>end: 1334545</label>
                <label>type: SNP</label>
              </div>
              <div className='mutationDiv'>
                <label>alternateBases: T</label>
                <label>referenceBases: C</label>
                <label>start: 3670751</label>
                <label>end: 3670752</label>
                <label>type: SNP</label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionVariant3}
                id='subscribeNews'
                name='subscribe'
                value='Oxaliplatin'
              />
              <label className='tittleVariant'>In gene:</label>
              <label>CTNNB1</label>
              <label className='label'>
                with Chemotherapy, tumor Stage IIA, Colon adenocarcinoma
              </label>
              <label className='onHover'>
                NCIT:C15632, NCIT:C27967, NCIT:C4349
              </label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionVariant4}
                id='subscribeNews'
                name='subscribe'
                value='Oxaliplatin'
              />
              <label className='tittleVariant'>In gene:</label>
              <label>CSDE1</label>
              <label className='label'>
                with Fluorouracil, tumor Stage IVA, Rectal adenocarcinoma
              </label>
              <label className='onHover'>
                NCIT:C505, NCIT:C27979, NCIT:C9383
              </label>
            </div>

            <div>
              <img
                className='dictionary'
                src='/../dictionary.png'
                alt='dictionary'
              ></img>
              <button
                className='othersButton'
                onClick={handleSeeFilteringTerms}
              >
                Others
              </button>
            </div>
          </ul>
        </div>
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
