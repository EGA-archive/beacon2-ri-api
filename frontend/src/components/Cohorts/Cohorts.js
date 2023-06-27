import './Cohorts.css';
import ApexCharts from 'apexcharts'
import axios from "axios";
import { useState, useEffect } from 'react';
import Layout from '../Layout/Layout';
import { useNavigate } from 'react-router-dom';

function Cohorts(props) {

  const API_ENDPOINT = "https://beacons.bsc.es/beacon-network/v2.0.0/cohorts/"

  const [error, setError] = useState(false)
  const navigate = useNavigate();

  const [options, setOptions] = useState([])


  const [trigger, setTrigger] = useState(false)

  const [nameCohort, setNameCohort] = useState('')

  const [showGraphs, setShowGraphs] = useState(false)

  const [showReset, setReset] = useState(false)
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



  const handleSelectedFilter = (e) => {
    setSelectedFilter(e.target.value)
  }

  const handleSelectedValue = (e) => {
    setSelectedValue(e.target.value)
    console.log(e.target.value)
  }

  useEffect(() => {
    let values = []
    let labels = []
    if (response !== '') {
      values = Object.values(response)
      labels = Object.keys(response)
    }
    console.log(values)
    console.log(labels)

    if (values.length > 0 && labels.length > 0) {
      var options = {

        chart: {
          type: 'pie'
        },
        title: {
          text: valueToFilter,
        },
        colors: ['#4dc5ff', '#FF96EF', '#7DF9FF', '#8B0000', '#AAFF00', '#98FB98', '#009E60', '#AF2BFF', '#FF0000', '#FF69B4', '#13D3B6', '#800080', '#FA8072', '#33b2df', '#546E7A', '#FEF300', '#2b908f', '#FE00FA',
          '#FE6800', '#69d2e7', '#13d8aa', '#A5978B', '#f9a3a4', '#FF4500', '#51f08e', '#b051f0',
          '#CCFF33', '#FF66CC', '#FF3333', '#6633CC', '#CD853F', '#3333FF', '#FF3333', '#BF40BF', 'DF00F9', '38ED61', '#FCF55F', '#00A9D1', '#041FCE', '#B4B5BC', '#C1E701', '#FF8604'],
        series: values,
        labels: labels,
      }

      console.log(options)

      if (selectedFilter === 'dis_eth') {

        var chartFiltered = new ApexCharts(document.querySelector("#chartFilteredDisease"), options);
        chartFiltered.render()
      } else if (selectedFilter === 'dis_sex') {

        var chartFiltered = new ApexCharts(document.querySelector("#chartFilteredDisease2"), options);

        chartFiltered.render()
      }
      else if (selectedFilter === 'eth_dis') {

        var chartFiltered = new ApexCharts(document.querySelector("#chartFilteredEthnicity"), options);

        chartFiltered.render()
      } else if (selectedFilter === 'eth_sex') {

        var chartFiltered = new ApexCharts(document.querySelector("#chartFilteredEthnicity2"), options);
        chartFiltered.render()
      }

    }


  }, [response])

  const submitFilters = (e) => {
    console.log("hola")

    if (selectedFilter === 'dis_eth') {
      setShowDis2(false)
      setShowEth2(false)
      setShowEth(false)
      setShowDis(true)
      if (dis_eth[valueToFilter] !== null && dis_eth[valueToFilter] !== undefined) {
        setResponse(dis_eth[`${valueToFilter}`])
      } else {
        setError('Not found')
      }

    } else if (selectedFilter === 'dis_sex') {
      setShowDis(false)
      setShowEth2(false)
      setShowEth(false)
      setShowDis2(true)
      if (dis_sex[valueToFilter] !== null && dis_sex[valueToFilter] !== undefined) {
        setResponse(dis_sex[`${valueToFilter}`])
      } else {
        setError('Not found')
      }

    } else if (selectedFilter === 'eth_sex') {
      setShowDis2(false)
      setShowDis(false)
      setShowEth(false)
      setShowEth2(true)
      if (eth_sex[valueToFilter] !== null && eth_sex[valueToFilter] !== undefined) {
        setResponse(eth_sex[`${valueToFilter}`])
      } else {
        setError('Not found')
      }


    } else if (selectedFilter === 'eth_dis') {
      setShowDis2(false)
      setShowDis(false)
      setShowEth2(false)
      setShowEth(true)
      console.log(eth_dis)
      if (eth_dis[valueToFilter] !== null && eth_dis[valueToFilter] !== undefined) {
        setResponse(eth_dis[`${valueToFilter}`])
      } else {
        setError('Not found')
      }

    }


  }


  useEffect(() => {
    console.log(showGraphs)
    const apiCall = async () => {

      try {

        const res = await axios.get(API_ENDPOINT)

        const cohortSelected = props.selectedCohort.value

        res.data.response.collections.forEach(element => {

          if (element.name === cohortSelected) {
            if (element.collectionEvents !== undefined) {

              element.collectionEvents.forEach(element2 => {

                if (Object.keys(element2).length !== 0) {

                  console.log(element2)
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
                  }
                  if (element2.eventEthnicities !== undefined) {
                    ethnicities = element2.eventEthnicities.distribution.ethnicities
                  }
                  if (element2.eventLocations !== undefined) {
                    geoData = element2.eventLocations.distribution.locations
                  }
                  if (element2.eventDiseases !== undefined) {
                    diseasesData = element2.eventDiseases.distribution.diseases
                    diseases_eth = element2.eventDiseases.distribution.diseases_ethnicity
                    diseases_sex = element2.eventDiseases.distribution.diseases_sex
                  }

                  if (diseases_eth !== '') {
                    setDisEth(diseases_eth)
                  }
                  if (diseases_sex !== '') {
                    setDisSex(diseases_sex)
                  }

                  if (element2.eventEthnicities !== undefined) {
                    ethnicities_dis = element2.eventEthnicities.distribution.ethnicities_disease
                    ethnicities_sex = element2.eventEthnicities.distribution.ethnicities_sex
                  }

                  if (ethnicities_dis !== '') {
                    setEthDis(ethnicities_dis)
                  }
                  if (ethnicities_sex !== '') {
                    setEthSex(ethnicities_sex)
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
                        text: 'Sex',
                      },
                      series: valuesSex,
                      labels: labelsSex,
                    }

                    var chartSex = new ApexCharts(document.querySelector("#chartSex"), optionsSex);
                    chartSex.render();
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
                  }

                  if (valuesGeo !== '' && labelsGeo !== '') {
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
                  }


                  if (valuesDiseases !== '' && labelsDiseases !== '') {
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

                }
              })
            }
          }

        })

      } catch (error) {
        setError(error)
        console.log(error)
      }

    }
    if (showGraphs === true) {
      apiCall()

    }

  }, [showGraphs])

  useEffect(() => {
    const fetchDataCohorts = async () => {

      try {

        let res = await axios.get('https://beacons.bsc.es/beacon-network/v2.0.0/cohorts/')
        
        res.data.response.collections.forEach(element => {

          if (element.name === undefined && element.cohortName !== undefined) {
            let obj = {
              value: element.cohortName,
              label: element.cohortName
            }
            options.push(obj)

          } else if (element.name !== undefined) {
            let obj = {
              value: element.name,
              label: element.name
            }
            options.push(obj)

          }

          console.log(options)
        })

        setTrigger(true)

      } catch (error) {
        console.log(error)
      }

    }
    fetchDataCohorts().catch(console.error)

  }, [])

  return (
    <div>
      {showGraphs === false && <Layout collection={'Cohorts'} setShowGraphs={setShowGraphs} options={options} />}

      {nameCohort !== '' && <h3>{nameCohort}</h3>}
      {showGraphs === true &&
        <div className='chartsModule'>
          <div id="chartSex"></div>
          <div id="chartGeo"></div>
          <hr></hr>
          <div className='ethnicity'>
            <div className='ethFilters'>
              <label for="ethnicities">Filter:</label>
              <select name="filters" id="filtersSelect" onChange={handleSelectedFilter}>
                <option value=''></option>
                <option value='eth_sex'>Ethnicities by sex</option>
                <option value='eth_dis'>Ethnicities by disease</option>
              </select>

              <label for="ethnicities">Select the ethnicity:</label>
              <select name="ethnicities" id="ethnicitiesSelect" onChange={handleSelectedValue}>
                <option value=''></option>
                {labelsEthnicities.map(element => {
                  return (
                    <option value={element}>{element}</option>
                  )
                })}
              </select>
              <button className="buttonSubmit" onClick={submitFilters}>Submit</button>
            </div>
            {showEthFiltered &&
              <div className="moduleFiltered">
                <div id="chartFilteredEthnicity"></div>
              </div>}
            {showEthFiltered2 &&
              <div className="moduleFiltered">
                <div id="chartFilteredEthnicity2"></div>
              </div>}
            <div id="chartEthnicity"></div>
          </div>
          <hr></hr>
          <div className='diseases'>
            <div className='diseasesFilters'>
              <label for="ethnicities">Filter:</label>
              <select name="filters" id="filtersSelect" onChange={handleSelectedFilter}>
                <option value=''></option>
                <option value='dis_eth'>Diseases by ethnicity</option>
                <option value='dis_sex'>Diseases by sex</option>
              </select>

              <select name="diseases" id="diseasesSelect" onChange={handleSelectedValue}>
                <option value=''></option>
                {labelsDiseases.map(element => {
                  return (
                    <option value={element}>{element}</option>
                  )
                })}
              </select>
              <button className="buttonSubmit" onClick={submitFilters}>Submit</button>
            </div>
            {showDisFiltered &&
              <div className="moduleFiltered">
                <div id="chartFilteredDisease"></div></div>}
            {showDisFiltered2 &&
              <div className="moduleFiltered">
                <div id="chartFilteredDisease2"></div>
              </div>}
            <div id="chartDiseases"></div>
          </div>
        </div>}


    </div>
  )
}

export default Cohorts