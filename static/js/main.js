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

    // --- Dynamic Formset for Contribution Page ---
    const addSnippetButton = document.getElementById('add-snippet-form');
    
    if (addSnippetButton) {
        const formContainer = document.getElementById('snippet-forms-container');
        const formTemplate = document.getElementById('snippet-form-template');
        const totalFormsInput = document.querySelector('input[name="snippets-TOTAL_FORMS"]');

        addSnippetButton.addEventListener('click', () => {
            // Get the current number of forms
            let formIndex = parseInt(totalFormsInput.value);

            // Clone the template's content
            const newForm = formTemplate.content.cloneNode(true);
            
            // Find all input/select/textarea elements in the new form
            const formFields = newForm.querySelectorAll('input, select, textarea');
            
            // Update the 'name' and 'id' attributes to use the new form index
            formFields.forEach(field => {
                field.name = field.name.replace('__prefix__', formIndex);
                field.id = field.id.replace('__prefix__', formIndex);
            });

            // Append the new form to the container
            formContainer.appendChild(newForm);

            // Increment the total forms count
            totalFormsInput.value = formIndex + 1;
        });
    }


    // --- Initialize CodeMirror & File Upload on Contribution Page ---
    const jsonTextarea = document.getElementById('id_json_data');
    let codeMirrorEditor = null; // To hold our editor instance

    if (jsonTextarea) {
        // Create the CodeMirror editor
        codeMirrorEditor = CodeMirror.fromTextArea(jsonTextarea, {
            mode: { name: "javascript", json: true },
            theme: "dracula",
            lineNumbers: true,
            lineWrapping: true,
            autoCloseBrackets: true
        });
    }

    const jsonFileInput = document.getElementById('json-file-input');
    
    // Check if both the file input and the editor exist on the page
    if (jsonFileInput && codeMirrorEditor) {
        jsonFileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];

            if (file) {
                const reader = new FileReader();

                // Define what happens after the file is read
                reader.onload = (e) => {
                    const fileContent = e.target.result;
                    // Set the CodeMirror editor's value to the file content
                    codeMirrorEditor.setValue(fileContent);
                };
                
                // Define what happens if there's an error
                reader.onerror = (e) => {
                    console.error("Error reading file:", e);
                    alert("Failed to read the file.");
                };
                
                // Start reading the file as text
                reader.readAsText(file);
            }
        });
    }

    // --- Profile Page Edit/View Toggle ---
    const viewMode = document.getElementById('profile-view-mode');
    const editMode = document.getElementById('profile-edit-mode');
    const editBtn = document.getElementById('edit-profile-btn');
    const cancelBtn = document.getElementById('cancel-edit-btn');

    if (viewMode && editMode && editBtn && cancelBtn) {
        editBtn.addEventListener('click', () => {
            viewMode.style.display = 'none';
            editMode.style.display = 'block';
        });

        cancelBtn.addEventListener('click', () => {
            editMode.style.display = 'none';
            viewMode.style.display = 'block';
        });
    }
    // --- Live Preview for Profile Picture Upload ---
    const profilePicInput = document.getElementById('id_profile_picture');
    const imagePreview = document.getElementById('image-preview');

    if (profilePicInput && imagePreview) {
        profilePicInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

     // --- Remove Profile Picture Logic ---
    const removePicBtn = document.getElementById('remove-pic-btn');
    // const imagePreview = document.getElementById('image-preview');
    // Find Django's hidden "clear" checkbox
    const clearCheckbox = document.getElementById('profile_picture-clear_id');

    if (removePicBtn && imagePreview && clearCheckbox) {
        removePicBtn.addEventListener('click', function() {
            // Check the hidden checkbox
            clearCheckbox.checked = true;

            // Instantly update the preview to the default image
            imagePreview.src = imagePreview.dataset.defaultUrl;
            
            // Hide the remove button since the picture is now "removed"
            this.style.display = 'none';
        });
    }

    // --- Advanced Instant Search Command Palette ---
    const overlay = document.getElementById('search-palette-overlay');
    const searchInput = document.getElementById('search-input');
    const resultsList = document.getElementById('search-results-list');
    const openSearchBtn = document.getElementById('open-search-btn');
    const searchCancelBtn = document.getElementById('search-cancel-btn'); // New cancel button
    const previewDefaultState = document.getElementById('preview-default-state');
    const previewContent = document.getElementById('preview-content');
    const previewCategoryIcon = document.getElementById('preview-category-icon');
    const previewTitle = document.getElementById('preview-title');
    const previewCategoryName = document.getElementById('preview-category-name');
    const previewTags = document.getElementById('preview-tags');
    const previewSections = document.getElementById('preview-sections');
    const previewFullLink = document.getElementById('preview-full-link');
    const searchPreviewRightPanel = document.getElementById('search-preview-right-panel');


    if (overlay && searchInput && resultsList && openSearchBtn && searchCancelBtn && previewDefaultState && previewContent && previewCategoryIcon && previewTitle && previewCategoryName && previewTags && previewSections && previewFullLink) {
        let activeResultIndex = -1; // For left panel results
        let activeSectionIndex = -1; // For right panel sections
        let currentResults = []; // Store fetched results for easier access

        const openPalette = () => {
            overlay.style.display = 'block';
            searchInput.focus();
            searchInput.value = '';
            resultsList.innerHTML = '';
            previewDefaultState.style.display = 'block';
            previewContent.style.display = 'none';
            activeResultIndex = -1;
            activeSectionIndex = -1;
            currentResults = [];
            document.body.classList.add('body-lock-scroll');
        };

        const closePalette = () => {
            overlay.style.display = 'none';
            document.body.classList.remove('body-lock-scroll');
        };

        // --- Left Panel: Results Navigation ---
        const updateActiveResult = () => {
            const items = resultsList.querySelectorAll('li a');
            items.forEach((item, index) => {
                if (index === activeResultIndex) {
                    item.classList.add('is-active');
                    item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
                    displayPreview(currentResults[index]); // Display preview for active item
                } else {
                    item.classList.remove('is-active');
                }
            });

            if (activeResultIndex === -1 && items.length > 0) {
                // If nothing is active, show the default preview or first item's
                displayPreview(currentResults[0]);
            } else if (items.length === 0) {
                previewDefaultState.style.display = 'block';
                previewContent.style.display = 'none';
            }
        };

        // --- Right Panel: Preview Display ---
        const displayPreview = (item) => {
            if (!item) {
                previewDefaultState.style.display = 'block';
                previewContent.style.display = 'none';
                return;
            }

            previewDefaultState.style.display = 'none';
            previewContent.style.display = 'block';
            searchPreviewRightPanel.scrollTop = 0; // Scroll to top when new item is displayed

            previewCategoryIcon.src = item.category_icon_url;
            previewCategoryIcon.alt = item.category_name + " icon";
            previewTitle.textContent = item.title;
            previewCategoryName.textContent = item.category_name;
            previewFullLink.href = item.url;

            // Render Tags
            previewTags.innerHTML = '';
            if (item.tags && item.tags.length > 0) {
                item.tags.forEach(tag => {
                    const span = document.createElement('span');
                    span.className = 'tag';
                    span.textContent = tag;
                    previewTags.appendChild(span);
                });
            } else {
                previewTags.innerHTML = '<span class="tag">No specific tags</span>';
            }

            // Render Sections
            previewSections.innerHTML = '';
            if (item.sections && item.sections.length > 0) {
                item.sections.forEach(section => {
                    const sectionDiv = document.createElement('div');
                    sectionDiv.innerHTML = `<h4>${section.title}</h4>`;
                    if (section.subsections && section.subsections.length > 0) {
                        const ul = document.createElement('ul');
                        section.subsections.forEach(subsection => {
                            const li = document.createElement('li');
                            // We will link to the full cheatsheet and add an anchor for future scrolling
                            li.innerHTML = `<a href="${item.url}#${subsection.heading.replace(/\s+/g, '-').toLowerCase()}">${subsection.heading}</a>`;
                            ul.appendChild(li);
                        });
                        sectionDiv.appendChild(ul);
                    }
                    previewSections.appendChild(sectionDiv);
                });
            } else {
                previewSections.innerHTML = '<p>No structured sections available.</p>';
            }
            activeSectionIndex = -1; // Reset active section on new preview
        };


        openSearchBtn.addEventListener('click', openPalette);
        searchCancelBtn.addEventListener('click', closePalette); // New cancel button listener

        // Keyboard shortcuts for opening/closing
        window.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                openPalette();
            }
            if (e.key === 'Escape') closePalette();
        });
        
        // Close when clicking the background overlay
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) closePalette();
        });

        // Keyboard navigation within the palette
        searchInput.addEventListener('keydown', (e) => {
            const items = resultsList.querySelectorAll('li a');
            if (items.length === 0) return;

            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    activeResultIndex = (activeResultIndex + 1) % items.length;
                    updateActiveResult();
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    activeResultIndex = (activeResultIndex - 1 + items.length) % items.length;
                    updateActiveResult();
                    break;
                case 'Enter':
                    e.preventDefault();
                    if (activeResultIndex > -1) {
                        // If an item is selected, go to its URL
                        items[activeResultIndex].click();
                    } else {
                        // If nothing is selected, perform a full search
                        const query = searchInput.value;
                        if (query) window.location.href = `/search/?q=${query}`;
                    }
                    break;
            }
        });

        // Fetch results as the user types
        searchInput.addEventListener('input', async () => {
            const query = searchInput.value;
            activeResultIndex = -1;
            currentResults = [];

            // Helper function to highlight text
            const highlight = (text, query) => {
                if (!query) return text;
                const regex = new RegExp(`(${query})`, 'gi');
                return text.replace(regex, `<span class="search-highlight">$1</span>`);
            };

            if (query.length < 2) {
                resultsList.innerHTML = ''; // Clear previous results
                previewDefaultState.style.display = 'block';
                previewContent.style.display = 'none';
                return;
            }

            // Add a loading state for better UX
            // resultsList.innerHTML = `<li class="search-loading">Searching...</li>`;

            const response = await fetch(`/api/live-search/?q=${query}`);
            const data = await response.json();
            currentResults = data.results;

            // Clear loading state
            resultsList.innerHTML = '';

            if (data.results.length > 0) {
                data.results.forEach((item, index) => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <a href="${item.url}" data-index="${index}">
                            <img src="${item.category_icon_url || '/static/profile_pics/default.svg'}" class="search-result-icon" alt="">
                            <div class="search-result-text">
                                <strong>${highlight(item.title, query)}</strong>
                                <span>in ${item.category_name}</span>
                            </div>
                        </a>`;
                    resultsList.appendChild(li);
                });

                const footerLi = document.createElement('li');
                footerLi.className = 'search-palette-footer';
                footerLi.innerHTML = `<a href="/search/?q=${query}">View all results for "${query}"</a>`;
                resultsList.appendChild(footerLi);

                if (currentResults.length > 0) {
                    activeResultIndex = 0;
                    updateActiveResult();
                }

            } else {
                // Enhanced "no results" message
                resultsList.innerHTML = `<center><li class="search-no-results">No results found for "<strong>${query}</strong>". Try another search.</li></center>`;
                previewDefaultState.style.display = 'block';
                previewContent.style.display = 'none';
            }
        });
    }


});