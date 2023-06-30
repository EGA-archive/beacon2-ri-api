import { useState, useEffect } from "react"
import './FilteringTerms.css'
import { TagBox } from 'react-tag-box'


function FilteringTerms(props) {

    console.log(props)

    const [error, setError] = useState(false)

    const [checked, setChecked] = useState(false)

    const [counter, setCounter] = useState(0)

    const [selected, setSelected] = useState([])

    const [tags, setTags] = useState([])

    const [results, setResults] = useState('')

    const [state, setstate] = useState({
        query: '',
        list: props.filteringTerms !== false ? props.filteringTerms.data.response.filteringTerms : "error"
    })

    const [trigger, setTrigger] = useState(false)

    const remove = tag => {

        setSelected(selected.filter(t => t.value !== tag.value))

        let inputs = document.getElementsByClassName('select-checkbox');
        inputs = Array.from(inputs)
        inputs.forEach(element => {
            if (tag.value === element.value) {
                element.checked = false
            }

        });

        props.filteringTerms.data.response.filteringTerms.forEach(element => {
            if (element.id === tag.value) {
                state.list.unshift(element)
            }
        })


        setTrigger(true)

        if (props.query.includes(`,${tag.value}`)) {
            props.setQuery(props.query.replace(`,${tag.value}`, ""))
        } else if (props.query.includes(`${tag.value},`)) {
            props.setQuery(props.query.replace(`${tag.value},`, ""))
        } else if (props.query.includes(`${tag.value}`)) {
            props.setQuery(props.query.replace(`${tag.value}`, ""))
        } else {
            props.setQuery(props.query.replace(tag.value, ""))
            props.setQuery('filtering term comma-separated, ID><=value')
        }

        if (props.query === '') {
            props.setQuery('filtering term comma-separated, ID><=value')
        }
    }


    useEffect(() => {
        if (state.list === "error") {
            setError(true)
        } else {
            setError(false)
        }

        console.log(state.list)
        setstate({
            query: '',
            list: props.filteringTerms !== false ? state.list : "error"
        })


        if (state.list !== "error") {
            const sampleTags =
                state.list.map(t => ({
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


    const handleChange = (e) => {


        const results = props.filteringTerms.data.response.filteringTerms.filter(post => {
            console.log(post)
            if (e.target.value === "") {
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

        })
        setstate({
            //query: e.target.value,
            list: results
        })

        setResults(results)

    }

    const handleChange2 = (e) => {


        const results = props.filteringTerms.data.response.filteringTerms.filter(post => {
            console.log(post)
            if (post.label !== '' && post.label !== undefined) {
                if (e.target.value === '') {
                    return props.filteringTerms.data.response.filteringTerms
                } else {
                    if (post.label !== 'undefined') {
                        if (post.label.toLowerCase().includes(e.target.value.toLowerCase())) {
                            return post
                        }
                    } else {
                        if (post.label.toLowerCase().includes(e.target.value.toLowerCase())) {
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

    const handleChange3 = (e) => {


        const results = props.filteringTerms.data.response.filteringTerms.filter(post => {
            console.log(post)
            if (e.target.value === "") {
                return props.filteringTerms.data.response.filteringTerms
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



    const handleCheck = (e) => {

        const alreadySelected = selected.filter(term => term.label === e.target.value)

        if (alreadySelected.length !== 0) {

            setSelected(selected.filter(t => t.value !== e.target.value))
        } else {

       //     for (let i = 0; i < tags.length; i++) {

             //   console.log(tags[i])

             //   if (tags[i].label === e.target.value) {

                    const newTag = {
                        label: e.target.value,
                        value: e.target.value
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

                    if (element === e.target.value) {
                        stringQuery = props.query
                    } else {
                        stringQuery = props.query + ',' + e.target.value
                    }

                })

                if (stringQuery === '' || stringQuery === ',') {
                    props.setQuery('filtering term comma-separated, ID><=value')
                } else {

                    props.setQuery(stringQuery)
                }


            } else {
              
                if ((e.target.value !== props.query && props.query !== '')) {

                    stringQuery = `${props.query},` + e.target.value
                    props.setQuery(stringQuery)
                } else if ((e.target.value !== props.query && props.query === '')) {
                    stringQuery = `${props.query}` + e.target.value
                    props.setQuery(stringQuery)
                }
            }

        } else {
            let stringQuery = e.target.value
            props.setQuery(stringQuery)
        }


        console.log(state.list)
        const filteredItems = state.list.filter(item => item.id !== e.target.value)
        e.target.checked = false

        setstate({
            query: '',
            list: filteredItems
        })
        setTrigger(true)
        console.log(state.list)

    }

    console.log(state.list)



    return (
        <div className="generalContainer">
            <TagBox
                tags={state.list}
                selected={selected}
                backspaceDelete={true}
                removeTag={remove}

            />
            {error && <h3>No filtering terms available. Please check your connection</h3>}

            {!error && <div className="tableWrapper">

                <table className="table">
                    <thead className="thead1">
                        <tr className="search-tr">
                            <th className="search-box sorting" tabIndex="0" aria-controls="DataTables_Table_0" rowSpan="1" colSpan="2" aria-sort="ascending" aria-label=": activate to sort column descending"><form><input className="searchTermInput1" type="search" value={state.query} onChange={handleChange} placeholder="Search term" /></form></th>

                        </tr>
                        <tr className="search-tr">
                            <th className="search-box sorting" tabIndex="0" aria-controls="DataTables_Table_0" rowSpan="1" colSpan="2" aria-sort="ascending" aria-label=": activate to sort column descending"><form><input className="searchTermInput" type="search" value={state.query2} onChange={handleChange2} placeholder="Search label" /></form></th>

                        </tr>
                        <tr className="search-tr">
                            <th className="search-box sorting" tabIndex="0" aria-controls="DataTables_Table_0" rowSpan="1" colSpan="2" aria-sort="ascending" aria-label=": activate to sort column descending"><form><input className="searchTermInput" type="search" value={state.query3} onChange={handleChange3} placeholder="Search by type" /></form></th>

                        </tr>
                    </thead>
                    <thead className="thead2">
                        <tr>
                            <th className="th4">term</th>
                            <th className="th5">label</th>
                            <th className="th6">type</th>
                        </tr>
                    </thead>
                    {props.filteringTerms.data !== undefined && state.list !== "error" && state.list.map((term, index) => {
                        return (<>


                            <tbody>

                                {index % 2 === 0 && <tr className="terms1">
                                    <td className="th2"> {(term.type=== "ontology" || term.type === "custom") && <input className="select-checkbox" onClick={handleCheck} type="checkbox" id='includeTerm' name="term" value={term.id} />}
                                        {term.id}</td>
                                    {term.label !== '' ? <td className="th1">{term.label}</td> : <td className="th1">-</td>}
                                    <td className="th1">{term.type}</td>
                                </tr>}
                                {index % 2 == !0 && <tr className="terms2">
                                    <td className="th2"> {(term.type=== "ontology" || term.type === "custom") &&  <input className="select-checkbox" onClick={handleCheck} type="checkbox" id="includeTerm" name="term" value={term.id} />}
                                        {term.id}</td>
                                    {term.label !== '' ? <td className="th1">{term.label}</td> : <td className="th1">-</td>}
                                    <td className="th1">{term.type}</td>
                        
                                </tr>}


                            </tbody>

                        </>
                        )
                    })

                    }
                </table>
            </div>}
        </div>
    )
}

export default FilteringTerms