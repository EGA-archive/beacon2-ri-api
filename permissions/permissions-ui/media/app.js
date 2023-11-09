const btnAdd = document.querySelector('#btnAdd');
const listbox = document.querySelector('#userslist');
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