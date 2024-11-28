document.addEventListener('DOMContentLoaded', function() {
    const notesDView = document.getElementById('notesDView');
    const notesGView = document.getElementById('notesGView');

    const noteImages = document.querySelectorAll('.note-image');
    const noteImagesGrouped = document.querySelectorAll('.note-image-grouped');
    const createNoteModal = document.querySelector('.create-note-modal');
    const closeModalBtn = document.querySelector('.close-modal-btn');
    const saveNoteBtn = document.querySelector('.save-note-btn');
    const noteTextarea = document.querySelector('.note-textarea');
    const modalTitle = document.querySelector('.modal-title'); // Ambil elemen judul modal

    function showView(viewToShow) {
        notesDView.style.display = 'none';
        notesGView.style.display = 'none';
        viewToShow.style.display = 'block';
    };

    notesDLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView(notesDView);
    });

    notesGLink.addEventListener('click', function(e){
        e.preventDefault();
        showView(notesGView);
    });

    // Menangani klik pada gambar catatan
    noteImages.forEach(image => {
        image.addEventListener('click', function() {
            const day = this.getAttribute('data-day'); // Ambil nama hari dari atribut data-day
            modalTitle.textContent = `Note ${day}`; // Ubah judul modal
            createNoteModal.style.display = 'flex'; // Tampilkan modal
        });
    });

    noteImagesGrouped.forEach(image => {
        image.addEventListener('click', function() {
            const group = this.getAttribute('data-group'); // Ambil nama grup dari atribut data-group
            modalTitle.textContent = `Create Note for ${group}`; // Ubah judul modal
            createNoteModal.style.display = 'flex'; // Tampilkan modal
        });
    });

    document.getElementById('imageUpload').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = 'auto'; // Mengatur lebar gambar secara otomatis
                img.style.height = 'auto'; // Mengatur tinggi gambar secara otomatis
                img.style.maxWidth = '100%'; // Agar gambar tidak melebihi lebar editor
                img.style.borderRadius = '8px'; // Sudut membulat untuk gambar
                img.style.cursor = 'nwse-resize'; // Menunjukkan bahwa gambar dapat diubah ukurannya
    
                // Membuat elemen wrapper untuk gambar
                const wrapper = document.createElement('div');
                wrapper.style.position = 'relative'; // Membuat posisi relatif untuk kontrol ukuran
                wrapper.appendChild(img);
    
                // Menambahkan kontrol untuk mengubah ukuran
                const resizeHandle = document.createElement('div');
                resizeHandle.style.width = '10px';
                resizeHandle.style.height = '10px';
                resizeHandle.style.backgroundColor = '#7b6ef6';
                resizeHandle.style.position = 'absolute';
                resizeHandle.style.right = '0';
                resizeHandle.style.bottom = '0';
                resizeHandle.style.cursor = 'nwse-resize'; // Menunjukkan bahwa ini adalah kontrol resize
                wrapper.appendChild(resizeHandle);
    
                // Menangani pengubahan ukuran
                resizeHandle.addEventListener('mousedown', function(e) {
                    e.preventDefault();
                    const startX = e.clientX;
                    const startY = e.clientY;
                    const startWidth = img.offsetWidth;
                    const startHeight = img.offsetHeight;
    
                    function resize(e) {
                        const newWidth = startWidth + (e.clientX - startX);
                        const newHeight = startHeight + (e.clientY - startY);
                        img.style.width = `${newWidth}px`;
                        img.style.height = `${newHeight}px`;
                    }
    
                    function stopResize() {
                        window.removeEventListener('mousemove', resize);
                        window.removeEventListener('mouseup', stopResize);
                    }
    
                    window.addEventListener('mousemove', resize);
                    window.addEventListener('mouseup', stopResize);
                });
    
                document.querySelector('.note-editor').appendChild(wrapper); // Tambahkan gambar ke editor
            };
            reader.readAsDataURL(file); // Membaca file sebagai URL data
        }
    });

    // Menangani klik tombol close
    closeModalBtn.addEventListener('click', function() {
        createNoteModal.style.display = 'none'; // Sembunyikan modal
        noteTextarea.value = ''; // Kosongkan textarea
    });

    // Menangani klik tombol save (tambahkan logika penyimpanan di sini)
    saveNoteBtn.addEventListener('click', function() {
        alert('Note saved'); // Ganti dengan logika penyimpanan yang sesuai
        createNoteModal.style.display = 'none'; // Sembunyikan modal setelah menyimpan
        document.querySelector('.note-editor').innerHTML = ''; // Kosongkan editor
        
        const noteContent = noteTextarea.value; // Ambil konten catatan
        fetch('/save_note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ note: noteContent }), // Kirim konten catatan sebagai JSON
        })
        .then(response => response.json())
        .then(data => {
        if (data.success) {
            alert('Note saved and PDF generated');
            createNoteModal.style.display = 'none'; // Sembunyikan modal setelah menyimpan
            document.querySelector('.note-editor').innerHTML = ''; // Kosongkan editor
        } else {
            alert('Error saving note');
        }
        });

    });
})