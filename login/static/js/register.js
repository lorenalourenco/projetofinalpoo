// static/js/register.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitButton = form.querySelector('button[type="submit"]');
    const buttonText = submitButton.querySelector('.btn-text');
    const buttonSpinner = submitButton.querySelector('.btn-spinner');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        buttonText.classList.add('hidden');
        buttonSpinner.classList.remove('hidden');
        submitButton.disabled = true;

        // Simulate form submission (replace with actual form submission)
        setTimeout(function() {
            form.submit();
        }, 1000);
    });
});