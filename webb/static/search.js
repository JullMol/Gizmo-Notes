document.addEventListener('DOMContentLoaded', function() {
    const searchView = document.getElementById('searchView');
    const searchLink = document.getElementById('searchLink');
    showView(homeView);

    // Fungsi untuk menampilkan view yang dipilih
    function showView(viewToShow) {
        // Sembunyikan semua view terlebih dahulu
        searchView.style.display = 'none';
        groupProjectView.style.display = 'none';
        // Tampilkan view yang dipilih
        viewToShow.style.display = 'block';
    }

    searchLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView(searchView); 'block'
    });
})