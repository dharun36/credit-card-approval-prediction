// Form validation and submission handling
const form = document.getElementById('approvalForm');
const submitButton = document.querySelector('button[type="submit"]');
const resultDiv = document.getElementById('result');
const predictionText = document.getElementById('predictionText');

// Utility function to format currency
function formatIndianNumber(value) {
  if (!value) return '';
  const number = parseFloat(value.toString().replace(/[^\d.]/g, ""));
  return !isNaN(number) ? "₹" + number.toLocaleString('en-IN') : '';
}

// Validation configuration
const validationConfig = {
  Income: {
    min: 0,
    message: 'Income must be a positive number'
  },
  Debt: {
    min: 0,
    message: 'Debt must be a positive number'
  },
  CreditScore: {
    min: 300,
    max: 850,
    message: 'Credit score must be between 300 and 850'
  },
  Age: {
    min: 18,
    max: 100,
    message: 'Age must be between 18 and 100'
  },
  YearsEmployed: {
    min: 0,
    max: 50,
    message: 'Years employed must be between 0 and 50'
  }
};

// Handle input validation
function validateInput(input) {
  const config = validationConfig[input.name];
  const errorElement = input.parentElement.querySelector('.error-message');
  let isValid = true;

  if (!errorElement) return true; // Skip if no error element found

  const value = input.classList.contains('currency')
    ? parseFloat(input.value.replace(/[₹,]/g, ""))
    : parseFloat(input.value);

  if (isNaN(value)) {
    errorElement.textContent = 'Please enter a valid number';
    errorElement.style.display = 'block';
    isValid = false;
  } else if (config.min !== undefined && value < config.min) {
    errorElement.textContent = config.message;
    errorElement.style.display = 'block';
    isValid = false;
  } else if (config.max !== undefined && value > config.max) {
    errorElement.textContent = config.message;
    errorElement.style.display = 'block';
    isValid = false;
  } else {
    errorElement.style.display = 'none';
  }

  return isValid;
}

// Handle currency input formatting
document.querySelectorAll('.currency').forEach(input => {
  input.addEventListener('input', function () {
    this.value = formatIndianNumber(this.value);
    validateInput(this);
  });
});

// Validate all number inputs
document.querySelectorAll('input[type="number"]').forEach(input => {
  input.addEventListener('input', () => validateInput(input));
});

// Form submission handler
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Validate all inputs
  let isValid = true;
  form.querySelectorAll('input, select').forEach(input => {
    if (!validateInput(input)) {
      isValid = false;
    }
  });

  if (!isValid) {
    return;
  }

  // Show loading state
  submitButton.disabled = true;
  submitButton.classList.add('loading');
  resultDiv.style.display = 'none';

  const formData = new FormData(form);
  const data = {};

  for (let [key, value] of formData.entries()) {
    if (key === 'Income' || key === 'Debt') {
      data[key] = parseFloat(value.replace(/[₹,]/g, ""));
    } else {
      data[key] = parseFloat(value);
    }
  }

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    resultDiv.style.display = 'block';
    if (result.approval) {
      resultDiv.className = 'prediction approved';
      predictionText.innerHTML = `🎉 Congratulations! Your credit card application is likely to be approved.${result.confidence ? ` (Confidence: ${result.confidence})` : ''
        }`;
    } else {
      resultDiv.className = 'prediction rejected';
      predictionText.innerHTML = `⚠️ Sorry, your credit card application might not be approved at this time.${result.confidence ? ` (Confidence: ${result.confidence})` : ''
        }`;
    }
  } catch (error) {
    console.error('Error:', error);
    resultDiv.style.display = 'block';
    resultDiv.className = 'prediction rejected';
    predictionText.innerHTML = '⚠️ An error occurred while processing your request. Please try again.';
  } finally {
    // Remove loading state
    submitButton.disabled = false;
    submitButton.classList.remove('loading');
  }
});