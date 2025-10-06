
window.addEventListener('pageshow', function(event) {
    // The 'persisted' property is true if the page is from the bfcache
    if (event.persisted) {
        const pageContent = document.getElementById('page-content');
        if (pageContent) {
            // Instantly reset the content to be visible
            pageContent.style.opacity = 1;
            pageContent.style.transform = 'translateY(0px)';
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {

    anime({
        targets: '#page-content',
        translateY: ['-20px', '0px'], // Slide down from a slightly higher position
        opacity: [0, 1],
        duration: 800,
        easing: 'easeOutExpo'
    });

    // 2. Page Exit (Fade Out) Animation
    // This runs when an internal link is clicked
    // const internalLinks = document.querySelectorAll('a[href^="/"]'); // Select all links that start with "/"
    // internalLinks.forEach(link => {
    //     link.addEventListener('click', function(e) {
    //         const destination = this.href;

    //         // Check if the link is to a different page
    //         if (destination !== window.location.href) {
    //             e.preventDefault(); // Stop the browser from navigating instantly

    //             // Animate the current page out
    //             anime({
    //                 targets: '#page-content',
    //                 translateY: ['0px', '-20px'], // Slide up
    //                 opacity: [1, 0],
    //                 duration: 400,
    //                 easing: 'easeInExpo',
    //                 complete: function() {
    //                     // Navigate to the new page AFTER the animation is complete
    //                     window.location.href = destination;
    //                 }
    //             });
    //         }
    //     });
    // });

    // 1. Hero Section Entrance Animation
    if (document.querySelector('.stagger-visual')) {
        anime({
            targets: '.stagger-visual',
            translateY: [50, 0],
            opacity: [0, 1],
            delay: anime.stagger(150),
            easing: 'easeOutExpo',
            duration: 1200
        });
    }

    // 2. Interactive Card Hover Animation
    const cards = document.querySelectorAll('.card');
    if (cards.length > 0) {
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                anime({
                    targets: card,
                    scale: 1.05,
                    duration: 300,
                    easing: 'easeOutQuad'
                });
            });

            card.addEventListener('mouseleave', () => {
                anime({
                    targets: card,
                    scale: 1.0,
                    duration: 300,
                    easing: 'easeInQuad'
                });
            });
        });
    }

    // 3. Button Hover Animation
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    if (buttons.length > 0) {
        buttons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                anime({
                    targets: button,
                    translateY: -3,
                    boxShadow: '0 8px 25px rgba(140, 82, 255, 0.5)',
                    duration: 250,
                    easing: 'easeOutSine'
                });
            });

            button.addEventListener('mouseleave', () => {
                anime({
                    targets: button,
                    translateY: 0,
                    boxShadow: '0 4px 15px rgba(140, 82, 255, 0.4)',
                    duration: 250,
                    easing: 'easeInSine'
                });
            });
        });
    }

    // 4. Scroll-triggered Animations (Moved inside)
    const scrollElements = document.querySelectorAll('.animate-on-scroll');
    if (scrollElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                // This condition is TRUE when the element is scrolling INTO view
                if (entry.isIntersecting) {
                    anime({
                        targets: entry.target,
                        translateY: [30, 0], // From 30px below to original position
                        opacity: [0, 1],     // Fade in
                        duration: 800,
                        easing: 'easeOutExpo'
                    });
                } 
                // This condition is FALSE when the element is scrolling OUT of view
                else {
                    anime({
                        targets: entry.target,
                        translateY: [0, 30], // From original position to 30px below
                        opacity: [1, 0],     // Fade out
                        duration: 400,
                        easing: 'easeInExpo'
                    });
                }
            });
        }, { threshold: 0.1 });

        scrollElements.forEach(el => {
            observer.observe(el);
        });
    }

    const animatedButtons = document.querySelectorAll('.btn-primary, .btn-secondary');

    animatedButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            anime({
                targets: button,
                scale: [
                    { value: 0.95, duration: 100, easing: 'easeOutQuad' }, // Press down
                    { value: 1.0, duration: 150, easing: 'easeInQuad' }   // Return to normal
                ]
            });
        });
    });

    // --- Floating Tech Icons Animation ---
    if (document.querySelector('.floating-icons')) {
        anime({
            targets: '.floating-icons .icon',
            translateY: ['-15px', '15px'],
            translateX: ['-10px', '10px'],
            rotate: () => anime.random(-10, 10),
            scale: () => anime.random(1, 1.2),
            duration: 6000,
            direction: 'alternate',
            loop: true,
            easing: 'easeInOutSine',
            delay: anime.stagger(400) // Each icon starts at a different time
        });
    }
});