import '../../App.css';

import FilteringTermsIndividuals from '../FilteringTerms/FilteringTerms';
import Cohorts from '../Cohorts/Cohorts';

import ResultsDatasets from '../Datasets/ResultsDatasets';
import VariantsResults from '../GenomicVariations/VariantsResults';

import Select from 'react-select'
import React, { useState, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useContext } from 'react';

import Switch from '@mui/material/Switch';
import MultiSwitch from 'react-multi-switch-toggle';

import axios from "axios";

import ReactModal from 'react-modal';
import makeAnimated from 'react-select/animated';

import IndividualsResults from '../Individuals/IndividualsResults';
import { LinearProgress } from '@mui/material';

function Layout(props) {
    console.log(props)
    const [error, setError] = useState(null)

    const [placeholder, setPlaceholder] = useState('')

    const [results, setResults] = useState(null)
    const [query, setQuery] = useState(null)
    const [exampleQ, setExampleQ] = useState([])

    const [resultSet, setResultset] = useState("HIT")

    const [descendantTerm, setDescendantTerm] = useState('true')

    const [similarity, setSimilarity] = useState("Select")

    const [cohorts, setShowCohorts] = useState(false)

    const [ID, setId] = useState("")
    const [operator, setOperator] = useState("")
    const [valueFree, setValueFree] = useState("")

    const [value, setValue] = useState("")

    const [popUp, setPopUp] = useState(false)

    const [showButton, setShowButton] = useState(true)

    const [showFilteringTerms, setShowFilteringTerms] = useState(false)
    const [filteringTerms, setFilteringTerms] = useState(false)

    const [showVariants, setShowVariants] = useState(false)

    const [trigger, setTrigger] = useState(false)
    const { storeToken, refreshToken, getStoredToken, authenticateUser, setExpirationTime, setExpirationTimeRefresh } = useContext(AuthContext);

    const [showBar, setShowBar] = useState(true)

    const [isOpenModal1, setIsOpenModal1] = useState(false);
    const [isOpenModal2, setIsOpenModal2] = useState(false);
    const [isOpenModal4, setIsOpenModal4] = useState(false);
    const [isOpenModal5, setIsOpenModal5] = useState(false);
    const [isOpenModal6, setIsOpenModal6] = useState(false);

    const [showExtraIndividuals, setExtraIndividuals] = useState(false)
    const [showOptions, setShowOptions] = useState(false)

    const [expansionSection, setExpansionSection] = useState(false)

    const [options, setOptions] = useState(

        props.options)


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

    const animatedComponents = makeAnimated();

    const [resetSearch, setResetSearch] = useState(false)

    const [state, setstate] = useState({
        query: '',
        list: []
    })

    const [checked, setChecked] = useState(true)
    const [checked2, setChecked2] = useState(false)
    const [checked3, setChecked3] = useState(false)

    const [isSubmitted, setIsSub] = useState(false)

    const [qeValue, setQEvalue] = useState('')
    const [ontologyValue, setOntologyValue] = useState('')

    const [selectedCohortsAux, setSelectedCohortsAux] = useState([])

    const [resultsQEexact, setResultsQEexact] = useState([])
    const [matchesQE, setMatchesQE] = useState([])
    const [showQEresults, setShowQEresults] = useState(false)
    const [showQEfirstResults, setShowQEfirstResults] = useState(false)

    const [arrayFilteringTerms, setArrayFilteringTerms] = useState([])
    const [arrayFilteringTermsQE, setArrayFilteringTermsQE] = useState([])

    const [showIds, setShowIds] = useState(false)

    const handleChangeSwitch = (e) => {

        setDescendantTerm(e.target.checked)
        setChecked(e.target.checked);

    }

    const onToggle = (selectedItem) => {
        console.log(selectedItem)
        if (selectedItem === 0) {
            setSimilarity('low')
        } else if (selectedItem === 1) {
            setSimilarity('medium')
        } else {
            setSimilarity('high')
        }

    }


    const onToggle2 = (selectedItem) => {
        console.log(selectedItem)
        if (selectedItem === 0) {
            setResultset("HIT")
        } else if (selectedItem === 1) {
            setResultset("MISS")
        } else if (selectedItem === 2) {
            setResultset("NONE")
        } else {
            setResultset("ALL")
        }

    }

    const triggerOptions = () => {
        setOptions(options)
    }


    const handleChangeCohorts = (selectedOption) => {
        setSelectedCohortsAux([])
        selectedCohortsAux.push(selectedOption)
        props.setSelectedCohorts(selectedCohortsAux)
    }

    const handleQEchanges = (e) => {

        setQEvalue(e.target.value.trim())
    }

    const handleNewQEsearch = () => {
        setShowQEresults(false)
    }

    const handleOntologyChanges = (e) => {
        setOntologyValue(e.target.value.trim())
    }

    const handleIdChanges = (e) => {
        setShowIds(true)
        setId(e.target.value)
        const results = arrayFilteringTerms.filter(post => {

            if (e.target.value === "") {
                return arrayFilteringTerms
            } else {
                if (post !== undefined) {
                    if (post.toLowerCase().includes(e.target.value.toLowerCase())) {
                        return post
                    }
                } else {
                    if (post.toLowerCase().includes(e.target.value.toLowerCase())) {
                        return post
                    }
                }
            }

        })
        setstate({
            query: e.target.value,
            list: results
        })

        if (e.target.value === '') {
            setShowIds(false)
        }


    }

    const handleSelectedId = (e) => {
        setShowIds(false)
        setId(e.target.value)
        setstate({
            query: e.target.value,
            list: state.list
        })
    }

    const handleOperatorchange = (e) => {
        setOperator(e.target.value)
        console.log()
    }


    const handleValueChanges = (e) => {
        setValueFree(e.target.value)
    }

    const handdleInclude = (e) => {
        console.log(ID)
        console.log(valueFree)
        console.log(operator)
        if (ID !== '' && valueFree !== '' && operator !== '') {
            if (query !== null) {
                setQuery(query + ',' + `${ID}${operator}${valueFree}`)
            } if (query === null) {
                setQuery(`${ID}${operator}${valueFree}`)
            }
        }

    }

    const handleHelpModal1 = () => {
        setIsOpenModal1(true)
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

    const handleFilteringTerms = async (e) => {


        if (props.collection === 'Individuals') {

            try {

                let res = await axios.get("https://beacons.bsc.es/beacon-network/v2.0.0/individuals/filtering_terms")
                console.log(res)
                if (res.data.response.filteringTerms !== undefined) {
                    setFilteringTerms(res)
                    setResults(null)
                } else {
                    setError("No filtering terms now available")
                }


            } catch (error) {
                console.log(error)
            }
        } else if (props.collection === 'Cohorts') {

            try {

                let res = await axios.get("https://beacons.bsc.es/beacon-network/v2.0.0/cohorts/filtering_terms")
                setFilteringTerms(res)
                setResults(null)

            } catch (error) {
                console.log(error)
            }
        } else if (props.collection === 'Variant') {
            try {

                let res = await axios.get("https://beacons.bsc.es/beacon-network/v2.0.0/g_variants/filtering_terms")
                setFilteringTerms(res)
                setResults(null)

            } catch (error) {
                console.log(error)
            }
        } else if (props.collection === 'Analyses') {
            try {

                let res = await axios.get("https://beacons.bsc.es/beacon-network/v2.0.0/analyses/filtering_terms")
                setFilteringTerms(res)
                setResults(null)

            } catch (error) {
                console.log(error)
            }
        } else if (props.collection === 'Runs') {
            try {

                let res = await axios.get("https://beacons.bsc.es/beacon-network/v2.0.0/runs/filtering_terms")
                setFilteringTerms(res)
                setResults(null)

            } catch (error) {
                console.log(error)
            }
        } else if (props.collection === 'Biosamples') {
            try {

                let res = await axios.get("https://beacons.bsc.es/beacon-network/v2.0.0/biosamples/filtering_terms")
                setFilteringTerms(res)
                setResults(null)

            } catch (error) {
                console.log(error)
            }
        }


        setShowFilteringTerms(true)


    }

    const handleExQueries = () => {
        if (props.collection === 'Individuals') {
            setExampleQ(['Weight>100', 'NCIT:C16352', 'geographicOrigin=%land%', 'geographicOrigin!England', 'NCIT:C42331'])
        } else if (props.collection === 'Variant') {
            setExampleQ(['22 : 16050310 - 16050740', '22 : 16050074 A > G'])
        }
    }

    const handleExtraSectionIndividuals = (e) => {
        setShowOptions(!showOptions)
        setShowButton(!showButton)
    }

    const handleChangeStart = (e) => {
        setStart(e.target.value)
    }
    const handleChangeStart2 = (e) => {
        setStart2(e.target.value)
    }
    const handleChangeRefN2 = (e) => {
        setRefName2(e.target.value)
    }
    const handleChangeAlternateB2 = (e) => {
        setAlternateBases2(e.target.value)
    }
    const handleChangeAssembly2 = (e) => {
        setAssemblyId2(e.target.value)
    }
    const handleChangeAssembly3 = (e) => {
        setAssemblyId3(e.target.value)
    }

    const handleChangeAlternateB = (e) => {
        setAlternateBases(e.target.value)
    }

    const handleChangeAlternateB3 = (e) => {
        setAlternateBases3(e.target.value)
    }

    const handleChangeReferenceB = (e) => {
        setRefBases(e.target.value)
    }
    const handleChangeReferenceB2 = (e) => {
        setRefBases2(e.target.value)
    }

    const handleChangeRefN = (e) => {
        setRefName(e.target.value)
    }

    const handleChangeEnd = (e) => {
        setEnd(e.target.value)
    }

    const handleChangeVariantType = (e) => {
        setVariantType(e.target.value)
    }
    const handleChangeVariantType2 = (e) => {
        setVariantType2(e.target.value)
    }

    const handleChangeAminoacid = (e) => {
        setAminoacid(e.target.value)
    }
    const handleChangeAminoacid2 = (e) => {
        setAminoacid2(e.target.value)
    }

    const handleChangeGeneId = (e) => {
        setGeneId(e.target.value)
    }

    const handleChangeAssembly = (e) => {
        setAssemblyId(e.target.value)
    }

    const handleClick = () => {
        setShowBar(!showBar)
    }

    const handleHideVariantsForm = (e) => {
        setHideForm(false)
    }

    const handleQEclick = (e) => {
        setExpansionSection(true)
    }

    const handleSubmitQE = async (e) => {
        try {
            if (ontologyValue !== '' && qeValue !== '') {

                resultsQEexact.splice(0, resultsQEexact.length)
                setError(null)
                const res = await axios.get(`http://goldorak.hesge.ch:8890/catalogue_explorer/HorizontalExpansionOls/?keywords=${qeValue}&ontology=${ontologyValue.toLowerCase()}`)
                console.log(res)
                let arrayResults = []
                if (res.data.response.ols[qeValue] !== undefined) {
                    arrayResults = res.data.response.ols[qeValue].search_term_expansion
                    if (arrayResults.length < 1) {
                        setError("Not found. Please check the keyword and ontologies and retry")
                    }

                } else {
                    arrayResults = res.data.response.ols[qeValue.toLowerCase()].search_term_expansion
                }

                console.log(arrayResults)
                arrayResults.forEach(element => {
                    if (element.label.trim().toLowerCase() === qeValue.toLowerCase()) {
                        //exact match
                        console.log(qeValue.toLowerCase)
                        console.log(element.label.trim().toLowerCase)
                        resultsQEexact.push(element)
                    }
                })


                if (resultsQEexact.length > 0) {
                    setShowQEfirstResults(true)
                    matchesQE.splice(0, matchesQE.length)
                    console.log(resultsQEexact)
                    resultsQEexact.forEach(element => {
                        console.log(element)
                        arrayFilteringTermsQE.forEach(element2 => {

                                if (element.obo_id.toLowerCase().trim() === element2.id.toLowerCase().trim()) {
                                    setError(null)
                                    matchesQE.push(element2.id)
                                    console.log(matchesQE)
                                    console.log("FOUND A MATCH")
                                    setShowQEresults(true)
                                }
                            
                        
                        })





                    })
                }

            } else {
                setError("Please write the keyword and at least one ontology")
            }

        } catch (error) {
            setError("NOT FOUND")
            console.log(error)
        }
    }

    const handleCheckQE = (e) => {
        if (e.target.checked === true) {
            if (query !== null && query !== '') {
                console.log(query)
                setQuery(query + ',' + e.target.value)
            } else {
                setQuery(e.target.value)
            }
        } else if (e.target.checked === false) {
            console.log(query)
            let varQuery = ''
            if (query.includes(',' + e.target.value)) {
                varQuery = query.replace(',' + e.target.value, '')
            } else if (query.includes(e.target.value + ',')) {
                varQuery = query.replace(e.target.value + ',', '')
            } else {
                varQuery = query.replace(e.target.value, '')
            }
            setQuery(varQuery)
        }



    }

    const handleForward = () => {
        setShowQEfirstResults(false)
        setShowQEresults(false)
    }
    
    const handleNext = () => {
        setShowQEfirstResults(false)
        setShowQEresults(true)
    }

    useEffect(() => {

        if (props.collection === 'Individuals') {
            setPlaceholder('filtering term comma-separated, ID><=value')
            setExtraIndividuals(true)

        } else if (props.collection === 'Biosamples') {
            setPlaceholder('key=value, key><=value, or filtering term comma-separated')
        } else if (props.collection === 'Cohorts') {
            setShowCohorts(true)
            setExtraIndividuals(false)
            setPlaceholder('Search for any cohort')
        } else if (props.collection === "Variant") {
            setPlaceholder('chr : pos ref > alt, chr: start-end')
            setExtraIndividuals(false)
            setShowVariants(true)

        } else if (props.collection === "Analyses") {
            setPlaceholder('chr : pos ref > alt')
            setExtraIndividuals(false)
        } else if (props.collection === "Runs") {
            setPlaceholder('chr : pos ref > alt')
            setExtraIndividuals(false)
        } else if (props.collection === 'Datasets') {
            setPlaceholder('Search for any cohort')
            setExtraIndividuals(false)
        } else {
            setPlaceholder('')
        }

        const fetchData = async () => {

            try {
                let res = await axios.get("https://ega-archive.org/test-beacon-apis/cineca/individuals/filtering_terms?skip=0&limit=0")
                if (res !== null) {
                    res.data.response.filteringTerms.forEach(element => {
                        if (element.type !== "custom") {
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
            .catch(console.error);


    }, [])




    const onSubmit = async (event) => {

        event.preventDefault()

        setIsSub(!isSubmitted)

        console.log(query)

        authenticateUser()

        setExampleQ([])


        setResetSearch(true)


        if (query === '1' || query === '') {
            setQuery(null)
        }
        if (props.collection === 'Individuals') {

            setResults('Individuals')
        } else if (props.collection === 'Variant') {
            setResults('Variant')
        }


    }

    const onSubmit2 = (event) => {

        setPlaceholder("filtering term comma-separated, ID><=value");


        setIsSub(!isSubmitted)

        setExampleQ([])


        if (query === '1' || query === '') {
            setQuery(null)
        }
        if (props.collection === 'Individuals') {
            setResults('Individuals')
        } else if (props.collection === 'Variant') {
            setResults('Variant')
        }


    }

    const onSubmitCohorts = () => {
        setResults('Cohorts')

        props.setShowGraphs(true)
    }

    function search(e) {
        setQuery(e.target.value)

    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setPlaceholder("filtering term comma-separated, ID><=value");
        setIsSub(!isSubmitted)
        setExampleQ([])
        setResults('Variant')
    }

    return (
        <div className="container1">
            <div className="container2">
                <button className="helpButton" onClick={handleHelpModal2}><img className="questionLogo2" src="./question.png" alt='questionIcon'></img><h5>Help for querying</h5></button>
                <div className='logos'>
                    <a href="https://www.cineca-project.eu/" target="_blank">
                        <img className="cinecaLogo" src="./CINECA_logo.png" alt='cinecaLogo'></img>
                    </a>
                    {/* <a href="https://elixir-europe.org/" target="_blank">
                        <img className="elixirLogo" src="./white-orange-logo.png" alt='elixirLogo'></img>
                    </a>*/}
                </div>
            </div>

            <div className='Modal1'>
                {popUp && <ReactModal
                    isOpen={popUp}
                    onRequestClose={handleCloseModal3}
                    shouldCloseOnOverlayClick={true}
                >
                    <button onClick={handleCloseModal3}><img className="closeLogo" src="./cancel.png" alt='cancelIcon'></img></button>

                    <p>Please, bear in mind that you might have to log in to get information from some datasets.</p>

                </ReactModal>
                }
            </div>
            <nav className="navbar">
                <div>
                    {expansionSection === false && cohorts === false &&
                        <button onClick={handleQEclick}><h2 className='queryExpansion'>Query expansion</h2></button>}
                </div>
                {expansionSection === true && <div>
                    <button onClick={() => setExpansionSection(false)}>
                        <img className="hideQE" src="../hide.png" alt='hideIcon'></img></button>
                    <div>
                        {showQEresults === false && showQEfirstResults === false &&<div className='qeSection'>
                            <h2 className='qeSubmitH2'>Horizontal query expansion</h2>
                            <input className="QEinput" type="text" value={qeValue} autoComplete='on' placeholder={"Type ONE keyword (what you want to search): e.g., melanoma"} onChange={(e) => handleQEchanges(e)} aria-label="ID" />
                            <input className="QEinput2" type="text" value={ontologyValue} autoComplete='on' placeholder={"Type the ontologies to include in the search comma-separated: e.g., mondo,ncit"} onChange={(e) => handleOntologyChanges(e)} aria-label="ID" />
                            <button onClick={handleSubmitQE}><h2 className='qeSubmit'>SUBMIT</h2></button>
                        </div>}
                        {showQEfirstResults === true && <div className='qeSection'>
                            <h2 className='qeSubmitH2'>Horizontal query expansion</h2>
                           
                            {ontologyValue.includes(',') && <p className='textQE2'>Results found of <b>exactly {qeValue} </b> keyword from <b>{ontologyValue.toUpperCase()}</b> ontologies:</p>}
                            {!ontologyValue.includes(',') && <p className='textQE2'>Results found of <b>exactly {qeValue} </b> keyword from <b>{ontologyValue.toUpperCase()}</b> ontology:</p>}
                            {resultsQEexact.map((element,index) => {
                                return (
                                    <div>
                                        <li className="qeListItem" key={index}>{element.obo_id}</li>
                                    </div>
                                )
                            })}
                             <button onClick={handleForward} className='forwardButton'>RETURN</button>
                            <button onClick={handleNext} className='nextButton'>SEARCH IN FILTERING TERMS</button>
                        </div>}
                        {showQEresults === true && showQEfirstResults === false && <div className='qeSection'>
                            <h2 className='qeSubmitH2'>Horizontal query expansion</h2>
                            {matchesQE.length > 0 && <p className='textQE'>We looked for all the ontology terms derived from the typed keyword <b>"{qeValue}" </b> that are part of the Beacon Network <b>filtering terms</b>. You can select them so that they are automatically copied to your query. Please be aware that if you want to look for individuals <b>with either one ontology or the other </b>you have to do different searches <b>for now.</b> In other words, one ontology term at a time. If you included all ontologies in a unique search you would be looking for individuals with several {qeValue} ontology terms in the same document, which does not makes much sense.</p>}
                            {matchesQE.length === 0 && <h5>Unfortunately the keyword is not among the current filtering terms</h5>}
                            {matchesQE.map((element) => {
                                return (
                                    <div className='divCheckboxQE'>
                                        <label className='labelQE'><input onChange={handleCheckQE} className='inputCheckbox' type='checkbox' value={element} />{element}</label>
                                    </div>
                                )


                            })}
                            <button onClick={handleNewQEsearch}><h2 className='newQEsearch'>New QE search</h2></button>
                        </div>}
                        {error !== null && <h6 className='errorQE'>{error}</h6>}
                    </div>

                </div>}


                {showBar === true && <div className="container-fluid">

                    {cohorts === false &&
                        showBar === true && <div>
                            <form className="d-flex" onSubmit={onSubmit}>
                                <input className="formSearch" type="search" placeholder={placeholder} value={query} onChange={(e) => search(e)} aria-label="Search" />
                                {!isSubmitted && <button className="searchButton" type="submit"><img className="searchIcon" src="./magnifier.png" alt='searchIcon'></img></button>}
                                {isSubmitted &&
                                    <div className="newSearch"><button className="newSearchButton" onClick={onSubmit2} type="submit">NEW SEARCH</button></div>}
                            </form>

                        </div>
                    }

                    {cohorts &&
                        <div className="cohortsModule">
                            <Select
                                onClick={triggerOptions}
                                closeMenuOnSelect={false}
                                components={animatedComponents}
                                defaultValue={[]}
                                isMulti
                                options={options}
                                onChange={handleChangeCohorts}
                                autoFocus={true}
                            //onToggleCallback={onToggle3}
                            />

                            <form className="d-flex2" onSubmit={onSubmitCohorts}>

                                {results !== 'Cohorts' && <button className="searchButton2" type="submit"><img className="forwardIcon" src="./adelante.png" alt='searchIcon'></img></button>}
                            </form>

                        </div>}

                </div>}


                <div className="additionalOptions">

                    <div className="example">
                        {cohorts === false && props.collection !== '' && showBar === true &&
                            <div className="bulbExample">
                                <button className="exampleQueries" onClick={handleExQueries}>Query Examples</button>
                                <img className="bulbLogo" src="../light-bulb.png" alt='bulbIcon'></img>
                                <div>
                                    {exampleQ[0] && exampleQ.map((result) => {

                                        return (<div id='exampleQueries'>


                                            <button className="exampleQuery" onClick={() => { setPlaceholder(`${result}`); setQuery(`${result}`); setValue(`${result}`) }}  >{result}</button>
                                        </div>)

                                    })}
                                </div>
                            </div>
                        }
                        {props.collection !== '' && showBar === true && <button className="filters" onClick={handleFilteringTerms}>
                            Filtering Terms
                        </button>}
                    </div>
                </div>
                {showVariants === true && showBar === true && <button className='modeVariants' onClick={handleClick}><h2 className='modeVariantsQueries'>Change to FORM mode</h2></button>}
                {showVariants === true && showBar === false && <button className='modeVariants' onClick={handleClick}><h2 className='modeVariantsQueries'>Change to BAR mode</h2></button>}
                <hr></hr>
                {showExtraIndividuals &&
                    <div className="containerExtraSections">
                        {showButton &&
                            <button className="arrowButton" onClick={handleExtraSectionIndividuals}><img className="arrowLogo" src="../arrow-down.png" alt='arrowIcon'></img></button>}
                        {!showButton &&
                            <button className="arrowButton" onClick={handleExtraSectionIndividuals}><img className="arrowLogo" src="../arrow-up.png" alt='arrowUpIcon'></img></button>}
                        {showOptions && <div className='extraSections'>

                            <div className='alphanumContainer'>

                                <div className='tittleAlph'>
                                    <h2>Alphanumerical and numerical queries</h2>
                                    <button className="helpButton" onClick={handleHelpModal1}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>
                                </div>
                                <div className='alphanumContainer2'>
                                    <div className='alphaIdModule'>
                                        <div className="listTerms">
                                            <label><h2>ID</h2></label>

                                            <input className="IdForm" type="text" value={state.query} autoComplete='on' placeholder={"write and filter by ID"} onChange={(e) => handleIdChanges(e)} aria-label="ID" />

                                            <div id="operator" >

                                                <select className="selectedOperator" onChange={handleOperatorchange} name="selectedOperator" >
                                                    <option value=''> </option>
                                                    <option value="=" >= </option>
                                                    <option value="<" >&lt;</option>
                                                    <option value=">" >&gt;</option>
                                                    <option value="!" >!</option>
                                                    <option value="%" >%</option>
                                                </select>

                                            </div>

                                            <label id="value"><h2>Value</h2></label>
                                            <input className="ValueForm" type="text" autoComplete='on' placeholder={"free text/ value"} onChange={handleValueChanges} aria-label="Value" />
                                        </div>
                                        {showIds && query !== '' &&
                                            <select className="selectedId" onChange={handleSelectedId} name="selectedId" multiple >
                                                {state.list.map(element => {
                                                    return (
                                                        <option value={element} >{element}</option>
                                                    )
                                                })}
                                            </select>}
                                    </div>
                                    <button className="buttonAlphanum" onClick={handdleInclude}>Include</button>
                                </div>

                                <div className="bulbExample">
                                    <button className="exampleQueries" onClick={handleExQueries}>Query Examples</button>
                                    <img className="bulbLogo" src="../light-bulb.png" alt='bulbIcon'></img>

                                </div>

                            </div>

                            <div className='advContainer'>
                                <form className='advSearchForm' onSubmit={onSubmit}>

                                    <div>
                                        <div className='resultset'>

                                            <div className="advSearch-module">
                                                <button className="helpButton2" onClick={handleHelpModal4}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>
                                                <label><h2>Include Resultset Responses</h2></label>
                                                <MultiSwitch
                                                    texts={["HIT", "MISS", "NONE", "ALL"]}
                                                    selectedSwitch={0}
                                                    bgColor={"white"}
                                                    onToggleCallback={onToggle2}
                                                    fontColor={"black"}
                                                    selectedFontColor={"white"}
                                                    border="0"
                                                    selectedSwitchColor="#e29348"
                                                    borderWidth="1"
                                                    height={"23px"}
                                                    fontSize={"12px"}
                                                    eachSwitchWidth={55}
                                                ></MultiSwitch>
                                            </div>

                                            <div className="advSearch-module">
                                                <button className="helpButton2" onClick={handleHelpModal5}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>
                                                <label><h2>Similarity</h2></label>
                                                <input id="similarityCheck" type="checkbox"
                                                    defaultChecked={false}
                                                    onChange={() => setChecked2(!checked2)}
                                                />

                                                {checked2 && <MultiSwitch
                                                    texts={["Low", "Medium", "High"]}
                                                    selectedSwitch={0}
                                                    bgColor={"white"}
                                                    onToggleCallback={onToggle}
                                                    fontColor={"black"}
                                                    selectedFontColor={"white"}
                                                    border="0"
                                                    selectedSwitchColor="#4f85bc"
                                                    borderWidth="1"
                                                    height={"23px"}
                                                    fontSize={"12px"}
                                                    eachSwitchWidth={60}
                                                ></MultiSwitch>}
                                            </div>
                                            <div className="advSearch-module">
                                                <button className="helpButton2" onClick={handleHelpModal6}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>
                                                <label><h2>Include Descendant Terms</h2></label>
                                                <div className="switchDescendants">
                                                    <h3>False</h3>
                                                    <Switch
                                                        checked={checked}
                                                        onChange={handleChangeSwitch}
                                                        inputProps={{ 'aria-label': 'controlled' }}
                                                        color="warning"
                                                        size="small"
                                                    />
                                                    <h3>True</h3>
                                                </div>

                                            </div>




                                        </div>


                                    </div>



                                </form>

                            </div>
                        </div>}
                    </div>}
                {hideForm === true && <button onClick={handleHideVariantsForm}><img className="arrowLogo" src="../arrow-down.png" alt='arrowIcon' /></button>}
                {showVariants && showBar === false && hideForm === false && <div>
                    <form onSubmit={handleSubmit}>
                        <div className='variantsContainer'>

                            <div className='moduleVariants'>
                                <label className='labelVariantsTittle'>Sequence queries</label>
                                <div>
                                    <label className='labelVariants'>Reference name</label>
                                    <input className='inputVariants' type='text' value={referenceName} onChange={handleChangeRefN}></input>
                                </div>
                                <div>
                                    <label className='labelVariants'>AssemblyID</label>
                                    <input className='inputVariants' type='text' value={assemblyId} onChange={handleChangeAssembly}></input>
                                </div>
                                <div>
                                    <label className='labelVariants'>Start (single value)*</label>
                                    <input className='inputVariants' type='text' value={start} onChange={handleChangeStart}></input>
                                </div>
                                <div>
                                    <label className='labelVariants'>alternateBases*</label>
                                    <input className='inputVariants' type='text' value={alternateBases} onChange={handleChangeAlternateB}></input>
                                </div>
                                <div>
                                    <label className='labelVariants'>referenceBases*</label>
                                    <input className='inputVariants' type='text' value={referenceBases} onChange={handleChangeReferenceB}></input>
                                </div>
                                <div className='DivButtonVariants'>
                                    <input className='buttonVariants' type="submit" value="Search" />
                                </div>
                            </div>
                            <div className='moduleVariants'>
                                <label className='labelVariantsTittle'>Range queries</label>
                                <div>
                                    <label className='labelVariants'>Reference name</label>
                                    <input className='inputVariants' type='text' value={referenceName2} onChange={handleChangeRefN2}></input>
                                </div>
                                <div>
                                    <label className='labelVariants'>AssemblyID</label>
                                    <input className='inputVariants' type='text' value={assemblyId2} onChange={handleChangeAssembly2}></input>
                                </div>
                                <div>
                                    <label className='labelVariants'>Start (single value)*</label>
                                    <input className='inputVariants' type='text' value={start2} onChange={handleChangeStart2}></input>
                                </div>
                                <div>
                                    <label className='labelVariants' >End (single value)*</label>
                                    <input className='inputVariants' type='text' value={end} onChange={handleChangeEnd}></input>
                                </div>
                                <div>
                                    <label className='labelVariants'>Variant type:</label>
                                    <input className='inputVariants' type='text' value={variantType} onChange={handleChangeVariantType}></input> </div>
                                <div><h3>OR</h3>
                                    <label className='labelVariants'>alternateBases:</label>
                                    <input className='inputVariants' type='text' value={alternateBases2} onChange={handleChangeAlternateB2}></input></div>
                                <div>
                                    <label className='labelVariants'>referenceBases:</label>
                                    <input className='inputVariants' type='text' value={referenceBases2} onChange={handleChangeReferenceB2}></input></div>
                                <div><h3>OR</h3>
                                    <label className='labelVariants'>Aminoacid Change:</label>
                                    <input className='inputVariants' type='text' value={aminoacid} onChange={handleChangeAminoacid}></input>
                                </div>
                                <div className='DivButtonVariants'>
                                    <input className='buttonVariants' type="submit" value="Search" />
                                </div>
                            </div>
                            <div className='moduleVariants'>
                                <label className='labelVariantsTittle'>Gene ID queries</label>
                                <div>
                                    <label className='labelVariants' >Gene ID*</label>
                                    <input className='inputVariants' type='text' value={geneID} onChange={handleChangeGeneId}></input>
                                </div>
                                <div>
                                    <label className='labelVariants'>AssemblyID</label>
                                    <input className='inputVariants' type='text' value={assemblyId3} onChange={handleChangeAssembly3}></input>
                                </div>
                                <div>
                                    <label className='labelVariants'>Variant type:</label>
                                    <input className='inputVariants' type='text' value={variantType2} onChange={handleChangeVariantType2}></input></div>
                                <div><h3>OR</h3>
                                    <label className='labelVariants'>alternateBases:</label>
                                    <input className='inputVariants' type='text' value={alternateBases3} onChange={handleChangeAlternateB3}></input></div>
                                <div><h3>OR</h3>
                                    <label className='labelVariants'>Aminoacid Change:</label>
                                    <input className='inputVariants' type='text' value={aminoacid2} onChange={handleChangeAminoacid2}></input>
                                </div>
                                <div className='DivButtonVariants'>
                                    <input className='buttonVariants' type="submit" value="Search" />
                                </div>
                            </div>
                        </div>

                    </form>

                </div>}

            </nav>

            <div>

                <ReactModal
                    isOpen={isOpenModal1}
                    onRequestClose={handleCloseModal1}
                    shouldCloseOnOverlayClick={true}
                >
                    <button onClick={handleCloseModal1}><img className="closeLogo" src="./cancel.png" alt='cancelIcon'></img></button>

                    <p>Help for alphanumerical and numerical queries.</p>

                </ReactModal>
                <ReactModal
                    isOpen={isOpenModal2}
                    onRequestClose={handleCloseModal2}
                    shouldCloseOnOverlayClick={true}
                >
                    <button onClick={handleCloseModal2}><img className="closeLogo" src="./cancel.png" alt='cancelIcon'></img></button>

                    <p>Help for queries.</p>

                </ReactModal>
            </div>


            <hr></hr>
            <div className="results">
                {results === null && !showFilteringTerms && <ResultsDatasets trigger={trigger} />}
                {isSubmitted && results === 'Individuals' &&
                    <div>
                        <IndividualsResults query={query} resultSets={resultSet} ID={ID} operator={operator} valueFree={valueFree} descendantTerm={descendantTerm} similarity={similarity} isSubmitted={isSubmitted} />
                    </div>
                }
                {isSubmitted && results === 'Variant' &&
                    <div>
                        <VariantsResults query={query} setHideForm={setHideForm} showBar={showBar} aminoacid2={aminoacid2} assemblyId2={assemblyId2} assemblyId3={assemblyId3} alternateBases3={alternateBases3} alternateBases2={alternateBases2} isSubmitted={isSubmitted} variantType2={variantType2} start2={start2} referenceName2={referenceName2} referenceName={referenceName} assemblyId={assemblyId} start={start} end={end} variantType={variantType} alternateBases={alternateBases} referenceBases={referenceBases} referenceBases2={referenceBases2} aminoacid={aminoacid} geneID={geneID} />
                    </div>
                }
                {results === null && showFilteringTerms && <FilteringTermsIndividuals filteringTerms={filteringTerms} collection={props.collection} setPlaceholder={setPlaceholder} placeholder={placeholder} query={query} setQuery={setQuery} />}

            </div>

        </div>

    );
}

export default Layout;