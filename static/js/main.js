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
});