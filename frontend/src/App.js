import 'devextreme/dist/css/dx.light.css';

import './App.css';
import { Route, Routes } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Individuals2 from './components/Individual2';
import GenomicVariations from './components/GenomicVariations';
import Biosamples from './components/Biosamples';
import Runs from './components/Runs';
import Analyses from './components/Analyses';
import Cohorts from './components/Cohorts';
import Datasets from './components/Datasets'
import ErrorPage from './pages/ErrorPage';
import Navbar from './components/Navbar';
import Members from './components/Members';
import History from './components/History';
import SignInForm from './components/SignInForm';
import SignUpForm from './components/SignUpForm';
import ResultsDatasets from './components/ResultsDatasets';
import FilteringTermsIndividuals from './components/FilteringTermsIndividuals';

import Select from 'react-select'

import { AuthContext } from './components/context/AuthContext';
import { useContext } from 'react';

import axios from "axios";

import ReactModal from 'react-modal';
import makeAnimated from 'react-select/animated';
import { renderActionsCell } from '@mui/x-data-grid';



function Layout() {

  const [error, setError] = useState(null)
  const [collectionType, setCollectionType] = useState(["Select collection", "Individuals", "Cohorts", "Datasets", "Biosamples", "Analyses", "Runs", "Variant"])
  const [collection, setCollection] = useState('')
  const [placeholder, setPlaceholder] = useState('')
  const [results, setResults] = useState(null)
  const [query, setQuery] = useState(null)
  const [exampleQ, setExampleQ] = useState([])
  const [showAdv, setShowAdv] = useState(false)
  const [showAlphanumValue, setAlphanumValue] = useState(false)
  const [resultSetType, setResultsetType] = useState(["Select", "HIT", "MISS", "NONE", "ALL"])
  const [resultSet, setResultset] = useState("HIT")

  const [cohorts, setShowCohorts] = useState(false)

  const [ID, setId] = useState("")
  const [operator, setOperator] = useState("")
  const [valueFree, setValueFree] = useState("")

  const [value, setValue] = useState("")

  const [popUp, setPopUp] = useState(false)

  const [descendantTermType, setDescendantTermType] = useState(["Select", "true", "false"])
  const [descendantTerm, setDescendantTerm] = useState("true")

  const [similarityType, setSimilarityType] = useState(["Select", "low", "medium", "high"])
  const [similarity, setSimilarity] = useState("Select")

  const [showFilteringTerms, setShowFilteringTerms] = useState(false)
  const [filteringTerms, setFilteringTerms] = useState(false)

  const { storeToken, refreshToken, getStoredToken, authenticateUser, setExpirationTime, setExpirationTimeRefresh } = useContext(AuthContext);

  const Add = collectionType.map(Add => Add)

  const Add2 = resultSetType.map(Add2 => Add2)

  const Add3 = descendantTermType.map(Add3 => Add3)

  const Add4 = similarityType.map(Add4 => Add4)

  const [isOpenModal1, setIsOpenModal1] = useState(false);
  const [isOpenModal2, setIsOpenModal2] = useState(false);
  const [isOpenModal4, setIsOpenModal4] = useState(false);
  const [isOpenModal5, setIsOpenModal5] = useState(false);
  const [isOpenModal6, setIsOpenModal6] = useState(false);

  const [showAlph, setShowAlph] = useState(false)
  const [showAdvButton, setShowAdvButton] = useState(false)

  const animatedComponents = makeAnimated();

  const [state, setstate] = useState({
    query: '',
    list: []
  })


  const [isSubmitted, setIsSub] = useState(false)

  const [options, setOptions] = useState([
    { value: 'CINECA_synthetic_cohort_UK1', label: 'CINECA_synthetic_cohort_UK1' },
    { value: 'Fake cohort 1', label: 'Fake cohort 1' },
    { value: 'Fake cohort 2', label: 'Fake cohort 2' }
  ])

  const [arrayFilteringTerms, setArrayFilteringTerms] = useState([])

  const [showIds, setShowIds] = useState(false)

  const handleAddrTypeChange = (e) => {

    setCollection(collectionType[e.target.value])
    setExampleQ([])
    setFilteringTerms(false)
    setShowFilteringTerms(false)

  }

  const handleClick = (e) => {
    setCollectionType(["Select collection", "Individuals", "Cohorts", "Datasets", "Biosamples", "Analyses", "Runs", "Variant"])
    setCollection(collectionType[e.target.value])
  }

  const handleResultsetChanges = (e) => {
    setResultset(resultSetType[e.target.value])
  }

  const handleDescendantTermChanges = (e) => {
    setDescendantTerm(descendantTermType[e.target.value])
  }

  const handleSimilarityChanges = (e) => {

    setSimilarity(similarityType[e.target.value])
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

  const handleOperatorChanges = (e) => {
    setOperator(e.target.value)

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

    console.log(collection)
    if (collection === 'Individuals') {

      try {

        let res = await axios.get("http://localhost:5050/api/individuals/filtering_terms?limit=0")
        setFilteringTerms(res)
        setResults(null)


      } catch (error) {
        console.log(error)
      }
    } else if (collection === 'Cohorts') {

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
    if (collection === 'Individuals') {
      setExampleQ(['Weight>100', 'NCIT:C16352', 'geographicOrigin=%land%', 'geographicOrigin!England', 'NCIT:C42331'])
    }
  }

  const handleExQueriesAlphaNum = () => {

  }

  const Operatorchange = (e) => {
    setOperator(e.target.value)
    console.log()
  }

  useEffect(() => {
    const token = getStoredToken()

    if (token === null) {
      const timer = setTimeout(() => setPopUp(true), 1000);
      setPopUp(false)
      return () => clearTimeout(timer);
    }



    // declare the data fetching function
    const fetchData = async () => {

      try {
        let res = await axios.get("http://localhost:5050/api/individuals/filtering_terms?limit=0")
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

    setShowCohorts(false)


    if (collection === 'Individuals') {
      setPlaceholder('filtering term comma-separated, ID><=value')
      setShowAlph(true)
      setShowAdv(true)
    } else if (collection === 'Biosamples') {
      setPlaceholder('key=value, key><=value, or filtering term comma-separated')
    } else if (collection === 'Cohorts') {
      setShowCohorts(true)
      setShowAlph(false)
      setShowAdv(false)
      setPlaceholder('Search for any cohort')
    } else if (collection === "Variant") {
      setPlaceholder('chr : pos ref > alt')
    } else if (collection === "Analyses") {
      setPlaceholder('chr : pos ref > alt')
    } else if (collection === "Runs") {
      setPlaceholder('chr : pos ref > alt')
    } else if (collection === 'Datasets') {
      setPlaceholder('Search for any cohort')
    } else {
      setPlaceholder('')
    }

  }, [collection])


  const onSubmit = async (event) => {


    event.preventDefault()

    setIsSub(!isSubmitted)

    console.log(query)



    setCollectionType([`${collection}`])

    authenticateUser()

    setExampleQ([])


    setAlphanumValue(false)

    try {
      if (query === '1' || query === '') {
        setQuery(null)
      }
      if (collection === 'Individuals') {


        setResults('Individuals')

      } else if (collection === 'Cohorts') {
        setResults('Cohorts')
      }


    } catch (error) {
      console.log(error)
      setError(error.response.data.errorMessage)
    }
  }

  function search(e) {
    setQuery(e.target.value)

  }

  return (
    <div className="container1">
      <div className='logos'>
        <a href="https://www.cineca-project.eu/">
          <img className="cinecaLogo" src="./CINECA_logo.png" alt='cinecaLogo'></img>
        </a>
        <a href="https://elixir-europe.org/">
          <img className="elixirLogo" src="./white-orange-logo.png" alt='elixirLogo'></img>
        </a>
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

      <button className="helpButton" onClick={handleHelpModal2}><img className="questionLogo2" src="./question.png" alt='questionIcon'></img><h5>Help for querying</h5></button>
      <nav className="navbar">
        {isSubmitted && 
        <div className="newSearch"><button className="newSearchButton" onClick={onSubmit} type="submit">NEW SEARCH</button></div>}
        <div className="container-fluid">
          <select className="form-select" aria-label="Default select example" onClick={handleClick} onChange={e => { handleAddrTypeChange(e) }}>
            {
              Add.map((collection, key) => <option key={key} value={key}>{collection}
              </option>)
            }
          </select>

          {cohorts === false &&
            <form className="d-flex" onSubmit={onSubmit}>
              <input className="formSearch" type="search" placeholder={placeholder} value={query} onChange={(e) => search(e)} aria-label="Search" />
              {!isSubmitted && <button className="searchButton" type="submit"><img className="searchIcon" src="./magnifier.png" alt='searchIcon'></img></button>}

            </form>}

          {cohorts &&

            <form className="d-flex2" onSubmit={onSubmit}>

              {results !== 'Cohorts' && <button className="searchButton2" type="submit"><img className="forwardIcon" src="./adelante.png" alt='searchIcon'></img></button>}
            </form>
          }
          {results === "Cohorts" && <Select
            closeMenuOnSelect={false}
            components={animatedComponents}
            defaultValue={[options[0]]}
            isMulti
            options={options}
          />}

        </div>


        <div className="additionalOptions">

          <div className="example">
            {cohorts === false && collection !== '' &&
              <div className="bulbExample">
                <button className="exampleQueries" onClick={handleExQueries}>Query Examples</button>
                <img className="bulbLogo" src="../light-bulb.png" alt='bulbIcon'></img>
                <div>
                  {exampleQ[0] && exampleQ.map((result) => {

                    return (<div id='exampleQueries'>


                      <button className="exampleQuery" onClick={() => { setPlaceholder(`${result}`); setQuery(`${result}`); setResults(null); setValue(`${result}`) }}  >{result}</button>
                    </div>)

                  })}
                </div>
              </div>
            }

            {collection !== '' && <button className="filters" onClick={handleFilteringTerms}>
              Filtering Terms
            </button>}

            {collection === '' && <button className="filters" onClick={handleFilteringTermsAll}>
              Filtering terms of all collections
            </button>}

          </div>


        </div>
        <hr></hr>
        <div className='extraSections'>

          {showAlph && <div className='alphanumContainer'>

            <div className='tittleAlph'>
              <h2>Alphanumerical and numerical queries</h2>
              <button className="helpButton" onClick={handleHelpModal1}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>
            </div>
            <div className='alphanumContainer2'>
              <div className="listTerms">
                <label><h2>ID</h2></label>
                <input className="IdForm" type="text" value={state.query} autoComplete='on' placeholder={"write and filter by ID"} onChange={(e) => handleIdChanges(e)} aria-label="ID" />


                <div id="operator" >

                  <select className="selectedOperator" onChange={Operatorchange} name="selectedOperator" >
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

          </div>}
          {showAdv &&
            <div className='advContainer'>
              <form className='advSearchForm' onSubmit={onSubmit}>

                <div>


                  <div className='resultset'>



                    <div className="advSearch-module">
                      <button className="helpButton2" onClick={handleHelpModal4}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>
                      <label><h2>Include Resultset Responses</h2></label>
                      <select className="form-select2" aria-label="" onChange={(e) => handleResultsetChanges(e)}>
                        {
                          Add2.map((resultSet, key) => <option key={key} value={key}>{resultSet}
                          </option>)
                        }
                      </select>
                    </div>

                    <div className="advSearch-module">
                      <button className="helpButton2" onClick={handleHelpModal5}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>
                      <label><h2>Similarity</h2></label>
                      <select className="form-select2" aria-label="" onChange={e => { handleSimilarityChanges(e) }}>
                        {
                          Add4.map((similarity, key) => <option key={key} value={key}>{similarity}
                          </option>)
                        }
                      </select>
                    </div>
                    <div className="advSearch-module">
                      <button className="helpButton2" onClick={handleHelpModal6}><img className="questionLogo" src="./question.png" alt='questionIcon'></img></button>
                      <label><h2>Include Descendant Terms</h2></label>
                      <select className="form-select2" aria-label="" onChange={e => { handleDescendantTermChanges(e) }}>
                        {
                          Add3.map((descendantTerm, key) => <option key={key} value={key}>{descendantTerm}
                          </option>)
                        }
                      </select>
                    </div>




                  </div>


                </div>



              </form>

            </div>}
        </div>

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
        {isSubmitted &&
          <Individuals2 query={query} resultSets={resultSet} ID={ID} operator={operator} valueFree={valueFree} descendantTerm={descendantTerm} similarity={similarity} />
        }
        {results === null && showFilteringTerms && <FilteringTermsIndividuals filteringTerms={filteringTerms} collection={collection} setPlaceholder={setPlaceholder} placeholder={placeholder} />}
        {cohorts && results === 'Cohorts' &&

          <div>
            <Cohorts />
          </div>}
      </div>

    </div>

  );
}

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path='/' element={<Layout />} />
        <Route path='/individuals' element={<Individuals2 />} />
        <Route path='/genomicVariations' element={<GenomicVariations />} />
        <Route path='/biosamples' element={<Biosamples />} />
        <Route path='/runs' element={<Runs />} />
        <Route path='/analyses' element={<Analyses />} />
        <Route path='/cohorts' element={<Cohorts />} />
        <Route path='/datasets' element={<Datasets />} />
        <Route path='/members' element={<ResultsDatasets />} />
        <Route path='/history' element={<History />} />
        <Route path='/sign-up' element={<SignUpForm />} />
        <Route path="/sign-in" element={<SignInForm />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </div>
  );
}



export default App;