const btnAdd2 = document.querySelector('#btnAdd2');
const btnRemove = document.querySelector('#btnRemove');
const datasets = document.querySelector('#datasets');
const listbox = document.querySelector('#list');
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