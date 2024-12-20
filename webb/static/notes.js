document.addEventListener('DOMContentLoaded', function() {
    const noteImages = document.querySelectorAll('.note-image');
    const noteImagesGrouped = document.querySelectorAll('.note-image-grouped');
    const createNoteModal = document.querySelector('.create-note-modal');
    const closeModalBtn = document.querySelector('.close-modal-btn');
    const saveNoteBtn = document.querySelector('.save-note-btn');
    const modalTitle = document.querySelector('.modal-title'); // Ambil elemen judul modal
    const delete_content = document.querySelectorAll('.delete-btn2');
    const note = document.querySelector('.note-editor')

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
        note.value = ''; // Kosongkan textarea
    });

    // function add_notesContent(){
    //     table = contentnote.insertRow();

    // }

    // Menangani klik tombol save (tambahkan logika penyimpanan di sini)
    saveNoteBtn.addEventListener('click', function() {
        const photo = note.querySelectorAll('img');
        fetch('/save_note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "day": modalTitle.textContent.split(' ')[1],
            "content" : note.textContent,
            "photolist": Array.from(photo).map( pho => pho.src)
         }), // Kirim konten catatan sebagai JSON
        })
        .then(response => response.json())
        .then(data => {
        if (data.success) {
            alert(data.message);
            createNoteModal.style.display = 'none'; // Sembunyikan modal setelah menyimpan
            note.innerHTML = ''; // Kosongkan editor
            renderList();
        } else {
            alert(data.message);
        }
        });

    });
    renderList()
    async function renderList() {
        const response = await fetch('/get_notes')
        const data_notes = await response.json()
        const contentnote = document.getElementById('tabel-content')
        data_notes.forEach((data_note) =>{
            const row = contentnote.insertRow();
            const hari = row.insertCell(0);
            const isinote = row.insertCell(1);
            const photo = row.insertCell(2);
            const actionCell = row.insertCell(3);
            
        hari.innerHTML = data_note.day;
        isinote.innerHTML = data_note.content;
        data_note.photolist.forEach(img_src => {
            const photo_btn = document.createElement('button')
            const img_btn = document.createElement('img');
            img_btn.src = img_src;
            img_btn.style.width = '24px';
            img_btn.style.height = '24px';
            photo_btn.appendChild(img_btn);
            photo_btn.onclick = () =>{
                const modal = document.getElementById('image-show');
                modal.innerHTML = ''
                const image = document.createElement('img')
                image.src = img_src; 
                modal.appendChild(image);
                modal.style.display = "flex";
                const close_btn = document.createElement('button')
                close_btn.innerHTML = '&nbsp;X&nbsp;';
                close_btn.onclick = () =>{
                    modal.style.display = "none";
                }
                modal.appendChild(close_btn);
            }
            photo.appendChild(photo_btn);
        });
    
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn2';
        deleteBtn.innerText = 'Delete';
        deleteBtn.onclick = () => {
            fetch(`delete_note/${data_note.id}`)
            .then(response => response.json())
            .then(data => {
                if (data.success){
                    alert(data.message);
                    contentnote.deleteRow(row.rowIndex);
                }else{
                    alert(data.message);
                }
            })
        };
        actionCell.appendChild(deleteBtn);
        })
    }
})


// function addProject() {
//     const nama_Notes = document.getElementById('nama_Notes').value;
//     const Notesnya = document.getElementById('Notesnya').value;
    

//     if (nama_Notes && Notesnya) {
//         // save
//         fetch('/saveproject', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({
//                 // nama harus sesuai dengan di py nya
//                 projekname : projectName,
//                 session2 : sessionTime,
//             })
//         }).then(() => {
//             window.location.reload()
//         })

//         // Reset input form
//         document.getElementById('nama_Notes').value= '';
//         document.getElementById('Notesnya').value= '';
//     } else {
//         alert('Please fill in all fields');
//     }
// }