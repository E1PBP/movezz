document.addEventListener('DOMContentLoaded', function () {
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

    function createCommentAvatar(comment) {
        if (comment.avatar_url) {
            return `<img src="${comment.avatar_url}" alt="${comment.author}'s avatar" />`;
        } else {
            const initial = comment.username ? comment.username.slice(0, 1).toUpperCase() : 'A';
            return `<div class="w-full h-full bg-primary text-primary-content flex items-center justify-center"><span class="font-bold">${initial}</span></div>`;
        }
    }

    document.body.addEventListener('click', function(event) {
        const commentBtn = event.target.closest('.comment-btn');
        if (commentBtn) {
            const postId = commentBtn.dataset.postId;
            const commentSection = document.getElementById(`comment-section-${postId}`);
            const commentList = document.getElementById(`comment-list-${postId}`);

            if (commentSection.classList.contains('hidden')) {
                commentSection.classList.remove('hidden');
                fetch(`/feeds/get_comments/?post_id=${postId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            commentList.innerHTML = '';
                            data.comments.forEach(comment => {
                                const commentEl = document.createElement('div');
                                commentEl.classList.add('flex', 'items-start', 'gap-2');
                                commentEl.innerHTML = `
                                    <div class="avatar">
                                        <div class="w-8 h-8 rounded-full overflow-hidden">
                                            ${createCommentAvatar(comment)}
                                        </div>
                                    </div>
                                    <div class="bg-base-200 rounded-lg p-2">
                                        <p class="font-bold">${comment.author}</p>
                                        <p>${comment.text}</p>
                                    </div>
                                `;
                                commentList.appendChild(commentEl);
                            });
                        }
                    });
            } else {
                commentSection.classList.add('hidden');
            }
        }
    });

    document.body.addEventListener('submit', function(event) {
        const addCommentForm = event.target.closest('.add-comment-form');
        if (addCommentForm) {
            event.preventDefault();
            const postId = addCommentForm.dataset.postId;
            const commentText = addCommentForm.querySelector('input[name="comment_text"]').value;
            const commentList = document.getElementById(`comment-list-${postId}`);
            const commentsCountSpan = document.querySelector(`.comment-btn[data-post-id="${postId}"] .comments-count`);

            const formData = new FormData();
            formData.append('post_id', postId);
            formData.append('comment_text', commentText);

            fetch(`/feeds/add_comment/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const comment = data.comment;
                    const commentEl = document.createElement('div');
                    commentEl.classList.add('flex', 'items-start', 'gap-2');
                    commentEl.innerHTML = `
                        <div class="avatar">
                            <div class="w-8 h-8 rounded-full overflow-hidden">
                                ${createCommentAvatar(comment)}
                            </div>
                        </div>
                        <div class="bg-base-200 rounded-lg p-2">
                            <p class="font-bold">${comment.author}</p>
                            <p>${comment.text}</p>
                        </div>
                    `;
                    commentList.appendChild(commentEl);
                    addCommentForm.reset();
                    commentsCountSpan.textContent = data.comments_count;
                }
            });
        }
    });
});
