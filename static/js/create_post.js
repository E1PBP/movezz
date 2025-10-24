    function openPostModal() {
      const postFormPreTextarea = document.querySelector(
        '#post-form-pre textarea[name="text"]'
      );
      const finalFormTextarea = document.querySelector('#post-form-final textarea[name="text"]');

      if (postFormPreTextarea && finalFormTextarea) {
        finalFormTextarea.value = postFormPreTextarea.value;
        postFormPreTextarea.value = ''; 
      } else if (finalFormTextarea) {
        finalFormTextarea.value = ''; 
      }

      const modal = document.getElementById("post-modal");
      if (modal) {
        modal.showModal();
      }
    }
  
    const hashtagContainer = document.getElementById('hashtag-container');
    const hashtagInput = document.getElementById('hashtag-input');
    const hiddenInput = document.getElementById('hashtags-hidden-input');
    let hashtags = [];
  
    const imageUpload = document.getElementById('image-upload');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImageBtn = document.getElementById('remove-image-btn');
  
    function renderHashtags() {
      const chips = hashtagContainer.querySelectorAll('div.badge');
      chips.forEach(chip => chip.remove());
  
      hashtags.forEach(tag => {
        const chip = document.createElement('div');
        chip.className = 'badge badge-neutral gap-2';
        chip.textContent = `#${tag}`;
        
        const removeBtn = document.createElement('span');
        removeBtn.className = 'cursor-pointer';
        removeBtn.innerHTML = '&times;';
        removeBtn.onclick = () => {
          hashtags = hashtags.filter(t => t !== tag);
          renderHashtags();
        };
        
        chip.appendChild(removeBtn);
        hashtagContainer.insertBefore(chip, hashtagInput);
      });
      hiddenInput.value = hashtags.join(',');
      hashtagInput.focus();
    }
  
    imageUpload.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
          imagePreview.src = event.target.result;
          imagePreviewContainer.classList.remove('hidden');
          lucide.createIcons(); // Redraw icons if needed
        }
        reader.readAsDataURL(file);
      }
    });
  
    removeImageBtn.addEventListener('click', function() {
      imageUpload.value = ''; // Clear the file input
      imagePreview.src = '#';
      imagePreviewContainer.classList.add('hidden');
    });
  
    hashtagInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && hashtagInput.value.trim() !== '') {
        e.preventDefault();
        const newTag = hashtagInput.value.trim().replace(/[^a-zA-Z0-9]/g, '');
        if (newTag && !hashtags.includes(newTag) && hashtags.length < 5) {
          hashtags.push(newTag);
          hashtagInput.value = '';
          renderHashtags();
        }
      }
    });
  
    document
      .getElementById("post-form-final")
      .addEventListener("submit", function (e) {
        e.preventDefault();
  
        let formData = new FormData(this);
        
        fetch(this.action, {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              window.location.reload();
            } else {
              console.error("Error:", data.errors);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      });