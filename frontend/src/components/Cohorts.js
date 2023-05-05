import ApexCharts from 'apexcharts'
import axios from "axios";
import { useState, useEffect } from 'react';
import './Cohorts.css';


function Cohorts(props) {
  console.log(props)
  const API_ENDPOINT = "http://localhost:5050/api/cohorts"

  const [error, setError] = useState(false)
  const [sampleData, setSampleData] = useState([])

  const [nameCohort, setNameCohort] = useState('')
  const [timeOut, setTimeOut] = useState(false)
  const [numberResults, setNumberResults] = useState(0)
  const [boolean, setBoolean] = useState(false)
  const [results, setResults] = useState([])

  const [show1, setShow1] = useState(false)
  const [show2, setShow2] = useState(false)
  const [show3, setShow3] = useState(false)

  const [limit, setLimit] = useState(10)
  const [skip, setSkip] = useState(0)

  const [skipTrigger, setSkipTrigger] = useState(0)
  const [limitTrigger, setLimitTrigger] = useState(0)


  const [showGraphs, setShowGraphs] = useState(false)

 

  useEffect(() => {
    const apiCall = async () => {
      try {

      

          setShowGraphs(true)

          const res = await axios.post(API_ENDPOINT)
          console.log(res.data.response.collections)

          for (var i = 0; i < res.data.response.collections.length; i++) {
            console.log(i)
            const sexs = res.data.response.collections[i].collectionEvents[0].eventGenders.distribution.genders
            const ethnicities = res.data.response.collections[i].collectionEvents[0].eventEthnicities.distribution.ethnicities
            const geoData = res.data.response.collections[i].collectionEvents[0].eventLocations.distribution.locations
            const diseasesData = res.data.response.collections[i].collectionEvents[0].eventDiseases.distribution.diseases

            setNameCohort(res.data.response.collections[i].name)
            console.log(geoData)

            const valuesSex = Object.values(sexs)
            const labelsSex = Object.keys(sexs)

            const valuesEthnicities = Object.values(ethnicities)
            const labelsEthnicities = Object.keys(ethnicities)

            const valuesGeo = Object.values(geoData)
            const labelsGeo = Object.keys(geoData)
            const entriesGeo = Object.entries(geoData)

            const valuesDiseases = Object.values(diseasesData)
            const labelsDiseases = Object.keys(diseasesData)


            var optionsSex = {

              chart: {
                type: 'donut'
              },
              title: {
                text: 'Sex',
              },
              series: valuesSex,
              labels: labelsSex,
            }

            var chartSex = new ApexCharts(document.querySelector("#chartSex"), optionsSex);
            chartSex.render();

            var optionsEthnicity = {
              chart: {
                type: 'bar'
              },
              title: {
                text: 'Ethnicity',
                align: 'center',
                floating: true
              },
              series: [{
                name: 'Number of individuals',
                data: valuesEthnicities
              }],
              xaxis: {
                categories: labelsEthnicities
              }
            }

            var chartEthnicity = new ApexCharts(document.querySelector("#chartEthnicity"), optionsEthnicity);
            chartEthnicity.render()

            var optionsGeo = {

              chart: {
                type: 'pie'
              },
              title: {
                text: 'Geographical origin',

              },
              series: valuesGeo,
              labels: labelsGeo,
            }

            var chartGeo = new ApexCharts(document.querySelector("#chartGeo"), optionsGeo);
            chartGeo.render()


            var optionsDiseases = {
              series: [{
                data: valuesDiseases
              }],
              chart: {
                type: 'bar',
                height: 630
              },
              plotOptions: {
                bar: {
                  barHeight: '100%',
                  distributed: true,
                  horizontal: true,
                  dataLabels: {
                    position: 'bottom'
                  },
                }
              },
              colors: ['#33b2df', '#546E7A', '#FFD700', '#2b908f', '#DC143C',
                '#f48024', '#69d2e7', '#13d8aa', '#A5978B', '#f9a3a4', '#FF4500', '#51f08e', '#b051f0',
                '#CCFF33', '#FF66CC', '#FF3333', '#6633CC', '#CD853F', '#3333FF', '#FF3333'
              ],
              dataLabels: {
                enabled: true,
                textAnchor: 'start',
                style: {
                  colors: ['#fff']
                },
                formatter: function (val, opt) {
                  return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
                },
                offsetX: 0,
                dropShadow: {
                  enabled: true
                }
              },
              stroke: {
                width: 1,
                colors: ['#fff']
              },
              xaxis: {
                categories: labelsDiseases,
              },
              yaxis: {
                labels: {
                  show: false
                }
              },
              title: {
                text: 'Diseases',
                align: 'center',
                floating: true
              },
              tooltip: {
                theme: 'dark',
                x: {
                  show: false
                },
                y: {
                  title: {
                    formatter: function () {
                      return ''
                    }
                  }
                }
              }
            };

            var chartDiseases = new ApexCharts(document.querySelector("#chartDiseases"), optionsDiseases);
            chartDiseases.render()
          }


     
          const arrayFilter = []
          const queryStringTerm = props.query.split(',')

          queryStringTerm.forEach((element, index) => {

            element = element.trim()


            const filter = {
              "id": element,
            }

            arrayFilter.push(filter)
          })

          var jsonData1 = {

            "meta": {
              "apiVersion": "2.0"
            },
            "query": {
              "filters": arrayFilter,
              "includeResultsetResponses": `${props.resultSets}`,
              "pagination": {
                "skip": 0,
                "limit": 10
              },
              "testMode": false,
              "requestedGranularity": "record",
            }
          }


          jsonData1 = JSON.stringify(jsonData1)

          const res2 = await axios.post("http://localhost:5050/api/cohorts", jsonData1, {
            headers: {
              'Content-Type': 'application/json',
              // 'Authorization': `Bearer ${token}`
            }
          })


          setTimeOut(true)


          if (res2.data.response.resultSets[0].results[0] === undefined) {
            setError("No results. Please check the query and retry")
            setNumberResults(0)
            setBoolean(false)

          }
          else {
            res2.data.response.resultSets[0].results.forEach((element, index) => {

              results.push(res2.data.response.resultSets[0].results[index].json())


            })

            setNumberResults(res2.data.responseSummary.numTotalResults)
            setBoolean(res2.data.responseSummary.exists)
          }
        



      } catch (error) {
        setError(error)
        console.log(error)
      }
    }
    apiCall()
  }, [])



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
      {showGraphs === false &&
        <div>
          <form className='skipLimit'>
            <div className='skipAndLimit'>
              <div>
                <label>SKIP</label>
                <input className="skipForm" type="number" autoComplete='on' placeholder={0} onChange={(e) => handleSkipChanges(e)} aria-label="Skip" />
              </div>
              <div>
                <label>LIMIT</label>
                <input className="limitForm" type="number" autoComplete='on' placeholder={10} onChange={(e) => handleLimitChanges(e)} aria-label="Limit" />
              </div>
              <button type="button" onClick={onSubmit} className="skipLimitButton">APPLY</button>
            </div>


          </form>

          <div> {timeOut &&
            <div className='selectGranularity'>
              <button className='typeResults' onClick={handleTypeResults1}> Boolean</button>
              <button className='typeResults' onClick={handleTypeResults2}>Count</button>
              <button className='typeResults' onClick={handleTypeResults3}>Full</button>
            </div>}

            <div className='resultsContainer'>
              {show1 && boolean && <p className='p1'>YES</p>}
              {show1 && !boolean && <p className='p1'>N0</p>}

              {show2 && numberResults !== 1 && <p className='p1'>{numberResults} &nbsp; Results</p>}
              {show2 && numberResults === 1 && <p className='p1'>{numberResults} &nbsp; Result</p>}

              {show3 && <div className="results">

                {!error && results[0] && results.map((result) => {
                  <p>{result}</p>
                })}
              </div>}
            </div>
          </div>
        </div>}

      {showGraphs === true &&
        <div>
          {nameCohort !== '' && <h3>{nameCohort}</h3>}
          <div className='chartsModule'>
            <div id="chartSex"></div>
            <div id="chartGeo"></div>
            <div id="chartEthnicity"></div>
            <div id="chartDiseases"></div>
          </div>
        </div>}

    </div>
  )
}

export default Cohorts