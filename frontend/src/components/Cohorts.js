import './Cohorts.css';
import ApexCharts from 'apexcharts'
import axios from "axios";
import { useState, useEffect } from 'react';
import LayoutIndividuals from './LayoutIndividuals';
import { useNavigate } from 'react-router-dom';

function Cohorts(props) {

  const API_ENDPOINT = "https://beacons.bsc.es/beacon-network/v2.0.0/cohorts"

  const [error, setError] = useState(false)
  const navigate = useNavigate();

  const [nameCohort, setNameCohort] = useState('')

  const [showGraphs, setShowGraphs] = useState(false)

  const [logged, setLogged] = useState(false)

  const [labelsDiseases, setLabelsDiseases] = useState([])
  const [labelsEthnicities, setLabelsEthnicities] = useState([])

  const [eth_sex, setEthSex] = useState({})
  const [eth_dis, setEthDis] = useState({})

  const [dis_sex, setDisSex] = useState({})
  const [dis_eth, setDisEth] = useState({})

  const [selectedFilter, setSelectedFilter] = useState('')
  const [valueToFilter, setSelectedValue] = useState('')

  const handleClick = () => {
    setLogged(!logged)
    setShowGraphs(false)
  }

  const handleSelectedFilter = (e) => {
    setSelectedFilter(e.target.value)
  }

  const handleSelectedValue = (e) => {
    setSelectedValue(e.target.value)
  }

  const submitFilters = (e) => {
    let res = ''
    if (selectedFilter === 'dis_eth') {
      res = dis_eth.valueToFilter
    } else if (selectedFilter === 'dis_sex') {
      res = dis_sex.valueToFilter
    } else if (selectedFilter === 'eth_sex') {
      res = eth_sex.valueToFilter
    } else if (selectedFilter === 'eth_dis') {
      res = eth_dis.valueToFilter
    } else {
      res = ''
    }

    let values = []
    let labels = []
    if (res !== '') {
      values = Object.values(res)
      labels = Object.keys(res)
    }

    if (values.length > 0 && labels.length > 0) {
      var options = {

        chart: {
          type: 'pie'
        },
        title: {
          text: 'Filtered graphic',

        },
        series: values,
        labels: labels,
      }

      var chartFiltered = new ApexCharts(document.querySelector("#chartFiltered"), options);
      chartFiltered.render()
    }



  }

  useEffect(() => {
    const apiCall = async () => {

      try {

        const res = await axios.get(API_ENDPOINT)
        console.log(res.data)
        console.log(res.data.response.collections)
        let i = 11
        // for (var i = 0; i < res.data.response.collections.length; i++) {
        console.log(i)
        const sexs = res.data.response.collections[i].collectionEvents[0].eventGenders.distribution.genders
        const ethnicities = res.data.response.collections[i].collectionEvents[0].eventEthnicities.distribution.ethnicities
        const geoData = res.data.response.collections[i].collectionEvents[0].eventLocations.distribution.locations
        const diseasesData = res.data.response.collections[i].collectionEvents[0].eventDiseases.distribution.diseases

        const diseases_eth = res.data.response.collections[i].collectionEvents[0].eventDiseases.distribution.diseases_ethnicity
        const diseases_sex = res.data.response.collections[i].collectionEvents[0].eventDiseases.distribution.diseases_sex
        setDisEth(diseases_eth)
        setDisSex(diseases_sex)

        const ethnicities_dis = res.data.response.collections[i].collectionEvents[0].eventEthnicities.distribution.ethnicities_diseases
        const ethnicities_sex = res.data.response.collections[i].collectionEvents[0].eventEthnicities.distribution.ethnicities_sex

        setEthDis(ethnicities_dis)
        setEthSex(ethnicities_sex)


        setNameCohort(res.data.response.collections[i].name)
        console.log(geoData)

        const valuesSex = Object.values(sexs)
        const labelsSex = Object.keys(sexs)

        const valuesEthnicities = Object.values(ethnicities)
        const labelsEthnicities = Object.keys(ethnicities)
        setLabelsEthnicities(labelsEthnicities)

        const valuesGeo = Object.values(geoData)
        const labelsGeo = Object.keys(geoData)
        const entriesGeo = Object.entries(geoData)

        const valuesDiseases = Object.values(diseasesData)
        const labelsDiseases = Object.keys(diseasesData)
        setLabelsDiseases(labelsDiseases)

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
        // }

      } catch (error) {
        setError(error)
        console.log(error)
      }
    }
    apiCall()
  }, [logged])

  return (

    <div>
        {showGraphs === true && <button className="back" onClick={handleClick}><h2>Back to Cohorts search</h2></button>}
        {showGraphs === false && <LayoutIndividuals collection={'Cohorts'} setShowGraphs={setShowGraphs} setLogged={setLogged} logged={logged} />}
        <h1>Filters</h1>
        <label for="filters">Select an option to filter</label>
        <select name="filters" id="filtersSelect" onChange={handleSelectedFilter}>
          <option value=''></option>
          <option value='eth_sex'>Ethnicities by sex</option>
          <option value='eth_dis'>Ethnicities by disease</option>
          <option value='dis_eth'>Diseases by ethnicity</option>
          <option value='dis_sex'>Diseases by sex</option>
        </select>
        {selectedFilter === 'dis_eth' &&
          <div>
            <label for="diseases">Select the disease:</label>
            <select name="diseases" id="diseasesSelect" onChange={handleSelectedValue}>
              <option value=''></option>
              {labelsDiseases.map(element => {
                return (
                  <option value={element}>{element}</option>
                )
              })}
            </select>
          </div>
        }
        {selectedFilter === 'dis_sex' &&
          <div>
            <label for="diseases">Select the disease:</label>
            <select name="diseases" id="diseasesSelect2" onChange={handleSelectedValue}>
              <option value=''></option>
              {labelsDiseases.map(element => {
                return (
                  <option value={element}>{element}</option>
                )
              })}
            </select>
          </div>}

        {selectedFilter === 'eth_sex' &&
          <div>
            <label for="ethnicities">Select the ethnicity:</label>
            <select name="ethnicities" id="ethnicitiesSelect" onChange={handleSelectedValue}>
              <option value=''></option>
              {labelsEthnicities.map(element => {
                return (
                  <option value={element}>{element}</option>
                )
              })}
            </select>
          </div>}
        {selectedFilter === 'eth_dis' &&
          <div>
            <label for="ethnicities">Select the ethnicity:</label>

            <select name="ethnicities" id="ethnicitiesSelect2" onChange={handleSelectedValue}>
              <option value=''></option>
              {labelsEthnicities.map(element => {
                return (
                  <option value={element}>{element}</option>
                )
              })}
            </select>
          </div>}

        <button onClick={submitFilters}>Submit</button>
    

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