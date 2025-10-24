function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const likeUrl = document.body.dataset.likeUrl;

if (likeUrl) {
    document.body.addEventListener('click', function(event) {
        const likeBtn = event.target.closest('.like-btn');
        if (likeBtn) {
            const postId = likeBtn.dataset.postId;
            const likesCountSpan = likeBtn.querySelector('.likes-count');
            const heartIcon = likeBtn.querySelector('i');

            const formData = new FormData();
            formData.append('post_id', postId);

            fetch(likeUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    likesCountSpan.textContent = data.likes_count;
                    if (data.liked) {
                        heartIcon.classList.add('text-red-500', 'fill-current');
                    } else {
                        heartIcon.classList.remove('text-red-500', 'fill-current');
                    }
                } else {
                    console.error('Liking post failed:', data);
                }
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        }
    });
} else {
    console.error('Like URL not found on body data-like-url attribute.');
}

