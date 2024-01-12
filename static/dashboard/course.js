

$(document).ready(function() {
    // Add new field
    $(".add-field").click(function() {
        var clone = $(".multi-field:first").clone(true);
        clone.find("input, textarea").val("");
        clone.appendTo(".multi-fields");
    });

    // Remove field
    $(".multi-fields").on("click", ".remove-field", function() {
        if ($(".multi-field").length > 1) {
            $(this).closest(".multi-field").remove();
        }
    });
});




$("#CourseForm").submit(function(event) {
    event.preventDefault();
    
    // // Create a new FormData object
    var formData = new FormData($("#CourseForm")[0]);

    // Append the course_image to the FormData
    var courseImageInput = $('#course_image')[0];
    if (courseImageInput.files.length > 0) {
        // Append the course_image to the FormData
        formData.append('course_image', courseImageInput.files[0]);
    };
    var url = $("#CourseForm").attr('action');

    $.ajax({
            url: url,
            method: "POST",
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            mimeType: "multipart/form-data",
            headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
            beforeSend: function () {
                $("#submit_btn").prop("disabled",true);
            },

            success: function (response) {
                var response = JSON.parse(response)
                if (response.status) {
                    alert(response)
                    $(".msg_desc").text(response.message)
                    $("#flash_message_success").attr("style", "display:block;")
                    setTimeout(function() {
                        $("#flash_message_success").attr("style", "display:none;")
                    }, 3500)
                    location.href = response.redirect_url;
                } else {
                    $(".msg_desc").text(response.message)
                    $("#flash_message_error").attr("style", "display:block;")
                    setTimeout(function () {
                        $("#flash_message_error").attr("style", "display:none;")
                    }, 3500)
                }
            },
            complete: function () {

            },
        });
    
});


function FilterCourse(page) {
    if (page === '') {
        page = $('#current_page').val(); 
    }
    var query = $('#filter_courses').val()
    $.ajax({
        url: '/courses/',
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {'page': page,'query': query,},
        beforeSend: function () { },
        success: function (response) {
            $('#course_table').html(response.template) 
            $('#course_pagination').html(response.pagination) 
        },
    });
}