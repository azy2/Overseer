$(document).ready(function() {
  alert("P");
  var emails = ['resident@gmail.com','xyu37@illinois.edu'];

  $( "#add_form-recipient_email" ).autocomplete({
    source: emails
  });
});
