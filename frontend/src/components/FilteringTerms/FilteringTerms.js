import { useState, useEffect } from 'react'
import './FilteringTerms.css'
import { TagBox } from 'react-tag-box'

function FilteringTerms (props) {
  const [error, setError] = useState(false)

  const [checked, setChecked] = useState(false)

  const [counter, setCounter] = useState(0)

  const [selected, setSelected] = useState([])

  const [tags, setTags] = useState([])

  const [alphaNumSection, setAlphanum] = useState(false)

  const [results, setResults] = useState('')

  const [popUp, showPopUp] = useState(false)

  const [state, setstate] = useState({
    query: '',
    list: props.filteringTerms !== undefined ? props.filteringTerms : 'error'
  })

  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10 // Adjust the number of items per page
  const indexOfLastItem = currentPage * itemsPerPage
  const indexOfFirstItem = indexOfLastItem - itemsPerPage
  const currentItems = state.list.slice(indexOfFirstItem, indexOfLastItem)

  // Handle pagination controls
  const handlePreviousPage = () => {
    setCurrentPage(prevPage => Math.max(prevPage - 1, 1))
  }

  const handleNextPage = () => {
    setCurrentPage(prevPage => prevPage + 1)
  }

  const totalPages = Math.ceil(state.list.length / itemsPerPage)

  const [trigger, setTrigger] = useState(false)

  const [hide, setHide] = useState(true)
  const remove = tag => {
    setSelected(selected.filter(t => t.value !== tag.value))

    let inputs = document.getElementsByClassName('select-checkbox')
    inputs = Array.from(inputs)
    inputs.forEach(element => {
      if (tag.value === element.value) {
        element.checked = false
      }
    })

    props.filteringTerms.forEach(element => {
      if (element.id === tag.value) {
        state.list.unshift(element)
      }
    })

    setTrigger(true)

    if (props.query.includes(`,${tag.value}`)) {
      props.setQuery(props.query.replace(`,${tag.value}`, ''))
    } else if (props.query.includes(`${tag.value},`)) {
      props.setQuery(props.query.replace(`${tag.value},`, ''))
    } else if (props.query.includes(`${tag.value}`)) {
      props.setQuery(props.query.replace(`${tag.value}`, ''))
    } else {
      props.setQuery(props.query.replace(tag.value, ''))
      props.setQuery('filtering term comma-separated, ID><=value')
    }

    if (props.query === '') {
      props.setQuery('filtering term comma-separated, ID><=value')
    }
  }

  const handleIdChanges = e => {
    setId(e.target.value)
  }

  const handleOperatorchange = e => {
    setOperator(e.target.value)
  }

  const [valueChosen, setValueChosen] = useState([])

  const handleInclude = e => {
    if (ID !== '' && valueFree !== '' && operator !== '') {
      if (props.query !== null && props.query !== '') {
        props.setQuery(props.query + ',' + `${ID}${operator}${valueFree}`)
      }
      if (props.query === null || props.query === '') {
        props.setQuery(`${ID}${operator}${valueFree}`)
      }
    }
  }

  const [operator, setOperator] = useState('')
  const [valueFree, setValueFree] = useState('')
  const handleValueChanges = e => {
    setValueFree(e.target.value)
  }

  const [ID, setId] = useState('')

  useEffect(() => {
    if (state.list === 'error') {
      setError(true)
    } else {
      setError(false)
    }

    state.list.forEach((element, index) => {
      if (element.scopes.length > 1) {
        element.scopes.forEach(scope => {
          let arrayNew = { ...element }
          arrayNew['scopes'] = [scope]
          state.list.push(arrayNew)
        })

        // Mark the original element for deletion
        element.toBeDeleted = true
      }
    })

    // Remove the original elements with multiple scopes
    state.list = state.list.filter(element => !element.toBeDeleted)

    setstate({
      query: '',
      list: props.filteringTerms !== false ? state.list : 'error'
    })

    if (state.list !== 'error') {
      const sampleTags = state.list.map(t => ({
        label: t.id,
        value: t.id
      }))

      setTags(sampleTags)
    }
  }, [props.filteringTerms, trigger])

  const handleChange = e => {
    const results = props.filteringTerms.filter(post => {
      if (e.target.value === '') {
        return props.filteringTerms
      } else {
        if (post.id != undefined) {
          if (post.id.toLowerCase().includes(e.target.value.toLowerCase())) {
            return post
          }
        } else {
          if (post.id.toLowerCase().includes(e.target.value.toLowerCase())) {
            return post
          }
        }
      }
    })
    setstate({
      //query: e.target.value,
      list: results
    })

    setResults(results)
  }

  const handleChange2 = e => {
    const results = props.filteringTerms.filter(post => {
      if (post.label !== '' && post.label !== undefined) {
        if (e.target.value === '') {
          return props.filteringTerms
        } else {
          if (post.label !== undefined) {
            if (
              post.label.toLowerCase().includes(e.target.value.toLowerCase())
            ) {
              return post
            }
          }
        }
      }
    })
    setstate({
      list: results
    })
  }

  const handleChange3 = e => {
    const results = props.filteringTerms.filter(post => {
      if (e.target.value === '') {
        return props.filteringTerms
      } else {
        if (post.type !== undefined) {
          if (post.type.toLowerCase().includes(e.target.value.toLowerCase())) {
            return post
          }
        } else {
          if (post.type.toLowerCase().includes(e.target.value.toLowerCase())) {
            return post
          }
        }
      }
    })
    setstate({
      list: results
    })
  }

  const handleChange4 = e => {
    const results = props.filteringTerms.filter(post => {
      if (e.target.value === '') {
        return props.filteringTerms
      } else {
        if (post.scopes !== undefined) {
          var returnedPosts = []
          post.scopes.forEach(element => {
            if (element.toLowerCase().includes(e.target.value.toLowerCase())) {
              returnedPosts.push(post)
            }
          })
          if (returnedPosts.length > 0) {
            return returnedPosts
          }
        }
      }
    })
    setstate({
      list: results
    })
  }

  const handleCheck = e => {
    let infoValue = e.target.value.split(',')

    if (infoValue[2].toLowerCase() !== 'alphanumeric') {
      if (props.query !== null) {
        let stringQuery = ''
        if (props.query.includes(',')) {
          let arrayTerms = props.query.split(',')
          arrayTerms.forEach(element => {
            if (infoValue[1]) {
              if (element === `${infoValue[3]}=${infoValue[1]}`) {
                stringQuery = props.query
              } else {
                stringQuery =
                  props.query + ',' + `${infoValue[3]}=${infoValue[1]}`
              }
            } else {
              if (element === `${infoValue[3]}=${infoValue[0]}`) {
                stringQuery = props.query
              } else {
                stringQuery =
                  props.query + ',' + `${infoValue[3]}=${infoValue[0]}`
              }
            }
          })

          if (stringQuery === '' || stringQuery === ',') {
            props.setQuery('filtering term comma-separated, ID><=value')
          } else {
            props.setQuery(stringQuery)
          }
        } else {
          if (infoValue[1]) {
            if (
              `${infoValue[3]}=${infoValue[1]}` !== props.query &&
              props.query !== ''
            ) {
              stringQuery =
                `${props.query},` + `${infoValue[3]}=${infoValue[1]}`

              props.setQuery(stringQuery)
            } else if (
              `${infoValue[3]}=${infoValue[1]}` !== props.query &&
              props.query === ''
            ) {
              stringQuery = `${props.query}` + `${infoValue[3]}=${infoValue[1]}`
              props.setQuery(stringQuery)
            }
          } else {
            if (
              `${infoValue[3]}=${infoValue[0]}` !== props.query &&
              props.query !== ''
            ) {
              stringQuery =
                `${props.query},` + `${infoValue[3]}=${infoValue[0]}`
              props.setQuery(stringQuery)
            } else if (
              `${infoValue[3]}=${infoValue[0]}` !== props.query &&
              props.query === ''
            ) {
              stringQuery = `${props.query}` + `${infoValue[3]}=${infoValue[0]}`
              props.setQuery(stringQuery)
            }
          }
        }
      } else {
        if (infoValue[1]) {
          let stringQuery = `${infoValue[3]}=${infoValue[1]}`
          props.setQuery(stringQuery)
        } else {
          let stringQuery = `${infoValue[3]}=${infoValue[0]}`
          props.setQuery(stringQuery)
        }
      }
      const filteredItems = state.list.filter(item => item.id !== infoValue[0])
      e.target.checked = false

      setstate({
        query: '',
        list: filteredItems
      })
      setTrigger(true)
    }
  }

  const handleCheck2 = e => {
    if (e.target.checked === false) {
      let newValueChosen = valueChosen.filter(valor => valor !== e.target.value)
      setValueChosen(newValueChosen)
    } else {
      valueChosen.push(e.target.value)
      setId(e.target.value)
    }

    setstate({
      query: '',
      list: state.list
    })
  }

  return (
    <div className='generalContainer'>
      <TagBox
        tags={state.list}
        selected={selected}
        backspaceDelete={true}
        removeTag={remove}
      />

      <div>
        {!error && (
          <div className='tableWrapper'>
            <table id='table'>
              <thead className='thead2'>
                <tr>
                  <th className='th4'>term</th>
                  <th className='th5'>label</th>
                  {hide === false && <th className='th6'>type</th>}
                  <th className='th7'>scopes</th>
                </tr>
              </thead>
              <thead className='thead1'>
                <tr className='search-tr1'>
                  <th
                    className='search-box sorting'
                    tabIndex='0'
                    aria-controls='DataTables_Table_0'
                    rowSpan='1'
                    colSpan='2'
                    aria-sort='ascending'
                    aria-label=': activate to sort column descending'
                  >
                    <form className='inputTerm'>
                      <input
                        className='searchTermInput1'
                        type='search'
                        value={state.query}
                        onChange={handleChange}
                        placeholder='Search term'
                      />
                    </form>
                  </th>
                </tr>
                <tr className='search-tr2'>
                  <th
                    className='search-box sorting'
                    tabIndex='0'
                    aria-controls='DataTables_Table_0'
                    rowSpan='1'
                    colSpan='2'
                    aria-sort='ascending'
                    aria-label=': activate to sort column descending'
                  >
                    <form className='inputLabel'>
                      <input
                        className='searchTermInput'
                        type='search'
                        onChange={handleChange2}
                        placeholder='Search label'
                      />
                    </form>
                  </th>
                </tr>
                {hide === false && (
                  <tr className='search-tr'>
                    <th
                      className='search-box sorting'
                      tabIndex='0'
                      aria-controls='DataTables_Table_0'
                      rowSpan='1'
                      colSpan='2'
                      aria-sort='ascending'
                      aria-label=': activate to sort column descending'
                    >
                      <form>
                        <input
                          className='searchTermInput'
                          type='search'
                          onChange={handleChange3}
                          placeholder='Search by type'
                        />
                      </form>
                    </th>
                  </tr>
                )}
                {
                  <tr className='search-tr'>
                    <th
                      className='search-box sorting'
                      tabIndex='0'
                      aria-controls='DataTables_Table_0'
                      rowSpan='1'
                      colSpan='2'
                      aria-sort='ascending'
                      aria-label=': activate to sort column descending'
                    >
                      <form>
                        <input
                          className='searchTermInput'
                          type='search'
                          onChange={handleChange4}
                          placeholder='Search by scope'
                        />
                      </form>
                    </th>
                  </tr>
                }
              </thead>

              {props.filteringTerms !== undefined &&
                state.list !== 'error' &&
                currentItems.map((term, index) => {
                  return (
                    <>
                      <tbody key={index}>
                        {index % 2 === 0 && (
                          <tr className='terms1'>
                            {term.type.toLowerCase() !== 'alphanumeric' && (
                              <td className='th2'>
                                {' '}
                                <input
                                  className='select-checkbox'
                                  onClick={handleCheck}
                                  type='checkbox'
                                  id={term.id}
                                  name={term.id}
                                  value={[
                                    term.id,
                                    term.label,
                                    term.type,
                                    [term.scopes],
                                    index
                                  ]}
                                />
                                {term.id}
                              </td>
                            )}
                            {term.type.toLowerCase() === 'alphanumeric' && (
                              <td className='th2'>
                                {' '}
                                <input
                                  className='select-checkbox'
                                  onClick={handleCheck2}
                                  type='checkbox'
                                  id={term.id}
                                  name={term.id}
                                  value={term.id}
                                />
                                {term.id}
                              </td>
                            )}
                            {term.label !== '' ? (
                              <td className='th1'>{term.label}</td>
                            ) : (
                              <td className='th1'>-</td>
                            )}

                            {hide === false && (
                              <td className='th3'>{term.type}</td>
                            )}

                            <td className='th4'>
                              {Array.isArray(term.scopes) &&
                                term.scopes.map((term2, index) => {
                                  return index < term.scopes.length - 1
                                    ? term2 + '' + ','
                                    : term2 + ''
                                })}
                            </td>
                          </tr>
                        )}
                        {index % 2 !== 0 && (
                          <tr className='terms2'>
                            {term.type.toLowerCase() !== 'alphanumeric' && (
                              <td className='th2'>
                                {' '}
                                <input
                                  className='select-checkbox'
                                  onClick={handleCheck}
                                  type='checkbox'
                                  id={term.id}
                                  name={term.id}
                                  value={[
                                    term.id,
                                    term.label,
                                    term.type,
                                    [term.scopes],
                                    index
                                  ]}
                                />
                                {term.id}
                              </td>
                            )}
                            {term.type.toLowerCase() === 'alphanumeric' && (
                              <td className='th2'>
                                {' '}
                                <input
                                  className='select-checkbox'
                                  onClick={handleCheck2}
                                  type='checkbox'
                                  id={term.id}
                                  name={term.id}
                                  value={term.id}
                                />
                                {term.id}
                              </td>
                            )}
                            {term.label !== '' ? (
                              <td className='th1'>{term.label}</td>
                            ) : (
                              <td className='th1'>-</td>
                            )}

                            {hide === false && (
                              <td className='th3'>{term.type}</td>
                            )}

                            <td className='th4'>
                              {Array.isArray(term.scopes) &&
                                term.scopes.map((term2, index) => {
                                  return index < term.scopes.length - 1
                                    ? term2 + '' + ','
                                    : term2 + ''
                                })}
                            </td>
                          </tr>
                        )}

                        {index % 2 !== 0 &&
                          term.type.toLowerCase() === 'alphanumeric' &&
                          valueChosen.includes(term.id) && (
                            <tr className='terms2'>
                              <div className='alphanumContainer2'>
                                <div className='alphaIdModule'>
                                  <div className='listTerms'>
                                    <label>
                                      <h2>ID</h2>
                                    </label>

                                    <input
                                      className='IdForm'
                                      type='text'
                                      value={term.id}
                                      autoComplete='on'
                                      placeholder={'write and filter by ID'}
                                      onChange={handleIdChanges}
                                      aria-label='ID'
                                    />

                                    <div id='operator'>
                                      <select
                                        className='selectedOperator'
                                        onChange={handleOperatorchange}
                                        name='selectedOperator'
                                      >
                                        <option value=''> </option>
                                        <option value='='>= </option>
                                        <option value='<'>&lt;</option>
                                        <option value='>'>&gt;</option>
                                        <option value='!'>!</option>
                                        <option value='%'>%</option>
                                      </select>
                                    </div>

                                    <label id='value'>
                                      <h2>Value</h2>
                                    </label>
                                    <input
                                      className='ValueForm'
                                      type='text'
                                      autoComplete='on'
                                      placeholder={'free text/ value'}
                                      onChange={handleValueChanges}
                                      aria-label='Value'
                                    />
                                  </div>
                                </div>
                                <button
                                  className='buttonAlphanum'
                                  onClick={handleInclude}
                                >
                                  <ion-icon name='add-circle'></ion-icon>
                                </button>
                              </div>
                            </tr>
                          )}
                        {index % 2 === 0 &&
                          term.type.toLowerCase() === 'alphanumeric' &&
                          valueChosen.includes(term.id) && (
                            <tr className='terms1'>
                              <div className='alphanumContainer2'>
                                <div className='alphaIdModule'>
                                  <div className='listTerms'>
                                    <label>
                                      <h2>ID</h2>
                                    </label>

                                    <input
                                      className='IdForm'
                                      type='text'
                                      value={term.id}
                                      autoComplete='on'
                                      placeholder={'write and filter by ID'}
                                      onChange={handleIdChanges}
                                      aria-label='ID'
                                    />

                                    <div id='operator'>
                                      <select
                                        className='selectedOperator'
                                        onChange={handleOperatorchange}
                                        name='selectedOperator'
                                      >
                                        <option value=''> </option>
                                        <option value='='>= </option>
                                        <option value='<'>&lt;</option>
                                        <option value='>'>&gt;</option>
                                        <option value='!'>!</option>
                                        <option value='%'>%</option>
                                      </select>
                                    </div>

                                    <label id='value'>
                                      <h2>Value</h2>
                                    </label>
                                    <input
                                      className='ValueForm'
                                      type='text'
                                      autoComplete='on'
                                      placeholder={'free text/ value'}
                                      onChange={handleValueChanges}
                                      aria-label='Value'
                                    />
                                  </div>
                                </div>
                                <button
                                  className='buttonAlphanum'
                                  onClick={handleInclude}
                                >
                                  Include
                                </button>
                              </div>
                            </tr>
                          )}
                      </tbody>
                    </>
                  )
                })}
            </table>

            <div className='pagination'>
              <button className='buttonPaginationFilters' onClick={handlePreviousPage} disabled={currentPage === 1}>
                Previous
              </button>
              <span>
                Page {currentPage} of {totalPages}
              </span>
              <button
                onClick={handleNextPage}
                disabled={currentPage === totalPages}
                className='buttonPaginationFiltersNext'
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default FilteringTerms
