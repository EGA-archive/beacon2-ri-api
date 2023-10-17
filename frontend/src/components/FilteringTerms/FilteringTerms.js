import { useState, useEffect } from 'react'
import './FilteringTerms.css'
import { TagBox } from 'react-tag-box'

function FilteringTerms (props) {
  console.log(props)

  const [error, setError] = useState(false)

  const [checked, setChecked] = useState(false)

  const [counter, setCounter] = useState(0)

  const [selected, setSelected] = useState([])

  const [tags, setTags] = useState([])

  const [alphaNumSection, setAlphanum] = useState(false)

  const [results, setResults] = useState('')

  const [state, setstate] = useState({
    query: '',
    list:
      props.filteringTerms !== false
        ? props.filteringTerms.data.response.filteringTerms
        : 'error'
  })

  const [trigger, setTrigger] = useState(false)

  const remove = tag => {
    setSelected(selected.filter(t => t.value !== tag.value))

    let inputs = document.getElementsByClassName('select-checkbox')
    inputs = Array.from(inputs)
    inputs.forEach(element => {
      if (tag.value === element.value) {
        element.checked = false
      }
    })

    props.filteringTerms.data.response.filteringTerms.forEach(element => {
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
    console.log()
  }

  const [valueChosen, setValueChosen] = useState([])

  const handdleInclude = e => {
    console.log(ID)
    console.log(valueFree)
    console.log(operator)
    if (ID !== '' && valueFree !== '' && operator !== '') {
      console.log('hola')
      if (props.query !== null) {
        props.setQuery(props.query + ',' + `${ID}${operator}${valueFree}`)
      }
      if (props.query === null) {
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

    console.log(state.list)
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

    console.log(tags)

    //selected.push(state.list[0].id)

    // setSelected(selected)
    // setTags(state.list)
  }, [props.filteringTerms, trigger])

  const handleChange = e => {
    const results = props.filteringTerms.data.response.filteringTerms.filter(
      post => {
        console.log(post)
        if (e.target.value === '') {
          return props.filteringTerms.data.response.filteringTerms
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
      }
    )
    setstate({
      //query: e.target.value,
      list: results
    })

    setResults(results)
  }

  const handleChange2 = e => {
    const results = props.filteringTerms.data.response.filteringTerms.filter(
      post => {
        console.log(post)
        if (post.label !== '' && post.label !== undefined) {
          if (e.target.value === '') {
            return props.filteringTerms.data.response.filteringTerms
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
      }
    )
    setstate({
      list: results
    })
  }

  const handleChange3 = e => {
    const results = props.filteringTerms.data.response.filteringTerms.filter(
      post => {
        console.log(post)
        if (e.target.value === '') {
          return props.filteringTerms.data.response.filteringTerms
        } else {
          if (post.type !== undefined) {
            if (
              post.type.toLowerCase().includes(e.target.value.toLowerCase())
            ) {
              return post
            }
          } else {
            if (
              post.type.toLowerCase().includes(e.target.value.toLowerCase())
            ) {
              return post
            }
          }
        }
      }
    )
    setstate({
      list: results
    })
  }

  const handleChange4 = e => {
    const results = props.filteringTerms.data.response.filteringTerms.filter(
      post => {
        console.log(post)
        if (e.target.value === '') {
          return props.filteringTerms.data.response.filteringTerms
        } else {
          if (post.scopes !== undefined) {
            var returnedPosts = []
            post.scopes.forEach(element => {
              if (
                element.toLowerCase().includes(e.target.value.toLowerCase())
              ) {
                returnedPosts.push(post)
              }
            })
            if (returnedPosts.length > 0) {
              return returnedPosts
            }
          } else if (post.scope !== undefined) {
            var returnedPosts = []
              if (
                post.scope.toLowerCase().includes(e.target.value.toLowerCase())
              ) {
                returnedPosts.push(post)
              }
            
            if (returnedPosts.length > 0) {
              return returnedPosts
            }
          }
        }
      }
    )
    setstate({
      list: results
    })
  }

  const handleCheck = e => {
    console.log(e.target.value)
    let infoValue = e.target.value.split(',')
    console.log(infoValue[2])
    if (infoValue[1].toLowerCase() !== 'alphanumeric') {
      const alreadySelected = selected.filter(
        term => term.label === infoValue[0]
      )

      if (alreadySelected.length !== 0) {
        setSelected(selected.filter(t => t.value !== infoValue[0]))
      } else {
        //     for (let i = 0; i < tags.length; i++) {

        //   console.log(tags[i])

        //   if (tags[i].label === e.target.value) {

        const newTag = {
          label: infoValue[0],
          value: infoValue[0]
        }
        console.log(newTag)
        selected.push(newTag)

        //     }
        console.log(selected)
        //      }
      }

      if (props.query !== null) {
        let stringQuery = ''
        if (props.query.includes(',')) {
          let arrayTerms = props.query.split(',')
          arrayTerms.forEach(element => {
            if (element === infoValue[0]) {
              stringQuery = props.query
            } else {
              stringQuery = props.query + ',' + infoValue[0]
            }
          })

          if (stringQuery === '' || stringQuery === ',') {
            props.setQuery('filtering term comma-separated, ID><=value')
          } else {
            props.setQuery(stringQuery)
          }
        } else {
          if (infoValue[0] !== props.query && props.query !== '') {
            stringQuery = `${props.query},` + infoValue[0]
            props.setQuery(stringQuery)
          } else if (infoValue[0] !== props.query && props.query === '') {
            stringQuery = `${props.query}` + infoValue[0]
            props.setQuery(stringQuery)
          }
        }
      } else {
        let stringQuery = infoValue[0]
        props.setQuery(stringQuery)
      }

      console.log(state.list)
      const filteredItems = state.list.filter(item => item.id !== infoValue[0])
      e.target.checked = false

      setstate({
        query: '',
        list: filteredItems
      })
      setTrigger(true)
      console.log(state.list)
    }
  }

  const handleCheck2 = e => {
    console.log(e.target)
    console.log(e.target.value)
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

  console.log(state.list)
  return (
    <div className='generalContainer'>
      <TagBox
        tags={state.list}
        selected={selected}
        backspaceDelete={true}
        removeTag={remove}
      />
      {error && (
        <h3>No filtering terms available. Please check your connection</h3>
      )}

      {!error && (
        <div className='tableWrapper'>
          <table id='table'>
            <thead className='thead1'>
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
                      className='searchTermInput1'
                      type='search'
                      value={state.query}
                      onChange={handleChange}
                      placeholder='Search term'
                    />
                  </form>
                </th>
              </tr>
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
                      onChange={handleChange2}
                      placeholder='Search label'
                    />
                  </form>
                </th>
              </tr>
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
            </thead>
            <thead className='thead2'>
              <tr>
                <th className='th4'>term</th>
                <th className='th5'>label</th>
                <th className='th6'>type</th>
                <th className='th7'>scopes</th>
              </tr>
            </thead>
            {props.filteringTerms.data !== undefined &&
              state.list !== 'error' &&
              state.list.map((term, index) => {
                return (
                  <>
                    <tbody>
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
                                value={[term.id, term.type, index]}
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

                          <td className='th3'>{term.type}</td>

                          <td className='th1'>
                            {term.scopes !== undefined &&
                              term.scopes.map((term2, index) => {
                                return index < term.scopes.length - 1
                                  ? term2 + '' + ','
                                  : term2 + ''
                              })}
                            {term.scopes === undefined && term.scope}
                          </td>
                        </tr>
                      )}
                      {index % 2 == !0 && (
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
                                value={[term.id, term.type, index]}
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

                          <td className='th3'>{term.type}</td>

                          <td className='th1'>
                            {term.scopes !== undefined &&
                              term.scopes.map((term2, index) => {
                                return index < term.scopes.length - 1
                                  ? term2 + '' + ','
                                  : term2 + ''
                              })}
                            {term.scopes === undefined && term.scope}
                          </td>
                        </tr>
                      )}

                      {index % 2 == !0 &&
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
                                onClick={handdleInclude}
                              >
                                Include
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
                                onClick={handdleInclude}
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
        </div>
      )}
    </div>
  )
}

export default FilteringTerms
