import React from 'react'

const FilterContent = ({
  filters,
  handleOption,
  handleOptionAlphanum,
  handleInputChange,
  inputValues,
  checkedOptions,
  activeTab
}) => {
  return (
    <div className='filterTermsContainer'>
      {filters.map((filter, filterIndex) => (
        <div
          key={filterIndex}
          className={`divFilter ${
            filter.title === 'Variant' ? 'divFilterVariant' : ''
          }`}
        >
          <p>{filter.title}</p>
          <ul>
            {filter.options.map((optionsArray, optionIndex) => (
              <div key={optionIndex}>
                {filter.title === 'Variant' &&
                optionsArray.length > 0 &&
                optionsArray[0].type !== 'alphanumeric' ? (
                  <div className='containerExamplesVariant'>
                    {optionsArray.map((element, elementIndex) => (
                      <React.Fragment key={elementIndex}>
                        <div className='divKey'>
                          {elementIndex === 0 && (
                            <input
                              type='checkbox'
                              onClick={e =>
                                handleOption(
                                  e,
                                  optionsArray,
                                  optionIndex,
                                  activeTab
                                )
                              }
                              id={`option-${filterIndex}-${optionIndex}-${element.label}`}
                              name='subscribe2'
                              value={JSON.stringify(optionsArray)}
                              data-filter-index={filterIndex}
                              data-option-index={optionIndex}
                              data-element-label={element.label} // Add data attribute for element label
                              className='inputExamples'
                              checked={
                                checkedOptions[
                                  `option-${filterIndex}-${optionIndex}-${element.label}`
                                ] || false
                              }
                            />
                          )}
                          {element.subTitle && (
                            <label className='subTitle'>
                              {element.subTitle}
                            </label>
                          )}
                        </div>
                        <div className='containerExamplesDiv2'>
                          {!element.subTitle2 ? (
                            <div className='label-ontology-div'>
                              <label className='label'>{element.label}</label>
                              <label className='onHover'>
                                {element.ontology}
                              </label>
                            </div>
                          ) : filter.type === 'input' ? (
                            <div className='label-ontology-div2'>
                              <label>{element.subTitle2}</label>
                              <input
                                type='text'
                                className='label'
                                value={
                                  inputValues[
                                    `${optionIndex}-${element.label}-${element.schemaField}`
                                  ] || ''
                                }
                                onChange={e =>
                                  handleInputChange(
                                    e,
                                    `${optionIndex}-${element.label}-${element.schemaField}`,
                                    activeTab
                                  )
                                }
                              />
                            </div>
                          ) : (
                            <div className='label-ontology-div2'>
                              <label>{element.subTitle2}</label>
                              <label className='label'>{element.label}</label>
                              <label className='onHover'>
                                {element.ontology}
                              </label>
                            </div>
                          )}
                        </div>
                      </React.Fragment>
                    ))}
                  </div>
                ) : optionsArray.length > 0 &&
                  optionsArray[0].type === 'alphanumeric' ? (
                  <div>
                    <button
                      className='alphanumButton'
                      onClick={() =>
                        handleOptionAlphanum(
                          optionsArray[0].schemaField,
                          optionsArray[0].value
                        )
                      }
                    >
                      <img
                        className='formula'
                        src='/../formula.png'
                        alt='formula'
                      />
                      {optionsArray[0].label}
                    </button>
                  </div>
                ) : (
                  <div className='containerExamples1'>
                    {optionsArray.map((element, elementIndex) => (
                      <div key={elementIndex}>
                        <input
                          type='checkbox'
                          onClick={e =>
                            handleOption(
                              e,
                              optionsArray,
                              optionIndex,
                              activeTab
                            )
                          }
                          id={`option-${filterIndex}-${optionIndex}-${element.label}`}
                          name='subscribe'
                          value={element.value}
                          data-filter-index={filterIndex}
                          data-option-index={optionIndex}
                          data-element-label={element.label} // Add data attribute for element label
                          checked={
                            checkedOptions[
                              `option-${filterIndex}-${optionIndex}-${element.label}`
                            ] || false
                          }
                        />
                        <div className='containerExamplesDiv2'>
                          {element.subTitle && (
                            <label>{element.subTitle}</label>
                          )}
                          {!element.subTitle2 ? (
                            <div className='label-ontology-div'>
                              <label className='label'>{element.label}</label>
                              <label className='onHover'>
                                {element.ontology}
                              </label>
                            </div>
                          ) : filter.type === 'input' ? (
                            <div className='label-ontology-div2'>
                              <label>{element.subTitle2}</label>
                              <input
                                type='text'
                                className='label'
                                value={
                                  inputValues[
                                    `${optionIndex}-${element.label}-${element.schemaField}`
                                  ] || ''
                                }
                                onChange={e =>
                                  handleInputChange(
                                    e,
                                    `${optionIndex}-${element.label}-${element.schemaField}`,
                                    activeTab
                                  )
                                }
                              />
                              <label className='onHover'>
                                {element.ontology}
                              </label>
                            </div>
                          ) : (
                            <div className='label-ontology-div2'>
                              <label>{element.subTitle2}</label>
                              <label className='label'>{element.label}</label>
                              <label className='onHover'>
                                {element.ontology}
                              </label>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}

export default FilterContent
