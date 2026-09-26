// Main UI JavaScript functions
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alert banners after 5 seconds
    const alerts = document.querySelectorAll('.alert-banner');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease, margin-bottom 0.5s ease, padding 0.5s ease, height 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // Add subtle hover animations to buttons and input focuses
    const inputs = document.querySelectorAll('.form-input, .form-select');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', () => {
            input.parentElement.classList.remove('focused');
        });
    });
});
