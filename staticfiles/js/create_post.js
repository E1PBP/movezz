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
      if (typeof lucide !== 'undefined') {
        lucide.createIcons();
      }
    }
    reader.readAsDataURL(file);
  }
});

removeImageBtn.addEventListener('click', function() {
  imageUpload.value = '';
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

function addPostToGrid(postData) {
  const postsGrid = document.getElementById('posts-grid');
  if (!postsGrid) return;

  const emptyMessage = postsGrid.querySelector('p.text-base-content\\/60');
  if (emptyMessage) {
    emptyMessage.remove();
  }

  const postDiv = document.createElement('div');
  postDiv.className = 'rounded overflow-hidden bg-base-100 shadow-sm';
  postDiv.innerHTML = `
    <a href="/profile/${postData.username}/${postData.id}" class="block w-full h-48 overflow-hidden">
      <img src="${postData.image_url}" alt="post" class="w-full h-full object-cover"/>
    </a>
  `;

  postsGrid.insertBefore(postDiv, postsGrid.firstChild);

  const postCountElement = document.querySelector('b');
  if (postCountElement && postCountElement.nextSibling && postCountElement.nextSibling.textContent.includes('posts')) {
    const currentCount = parseInt(postCountElement.textContent) || 0;
    postCountElement.textContent = currentCount + 1;
  }
}

document.getElementById("post-form-final").addEventListener("submit", function (e) {
  e.preventDefault();

  const submitBtn = this.querySelector('button[type="submit"]');
  const originalText = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = 'Posting...';

  let formData = new FormData(this);
  
  fetch(this.action || "{% url 'feeds_module:create_post_ajax' %}", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        const modal = document.getElementById("post-modal");
        if (modal) {
          modal.close();
        }

        this.reset();
        hashtags = [];
        renderHashtags();
        imagePreview.src = '#';
        imagePreviewContainer.classList.add('hidden');

        if (data.post) {
          addPostToGrid(data.post);
        } else {
          window.location.reload();
        }
        
        console.log('Post created successfully!');
      } else {
        alert("Error: " + (data.message || "Failed to create post"));
        console.error("Error:", data.errors || data);
      }
    })
    .catch((error) => {
      alert("Network error. Please try again.");
      console.error("Error:", error);
    })
    .finally(() => {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
    });
});