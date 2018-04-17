var csrftoken = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

$(document).ready(function() {
  var emails = [];

  function getResidentEmails() {
    $.ajax({
        method: 'post',
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
