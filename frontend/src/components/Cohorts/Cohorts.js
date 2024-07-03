import './Cohorts.css'
import ApexCharts from 'apexcharts'
import axios from 'axios'
import { useState, useEffect } from 'react'
import Layout from '../Layout/Layout'
import { NavLink, useNavigate } from 'react-router-dom'
import configData from '../../config.json'
import CohortsModule from './CohortsModule'

function Cohorts (props) {
  const API_ENDPOINT = configData.API_URL + '/cohorts'

  const [error, setError] = useState(false)
  const navigate = useNavigate()

  const [arrayCohorts, setArrayCohorts] = useState([])

  const [optionsCohorts, setOptionsCohorts] = useState([])

  const [count, setCount] = useState(2)

  const [selectedCohorts, setSelectedCohorts] = useState([])

  const [cohortsIds, setCohortsIds] = useState([])

  const [nameCohort, setNameCohort] = useState('')

  const [showGraphs, setShowGraphs] = useState(false)

  const [response, setResponse] = useState('')

  const [labelsDiseases, setLabelsDiseases] = useState([])
  const [labelsEthnicities, setLabelsEthnicities] = useState([])

  const [eth_sex, setEthSex] = useState({})
  const [eth_dis, setEthDis] = useState({})

  const [dis_sex, setDisSex] = useState({})
  const [dis_eth, setDisEth] = useState({})

  const [selectedFilter, setSelectedFilter] = useState('')
  const [valueToFilter, setSelectedValue] = useState('')

  const [showEthFiltered, setShowEth] = useState(false)
  const [showEthFiltered2, setShowEth2] = useState(false)

  const [showDisFiltered, setShowDis] = useState(false)
  const [showDisFiltered2, setShowDis2] = useState(false)

  const [filterDisEth, setFilterDisEth] = useState(false)
  const [filterDisSex, setFilterDisSex] = useState(false)
  const [filterEthDis, setFilterEthDis] = useState(false)
  const [filterEthSex, setFilterEthSex] = useState(false)

  const [dataAvailable, setDataAvailable] = useState(false)
  const [timeOut, setTimeOut] = useState(false)

  const [triggerLayout, setTriggerLayout] = useState(false)

  const [trigger, setTrigger] = useState(false)

  const [trigger2, setTrigger2] = useState(false)
  const [noCollectionEvents, setNoCollectionEvents] = useState(false)

  const [alreadySelectedCohort, setAlreadySelectedCohort] = useState(true)

  //const handleSelectedFilter = e => {
  //setSelectedFilter(e.target.value)
  //}

  const handleSelectedValue = e => {
    setSelectedValue(e.target.value)
  }

  useEffect(() => {
    if (!props.newSearch) {
      const fetchDataCohorts = async () => {
        try {
          let res = await axios.get(configData.API_URL + '/cohorts')

          res.data.response.collections.forEach(element => {
            if (optionsCohorts.length > 0) {
              let found = 0
              optionsCohorts.forEach(cohort => {
                found = 0
                if (cohort.value === element.id) {
                  found = 1
                }
              })
              if (found === 0) {
                let obj = {
                  value: element.id,
                  label: element.id
                }
                optionsCohorts.push(obj)
              }
              if (found === 1) {
                let obj = {
                  value: element.id + count,
                  label: element.id + count
                }
                setCount(count + 1)
                element.id = element.id + count
                optionsCohorts.push(obj)
              }
            } else {
              let obj = {
                value: element.id,
                label: element.id
              }
              optionsCohorts.push(obj)
            }

            arrayCohorts.push(element)
            const timer = setTimeout(() => {
              setTriggerLayout(true)
            }, 2000)
            return () => clearTimeout(timer)
          })
        } catch (error) {
          setTimeOut(true)
          setError('No information available right now')
        }
      }
      fetchDataCohorts().catch(console.error)
    } else {
      setTimeOut(true)
    }
  }, [])

  // const submitFilters = e => {
  //   if (selectedFilter === 'dis_eth') {
  //     setShowDis2(false)
  //     setShowEth2(false)
  //     setShowEth(false)
  //     setShowDis(true)
  //     if (
  //       dis_eth[valueToFilter] !== null &&
  //       dis_eth[valueToFilter] !== undefined
  //     ) {
  //       setResponse(dis_eth[`${valueToFilter}`])
  //     } else {
  //       setError('Not found')
  //     }
  //   } else if (selectedFilter === 'dis_sex') {
  //     setShowDis(false)
  //     setShowEth2(false)
  //     setShowEth(false)
  //     setShowDis2(true)
  //     if (
  //       dis_sex[valueToFilter] !== null &&
  //       dis_sex[valueToFilter] !== undefined
  //     ) {
  //       setResponse(dis_sex[`${valueToFilter}`])
  //     } else {
  //       setError('Not found')
  //     }
  //   } else if (selectedFilter === 'eth_sex') {
  //     setShowDis2(false)
  //     setShowDis(false)
  //     setShowEth(false)
  //     setShowEth2(true)
  //     if (
  //       eth_sex[valueToFilter] !== null &&
  //       eth_sex[valueToFilter] !== undefined
  //     ) {
  //       setResponse(eth_sex[`${valueToFilter}`])
  //     } else {
  //       setError('Not found')
  //     }
  //   } else if (selectedFilter === 'eth_dis') {
  //     setShowDis2(false)
  //     setShowDis(false)
  //     setShowEth2(false)
  //     setShowEth(true)
  //     if (
  //       eth_dis[valueToFilter] !== null &&
  //       eth_dis[valueToFilter] !== undefined
  //     ) {
  //       setResponse(eth_dis[`${valueToFilter}`])
  //     } else {
  //       setError('Not found')
  //     }
  //   }
  // }

  useEffect(() => {
    const apiCall = () => {
      arrayCohorts.forEach(element => {
        if (element.id === selectedCohorts.value) {
          if (element.collectionEvents) {
            element.collectionEvents.forEach(element2 => {
              if (Object.keys(element2).length !== 0) {
                let sexs = ''
                let ethnicities = ''
                let geoData = ''
                let diseasesData = ''
                let diseases_eth = ''
                let diseases_sex = ''
                let ethnicities_dis = ''
                let ethnicities_sex = ''
                let valuesSex = ''
                let labelsSex = ''
                let valuesEthnicities = ''
                let labelsEthnicities = ''
                let valuesGeo = ''
                let labelsGeo = ''
                let entriesGeo = ''
                let valuesDiseases = ''
                let labelsDiseases = ''

                // for (var i = 0; i < res.data.response.collections.length; i++) {
                if (element2.eventGenders !== undefined) {
                  sexs = element2.eventGenders.distribution.genders
                  setDataAvailable(true)
                }
                if (element2.eventEthnicities !== undefined) {
                  ethnicities =
                    element2.eventEthnicities.distribution.ethnicities
                }
                if (element2.eventLocations !== undefined) {
                  geoData = element2.eventLocations.distribution.locations
                }
                if (element2.eventDiseases !== undefined) {
                  diseasesData = element2.eventDiseases.distribution.diseases
                  diseases_eth =
                    element2.eventDiseases.distribution.diseases_ethnicity
                  diseases_sex =
                    element2.eventDiseases.distribution.diseases_sex
                }

                if (diseases_eth !== '') {
                  setDisEth(diseases_eth)
                  setFilterDisEth(true)
                }
                if (diseases_sex !== '') {
                  setDisSex(diseases_sex)
                  setFilterDisSex(true)
                }

                if (element2.eventEthnicities !== undefined) {
                  ethnicities_dis =
                    element2.eventEthnicities.distribution.ethnicities_disease
                  ethnicities_sex =
                    element2.eventEthnicities.distribution.ethnicities_sex
                }

                if (ethnicities_dis !== '') {
                  setEthDis(ethnicities_dis)
                  setFilterEthDis(true)
                }
                if (ethnicities_sex !== '') {
                  setEthSex(ethnicities_sex)
                  setFilterEthSex(true)
                }

                setNameCohort(element.name)

                if (sexs !== '') {
                  valuesSex = Object.values(sexs)
                  labelsSex = Object.keys(sexs)
                }

                if (ethnicities !== '') {
                  valuesEthnicities = Object.values(ethnicities)
                  labelsEthnicities = Object.keys(ethnicities)
                }

                if (labelsEthnicities !== '') {
                  setLabelsEthnicities(labelsEthnicities)
                }

                if (geoData !== '') {
                  valuesGeo = Object.values(geoData)
                  labelsGeo = Object.keys(geoData)
                  entriesGeo = Object.entries(geoData)
                }

                if (diseasesData !== '') {
                  valuesDiseases = Object.values(diseasesData)
                  labelsDiseases = Object.keys(diseasesData)
                }

                if (labelsDiseases !== '') {
                  setLabelsDiseases(labelsDiseases)
                }

                if (valuesSex !== '' && labelsSex !== '') {
                  var optionsSex = {
                    chart: {
                      type: 'donut'
                    },
                    title: {
                      text: 'Sex'
                    },
                    series: valuesSex,
                    labels: labelsSex
                  }

                  var chartSex = new ApexCharts(
                    document.querySelector('#chartSex'),
                    optionsSex
                  )

                  chartSex.render()
                }

                if (valuesEthnicities !== '' && labelsEthnicities !== '') {
                  var optionsEthnicity = {
                    chart: {
                      type: 'bar'
                    },
                    title: {
                      text: 'Ethnicity',
                      align: 'center',
                      floating: true
                    },
                    series: [
                      {
                        name: 'Number of individuals',
                        data: valuesEthnicities
                      }
                    ],
                    xaxis: {
                      categories: labelsEthnicities
                    }
                  }

                  var chartEthnicity = new ApexCharts(
                    document.querySelector('#chartEthnicity'),
                    optionsEthnicity
                  )
                  chartEthnicity.render()
                }

                if (valuesGeo !== '' && labelsGeo !== '') {
                  var optionsGeo = {
                    chart: {
                      type: 'pie'
                    },
                    title: {
                      text: 'Geographical origin'
                    },
                    series: valuesGeo,
                    labels: labelsGeo
                  }

                  var chartGeo = new ApexCharts(
                    document.querySelector('#chartGeo'),
                    optionsGeo
                  )
                  chartGeo.render()
                }

                if (valuesDiseases !== '' && labelsDiseases !== '') {
                  var optionsDiseases = {
                    series: [
                      {
                        data: valuesDiseases
                      }
                    ],
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
                        }
                      }
                    },
                    colors: [
                      '#33b2df',
                      '#546E7A',
                      '#FFD700',
                      '#2b908f',
                      '#DC143C',
                      '#f48024',
                      '#69d2e7',
                      '#13d8aa',
                      '#A5978B',
                      '#f9a3a4',
                      '#FF4500',
                      '#51f08e',
                      '#b051f0',
                      '#CCFF33',
                      '#FF66CC',
                      '#FF3333',
                      '#6633CC',
                      '#CD853F',
                      '#3333FF',
                      '#FF3333'
                    ],
                    dataLabels: {
                      enabled: true,
                      textAnchor: 'start',
                      style: {
                        colors: ['#fff']
                      },
                      formatter: function (val, opt) {
                        return (
                          opt.w.globals.labels[opt.dataPointIndex] + ':  ' + val
                        )
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
                      categories: labelsDiseases
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
                  }

                  var chartDiseases = new ApexCharts(
                    document.querySelector('#chartDiseases'),
                    optionsDiseases
                  )
                  chartDiseases.render()
                }
                setTimeOut(true)
              } else {
                setTimeOut(true)
                setDataAvailable(false)
              }
            })
          } else {
            setNoCollectionEvents(true)
          }
        }
      })
    }
    setTrigger(true)
    if (selectedCohorts) {
      apiCall()
    }
  }, [showGraphs, trigger, trigger2])

  return (
    <div className='graphsDiv'>
      {showGraphs === false && triggerLayout === false && !timeOut && (
        <div class='middle'>
          <div class='bar bar1'></div>
          <div class='bar bar2'></div>
          <div class='bar bar3'></div>
          <div class='bar bar4'></div>
          <div class='bar bar5'></div>
          <div class='bar bar6'></div>
          <div class='bar bar7'></div>
          <div class='bar bar8'></div>
        </div>
      )}
      {showGraphs === false && triggerLayout && (
        <Layout
          collection={'Cohorts'}
          setShowGraphs={setShowGraphs}
          selectedCohorts={selectedCohorts}
          setSelectedCohorts={setSelectedCohorts}
          optionsCohorts={optionsCohorts}
        />
      )}
      {showGraphs === true && (
        <button
          onClick={() => {
            window.location.reload()
          }}
          className='buttonGoBack'
        >
          RETURN
        </button>
      )}

      {error !== '' && <h10>{error}</h10>}

      {trigger && trigger2 && !noCollectionEvents && showGraphs && (
        <>
          <CohortsModule
            optionsCohorts={optionsCohorts}
            selectedCohorts={selectedCohorts}
            setSelectedCohorts={setSelectedCohorts}
            setShowGraphs={setShowGraphs}
            alreadySelectedCohort={alreadySelectedCohort}
            response={response}
            setResponse={setResponse}
            setTrigger2={setTrigger2}
            trigger2={trigger2}
          />
          {nameCohort !== '' && <h3>{nameCohort}</h3>}
          {showGraphs === true && (
            <div className='chartModule'>
              <div id='chartSex'></div>
              <div id='chartGeo'></div>
              <hr></hr>
              <div className='ethnicity'>
                {/* <div className='ethFilters'>
                  <label for='ethnicities'>Filter:</label>
                  <select
                    name='filters'
                    id='filtersSelect'
                    onChange={handleSelectedFilter}
                  >
                    <option value=''></option>
                    {filterEthSex && (
                      <option value='eth_sex'>Ethnicities by sex</option>
                    )}
                    {filterEthDis && (
                      <option value='eth_dis'>Ethnicities by disease</option>
                    )}
                  </select>

                  <label for='ethnicities'>Select the ethnicity:</label>
                  <select
                    name='ethnicities'
                    id='ethnicitiesSelect'
                    onChange={handleSelectedValue}
                  >
                    <option value=''></option>
                    {labelsEthnicities.map(element => {
                      return <option value={element}>{element}</option>
                    })}
                  </select>
                  <button className='buttonSubmit' onClick={submitFilters}>
                    Submit
                  </button>
                </div> */}

                {/* {showEthFiltered && (
                  <div className='moduleFiltered'>
                    <div id='chartFilteredEthnicity'></div>
                  </div>
                )}
                {showEthFiltered2 && (
                  <div className='moduleFiltered'>
                    <div id='chartFilteredEthnicity2'></div>
                  </div>
                )} */}
                <div id='chartEthnicity'></div>
              </div>
              <hr></hr>
              <div className='diseases'>
                {/* <div className='diseasesFilters'>
                  <label for='ethnicities'>Filter:</label>
                  <select
                    name='filters'
                    id='filtersSelect'
                    onChange={handleSelectedFilter}
                  >
                    <option value=''></option>
                    {filterDisEth && (
                      <option value='dis_eth'>Diseases by ethnicity</option>
                    )}
                    {filterDisSex && (
                      <option value='dis_sex'>Diseases by sex</option>
                    )}
                  </select>

                  <select
                    name='diseases'
                    id='diseasesSelect'
                    onChange={handleSelectedValue}
                  >
                    <option value=''></option>
                    {labelsDiseases.map(element => {
                      return <option value={element}>{element}</option>
                    })}
                  </select>
                  <button className='buttonSubmit' onClick={submitFilters}>
                    Submit
                  </button>
                </div>

                {showDisFiltered && (
                  <div className='moduleFiltered'>
                    <div id='chartFilteredDisease'></div>
                  </div>
                )}
                {showDisFiltered2 && (
                  <div className='moduleFiltered'>
                    <div id='chartFilteredDisease2'></div>
                  </div>
                )} */}
                <div id='chartDiseases'></div>
              </div>
            </div>
          )}
        </>
      )}
      {trigger && !trigger2 && !noCollectionEvents && showGraphs && (
        <>
          <CohortsModule
            optionsCohorts={optionsCohorts}
            selectedCohorts={selectedCohorts}
            setSelectedCohorts={setSelectedCohorts}
            setShowGraphs={setShowGraphs}
            alreadySelectedCohort={alreadySelectedCohort}
            response={response}
            setResponse={setResponse}
            setTrigger2={setTrigger2}
            trigger2={trigger2}
          />
          {nameCohort !== '' && <h3>{nameCohort}</h3>}
          {showGraphs === true && (
            <div className='chartModule'>
              <div id='chartSex'></div>
              <div id='chartGeo'></div>
              <hr></hr>
              <div className='ethnicity'>
                {/* <div className='ethFilters'>
                  <label for='ethnicities'>Filter:</label>
                  <select
                    name='filters'
                    id='filtersSelect'
                    onChange={handleSelectedFilter}
                  >
                    <option value=''></option>
                    {filterEthSex && (
                      <option value='eth_sex'>Ethnicities by sex</option>
                    )}
                    {filterEthDis && (
                      <option value='eth_dis'>Ethnicities by disease</option>
                    )}
                  </select>

                  <label for='ethnicities'>Select the ethnicity:</label>
                  <select
                    name='ethnicities'
                    id='ethnicitiesSelect'
                    onChange={handleSelectedValue}
                  >
                    <option value=''></option>
                    {labelsEthnicities.map(element => {
                      return <option value={element}>{element}</option>
                    })}
                  </select>
                  <button className='buttonSubmit' onClick={submitFilters}>
                    Submit
                  </button>
                </div> */}

                {/* {showEthFiltered && (
                  <div className='moduleFiltered'>
                    <div id='chartFilteredEthnicity'></div>
                  </div>
                )}
                {showEthFiltered2 && (
                  <div className='moduleFiltered'>
                    <div id='chartFilteredEthnicity2'></div>
                  </div>
                )} */}
                <div id='chartEthnicity'></div>
              </div>
              <hr></hr>
              <div className='diseases'>
                {/* <div className='diseasesFilters'>
                  <label for='ethnicities'>Filter:</label>
                  <select
                    name='filters'
                    id='filtersSelect'
                    onChange={handleSelectedFilter}
                  >
                    <option value=''></option>
                    {filterDisEth && (
                      <option value='dis_eth'>Diseases by ethnicity</option>
                    )}
                    {filterDisSex && (
                      <option value='dis_sex'>Diseases by sex</option>
                    )}
                  </select>

                  <select
                    name='diseases'
                    id='diseasesSelect'
                    onChange={handleSelectedValue}
                  >
                    <option value=''></option>
                    {labelsDiseases.map(element => {
                      return <option value={element}>{element}</option>
                    })}
                  </select>
                  <button className='buttonSubmit' onClick={submitFilters}>
                    Submit
                  </button>
                </div>

                {showDisFiltered && (
                  <div className='moduleFiltered'>
                    <div id='chartFilteredDisease'></div>
                  </div>
                )}
                {showDisFiltered2 && (
                  <div className='moduleFiltered'>
                    <div id='chartFilteredDisease2'></div>
                  </div>
                )} */}
                <div id='chartDiseases'></div>
              </div>
            </div>
          )}
        </>
      )}

      {trigger && noCollectionEvents && showGraphs && (
        <h10>NO GRAPHICS AVAILABLE FOR THE SELECTED COHORT</h10>
      )}
      {showGraphs === true && dataAvailable === false && timeOut === true && (
        <div>
          <h12>
            UNFORTUNATELY, THERE ARE NO GRAPHICS AVAILABLE RIGHT NOW FOR THE
            SELECTED COHORT
          </h12>
        </div>
      )}
    </div>
  )
}

export default Cohorts
