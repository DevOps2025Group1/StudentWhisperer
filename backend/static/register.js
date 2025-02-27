// Register/Login constants
const form = document.getElementById('form')
const name_input = document.getElementById('name-input')
const email_input = document.getElementById('email-input')
const password_input = document.getElementById('password-input')
const repeat_password_input = document.getElementById('repeat-password-input')
const error_message = document.getElementById('error-message')

/* Register/Login */
form.addEventListener('submit', async (e) => {
  let errors = []
  console.log("Maybe a bug here")
  if(name_input){
    // If we have a name input then we are in the signup
    errors = getSignupFormErrors(name_input.value, email_input.value, password_input.value, repeat_password_input.value)
  }
  else{
    // If we don't have a name input then we are in the login
    errors = getLoginFormErrors(email_input.value, password_input.value)
  }

  if(errors.length > 0){
    // If there are any errors
    e.preventDefault()
    error_message.innerText  = errors.join(". ")
  }

  const formData = new FormData();
  formData.append('name', name_input.value.trim());
  formData.append('email', email_input.value.trim());
  formData.append('password', password_input.value.trim());
  if (repeat_password_input) {
    formData.append('repeat-password', repeat_password_input.value.trim());
  }

  // 3) Send data to Flask route via fetch
  try {
    const response = await fetch('/register', {
      method: 'POST',
      body: formData
    });

    // 4) Handle server response
    if (!response.ok) {
      // For a 4xx or 5xx status code, we can assume an error from server
      let data = await response.json();
      error_message.innerText = data.error || 'An error occurred.';
    } else {
      // For a 2xx success status
      let data = await response.json();
      if (data.success) {
        // For example, redirect or show success
        window.location.href = '/chatbot';
      } else {
        // If server returns success=false, show message
        error_message.innerText = data.error || 'Registration failed.';
      }
    }
  } catch (err) {
    // Handle network or unexpected errors
    error_message.innerText = 'Error connecting to the server.';
  }
})


function getSignupFormErrors(name, email, password, repeatPassword){
    let errors = []

    if(name === '' || name == null){
      errors.push('name is required')
      name_input.parentElement.classList.add('incorrect')
    }
    if(email === '' || email == null){
      errors.push('Email is required')
      email_input.parentElement.classList.add('incorrect')
    }
    if(password === '' || password == null){
      errors.push('Password is required')
      password_input.parentElement.classList.add('incorrect')
    }
    if(password.length < 8){
      errors.push('Password must have at least 8 characters')
      password_input.parentElement.classList.add('incorrect')
    }
    if(password !== repeatPassword){
      errors.push('Password does not match repeated password')
      password_input.parentElement.classList.add('incorrect')
      repeat_password_input.parentElement.classList.add('incorrect')
    }

    return errors;
}

function getLoginFormErrors(email, password){
    let errors = []

    if(email === '' || email == null){
      errors.push('Email is required')
      email_input.parentElement.classList.add('incorrect')
    }
    if(password === '' || password == null){
      errors.push('Password is required')
      password_input.parentElement.classList.add('incorrect')
    }

    return errors;
}

const allInputs = [name_input, email_input, password_input, repeat_password_input].filter(input => input != null)

allInputs.forEach(input => {
input.addEventListener('input', () => {
    if(input.parentElement.classList.contains('incorrect')){
    input.parentElement.classList.remove('incorrect')
    error_message.innerText = ''
    }
})
})