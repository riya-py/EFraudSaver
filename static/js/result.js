document.addEventListener('DOMContentLoaded', () => {
    // Add animation for result display
    const predictionResult = document.querySelector('.predictionResult');
    if (predictionResult) {
        predictionResult.style.opacity = '0';
        setTimeout(() => {
            predictionResult.style.transition = 'opacity 0.5s ease-in-out';
            predictionResult.style.opacity = '1';
        }, 100);
    }

    // Add click handlers for action buttons
    const actionButtons = document.querySelectorAll('.button');
    actionButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.style.transform = 'scale(0.98)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
            }, 100);
        });
    });
});