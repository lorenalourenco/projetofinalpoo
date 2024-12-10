// static/js/dashboard.js
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

    // Auto-hide toast messages after 5 seconds
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(function(toast) {
        setTimeout(function() {
            toast.style.opacity = '0';
            setTimeout(function() {
                toast.remove();
            }, 300);
        }, 5000);
    });
});