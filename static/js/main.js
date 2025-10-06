document.addEventListener('DOMContentLoaded', () => {
    // Select all copy buttons
    const allCopyButtons = document.querySelectorAll('.copy-btn');

    allCopyButtons.forEach(copyButton => {
        copyButton.addEventListener('click', (event) => {
            const button = event.currentTarget;
            
            // Find the code block within the same wrapper
            const codeWrapper = button.closest('.code-block-wrapper');
            const codeElement = codeWrapper.querySelector('pre code');
            
            if (codeElement && !button.classList.contains('copied')) {
                navigator.clipboard.writeText(codeElement.innerText).then(() => {
                    // --- Animated Visual Confirmation ---
                    const originalIcon = button.innerHTML; // Save the original copy icon
                    
                    // The SVG for our checkmark. It's a "polyline" (a path).
                    const checkmarkSVG = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#28c76f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    `;
                    
                    // Change button content to the checkmark
                    button.innerHTML = checkmarkSVG;
                    button.classList.add('copied');
                    button.disabled = true;

                    // Use Anime.js to "draw" the checkmark
                    anime({
                        targets: button.querySelector('polyline'),
                        strokeDashoffset: [anime.setDashoffset, 0], // Animate from full offset to zero
                        duration: 600,
                        easing: 'easeInOutSine',
                        complete: function() {
                            // After the animation, wait 1.5 seconds then revert
                            setTimeout(() => {
                                button.innerHTML = originalIcon; // Restore the original copy icon
                                button.classList.remove('copied');
                                button.disabled = false;
                            }, 1500);
                        }
                    });

                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            }
        });
    });

    // --- Mobile Navigation Toggle ---
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('is-active');
        navToggle.classList.toggle('is-active');
        
        // Add/remove class to the body to prevent scrolling
        document.body.classList.toggle('nav-open');
    });
}
});