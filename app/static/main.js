$(document).ready(function() {
    $('#addBtn').click(function() {
        const addUrlEndpoint = $('body').data('add-url');
        const csrfToken = $('body').data('csrf-token');

        // Get the URL from the input field
        const url = $('#basic-url').val();

        // Send the URL to the Django backend using AJAX
        $.ajax({
            type: 'POST',
            url: addUrlEndpoint,
            data: {
                'url': url,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                // Handle the response from the backend (if needed)
                console.log(`success: ${response}`);
            },
            error: function(error) {
                console.log(`error: ${error}`);
            }
        });

        // Close the modal
        $('#exampleModal').modal('hide');
        $('#basic-url').val('');
    });
});