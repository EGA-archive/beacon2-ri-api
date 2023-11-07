const btnAdd2 = document.querySelector('#btnAdd2');
const btnRemove = document.querySelector('#btnRemove');
const datasets = document.querySelector('#list_datasets');
const framework = document.querySelector('#framework');
btnAdd2.onclick = (e) => {
    e.preventDefault();
  
    // validate the option
    let selected = [];
  
    for (let i = 0; i < datasets.options.length; i++) {
      selected[i] = datasets.options[i].selected;
      if (datasets.options[i].selected == true){
          selected[i] = datasets.options[i].value
      }
    }
  
  
    for (let i = 0; i < selected.length; i++) {
      console.log(selected[i])
      const option = new Option(selected[i], selected[i]);
      option.setAttribute('selected', 'selected');
      // add it to the list
      listbox.add(option, undefined);
    }
    // create a new option

    if (framework.value == '') {
        alert('Please enter the name.');
        return;
      }
      
      // create a new option
      const option = new Option(framework.value, framework.value);
      option.setAttribute('selected', 'selected');
      // add it to the list
      listbox.add(option, undefined);
    
      // reset the value of the input
      framework.value = '';
      framework.focus();
  
  
  
  };

// remove selected option
btnRemove.onclick = (e) => {
  e.preventDefault();

  // save the selected options
  let selected = [];

  for (let i = 0; i < listbox.options.length; i++) {
    selected[i] = listbox.options[i].selected;
  }

  // remove all selected option
  let index = listbox.options.length;
  while (index--) {
    if (selected[index]) {
      listbox.remove(index);
    }
  }
};