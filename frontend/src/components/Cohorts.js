import './Cohorts.css';
import ApexCharts from 'apexcharts'
import axios from "axios";
import { useState, useEffect } from 'react';
import LayoutIndividuals from './LayoutIndividuals';
import { useNavigate } from 'react-router-dom';

function Cohorts(props) {

  const API_ENDPOINT = "https://beacons.bsc.es/beacon-network/v2.0.0/cohorts/"

  const [error, setError] = useState(false)
  const navigate = useNavigate();

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
      if (dis_eth[valueToFilter] !== null && dis_eth[valueToFilter] !== undefined ){
        setResponse(dis_eth[`${valueToFilter}`])
      } else {
        setError('Not found')
      }
     
    } else if (selectedFilter === 'dis_sex') {
      setShowDis(false)
      setShowEth2(false)
      setShowEth(false)
      setShowDis2(true)
      if (dis_sex[valueToFilter] !== null && dis_sex[valueToFilter]!== undefined){
        setResponse(dis_sex[`${valueToFilter}`])
      } else{
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
      if (eth_dis[valueToFilter] !== null && eth_dis[valueToFilter] !== undefined){
        setResponse(eth_dis[`${valueToFilter}`])
      } else{
        setError('Not found')
      }

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
        console.log(diseases_eth)
        console.log(diseases_sex)
        const ethnicities_dis = res.data.response.collections[i].collectionEvents[0].eventEthnicities.distribution.ethnicities_disease
        const ethnicities_sex = res.data.response.collections[i].collectionEvents[0].eventEthnicities.distribution.ethnicities_sex

        setEthDis(ethnicities_dis)
        setEthSex(ethnicities_sex)
        console.log(ethnicities_dis)
        console.log(ethnicities_sex)

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
  }, [])

  return (

    <div>

      {showGraphs === false && <LayoutIndividuals collection={'Cohorts'} setShowGraphs={setShowGraphs} />}

      {nameCohort !== '' && <h3>{nameCohort}</h3>}

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
      </div>

    </div>
  )
}

export default Cohorts