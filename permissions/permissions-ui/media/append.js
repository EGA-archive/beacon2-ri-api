$('#datasets').on('change', function() {

    var val = $(this).val(),
      text = $(this).find("option:selected").text();
  
    $('#list').append(new Option(text, val));
  
  });