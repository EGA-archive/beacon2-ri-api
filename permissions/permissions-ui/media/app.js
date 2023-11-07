const btnAdd = document.querySelector('#btnAdd');
const btnRemove = document.querySelector('#btnRemove');
const listbox = document.querySelector('#list');
const framework = document.querySelector('#framework');

btnAdd.onclick = (e) => {
  e.preventDefault();

  // validate the option
  if (framework.value == '') {
    alert('Please enter the name.');
    return;
  }
  // create a new option
  console.log(framework.value)
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