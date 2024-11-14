// script.js

function changeImage(src) {
    document.getElementById('mainImage').src = src;
}

$(document).ready(function() {
    $('.btn-custom').hover(
        function() {
            $(this).html('Commander');
        },
        function() {
            $(this).html('Commander');
        }
    );

    // Order button click handler
    $('#orderButton').click(function() {
        $('#orderModal').modal('show');
    });

    const submitButton = document.getElementById('submitOrder');
    const form = document.getElementById('orderForm');
    const loadingOverlay = document.getElementById('loadingOverlay');

    // Function to create and append error message
    function createErrorMessage(input, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-danger mt-1';
        errorDiv.textContent = message;
        input.parentNode.appendChild(errorDiv);
    }

    // Function to remove error styling and message
    function removeError(input) {
        input.style.borderColor = '';
        const errorDiv = input.parentNode.querySelector('.text-danger');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    // Add input event listeners to remove error styling when user types
    ['first_name', 'last_name', 'phone', 'location'].forEach(id => {
        const input = document.getElementById(id);
        input.addEventListener('input', function() {
            removeError(this);
        });
    });

    submitButton.addEventListener('click', function(e) {
        e.preventDefault();

        let isValid = true;

        // Validate each field
        ['first_name', 'last_name', 'phone', 'location'].forEach(id => {
            const input = document.getElementById(id);
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = 'red';
                removeError(input); // Remove any existing error message
                createErrorMessage(input, 'Ce champ est obligatoire.');
            } else {
                removeError(input);
            }
        });

        if (!isValid) {
            return;
        }

        // Create order object
        const orderData = {
            first_name: document.getElementById('first_name').value,
            last_name: document.getElementById('last_name').value,
            phone: document.getElementById('phone').value,
            location: document.getElementById('location').value,
            id_computer: "{{id_computer}}"
        };

        // Send data to the server
        loadingOverlay.style.display = 'flex'; // Show loading

        fetch("{% url 'process-order' %}", {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "success") {  // Corrected '=' to '===' for comparison
                $('#orderModal').modal('hide');
                form.reset();
                setTimeout(function() {
                    loadingOverlay.style.display = 'none';
                    window.location.href = "{% url 'success-order' %}";
                }, 3000);
            } else {
                setTimeout(function() {
                    loadingOverlay.style.display = 'none';
                    window.location.href = "{% url 'success-order' %}";
                }, 3000);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            setTimeout(function() {
                loadingOverlay.style.display = 'none';
                window.location.href = "{% url 'success-order' %}";
            }, 3000);
        });
    });
});