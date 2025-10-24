document.addEventListener('DOMContentLoaded', function () {
    const loadMoreBtn = document.getElementById('load-more-btn');
    if (!loadMoreBtn) return;

    let page = 1;
    const postList = document.getElementById('post-list');
    const activeTab = new URLSearchParams(window.location.search).get('tab') || 'foryou';
    const loadMoreUrl = loadMoreBtn.dataset.url;

    loadMoreBtn.addEventListener('click', function () {
        page++;
        fetch(`${loadMoreUrl}?page=${page}&tab=${activeTab}`)
            .then(response => response.json())
            .then(data => {
                if (data.html) {
                    postList.insertAdjacentHTML('beforeend', data.html);
                }
                if (!data.has_next) {
                    loadMoreBtn.style.display = 'none';
                }
            })
            .catch(error => console.error('Error loading more posts:', error));
    });
});
