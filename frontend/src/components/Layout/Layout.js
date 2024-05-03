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

  const [showFilters, setShowFilters] = useState(true)
  const [expansionSection, setExpansionSection] = useState(false)
  const [arrayFilteringTermsQE, setArrayFilteringTermsQE] = useState([])

  const [resultSet, setResultset] = useState('HIT')
  const [resultSetAux, setResultsetAux] = useState('HIT')

  const [descendantTerm, setDescendantTerm] = useState('true')

  const [similarity, setSimilarity] = useState('Select')

  const [cohorts, setShowCohorts] = useState(false)

  const [ID, setId] = useState('diseases.ageOfOnset.iso8601duration')
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
  const [showOptions, setShowOptions] = useState(false)

  const [referenceName, setRefName] = useState('')
  const [referenceName2, setRefName2] = useState('')
  const [start, setStart] = useState('110173330')
  const [start2, setStart2] = useState('1334544')
  const [start3, setStart3] = useState('3670751')
  const [end, setEnd] = useState('110173331')
  const [end2, setEnd2] = useState('1334545')
  const [end3, setEnd3] = useState('3670752')
  const [variantType, setVariantType] = useState('SNP')
  const [variantType2, setVariantType2] = useState('SNP')
  const [variantType3, setVariantType3] = useState('SNP')
  const [alternateBases, setAlternateBases] = useState('T')
  const [alternateBases2, setAlternateBases2] = useState('A')
  const [alternateBases3, setAlternateBases3] = useState('T')
  const [referenceBases, setRefBases] = useState('C')
  const [referenceBases2, setRefBases2] = useState('T')
  const [referenceBases3, setRefBases3] = useState('C')
  const [aminoacid, setAminoacid] = useState('p.Gly12Cys')
  const [aminoacid2, setAminoacid2] = useState('')
  const [geneID, setGeneId] = useState('KRAS')
  const [geneID2, setGeneId2] = useState('KRAS')
  const [geneID3, setGeneId3] = useState('TP53')
  const [geneID4, setGeneId4] = useState('CTNNB1')
  const [geneID5, setGeneId5] = useState('CSDE1')
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

  const [geneSubmitted3, setGeneSub3] = useState(false)

  const [geneSubmitted4, setGeneSub4] = useState(false)
  const [geneSubmitted5, setGeneSub5] = useState(false)

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

  const removeModule = e => {
    setGeneSub(false)
  }
  const removeModule2 = e => {
    setGeneSub2(false)
  }
  const removeModule3 = e => {
    setRangeSub2(false)
    handleOptionVariant3()
  }

  const handleChangeStart = e => {
    setStart(e.target.value)
  }
  const handleChangeStart2 = e => {
    setStart2(e.target.value)
  }
  const handleChangeStart3 = e => {
    setStart3(e.target.value)
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

  const handleChangeReferenceB3 = e => {
    setRefBases3(e.target.value)
  }

  const handleChangeRefN = e => {
    setRefName(e.target.value)
  }

  const handleChangeEnd = e => {
    setEnd(e.target.value)
  }
  const handleChangeEnd2 = e => {
    setEnd2(e.target.value)
  }
  const handleChangeEnd3 = e => {
    setEnd3(e.target.value)
  }

  const handleChangeVariantType = e => {
    setVariantType(e.target.value)
  }
  const handleChangeVariantType2 = e => {
    setVariantType2(e.target.value)
  }
  const handleChangeVariantType3 = e => {
    setVariantType3(e.target.value)
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
  const handleChangeGeneId2 = e => {
    setGeneId2(e.target.value)
  }
  const handleChangeGeneId3 = e => {
    setGeneId3(e.target.value)
  }
  const handleChangeGeneId4 = e => {
    setGeneId4(e.target.value)
  }
  const handleChangeGeneId5 = e => {
    setGeneId5(e.target.value)
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

  const handleOptionVariant5 = e => {
    if (e.target.checked) {
      if (query !== null && query !== '') {
        setQuery(query + ',' + `geneId:${geneID2}`)
      } else {
        setQuery(`geneId:${geneID2}`)
      }

      setGeneSub3(true)
    } else {
      setGeneSub3(false)
      setGeneModuleArray([])
    }
  }
  const handleOptionVariant7 = e => {
    if (e.target.checked) {
      if (query !== null && query !== '') {
        setQuery(query + ',' + `molecularAttributes.geneIds=${geneID3}`)
      } else {
        setQuery(`molecularAttributes.geneIds=${geneID3}`)
      }
    } else {
      setGeneModuleArray([])
      if (query.includes(`,molecularAttributes.geneIds=${geneID3}`)) {
        setQuery(query.replace(`,molecularAttributes.geneIds=${geneID3}`, ''))
      } else if (query.includes(`molecularAttributes.geneIds=${geneID3},`)) {
        setQuery(query.replace(`molecularAttributes.geneIds=${geneID3},`, ''))
      } else {
        setQuery(query.replace(`molecularAttributes.geneIds=${geneID3}`, ''))
      }
    }
  }
  const handleOptionVariant6 = e => {
    if (e.target.checked) {
      if (query !== null && query !== '') {
        setQuery(query + ',' + `geneId:${geneID}&aminoacidChange:${aminoacid}`)
      } else {
        setQuery(`geneId:${geneID}&aminoacidChange:${aminoacid}`)
      }

      setGeneSub4(true)
    } else {
      setGeneSub4(false)
      setGeneModuleArray([])
    }
  }

  const handleOptionVariant = e => {
    if (e.target.checked) {
      if (query !== null && query !== '') {
        setQuery(
          query +
            ',' +
            `${start}-${end}:${variantType}:${referenceBases}>${alternateBases}`
        )
      } else {
        setQuery(
          `${start}-${end}:${variantType}:${referenceBases}>${alternateBases}`
        )
      }
    } else {
      setRangeSub1(false)
      setRangeModuleArray([])
    }
  }

  const handleOptionVariant2 = e => {
    if (e.target.checked) {
      // let objectRange = {
      //   assemblyId: assemblyId2,
      //   referenceName: referenceName2,
      //   start: '1334544',
      //   end: '1334545',
      //   variantType: 'SNP',
      //   alternateBases: 'A',
      //   referenceBases: 'T',
      //   aminoacid: aminoacid,
      //   variantMinLength: variantMinLength,
      //   variantMaxLength: variantMaxLength,
      //   clinicalRelevance: clinicalRelevance2
      // }
      // let objectRange2 = {
      //   assemblyId: assemblyId2,
      //   referenceName: referenceName2,
      //   start: '3670751',
      //   end: '3670752',
      //   variantType: 'SNP',
      //   alternateBases: 'T',
      //   referenceBases: 'C',
      //   aminoacid: aminoacid,
      //   variantMinLength: variantMinLength,
      //   variantMaxLength: variantMaxLength,
      //   clinicalRelevance: clinicalRelevance2
      // }
      // rangeModuleArray.push(objectRange)
      // rangeModuleArray.push(objectRange2)
      // console.log(rangeModuleArray)
      // setRangeSub2(true)

      if (query !== null && query !== '') {
        setQuery(
          query +
            ',' +
            `${start3}-${end3}:${variantType3}:${referenceBases3}>${alternateBases3}, ${start2}-${end2}:${variantType2}:${referenceBases2}>${alternateBases2}`
        )
      } else {
        setQuery(
          `${start3}-${end3}:${variantType3}:${referenceBases3}>${alternateBases3}, ${start2}-${end2}:${variantType2}:${referenceBases2}>${alternateBases2}`
        )
      }
    } else {
      setRangeSub2(false)
      setRangeModuleArray([])
    }
  }
  const handleOptionVariant3 = e => {
    console.log(geneSubmitted2)
    if (e.target.checked) {
      setGeneSub(true)

      if (query !== null && query !== '') {
        setQuery(
          query +
            ',' +
            `geneId:${geneID4}, treatment=Chemotherapy, disease=STAGE IIIB, disease=Colon adenocarcinoma`
        )
      } else {
        setQuery(
          `geneId:${geneID4}, treatment=Chemotherapy, disease=STAGE IIIB, disease=Colon adenocarcinoma`
        )
      }
    } else {
      setGeneSub(false)
      setGeneModuleArray([])
    }
  }
  const handleOptionVariant4 = e => {
    if (e.target.checked) {
      setGeneSub2(true)
      if (query !== null && query !== '') {
        setQuery(
          query +
            ',' +
            `geneId:${geneID5}, treatment=Chemotherapy, disease=STAGE IIIB, disease=Colon adenocarcinoma`
        )
      } else {
        setQuery(
          `geneId:${geneID5}, treatment=Chemotherapy, disease=STAGE IIIB, disease=Colon adenocarcinoma`
        )
      }
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
    setQuery(e.target.value)
    var ele = document.getElementsByName('subscribe')
    for (var i = 0; i < ele.length; i++) {
      if (query.includes(ele[i].value)) {
        ele[i].checked = true
      } else {
        ele[i].checked = false
      }
    }
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
            <h1 className='version'>v0.5.3</h1>
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
                  value={'age at diagnosis'}
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

      <div
        className={
          showFilters ? 'filterTermsContainer' : 'filterTermsContainer2'
        }
      >
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
              <div className='label-ontology-div'>
                <label className='label'>Colon adenocarcinoma</label>
                <label className='onHover'>NCIT:C4349</label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionDisease}
                id='subscribeNews'
                name='subscribe'
                value='Mucinous Adenocarcinoma of the Colon and Rectum'
              />
              <div className='label-ontology-div'>
                <label className='label'>
                  Mucinous Adenocarcinoma of the Colon and Rectum
                </label>
                <label className='onHover'>NCIT:C7966</label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionDisease}
                id='subscribeNews'
                name='subscribe'
                value='Rectal Adenocarcinoma'
              />
              <div className='label-ontology-div'>
                <label className='label'>Rectal Adenocarcinoma</label>
                <label className='onHover'>NCIT:C9383</label>
              </div>
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
              <div className='label-ontology-div'>
                <label className='label'>Female</label>
                <label className='onHover'>NCIT:C16576</label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionSex}
                id='subscribeNews'
                name='subscribe'
                value='Male'
              />
              <div className='label-ontology-div'>
                <label className='label'>Male</label>
                <label className='onHover'>NCIT:C20197</label>
              </div>
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
              <div className='label-ontology-div'>
                <label className='label'>Radiation Therapy</label>
                <label className='onHover'>NCIT:C15313</label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Chemotherapy'
              />
              <div className='label-ontology-div'>
                <label className='label'>Chemotherapy</label>
                <label className='onHover'>NCIT:C15632</label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Fluorouracil'
              />
              <div className='label-ontology-div'>
                <label className='label'>Fluorouracil</label>
                <label className='onHover'>NCIT:C505</label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Oxaliplatin'
              />
              <div className='label-ontology-div'>
                <label className='label'>Oxaliplatin</label>
                <label className='onHover'>NCIT:C1181</label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Zoledronic Acid'
              />
              <div className='label-ontology-div'>
                <label className='label'>Zoledronic Acid</label>
                <label className='onHover'>NCIT:C1699</label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionTreatment}
                id='subscribeNews'
                name='subscribe'
                value='Irinotecan'
              />
              <div className='label-ontology-div'>
                <label className='label'>Irinotecan</label>
                <label className='onHover'>NCIT:C62040</label>
              </div>
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
                <div className='label-ontology-div'>
                  <label className='label'>Ascending colon</label>
                  <label className='onHover'>ICD10:C18.2</label>
                </div>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Descending colon'
                />
                <div className='label-ontology-div'>
                  <label className='label'>Descending colon</label>
                  <label className='onHover'>ICD10:C18.6</label>
                </div>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Transverse colon'
                />
                <div className='label-ontology-div'>
                  <label className='label'>Transverse colon</label>
                  <label className='onHover'>ICD10:C18.4</label>
                </div>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Hepatic flexure'
                />
                <div className='label-ontology-div'>
                  <label className='label'>Hepatic flexure</label>
                  <label className='onHover'>ICD10:C18.3</label>
                </div>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Splenic flexure'
                />
                <div className='label-ontology-div'>
                  <label className='label'>Splenic flexure</label>
                  <label className='onHover'>ICD10:C18.5</label>
                </div>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Sigmoid colon'
                />
                <div className='label-ontology-div'>
                  <label className='label'>Sigmoid colon</label>
                  <label className='onHover'>ICD10:C18.7</label>
                </div>
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
                <div className='label-ontology-div'>
                  <label className='label'>Caecum</label>
                  <label className='onHover'>ICD10:C18.0</label>
                </div>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Stage I'
                />
                <div className='label-ontology-div'>
                  <label className='label'>Tumor stage I</label>
                  <label className='onHover'>NCIT:C27966</label>
                </div>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Stage II'
                />
                <div className='label-ontology-div'>
                  <label className='label'>Tumor stage II</label>
                  <label className='onHover'>NCIT:C28054</label>
                </div>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Stage III'
                />
                <div className='label-ontology-div'>
                  <label className='label'>Tumor stage III</label>
                  <label className='onHover'>NCIT:C27970</label>
                </div>
              </div>
              <div>
                <input
                  type='checkbox'
                  onClick={handleOptionHisto}
                  id='subscribeNews'
                  name='subscribe'
                  value='Stage IV'
                />
                <div className='label-ontology-div'>
                  <label className='label'>Tumor stage IV</label>
                  <label className='onHover'>NCIT:C27971</label>
                </div>
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
                onClick={handleOptionVariant6}
                id='subscribeNews'
                name='subscribe'
                value='KRAS-G12C'
              />

              <label className='tittleVariant'>Mutations in:</label>
              <label>gene:</label>
              <input
                className='inputVariants'
                type='text'
                value={geneID}
                onChange={handleChangeGeneId}
              ></input>
              <label>aminoacid</label>
              <input
                className='inputVariants'
                type='text'
                value={aminoacid}
                onChange={handleChangeAminoacid}
              ></input>
            </div>
            <div className='containerMutation'>
              <input
                type='checkbox'
                onClick={handleOptionVariant5}
                id='subscribeNews'
                name='subscribe'
                value='KRAS'
              />

              <label className='tittleVariant'>Mutations in:</label>

              <label>gene</label>
              <input
                className='inputVariants'
                type='text'
                value={geneID2}
                onChange={handleChangeGeneId2}
              ></input>
            </div>
            <div className='containerMutation'>
              <input
                type='checkbox'
                onClick={handleOptionVariant7}
                id='subscribeNews'
                name='subscribe'
                value='molecularAttributes.geneIds=TP53'
              />

              <label className='tittleVariant'>Mutations in:</label>
              <label>gene</label>
              <input
                className='inputVariants'
                type='text'
                value={geneID3}
                onChange={handleChangeGeneId3}
              ></input>
            </div>
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
                  <div>
                    {' '}
                    <label>alternateBases:</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={alternateBases}
                      onChange={handleChangeAlternateB}
                    ></input>
                  </div>
                  <div>
                    {' '}
                    <label>referenceBases:</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={referenceBases}
                      onChange={handleChangeReferenceB}
                    ></input>
                  </div>
                  <div>
                    {' '}
                    <label>start:</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={start}
                      onChange={handleChangeStart}
                    ></input>
                  </div>
                  <div>
                    {' '}
                    <label>end:</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={end}
                      onChange={handleChangeEnd}
                    ></input>
                  </div>
                  <div>
                    {' '}
                    <label>type:</label>
                    <input
                      className='inputVariants'
                      type='text'
                      value={variantType}
                      onChange={handleChangeVariantType}
                    ></input>
                  </div>
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
                <div>
                  {' '}
                  <label>alternateBases:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={alternateBases3}
                    onChange={handleChangeAlternateB3}
                  ></input>
                </div>
                <div>
                  {' '}
                  <label>referenceBases:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={referenceBases3}
                    onChange={handleChangeReferenceB3}
                  ></input>
                </div>
                <div>
                  {' '}
                  <label>start:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={start3}
                    onChange={handleChangeStart3}
                  ></input>
                </div>
                <div>
                  {' '}
                  <label>end:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={end3}
                    onChange={handleChangeEnd3}
                  ></input>
                </div>
                <div>
                  {' '}
                  <label>type:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={variantType3}
                    onChange={handleChangeVariantType3}
                  ></input>
                </div>
              </div>
              <div className='mutationDiv'>
                <div>
                  {' '}
                  <label>alternateBases:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={alternateBases2}
                    onChange={handleChangeAlternateB2}
                  ></input>
                </div>
                <div>
                  {' '}
                  <label>referenceBases:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={referenceBases2}
                    onChange={handleChangeReferenceB2}
                  ></input>
                </div>
                <div>
                  {' '}
                  <label>start:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={start2}
                    onChange={handleChangeStart2}
                  ></input>
                </div>
                <div>
                  {' '}
                  <label>end:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={end2}
                    onChange={handleChangeEnd2}
                  ></input>
                </div>
                <div>
                  {' '}
                  <label>type:</label>
                  <input
                    className='inputVariants'
                    type='text'
                    value={variantType2}
                    onChange={handleChangeVariantType2}
                  ></input>
                </div>
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
              <label>In gene</label>
              <input
                className='inputVariants'
                type='text'
                value={geneID4}
                onChange={handleChangeGeneId4}
              ></input>
              <div className='termsOntologies'>
                <label className='label'>
                  with Chemotherapy, tumor Stage IIIB, Colon adenocarcinoma
                </label>
                <label className='onHover'>
                  NCIT:C15632, NCIT:C27978, NCIT:C4349
                </label>
              </div>
            </div>
            <div>
              <input
                type='checkbox'
                onClick={handleOptionVariant4}
                id='subscribeNews'
                name='subscribe'
                value='Oxaliplatin'
              />

              <label>In gene</label>
              <input
                className='inputVariants'
                type='text'
                value={geneID5}
                onChange={handleChangeGeneId5}
              ></input>
              <div className='termsOntologies'>
                <label className='label'>
                  with Fluorouracil, tumor Stage IVA, Rectal adenocarcinoma
                </label>
                <label className='onHover'>
                  NCIT:C505, NCIT:C27979, NCIT:C9383
                </label>
              </div>
            </div>
          </ul>
        </div>

        <div className='divOthers'>
          <img
            className='dictionary'
            src='/../dictionary.png'
            alt='dictionary'
          ></img>
          <button className='othersButton' onClick={handleSeeFilteringTerms}>
            Others
          </button>
        </div>
      </div>

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
