$(document).ready(function() {
    // Function to get CSRF token from cookies
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                return cookie.substring('csrftoken='.length, cookie.length);
            }
        }
        return null;
    }
    
    show_data()

    // Get data from the Django backend using a GET request
    function show_data() {
        const list_products = document.getElementById('list_products')
        list_products.innerHTML = "";
        $.ajax({
            url: '/api_links/',
            method: 'GET',
            contentType: 'application/json',
            success: function(data) {
                console.log('Data from GET request:', data);
                let dif_price=''
                for (let i = 0; i < data.length; i++) {
                    if (data[i].price_difference < 0 ){
                        dif_price = `<span class="text-danger">${data[i].price_difference }</span>`
                    }else{
                        dif_price=`<span class="text-success">${data[i].price_difference }</span>`
                    }
                    const item=`<div class="card m-3 shadow-lg p-3 mb-5 bg-body rounded" style="max-width: 100%">
                                    <div class="row g-0">
                                    <div class="col-md-4 col-sm-12 text-center">
                                        <img src="${data[i].img_url }" class="img-fluid rounded-start" alt="..."/>
                                    </div>
                                    <div class="col-md-8">
                                        <div class="card-header fw-bold fs-4">${data[i].name}</div>
                                        <div class="card-body d-flex flex-column justify-content-evenly">
                                        <ul>
                                            <li>
                                            <span class="fw-bold">Current Price ($): </span>
                                            <span> ${data[i].current_price }</span>
                                            </li>
                                            <li>
                                            <span class="fw-bold">Old Price ($): </span>
                                            <span> ${data[i].old_price }</span>
                                            </li>
                                            <li>
                                            <span class="fw-bold">Difference ($): </span>
                                            ${dif_price}
                                            </li>
                                            <li>
                                            <span class="fw-bold">Date: </span><span>${data[i].date}</span>
                                            </li>
                                        </ul>
                                        </div>
                                        <div class="card_footer d-flex justify-content-between">
                                        <a href="${data[i].url }" target="_blank" class="btn btn-link"
                                            >Go Link...</a
                                        >
                                        <form action="{% url 'delete_url' id=${data[i].id } %}" method="post">
                                            <button class="btn btn-danger" type="submit" id="{{ i.id }}">
                                            Delete
                                            </button>
                                        </form>
                                        </div>
                                    </div>
                                    </div>
                                </div>`
                    list_products.innerHTML += item;}
            },
            error: function(error) {
                console.error('Error in GET request:', error);
            }
        });
    }
    




    // Get the URL from the input field and send to the Django backend
    $('#addBtn').click(function() {
        const addUrlEndpoint = $('body').data('add-url');
        const csrfToken = getCSRFToken();

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
                console.log(`success: Add new product`);
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