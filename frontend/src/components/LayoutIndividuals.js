import '../App.css';

import FilteringTermsIndividuals from './FilteringTermsIndividuals';
import Individuals2 from './Individual2';
import Cohorts from './Cohorts';

import ResultsDatasets from './ResultsDatasets';

import Select from 'react-select'
import React, { useState, useEffect } from 'react';
import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';

import Switch from '@mui/material/Switch';
import MultiSwitch from 'react-multi-switch-toggle';

import axios from "axios";

import ReactModal from 'react-modal';
import makeAnimated from 'react-select/animated';

import IndividualsResults from './IndividualsResults';

function LayoutIndividuals(props) {

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

    const [trigger, setTrigger] = useState(false)
    const { storeToken, refreshToken, getStoredToken, authenticateUser, setExpirationTime, setExpirationTimeRefresh } = useContext(AuthContext);


    const [isOpenModal1, setIsOpenModal1] = useState(false);
    const [isOpenModal2, setIsOpenModal2] = useState(false);
    const [isOpenModal4, setIsOpenModal4] = useState(false);
    const [isOpenModal5, setIsOpenModal5] = useState(false);
    const [isOpenModal6, setIsOpenModal6] = useState(false);

    const [showExtraIndividuals, setExtraIndividuals] = useState(false)
    const [showOptions, setShowOptions] = useState(false)

    const [counter, setCounter] = useState(0)

    const animatedComponents = makeAnimated();

    const [resetSearch, setResetSearch] = useState(false)

    const [state, setstate] = useState({
        query: '',
        list: []
    })

    const [checked, setChecked] = useState(true)
    const [checked2, setChecked2] = useState(false)

    const [isSubmitted, setIsSub] = useState(false)

    const [options, setOptions] = useState([
        { value: 'CINECA_synthetic_cohort_UK1', label: 'CINECA_synthetic_cohort_UK1' },
        { value: 'Fake cohort 1', label: 'Fake cohort 1' },
        { value: 'Fake cohort 2', label: 'Fake cohort 2' }
    ])

    const [arrayFilteringTerms, setArrayFilteringTerms] = useState([])

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

    const handleOperatorchange = (e) => {
        setOperator(e.target.value)
        console.log()
    }


    const handleValueChanges = (e) => {
        setValueFree(e.target.value)
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
    const handleCloseModal4 = () => {
        setIsOpenModal4(false)
    }

    const handleHelpModal5 = () => {
        setIsOpenModal5(true)
    }
    const handleCloseModal5 = () => {
        setIsOpenModal5(false)
    }

    const handleHelpModal6 = () => {
        setIsOpenModal6(true)
    }
    const handleCloseModal6 = () => {
        setIsOpenModal6(false)
    }


    const handleFilteringTerms = async (e) => {


        if (props.collection === 'Individuals') {

            try {

                let res = await axios.get("http://localhost:5050/api/individuals/filtering_terms?limit=0")
                setFilteringTerms(res)
                setResults(null)


            } catch (error) {
                console.log(error)
            }
        } else if (props.collection === 'Cohorts') {

            try {

                let res = await axios.get("http://localhost:5050/api/cohorts/filtering_terms?limit=0")
                setFilteringTerms(res)
                setResults(null)

            } catch (error) {
                console.log(error)
            }
        }


        setShowFilteringTerms(true)


    }

    const handleFilteringTermsAll = async (e) => {
    }

    const handleExQueries = () => {
        if (props.collection === 'Individuals') {
            setExampleQ(['Weight>100', 'NCIT:C16352', 'geographicOrigin=%land%', 'geographicOrigin!England', 'NCIT:C42331'])
        }
    }

    const handleExQueriesAlphaNum = () => {

    }

    const handleExtraSectionIndividuals = (e) => {
        setShowOptions(!showOptions)
        setShowButton(!showButton)
    }



    useEffect(() => {
        //  const token = getStoredToken()

        //  if (token === null) {
        //    const timer = setTimeout(() => setPopUp(true), 1000);
        //  setPopUp(false)
        //            return () => clearTimeout(timer);
        //      }



        // declare the data fetching function
        const fetchData = async () => {

            try {
                let res = await axios.get("https://ega-archive.org/test-beacon-apis/cineca/individuals/filtering_terms")
                if (res !== null) {
                    res.data.response.filteringTerms.forEach(element => {
                        arrayFilteringTerms.push(element.id)
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
            setPlaceholder('chr : pos ref > alt')
            setExtraIndividuals(false)
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
        }


    }

    const onSubmitCohorts = () => {
        setResults('Cohorts')
        props.setShowGraphs(true)
        props.setLogged(!props.logged)
    }

    function search(e) {
        setQuery(e.target.value)

    }

    return (
        <div className="container1">
            <div className="container2">
                <button className="helpButton" onClick={handleHelpModal2}><img className="questionLogo2" src="./question.png" alt='questionIcon'></img><h5>Help for querying</h5></button>
                <div className='logos'>
                    <a href="https://www.cineca-project.eu/">
                        <img className="cinecaLogo" src="./CINECA_logo.png" alt='cinecaLogo'></img>
                    </a>
                    <a href="https://elixir-europe.org/">
                        <img className="elixirLogo" src="./white-orange-logo.png" alt='elixirLogo'></img>
                    </a>
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

                <div className="container-fluid">

                    {cohorts === false &&
                        <form className="d-flex" onSubmit={onSubmit}>
                            <input className="formSearch" type="search" placeholder={placeholder} value={query} onChange={(e) => search(e)} aria-label="Search" />
                            {!isSubmitted && <button className="searchButton" type="submit"><img className="searchIcon" src="./magnifier.png" alt='searchIcon'></img></button>}
                            {isSubmitted &&
                                <div className="newSearch"><button className="newSearchButton" onClick={onSubmit2} type="submit">NEW SEARCH</button></div>}
                        </form>}

                    {cohorts &&
                        <div className="cohortsModule">
                            <Select
                                closeMenuOnSelect={false}
                                components={animatedComponents}
                                defaultValue={[options[0]]}
                                isMulti
                                options={options}
                            />

                            <form className="d-flex2" onSubmit={onSubmitCohorts}>

                                {results !== 'Cohorts' && <button className="searchButton2" type="submit"><img className="forwardIcon" src="./adelante.png" alt='searchIcon'></img></button>}
                            </form>

                        </div>}

                </div>


                <div className="additionalOptions">

                    <div className="example">
                        {cohorts === false && props.collection !== '' &&
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

                        {props.collection !== '' && <button className="filters" onClick={handleFilteringTerms}>
                            Filtering Terms
                        </button>}

                        {props.collection === '' && <button className="filters" onClick={handleFilteringTermsAll}>
                            Filtering terms of all collections
                        </button>}

                    </div>


                </div>
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
                                    <div className="listTerms">
                                        <label><h2>ID</h2></label>
                                        <input className="IdForm" type="text" value={state.query} autoComplete='on' placeholder={"write and filter by ID"} onChange={(e) => handleIdChanges(e)} aria-label="ID" />


                                        <div id="operator" >

                                            <select className="selectedOperator" onChange={handleOperatorchange} name="selectedOperator" >
                                                <option value="=" >= </option>
                                                <option value=">" >&lt;</option>
                                                <option value="<" >&gt;</option>
                                                <option value="!" >!</option>
                                                <option value="%" >%</option>
                                            </select>

                                        </div>

                                        <label id="value"><h2>Value</h2></label>
                                        <input className="ValueForm" type="text" autoComplete='on' placeholder={"free text/ value"} onChange={(e) => handleValueChanges(e)} aria-label="Value" />
                                    </div>
                                    {showIds && query !== '' &&
                                        <ul className="ulIds">
                                            {state.list.map(item => (
                                                <li value={item}>
                                                    {item}
                                                </li>
                                            ))}
                                        </ul>}
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
                {results === null && !showFilteringTerms && <ResultsDatasets />}
                {isSubmitted && results === 'Individuals' &&
                    <div>
                        <IndividualsResults query={query} resultSets={resultSet} ID={ID} operator={operator} valueFree={valueFree} descendantTerm={descendantTerm} similarity={similarity} isSubmitted={isSubmitted} />
                    </div>
                }
                {results === null && showFilteringTerms && <FilteringTermsIndividuals filteringTerms={filteringTerms} collection={props.collection} setPlaceholder={setPlaceholder} placeholder={placeholder} query={query} setQuery={setQuery} />}
                {cohorts && results === 'Cohorts' &&

                    <div>
                        <Cohorts  />
                    </div>}
            </div>

        </div>

    );
}

export default LayoutIndividuals;