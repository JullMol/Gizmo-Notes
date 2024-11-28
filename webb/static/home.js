document.addEventListener('DOMContentLoaded', function() {
    const homeView = document.getElementById('homeView');
    const homeLink = document.getElementById('homeLink');
    showView(homeView)

    function showView(viewToShow) {
        homeView.style.display = 'none';
        viewToShow.style.display = 'block'
    }

    // Event listeners untuk navigasi
    homeLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView(homeView);
    });
})