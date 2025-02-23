document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.inputContainer');
    const submitBtn = document.querySelector('.formSubmit');
    const inputs = document.querySelectorAll('.inputBox');

    // Input validation functions
    const validators = {
        TrnAmn: (value) => {
            const amount = parseFloat(value);
            return amount > 0 ? '' : 'Amount must be greater than 0';
        },
        ZipCode: (value) => {  // Changed from PostalCode to ZipCode
            // Remove any whitespace
            const code = value.toString().trim();
            
            // Validate US ZIP code (5 digits)
            if (/^\d{5}$/.test(code)) {
                const zip = parseInt(code);
                const firstThree = Math.floor(zip / 100);
                
                // Valid US ZIP ranges
                const usRanges = [
                    [1, 339], [342, 399], [400, 599],
                    [600, 799], [800, 999]
                ];
                
                return usRanges.some(([min, max]) => 
                    firstThree >= min && firstThree <= max
                ) ? '' : 'Invalid US ZIP code';
            }
            
            // Validate Indian PIN code (6 digits)
            if (/^\d{6}$/.test(code)) {
                const firstDigit = parseInt(code[0]);
                // Indian PIN codes start from 1 and first digit can't be 0
                return firstDigit > 0 ? '' : 'Invalid Indian PIN code';
            }
            
            return 'Please enter a valid 5 or 6-digit PIN code';
        },
        TrnHr: (value) => {
            const hour = parseInt(value);
            return hour >= 0 && hour <= 23 ? '' : 'Hour must be between 0 and 23';
        },
        Age: (value) => {
            const age = parseInt(value);
            return age >= 18 && age <= 100 ? '' : 'Age must be between 18 and 100';
        }
    };

    // Add error message display functionality
    const showError = (input, message) => {
        const existingError = input.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.textContent = message;
        } else {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.style.color = '#ff4444';
            errorDiv.style.fontSize = '14px';
            errorDiv.style.marginTop = '5px';
            errorDiv.textContent = message;
            input.parentElement.appendChild(errorDiv);
        }
        input.style.borderColor = '#ff4444';
    };

    const clearError = (input) => {
        const errorDiv = input.parentElement.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
        input.style.borderColor = '';
    };

    // Add input validation
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            const validator = validators[input.id];
            if (validator) {
                const error = validator(input.value);
                if (error) {
                    showError(input, error);
                } else {
                    clearError(input);
                }
            }
        });
    });

    // Form submission handling
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        let hasErrors = false;

        // Validate all inputs before submission
        inputs.forEach(input => {
            const validator = validators[input.id];
            if (validator) {
                const error = validator(input.value);
                if (error) {
                    showError(input, error);
                    hasErrors = true;
                }
            }
        });

        if (!hasErrors) {
            submitBtn.classList.add('btnClicked');
            try {
                const formData = new FormData(form);
                const response = await fetch('/predict_credit_fraud', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const result = await response.text();
                document.body.innerHTML = result;
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while processing your request.');
            } finally {
                submitBtn.classList.remove('btnClicked');
            }
        }
    });
});