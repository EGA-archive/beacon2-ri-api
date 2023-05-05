import './Individuals.css';
import '../App.css';
import { useState, useEffect } from 'react';
import axios from "axios";

import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';

import TableResultsIndividuals from './TableResultsIndividuals';

function Individuals2(props) {


  const [error, setError] = useState(false)
  const [response, setResponse] = useState(null)
  const [numberResults, setNumberResults] = useState(0)
  const [boolean, setBoolean] = useState(false)
  const [results, setResults] = useState([])
  const [show1, setShow1] = useState(false)
  const [show2, setShow2] = useState(false)
  const [show3, setShow3] = useState(false)
  const [label, setLabel] = useState([])
  const [ident, setId] = useState([])
  const [operator, setOperator] = useState([])
  const [timeOut, setTimeOut] = useState(false)

  const [logInRequired, setLoginRequired] = useState(true)
  const [messageLogin, setMessageLogin] = useState('')

  const [limit, setLimit] = useState(10)
  const [skip, setSkip] = useState(0)

  const [skipTrigger, setSkipTrigger] = useState(0)
  const [limitTrigger, setLimitTrigger] = useState(0)

  const { getStoredToken, authenticateUser } = useContext(AuthContext);

  const [queryArray, setQueryArray] = useState([])
  const [arrayFilter, setArrayFilter] = useState([])

  const [CardMode, setCardMode] = useState(true)

  const API_ENDPOINT = "http://localhost:5050/api/individuals"

  let queryStringTerm = ''

  let keyTerm = []
  let resultsAux = []
  let obj = {}
  let res = ""


  useEffect(() => {
    const apiCall = async () => {
      let descendantTerm = 0
      authenticateUser()
      const token = getStoredToken()
      console.log(token)
      if (token !== undefined) {

        setLoginRequired(false)
      } else {
        setMessageLogin("PLEASE CREATE AN ACCOUNT AND LOG IN FOR QUERYING")
        console.log("ERROR")
      }

      if (props.descendantTerm === "true") {
        descendantTerm = true
      }

      if (props.descendantTerm === "false") {
        descendantTerm = false
      }

      if (props.query !== null) {

        queryStringTerm = props.query.split(',')
        console.log(queryStringTerm)
        queryStringTerm.forEach((element, index) => {

          element = element.trim()

          if (element.includes('=') || element.includes('>') || element.includes('<') || element.includes('!') || element.includes('%')) {

            if (element.includes('=')) {
              queryArray[index] = element.split('=')
              queryArray[index].push('=')
            }
            else if (element.includes('>')) {
              queryArray[index] = element.split('>')
              queryArray[index].push('>')
            } else if (element.includes('<')) {
              queryArray[index] = element.split('<')
              queryArray[index].push('<')
            } else if (element.includes('!')) {
              queryArray[index] = element.split('!')
              queryArray[index].push('!')
            } else {
              queryArray[index] = element.split('%')
              queryArray[index].push('%')
            }

            console.log(queryArray)
            const alphaNumFilter = {
              "id": queryArray[index][0],
              "operator": queryArray[index][2],
              "value": queryArray[index][1],
            }
            arrayFilter.push(alphaNumFilter)

          } else {

            const filter2 = {
              "id": element,
              "includeDescendantTerms": descendantTerm
            }
            arrayFilter.push(filter2)
          }

        })

        console.log(queryArray)

      }

      try {
        console.log(props.operator)
        if (props.value !== '' && props.operator !== '' && props.ID !== '') {

          console.log("holiii")
          //alphanumerical query

          const alphaNumFilter = {
            "id": `${props.ID}`,
            "operator": `${props.operator}`,
            "value": `${props.value}`,
          }

          arrayFilter.push(alphaNumFilter)


        }

        if (props.query === null) {

          // show all individuals

          var jsonData1 = {

            "meta": {
              "apiVersion": "2.0"
            },
            "query": {
              "filters": arrayFilter,
              "includeResultsetResponses": `${props.resultSets}`,
              "pagination": {
                "skip": skip,
                "limit": limit
              },
              "testMode": false,
              "requestedGranularity": "record",
            }
          }


          jsonData1 = JSON.stringify(jsonData1)
          console.log(jsonData1)
          console.log(token)
          //ORIOL 
          //res = await axios.post("http://localhost:5050/api/individuals", jsonData1)
          console.log(token)
          const headers = { 'Authorization': `Bearer ${token}` , 'Content-Type': "application/json",}
          res = axios.post('http://localhost:5050/api/individuals', { headers }, jsonData1)
            .then(response => console.log(response));

          setNumberResults(res.data.responseSummary.numTotalResults)
          setBoolean(res.data.responseSummary.exists)
          setTimeOut(true)
          res.data.response.resultSets[0].results.forEach((element, index) => {

            results.push(res.data.response.resultSets[0].results[index])


          })

        } else {

          var jsonData2 = {

            "meta": {
              "apiVersion": "2.0"
            },
            "query": {
              "filters": arrayFilter,
              "includeResultsetResponses": `${props.resultSets}`,
              "pagination": {
                "skip": skip,
                "limit": limit
              },
              "testMode": false,
              "requestedGranularity": "record",
            }
          }
          jsonData2 = JSON.stringify(jsonData2)
          console.log(jsonData2)

          res = await axios.post("http://localhost:5050/api/individuals", jsonData2)

          setTimeOut(true)

          if (res.data.response.resultSets[0].results[0] === undefined) {
            setError("No results. Please check the query and retry")
            setNumberResults(0)
            setBoolean(false)

          }
          else {
            res.data.response.resultSets[0].results.forEach((element, index) => {

              results.push(res.data.response.resultSets[0].results[index])
            })

            setNumberResults(res.data.responseSummary.numTotalResults)
            setBoolean(res.data.responseSummary.exists)
          }

        }

      } catch (error) {
        setTimeOut(true)
        setError("No results found. Please check the query and retry")
      }
    };
    apiCall();
  }, [skipTrigger, limitTrigger])


  const handleResultsMode = () => {
    setCardMode(!CardMode)
  }
  const handleTypeResults1 = () => {
    setShow1(true)
    setShow2(false)
    setShow3(false)
  }

  const handleTypeResults2 = () => {
    setShow2(true)
    setShow1(false)
    setShow3(false)

  }

  const handleTypeResults3 = () => {
    setShow3(true)
    setShow1(false)
    setShow2(false)
  }

  const handleSkipChanges = (e) => {
    setSkip(Number(e.target.value))
  }

  const handleLimitChanges = (e) => {
    setLimit(Number(e.target.value))

  }

  const onSubmit = () => {
    setSkipTrigger(skip)
    setLimitTrigger(limit)
    setTimeOut(false)

  }

  return (
    <div>
      {logInRequired === false &&

        <div>


          <div> {timeOut &&
            <div>
              <form className='skipLimit'>
                <div className='skipAndLimit'>
                  <div className='moduleSkip'>
                    <label>SKIP</label>
                    <input className="skipForm" type="number" autoComplete='on' placeholder={0} onChange={(e) => handleSkipChanges(e)} aria-label="Skip" />
                  </div>
                  <div className='moduleLimit'>
                    <label>LIMIT</label>
                    <input className="limitForm" type="number" autoComplete='on' placeholder={10} onChange={(e) => handleLimitChanges(e)} aria-label="Limit" />
                  </div>
                  <button type="button" onClick={onSubmit} className="skipLimitButton">APPLY</button>
                </div>


              </form>
              <div className='selectGranularity'>
                <h4>Granularity:</h4>
                <button className='typeResults' onClick={handleTypeResults1}><h5>Boolean</h5></button>
                <button className='typeResults' onClick={handleTypeResults2}><h5>Count</h5></button>
                <button className='typeResults' onClick={handleTypeResults3}><h5>Full response</h5></button>
              </div>
            </div>}

            {!CardMode && <div>
              <button className="cardTableButton" onClick={handleResultsMode}><h2>Change to card mode</h2></button>
              <TableResultsIndividuals results={results} ></TableResultsIndividuals>
            </div>}


            {CardMode &&
              <div className='resultsContainer'>

                {show1 && boolean && <p className='p1'>YES</p>}
                {show1 && !boolean && <p className='p1'>N0</p>}

                {show2 && numberResults !== 1 && <p className='p1'>{numberResults} &nbsp; Results</p>}
                {show2 && numberResults === 1 && <p className='p1'>{numberResults} &nbsp; Result</p>}

                {show3 && <div className="results">

                  <button className="cardTableButton" onClick={handleResultsMode}><h2>Change to table mode</h2></button>
                  {!error && results[0] && results.map((result) => {


                    return (
                      <div className="resultsIndividuals">

                        <div>
                          {result.id && <h2>ID</h2>}
                          {result.id && <h3>{result.id}</h3>}
                          {result.diseases && <h2>Disease</h2>}

                          {result.diseases && result.diseases.map((value) => {
                            return (
                              <div className='diseasesContainer'>
                                <h3>{value.diseaseCode.id}</h3>
                                <h3>{value.diseaseCode.label}</h3>
                              </div>)
                          })}

                        </div>

                        <div>
                          {result.ethnicity && <h2>Ethnicity</h2>}
                          {result.ethnicity && <h3>{result.ethnicity.id}</h3>}
                          {result.ethnicity && <h3>{result.ethnicity.label}</h3>}
                          {result.geographicOrigin && <h2>Geographic Origin</h2>}
                          {result.geographicOrigin && <h3>{result.geographicOrigin.id}</h3>}
                          {result.geographicOrigin && <h3>{result.geographicOrigin.label}</h3>}
                          {result.sex && <h2>Sex</h2>}
                          {result.sex.id && <h3>{result.sex.id}</h3>}
                          {result.sex.label && <h3>{result.sex.label}</h3>}
                        </div>
                        <div className='measuresContainer'>
                          {result.measures && <h2>Measures</h2>}
                          {result.measures.map((value) => {
                            return (
                              <div className='measures'>
                                <div>
                                  <h4>assayCode ID:</h4>
                                  <h3>{value.assayCode.id}</h3>
                                </div>
                                <div>
                                  <h4>assayCode label:</h4>
                                  <h3>{value.assayCode.label}</h3>
                                </div>

                                <div>
                                  <h4>Measurament value quantity ID and label:</h4>
                                  <h3>{value.measurementValue.quantity.unit.id}</h3>
                                  <h3>{value.measurementValue.quantity.unit.label}</h3>
                                </div>
                                <div>
                                  <h4>Measurament value quantity value:</h4>
                                  <h3>{value.measurementValue.quantity.value}</h3>
                                </div>
                              </div>)
                          })}
                        </div>

                      </div>
                    )

                  })}

                  {error && <h3>&nbsp; {error} </h3>}
                </div>
                }
              </div>}
          </div >
        </div>}
      {logInRequired === true && <h3>{messageLogin}</h3>}
    </div>
  )
}

export default Individuals2