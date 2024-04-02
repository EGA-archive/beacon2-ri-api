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
  const [geneSubmitted, setGeneSub] = useState(false)

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

  const handleSequenceExample = e => {
    setAlternateBases('A')
    setRefBases('G')
    setStart('16050114')
  }

  const handleRangeExample = e => {
    if (props.collection === 'Variant') {
      setAlternateBases2('T')
      setRefBases2('C')
      setStart2('110173330')
      setEnd('110173331')
      setVariantType('SNP')
    }
    console.log(props.collection)
    if (props.collection === 'Individuals') {
      setAlternateBases2('A')
      setRefBases2('T')
      setStart2('1334544')
      setEnd('1334545')
      setVariantType('SNP')
    }
  }

  const handleRangeExample2 = e => {
    if (props.collection === 'Individuals') {
      setAlternateBases2('T')
      setRefBases2('C')
      setStart2('3670751')
      setEnd('3670752')
      setVariantType('SNP')
    }
  }

  const handleGeneExample = e => {
    setGeneId('CTNNB1')
    setQuery('NCIT:C15632,NCIT:C27967,NCIT:C4349')
  }

  const handleGeneExample2 = e => {
    setGeneId('CSDE1')
    setQuery('NCIT:C505,NCIT:C27979,NCIT:C9383')
  }

  const removeModuleQueryGene = e => {
    geneModuleArray.splice(e, 1)
    setGeneSub(!geneSubmitted)
  }

  const removeModuleQuerySeq = e => {
    seqModuleArray.splice(e, 1)
    setSequenceSub(!sequenceSubmitted)
  }

  const removeModuleQueryRange = e => {
    rangeModuleArray.splice(e, 1)
    setRangeSub(!rangeSubmitted)
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
  }

  const handleOptionDisease = e => {
    if (e.target.checked === true){
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
      setQuery(query.replace(`disease=${e.target.value}`, ''))

    }
  
  }

  const handleOptionSex = e => {
    filteringTerms.forEach(element => {
      if (element.label) {
        console.log(element.label.toLowerCase())
        console.log(e.target.innerText.toLowerCase())
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
  }
  const handleOptionAge = e => {
    setShowAlphanum(true)
  }

  const handleOptionHisto = e => {
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
            setQuery(query + ',' + 'histophatology=' + e.target.value)
          } else {
            setQuery('histophatology=' + e.target.value)
          }
        }
      }
    })
  }

  const handleOptionTreatment = e => {
    filteringTerms.forEach(element => {
      if (element.label) {
        console.log(element.label.toLowerCase())
        console.log(e.target.innerText.toLowerCase())
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
    console.log(e.target.innerText)
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
          </select>
          <h14>having ... </h14>
          <form onSubmit={onSubmit} className='formInput'>
            <textarea
              className='inputSearch'
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
              <label>Colon adenocarcinoma</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionDisease}
                id='subscribeNews'
                name='subscribe'
                value='Mucinous Adenocarcinoma of the Colon and Rectum'
              />
              <label>Mucinous Adenocarcinoma of the Colon and Rectum</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionDisease}
                id='subscribeNews'
                name='subscribe'
                value='Rectal Adenocarcinoma'
              />
              <label>Rectal Adenocarcinoma</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionDisease}
                id='subscribeNews'
                name='subscribe'
                value='Rectal Adenocarcinoma'
              />
              <label>Rectal Adenocarcinoma</label>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionDisease}
                id='subscribeNews'
                name='subscribe'
                value='Primary adenocarcinoma of colon'
              />
              <label>Primary adenocarcinoma of colon</label>
            </div>

            <button className='othersButton' onClick={handleSeeFilteringTerms}>
              Others
            </button>
          </ul>
        </div>
        <div className='divFilter'>
          <p>Demographics</p>

          <ul>
            <li onClick={handleOptionAge}>Age at diagnosis</li>
            <li onClick={handleOptionSex}>Female</li>
            <li onClick={handleOptionSex}>Male</li>

            <li>
              <button
                className='othersButton'
                onClick={handleSeeFilteringTerms}
              >
                Others
              </button>
            </li>
          </ul>
        </div>
        <div className='divFilter'>
          <p>Histopathology</p>

          <ul>
            <li onClick={handleOptionHisto}>Ascending colon</li>
            <li onClick={handleOptionHisto}>Descending colon</li>
            <li onClick={handleOptionHisto}>Transverse colon</li>
            <li onClick={handleOptionHisto}>Hepatic flexure</li>
            <li onClick={handleOptionHisto}>Splenic flexure</li>
            <li onClick={handleOptionHisto}>Sigmoid colon</li>
            <li onClick={handleOptionHisto}>Caecum</li>
            <li onClick={handleOptionHisto}>Tumor stage I</li>
            <li onClick={handleOptionHisto}>Tumor stage II</li>
            <li onClick={handleOptionHisto}>Tumor stage III</li>
            <li onClick={handleOptionHisto}>Tumor stage IV</li>

            <li>
              <button
                className='othersButton'
                onClick={handleSeeFilteringTerms}
              >
                Others
              </button>
            </li>
          </ul>
        </div>

        <div className='divFilter'>
          <p>Treatment</p>

          <ul>
            <li onClick={handleOptionTreatment}>Radiotherapy</li>
            <li onClick={handleOptionTreatment}>Surgery</li>
            <li onClick={handleOptionTreatment}>Systemic therapy</li>

            <li>
              <button
                className='othersButton'
                onClick={handleSeeFilteringTerms}
              >
                Others
              </button>
            </li>
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
              geneSubmitted={geneSubmitted}
              sequenceSubmitted={sequenceSubmitted}
              rangeSubmitted={rangeSubmitted}
              query={query}
              resultSets={resultSetAux}
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
              variantMaxLength={variantMaxLength}
              variantMaxLength2={variantMaxLength2}
              variantMinLength={variantMinLength}
              variantMinLength2={variantMinLength2}
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
              geneSubmitted={geneSubmitted}
              sequenceSubmitted={sequenceSubmitted}
              rangeSubmitted={rangeSubmitted}
              query={query}
              resultSets={resultSetAux}
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
              variantMaxLength={variantMaxLength}
              variantMaxLength2={variantMaxLength2}
              variantMinLength={variantMinLength}
              variantMinLength2={variantMinLength2}
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
              geneSubmitted={geneSubmitted}
              sequenceSubmitted={sequenceSubmitted}
              rangeSubmitted={rangeSubmitted}
              query={query}
              resultSets={resultSetAux}
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
              variantMaxLength={variantMaxLength}
              variantMaxLength2={variantMaxLength2}
              variantMinLength={variantMinLength}
              variantMinLength2={variantMinLength2}
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
              descendantTerm={descendantTerm}
              similarity={similarity}
              isSubmitted={isSubmitted}
            />
          </div>
        )}
        {isSubmitted && results === 'Biosamples' && !triggerQuery && (
          <div>
            <BiosamplesResults
              filteringTerms={filteringTerms}
              query={query}
              resultSets={resultSetAux}
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

        {timeOut === true && error && showFilteringTerms && <h5>{error}</h5>}
      </div>
    </div>
  )
}

export default Layout
