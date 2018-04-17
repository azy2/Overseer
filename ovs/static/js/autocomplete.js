$(document).ready(function() {
  var emails = [];

  function getResidentEmails() {
    $.ajax({
        method: 'get',
        url: '/manager/get_residents/',
        success: function (data) {
            for (var i = 0; i < data.length; i++) {
              emails.push(data[i]);
            }
		}
    });
  }

  getResidentEmails();

  $( "#add_form-recipient_email,#email" ).autocomplete({
    source: emails
  });
});
