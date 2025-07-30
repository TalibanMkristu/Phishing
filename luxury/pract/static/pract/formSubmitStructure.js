async function submitForm(event) {
    // Prevent default form submission
    event.preventDefault();
    
    // Get the form element
    const form = document.getElementById('prac-form');
    
    // Create FormData object from the form
    const formData = new FormData(form);
    
    // Get CSRF token from the form
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    try {
        const response = await fetch('/api/submit-prac-form/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                // 'Content-Type': 'multipart/form-data', // Not needed - browser sets it automatically with FormData
            },
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        console.log('Success:', data);
        // Handle success (e.g., show success message, redirect, etc.)
    } catch (error) {
        console.error('Error:', error);
        // Handle error (e.g., show error message to user)
    }
}




document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prac-form');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Determine if this is an AJAX submission
        const isAjax = true; // Since we're using fetch
        
        // Create FormData object from the form
        const formData = new FormData(form);
        
        // For AJAX detection on server side
        if (isAjax) {
            formData.append('is_ajax', 'true');
        }
        
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        try {
            const response = await fetch(form.action || '/api/submit-prac-form/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest' // Another way to detect AJAX
                },
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Handle successful response
            console.log('Success:', data);
            alert('Form submitted successfully via AJAX!');
            
        } catch (error) {
            console.error('Error:', error);
            alert('Error submitting form!');
        }
    });
});



document.getElementById('prac-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    
    try {
        const response = await fetch(this.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        });
        
        // ... rest of the code remains the same ...
    } catch (error) {
        // ... error handling ...
    }
});