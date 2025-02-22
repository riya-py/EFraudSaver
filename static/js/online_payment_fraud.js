document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.inputContainer');
    const submitBtn = document.querySelector('.formSubmit');
    const inputs = document.querySelectorAll('.inputBox');
    const radioInputs = document.querySelectorAll('.radioSelect');

    // Input validation functions
    const validators = {
        TrnAmn: (value) => {
            const amount = parseFloat(value);
            return amount > 0 ? '' : 'Amount must be greater than 0';
        },
        oldBalance: (value) => {
            const balance = parseFloat(value);
            return balance >= 0 ? '' : 'Balance cannot be negative';
        },
        newAccBalance: (value) => {
            const balance = parseFloat(value);
            return balance >= 0 ? '' : 'Balance cannot be negative';
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

        // Check if a transaction type is selected
        const transactionSelected = Array.from(radioInputs).some(radio => radio.checked);
        if (!transactionSelected) {
            alert('Please select a transaction type');
            hasErrors = true;
        }

        if (!hasErrors) {
            submitBtn.classList.add('btnClicked');
            try {
                const formData = new FormData(form);
                const response = await fetch('/predict_online_fraud', {
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
