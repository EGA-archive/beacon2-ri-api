import './TableResultsVariant.css'
import '../IndividualsResults/TableResultsIndividuals.css'
import '../../Dataset/BeaconInfo'
import * as React from 'react'
import { useState, useEffect } from 'react'
import CrossQueries from '../../CrossQueries/CrossQueries'
import { FaBars, FaEye, FaEyeSlash } from 'react-icons/fa' // Import icons from react-icons library
import { FiLayers, FiDownload } from 'react-icons/fi'

function TableResultsVariants (props) {
  const [showDatsets, setShowDatasets] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [resultsSelected, setResultsSelected] = useState(props.results)
  const [arrayBeaconsIds, setArrayBeaconsIds] = useState([])
  const [errorMessage, setErrorMessage] = useState('')
  const [resultsSelectedFinal, setResultsSelectedFinal] = useState([])
  const [editable, setEditable] = useState([])
  const [trigger, setTrigger] = useState(false)
  const [trigger2, setTrigger2] = useState(false)
  const [exportMenuVisible, setExportMenuVisible] = useState(false)
  const [showCrossQuery, setShowCrossQuery] = useState(false)
  const [parameterCrossQuery, setParamCrossQuery] = useState('')
  const [expandedRows, setExpandedRows] = useState(
    new Array(props.beaconsList.length).fill(false)
  )
  const [currentPage, setCurrentPage] = useState(1)
  const [rowsPerPage] = useState(10) // You can make this dynamic if needed

  const [filteredData, setFilteredData] = useState(editable)

  const indexOfLastRow = currentPage * rowsPerPage
  const indexOfFirstRow = indexOfLastRow - rowsPerPage
  const currentRows = filteredData.slice(indexOfFirstRow, indexOfLastRow)

  const totalPages = Math.ceil(filteredData.length / rowsPerPage)

  const [note, setNote] = useState('')
  const [isOpenModal2, setIsOpenModal2] = useState(false)

  const [filterValues, setFilterValues] = useState({
    IndividualId: '',
    ethnicity: '',
    Beacon: '',
    interventionsOrProcedures: '',
    sex: '',
    diseases: '',
    treatments: '',
    phenotypicFeatures: ''
    // Add other column names here
  })

  const [menuVisible, setMenuVisible] = useState(false)

  const toggleMenu = () => {
    setMenuVisible(prevState => !prevState)
  }

  const [columnVisibility, setColumnVisibility] = useState({
    IndividualId: true,
    ethnicity: true,
    Beacon: true,
    interventionsOrProcedures: true,
    sex: true,
    diseases: true,
    treatments: true,
    phenotypicFeatures: true
    // Add more columns as needed
  })
  const handleNextPage = () => {
    setCurrentPage(prevPage => Math.min(prevPage + 1, totalPages))
  }

  const handlePreviousPage = () => {
    setCurrentPage(prevPage => Math.max(prevPage - 1, 1))
  }

  const handlePageClick = pageNumber => {
    setCurrentPage(pageNumber)
  }

  const getPages = () => {
    const pages = []
    const maxDisplayedPages = 5
    const totalVisiblePages = maxDisplayedPages + 4 // Total number of buttons (first, last, current range, and ellipses)

    if (totalPages <= totalVisiblePages) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      const startRange = Math.max(2, currentPage - 2)
      const endRange = Math.min(totalPages - 1, currentPage + 2)

      pages.push(1)
      if (startRange > 2) pages.push('...')
      for (let i = startRange; i <= endRange; i++) {
        pages.push(i)
      }
      if (endRange < totalPages - 1) pages.push('...')
      pages.push(totalPages)
    }

    return pages
  }

  const showAllColumns = () => {
    const columns = document.querySelectorAll('th')
    const rows = document.querySelectorAll('td')

    // Update column visibility state and remove hidden class for all columns
    columns.forEach(column => {
      column.classList.remove('hidden')
      const columnName = column.dataset.columnName
      setColumnVisibility(prevState => ({
        ...prevState,
        [columnName]: true
      }))
    })

    // Change the icon of all rows to the normal eye
    rows.forEach(row => {
      row.classList.remove('hidden')
    })

    setColumnVisibility(prevState => {
      const updatedVisibility = {}
      Object.keys(prevState).forEach(column => {
        updatedVisibility[column] = true
      })
      return updatedVisibility
    })
  }

  const toggleColumnVisibility = columnName => {
    const columns = document.querySelectorAll('th[data-column-name]')
    const rows = document.querySelectorAll(
      `td[data-column-name="${columnName}"]`
    )

    columns.forEach(column => {
      if (column.dataset.columnName === columnName) {
        column.classList.toggle('hidden')
      }
    })

    rows.forEach(row => {
      row.classList.toggle('hidden')
    })

    setColumnVisibility(prevVisibility => ({
      ...prevVisibility,
      [columnName]: !prevVisibility[columnName]
    }))
  }

  const handleFilterChange = (e, columnName) => {
    const { value } = e.target
    setFilterValues({ ...filterValues, [columnName]: value })

    const updatedFilteredData = editable.filter(row =>
      row[columnName].toLowerCase().includes(value.toLowerCase())
    )

    setFilteredData(updatedFilteredData)
  }

  const toggleExportMenu = () => {
    setExportMenuVisible(prevState => !prevState)
  }

  const exportToCSV = () => {
    // Ensure props.results is not null or undefined
    if (!props.results) return

    // Get all keys from the first row of props.results
    const header = Object.keys(props.results[0])

    // Convert each row to CSV format
    const csv = [
      header.join(','), // Header row
      ...props.results.map(row =>
        header
          .map(fieldName => {
            const value = row[fieldName]
            // Check if the value is an object
            if (typeof value === 'object') {
              // Stringify the object
              return JSON.stringify(value)
            } else {
              // Otherwise, return the value as is
              return value
            }
          })
          .join(',')
      )
    ].join('\n')

    // Create a blob object from the CSV content
    const blob = new Blob([csv], { type: 'text/csv' })

    // Create a URL for the blob object
    const url = window.URL.createObjectURL(blob)

    // Create a temporary <a> element to trigger the download
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'exported_data.csv')

    // Programmatically click the link to start the download
    document.body.appendChild(link)
    link.click()

    // Clean up by revoking the URL and removing the temporary <a> element
    window.URL.revokeObjectURL(url)
    document.body.removeChild(link)
  }

  const exportToJSON = () => {
    // Ensure props.results is not null or undefined
    if (!props.results) return

    // Convert the results to JSON
    const jsonString = JSON.stringify(props.results, null, 2)

    // Create a blob object from the JSON content
    const blob = new Blob([jsonString], { type: 'application/json' })

    // Create a URL for the blob object
    const url = URL.createObjectURL(blob)

    // Create a temporary <a> element to trigger the download
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'exported_data.json')

    // Programmatically click the link to start the download
    document.body.appendChild(link)
    link.click()

    // Clean up by revoking the URL and removing the temporary <a> element
    URL.revokeObjectURL(url)
    document.body.removeChild(link)
  }

  const showNote = e => {
    setNote(e)
    setIsOpenModal2(true)
  }

  const handleShowCrossQuery = e => {
    setShowCrossQuery(true)
    console.log(e.target.innerText.trim())
    setParamCrossQuery(e.target.innerText)
  }
  const toggleRow = index => {
    setExpandedRows(prevState => {
      const currentIndex = prevState.indexOf(index)
      if (currentIndex === -1) {
        return [...prevState, index]
      } else {
        const updatedRows = [...prevState]
        updatedRows.splice(currentIndex, 1)
        return updatedRows
      }
    })
  }

  useEffect(() => {
    if (props.show === 'full') {
      setResultsSelectedFinal(resultsSelected)
      setShowResults(true)
      setShowDatasets(false)
      setTrigger(true)
    }

    if (resultsSelected.length === 0) {
      setErrorMessage('NO RESULTS')
    }
    resultsSelected.forEach((element, index) => {
      arrayBeaconsIds.push(element[0])
    })

    resultsSelectedFinal.forEach((element, index) => {
      if (element[1] !== undefined) {
        let variationJson = []
        if (element[1].variation !== '' && element[1].variation !== undefined) {
          variationJson = JSON.stringify(element[1].variation, null, 2)
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')

          variationJson = variationJson.toString()
          variationJson = variationJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          variationJson = variationJson.replaceAll(',', '')
        }

        let identifiersJson = []

        if (
          element[1].identifiers !== '' &&
          element[1].identifiers !== undefined
        ) {
          identifiersJson = JSON.stringify(element[1].identifiers, null, 2)
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')
          identifiersJson = identifiersJson.toString()
          identifiersJson = identifiersJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          identifiersJson = identifiersJson.replaceAll(',', '')
        }

        let molecularAttributesJson = []

        if (
          element[1].molecularAttributes !== '' &&
          element[1].molecularAttributes !== undefined
        ) {
          molecularAttributesJson = JSON.stringify(
            element[1].molecularAttributes,
            null,
            2
          )
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')
          molecularAttributesJson = molecularAttributesJson.toString()
          molecularAttributesJson = molecularAttributesJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          molecularAttributesJson = molecularAttributesJson.replaceAll(',', '')
        }

        let molecularEffectsJson = []

        if (
          element[1].molecularEffects !== '' &&
          element[1].molecularEffects !== undefined
        ) {
          molecularEffectsJson = JSON.stringify(
            element[1].molecularEffects,
            null,
            2
          )
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')
          molecularEffectsJson = molecularEffectsJson.toString()
          molecularEffectsJson = molecularEffectsJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          molecularEffectsJson = molecularEffectsJson.replaceAll(',', '')
        }

        let caseLevelDataJson = []

        if (
          element[1].caseLevelData !== '' &&
          element[1].caseLevelData !== undefined
        ) {
          caseLevelDataJson = JSON.stringify(element[1].caseLevelData, null, 2)
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')
          caseLevelDataJson = caseLevelDataJson.toString()
          caseLevelDataJson = caseLevelDataJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          caseLevelDataJson = caseLevelDataJson.replaceAll(',', '')
        }

        let variantLevelDataJson = []

        if (
          element[1].variantLevelData !== '' &&
          element[1].variantLevelData !== undefined
        ) {
          variantLevelDataJson = JSON.stringify(
            element[1].variantLevelData,
            null,
            2
          )
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')
          variantLevelDataJson = variantLevelDataJson.toString()
          variantLevelDataJson = variantLevelDataJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          variantLevelDataJson = variantLevelDataJson.replaceAll(',', '')
        }

        let frequencyInPopulationsJson = []

        if (
          element[1].frequencyInPopulations !== '' &&
          element[1].frequencyInPopulations !== undefined
        ) {
          frequencyInPopulationsJson = JSON.stringify(
            element[1].frequencyInPopulations,
            null,
            2
          )
            .replaceAll('[', '')
            .replaceAll(']', '')
            .replaceAll('{', '')
            .replaceAll('}', '')
            .replaceAll(',', '')
            .replaceAll(' ,', '')
            .replaceAll(', ', '')
            .replaceAll('"', '')
          frequencyInPopulationsJson = frequencyInPopulationsJson.toString()
          frequencyInPopulationsJson = frequencyInPopulationsJson
            .replaceAll(', ', ',')
            .replaceAll(' ,', ',')
          frequencyInPopulationsJson = frequencyInPopulationsJson.replaceAll(
            ',',
            ''
          )
        }

        editable.push({
          id: index,
          variantInternalId: element[1].variantInternalId,
          variation: variationJson,
          Beacon: element[0],
          identifiers: identifiersJson,
          molecularAttributes: molecularAttributesJson,
          molecularEffects: molecularEffectsJson,
          caseLevelData: caseLevelDataJson,
          variantLevelData: variantLevelDataJson,
          frequencyInPopulations: frequencyInPopulationsJson
        })

        if (index === resultsSelectedFinal.length - 1) {
          setTrigger2(true)
        }
      }
    })
  }, [trigger, resultsSelectedFinal])

  useEffect(() => {
    setShowDatasets(true)
  }, [])

  return (
    <div className='containerBeaconResults'>
      {showDatsets === true &&
        props.beaconsList.map(result => {
          return (
            <table className='tableGranularity'>
              <thead className='theadGranularity'>
                <tr id='trGranuHeader'>
                  <th className='thGranularityTitle'>Beacon</th>
                  <th className='thGranularityTitle'>Dataset</th>
                  <th className='thGranularityTitle'>Result</th>
                </tr>
              </thead>
              <tbody className='tbodyGranu'>
                {props.beaconsList.map((beacon, beaconIndex) => (
                  <React.Fragment key={beaconIndex}>
                    <tr
                      className='trGranuBeacon'
                      onClick={() => toggleRow(beaconIndex)}
                    >
                      <td className='tdGranu'>
                        {beacon.id}

                        {expandedRows.includes(beaconIndex) ? (
                          <ion-icon name='chevron-down-outline'></ion-icon>
                        ) : (
                          <ion-icon name='chevron-up-outline'></ion-icon>
                        )}
                      </td>
                    </tr>
                    {expandedRows.includes(beaconIndex) &&
                      props.resultsPerDataset &&
                      props.resultsPerDataset.map((element, index) => (
                        <React.Fragment key={`${beaconIndex}-${index}`}>
                          {index === beaconIndex &&
                            props.show === 'boolean' &&
                            element[1].map((booleanElement, booleanIndex) => (
                              <tr key={`boolean-${booleanIndex}`}>
                                <td className='tdGranu'></td>
                                <td
                                  className={`tdGranu ${
                                    booleanElement ? 'tdFound' : 'tdNotFound'
                                  }`}
                                >
                                  {element[0][booleanIndex]}
                                </td>
                                <td
                                  className={`tdGranu ${
                                    booleanElement
                                      ? 'tdFoundDataset'
                                      : 'tdNotFoundDataset'
                                  }`}
                                >
                                  {booleanElement ? 'YES' : 'No, sorry'}
                                </td>
                              </tr>
                            ))}
                          {index === beaconIndex &&
                            props.show === 'count' &&
                            element[2].map((countElement, countIndex) => (
                              <tr
                                className='trGranu'
                                key={`count-${countIndex}`}
                              >
                                <td className='tdGranu'></td>
                                <td
                                  className={`tdGranu ${
                                    countElement !== undefined &&
                                    countElement !== null &&
                                    countElement !== 0
                                      ? 'tdFoundDataset'
                                      : 'tdNotFoundDataset'
                                  }`}
                                >
                                  {element[0][countIndex]}
                                </td>
                                <td
                                  className={`tdGranu ${
                                    countElement !== undefined &&
                                    countElement !== null &&
                                    countElement !== 0
                                      ? 'tdFound'
                                      : 'tdNotFound'
                                  }`}
                                >
                                  {countElement}
                                </td>
                              </tr>
                            ))}
                        </React.Fragment>
                      ))}
                    {expandedRows.includes(beaconIndex) &&
                      props.resultsPerDataset.length === 0 &&
                      props.datasetList &&
                      props.datasetList.map((element, index) => {
                        if (index === beaconIndex) {
                          if (props.show === 'boolean') {
                            return (
                              <React.Fragment key={`boolean-${index}`}>
                                <tr key={`boolean-${index}`}>
                                  <td className='tdGranu'></td>
                                  <td className='tdGranu'>{element.name}</td>
                                  <td className='tdGranu'>No, sorry</td>
                                </tr>
                              </React.Fragment>
                            )
                          } else if (props.show === 'count') {
                            return (
                              <React.Fragment key={`count-${index}`}>
                                <tr className='trGranu' key={`count-${index}`}>
                                  <td className='tdGranu'></td>
                                  <td className='tdGranu'>{element.name}</td>
                                  <td className='tdGranu'>None</td>
                                </tr>
                              </React.Fragment>
                            )
                          }
                        }
                        return null
                      })}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          )
        })}

      {!showCrossQuery &&
        showDatsets === false &&
        showResults === true &&
        trigger2 === true && (
          <div className='table-container'>
            <div className='menu-icon-container'>
              <div className='export-menu'>
                <button className='exportButton' onClick={toggleExportMenu}>
                  <FiDownload />
                </button>
                {exportMenuVisible && (
                  <>
                    <ul className='column-list'>
                      <li onClick={exportToJSON}>Export to JSON</li>
                      <li onClick={exportToCSV}>Export to CSV</li>
                    </ul>
                  </>
                )}
              </div>
              <div className='menu-container'>
                <FaBars onClick={toggleMenu} />
                {menuVisible && (
                  <>
                    <ul className='column-list'>
                      <li onClick={showAllColumns}>
                        Show All Columns
                        <FiLayers />
                      </li>
                      {Object.keys(columnVisibility).map(column => (
                        <li
                          key={column}
                          onClick={() => toggleColumnVisibility(column)}
                        >
                          {column}
                          {columnVisibility[column] ? (
                            <FaEye />
                          ) : (
                            <FaEyeSlash />
                          )}
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            </div>
            <div className='header-container'>
              <table className='tableResults'>
                <thead className='theadResults'>
                  <tr>
                    <th
                      className={`sticky-header ${
                        columnVisibility.variantInternalId
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Variant ID</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('variantInternalId')
                        }
                      >
                        {columnVisibility.variantInternalId ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter Variant ID'
                        onChange={e =>
                          handleFilterChange(e, 'variantInternalId')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.variation ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Variation</span>
                      <button
                        onClick={() => toggleColumnVisibility('variation')}
                      >
                        {columnVisibility.variation ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter variation'
                        onChange={e => handleFilterChange(e, 'variation')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.Beacon ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Beacon</span>
                      <button onClick={() => toggleColumnVisibility('Beacon')}>
                        {columnVisibility.Beacon ? <FaEye /> : <FaEyeSlash />}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter Beacon'
                        onChange={e => handleFilterChange(e, 'Beacon')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.identifiers ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Identifiers</span>
                      <button
                        onClick={() => toggleColumnVisibility('identifiers')}
                      >
                        {columnVisibility.identifiers ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter identifiers'
                        onChange={e => handleFilterChange(e, 'identifiers')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.molecularAttributes
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Molecular Attributes</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('molecularAttributes')
                        }
                      >
                        {columnVisibility.molecularAttributes ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter molecular attributes'
                        onChange={e =>
                          handleFilterChange(e, 'molecularAttributes')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.molecularEffects ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Molecular Effects</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('molecularEffects')
                        }
                      >
                        {columnVisibility.molecularEffects ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter molecular effects'
                        onChange={e =>
                          handleFilterChange(e, 'molecularEffects')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.caseLevelData ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Case Level Data</span>
                      <button
                        onClick={() => toggleColumnVisibility('caseLevelData')}
                      >
                        {columnVisibility.caseLevelData ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter case level data'
                        onChange={e => handleFilterChange(e, 'caseLevelData')}
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.variantLevelData ? 'visible' : 'hidden'
                      }`}
                    >
                      <span>Variant Level Data</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('variantLevelData')
                        }
                      >
                        {columnVisibility.variantLevelData ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter variant level data'
                        onChange={e =>
                          handleFilterChange(e, 'variantLevelData')
                        }
                      />
                    </th>
                    <th
                      className={`sticky-header ${
                        columnVisibility.frequencyInPopulations
                          ? 'visible'
                          : 'hidden'
                      }`}
                    >
                      <span>Frequency In Populations</span>
                      <button
                        onClick={() =>
                          toggleColumnVisibility('frequencyInPopulations')
                        }
                      >
                        {columnVisibility.frequencyInPopulations ? (
                          <FaEye />
                        ) : (
                          <FaEyeSlash />
                        )}
                      </button>
                      <input
                        type='text'
                        placeholder='Filter frequency in populations'
                        onChange={e =>
                          handleFilterChange(e, 'frequencyInPopulations')
                        }
                      />
                    </th>

                    {/* Add more column headers here */}
                  </tr>
                </thead>
              </table>
            </div>
            <div className='body-container'>
              <table className='tableResults'>
                <tbody className='tbodyResults'>
                  {filteredData.map((row, index) => (
                    <tr key={index}>
                      <td
                        className={
                          columnVisibility.variantInternalId
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.variantInternalId}
                      </td>
                      <td
                        className={
                          columnVisibility.variation ? 'visible' : 'hidden'
                        }
                      >
                        {row.variation}
                      </td>
                      <td
                        className={
                          columnVisibility.Beacon ? 'visible' : 'hidden'
                        }
                      >
                        {row.Beacon}
                      </td>
                      <td
                        className={
                          columnVisibility.identifiers ? 'visible' : 'hidden'
                        }
                      >
                        {row.identifiers}
                      </td>
                      <td
                        className={
                          columnVisibility.molecularAttributes
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.molecularAttributes}
                      </td>
                      <td
                        className={
                          columnVisibility.molecularEffects
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.molecularEffects}
                      </td>
                      <td
                        className={
                          columnVisibility.caseLevelData ? 'visible' : 'hidden'
                        }
                      >
                        {row.caseLevelData}
                      </td>
                      <td
                        className={
                          columnVisibility.variantLevelData
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.variantLevelData}
                      </td>
                      <td
                        className={
                          columnVisibility.frequencyInPopulations
                            ? 'visible'
                            : 'hidden'
                        }
                      >
                        {row.frequencyInPopulations}
                      </td>

                      {/* Render other row cells here */}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      {props.show === 'full' && !showCrossQuery && (
        <div className='pagination-controls'>
          <button onClick={handlePreviousPage} disabled={currentPage === 1}>
            Previous
          </button>
          {getPages().map((page, index) =>
            typeof page === 'number' ? (
              <button
                key={index}
                onClick={() => handlePageClick(page)}
                className={currentPage === page ? 'active' : ''}
              >
                {page}
              </button>
            ) : (
              <span key={index} className='ellipsis'>
                {page}
              </span>
            )
          )}
          <button
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      )}
      {showCrossQuery && (
        <CrossQueries
          parameter={parameterCrossQuery}
          collection={'g_variants'}
          setShowCrossQuery={setShowCrossQuery}
        />
      )}
    </div>
  )
}

export default TableResultsVariants
