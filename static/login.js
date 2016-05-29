$(function() {

    $("input,textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function($form, event) {
            event.preventDefault(); // prevent default submit behaviour
            // get values from FORM
            var email = $("input#email").val();
            var password = $("input#password").val();

            $.ajax({
                url: "/login",
                type: "POST",
                data: {
                    email: email,
                    password: password,
                },
                cache: false,
                success: function(jsondata) {
                    if(jsondata['login']) {
                        window.location = '/begin';
                    }
                    else {
                        $('#success').html("<div class='alert alert-danger'>");
                        $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                            .append("</button>");
                        $('#success > .alert-danger')
                            .append("<strong>Incorrect username password combination.</strong>");
                        $('#success > .alert-danger')
                            .append('</div>');
                        //clear all fields
                        $('#contactForm').trigger("reset");
                    };
                },
                error: function() {
                    // Fail message
                    $('#success').html("<div class='alert alert-danger'>");
                    $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#success > .alert-danger').append("<strong>Sorry " + firstName + ", the server is not responding right now. Please try again later!");
                    $('#success > .alert-danger').append('</div>');
                    //clear all fields
                    $('#contactForm').trigger("reset");
                },
            })
        },
        filter: function() {
            return $(this).is(":visible");
        },
    });

    $("a[data-toggle=\"tab\"]").click(function(e) {
        e.preventDefault();
        $(this).tab("show");
    });
});


/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
    $('#success').html('');
});
