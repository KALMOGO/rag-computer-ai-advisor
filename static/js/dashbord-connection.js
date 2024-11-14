/**
 * 
 * PAge d'authentification
 */
function sendDataToServer(formData) {
  const url = LOGIN_URL; 
  
   fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': CSRF_TOKEN
          },
          body: JSON.stringify(formData)
      }).then(response => response.json())
      .then(data => {
        handleResponse(data);
      }).catch(error => {
        // console.log(error)
          handleError(error);
      });
}

function handleResponse(response) {
  window.location.href = INDEX_URL;
}
   // Handle errors
function handleError(error) {
    showError(error.message, error.tryTime);
}

// Show error message
function showMessageError(message) {
    // Create the error container if it doesn't exist
    let errorContainer = document.getElementById('error-container');
    if (!errorContainer) {
        errorContainer = document.createElement('div');
        errorContainer.id = 'error-container';
        errorContainer.style.position = 'fixed';
        errorContainer.style.top = '20px';
        errorContainer.style.right = '20px';
        errorContainer.style.zIndex = '1000';
        document.body.appendChild(errorContainer);
    }

    // Create the error message div
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger';
    errorDiv.style.minWidth = '250px';
    errorDiv.style.marginBottom = '10px';
    errorDiv.textContent = message;

    // Add the error to the container
    errorContainer.appendChild(errorDiv);

    // Remove the error after 3 seconds
    setTimeout(() => {
        errorDiv.remove();
        // Remove container if it's empty
        if (!errorContainer.hasChildNodes()) {
            errorContainer.remove();
        }
    }, 3000);
}
function showError(message, tryTime=1) {
    if (tryTime == 3 ){
      const messageWait = "Patienter 1 minute et essayer de nouveau!";
      showMessageError(messageWait);
      makeFormDisappear();
    }else{
      showMessageError(message);
    }
}

function validateForm() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const keyword = document.getElementById('keyword').value;

    // check if email is email format
    if (!email.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/)) {
        showError('Veuillez entrer une adresse email valide');
        return false;
    }
    // check if password is at least 8 characters long
    if (password.length < 8) {
        showError('Le mot de passe doit contenir au moins 8 caractères');
        return false;
    }
    // check if email and password are not empty
    if (!email || !password || !keyword) {
        showError('Veuillez remplir tous les champs');
        return false;
    }
    return true;
}

// IF user submit data tree times with no success make the form disappear for 5 seconds
function makeFormDisappear() {
    const form = document.getElementById('loginForm');
    const timeout = document.getElementById('timeout');
    
    form.style.display = 'none';
    timeout.style.display = 'block';
    
    // create setInteral and I should stop the setInterval
    let seconds = 0;
    const interval = setInterval(() => {
        seconds += 1;
        timeout.innerHTML = ` <b> Temps restant: ${60 - seconds} secondes </b>`;
    }, 1000);

    // I should hide the form after 5 seconds
    setTimeout(() => {
        // I want to show the form
        form.style.display = 'block';
        // I want to reset the form
        document.getElementById('loginForm').reset();
        // I want to remove stop the setInterval
        clearInterval(interval);
        // I want to remove the timeout
        timeout.textContent = '';
        // I want to hide the timeout
        timeout.style.display = 'none';
    }, WAITING_TIME);
}

// Submit form
document.addEventListener('DOMContentLoaded', () => {
  // recuperation des données
    const form = document.getElementById('loginForm');
    const inputs = form.querySelectorAll('input');
    const btnSubmit = document.getElementById('loginBtn');

    // Animation du formulaire
    gsap.from('.auth-container', {
      duration: 1,
      y: 50,
      opacity: 0,
      ease: 'power3.out'
    });

    inputs.forEach(input => {
      input.addEventListener('focus', () => {
        gsap.to(input, {
          duration: 0.3,
          scale: 1.05,
          ease: 'power2.out'
        });
      });

      input.addEventListener('blur', () => {
        gsap.to(input, {
          duration: 0.3,
          scale: 1,
          ease: 'power2.out'
        });
      });
    });

 
    // Soumission des données
    btnSubmit.addEventListener('click',  async function(e) {
      e.preventDefault();
      
           // Validate form before submission
          if (!validateForm()) {
            return;
        }
      const formData = {
        "email": document.getElementById('email').value,
        "password": document.getElementById('password').value,
        "keyword": document.getElementById('keyword').value
    };
     sendDataToServer(formData);

      // Animate the form submission
      gsap.to(form, {
        duration: 0.5,
        scale: 0.95,
        opacity: 0.5,
        ease: 'power2.inOut',
        onComplete: () => {
          gsap.to(form, {
            duration: 0.5,
            scale: 1,
            opacity: 1,
            ease: 'power2.out'
          });
        }
      });
    });

    // Validation initialisation
    validateForm();
});