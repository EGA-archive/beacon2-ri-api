import './TableResultsVariant.css'
import { useState, useEffect } from 'react'

function TableResultsIndividuals (props) {
  const [resultsJSON, setResultsJSON] = useState([])
  const [results, setResults] = useState('')
  const [trigger, setTrigger] = useState(false)
  const [stringDataToCopy, setStringDataToCopy] = useState('')

  const copyData = e => {

    navigator.clipboard
    .writeText(stringDataToCopy)
    .then(() => {
      alert("successfully copied");
    })
    .catch(() => {
      alert("something went wrong");
    });
    console.log('COPY DONE')
  }

  useEffect(() => {
    console.log(props.results)
    props.results.forEach((element, index) => {
      console.log(element)
      //    element.forEach(element2 => {
      //    console.log(element2)
      // element2[1].results.forEach(element3 => {
      // resultsJSON.push([
      // element2[0],
      //JSON.stringify(element3, null, 2).replace('[', '').replace(']', '')
      //])
      resultsJSON.push([
        element[0],
        JSON.stringify(element[1], null, 2).replace('[', '').replace(']', '')
      ])
    })
    setTrigger(true)
    console.log(resultsJSON)
    setStringDataToCopy(resultsJSON)
  }, [])

  return (
    <div className='containerVariants'>
      {trigger === true && (
        <div className='copyDivVariants'>
          <button className='buttonCopy' onClick={copyData}>
            <h7>COPY ALL RESULTS</h7>
            <img className='copyLogo' src='../copy.png' alt='copyIcon'></img>
          </button>
        </div>
      )}
      {trigger === true &&
        resultsJSON.map(element => {
          return (
            <pre className='resultsVariants'>
              <p>{element[1]}</p>
            </pre>
          )
        })}
    </div>
  )
}

export default TableResultsIndividuals
