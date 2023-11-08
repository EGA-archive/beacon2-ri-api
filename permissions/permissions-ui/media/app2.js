const btnAdd2 = document.querySelector('#btnAdd2');
const btnRemove = document.querySelector('#btnRemove');
const datasets = document.querySelector('#datasets');
const listbox2 = document.querySelector('#list');
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
      if (!selected[i] == false){
      const option = new Option(selected[i], selected[i]);
      option.setAttribute('selected', 'selected');
      // add it to the list
      listbox2.add(option, undefined);
      }
    }
    // create a new option

  
  
  };
// remove selected option
btnRemove.onclick = (e) => {
  e.preventDefault();
  // save the selected options
  let selected = [];

  for (let i = 0; i < listbox2.options.length; i++) {
    selected[i] = listbox2.options[i].selected;
  }

  // remove all selected option
  let index = listbox2.options.length;
  while (index--) {
    if (selected[index]) {
      listbox2.remove(index);
    }
  }
};