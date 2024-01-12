$("#signinForm").submit(function () {

    alert('hello')
    var data = $(this).serializeArray();
    alert('hii')
    $.ajax({
        url: $(this).attr('action'),
        headers: {
            "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
        },
        method: "POST",
        data: data,
        async:true,
        beforeSend: function () {
            $("#signbtn").attr("disabled", "disabled");
        },
        success: function (response) {
            if (response.result == 'success') {
                alert('succceess')
            }
            else {
                $("#forget-password-email-div").html(response.template)
                $("#id_email-error").html(response.message)
                $("#id_email-error").css('display', 'block')
            }
        },
        complete: function () {
            $("#signbtn").attr("disabled", false);
            $("#signbtn").html("Verify");
            button = false
        },
    })


    return false
});