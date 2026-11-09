/**
 * repository.js — Logic JavaScript untuk halaman Master Repository Training
 * Dipisah dari template HTML untuk kemudahan maintenance
 */

$(document).ready(function () {

    // ── Inisialisasi DataTable ──────────────────────────────────────────────
    $('#repoTable').DataTable({
        pageLength: 10,
        language: {
            search:     'Cari Master Training:',
            lengthMenu: 'Tampilkan _MENU_ entri',
            paginate:   { previous: 'Sebelumnya', next: 'Selanjutnya' }
        }
    });

    // ── Submit: Tambah Master Training Baru ────────────────────────────────
    $('#addRepoForm').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            url:  '/add-repository',
            type: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                if (res.success) {
                    $('#addRepoModal').modal('hide');
                    Swal.fire({
                        title: 'Berhasil!',
                        text:  'Data berhasil ditambahkan ke Master Repository',
                        icon:  'success',
                        confirmButtonColor: '#0d6efd',
                        confirmButtonText:  'OK'
                    }).then(function (result) {
                        if (result.isConfirmed) location.reload();
                    });
                }
            },
            error: function (xhr) {
                var err = JSON.parse(xhr.responseText);
                $('#repo_alert_error').removeClass('d-none').text(err.message);
            }
        });
    });

    // ── Submit: Edit Master Training ───────────────────────────────────────
    $('#editRepoForm').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            url:  '/update-repository',
            type: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                if (res.success) {
                    Swal.fire({
                        title: 'Berhasil!',
                        text:  'Master Training berhasil diperbarui',
                        icon:  'success',
                        confirmButtonColor: '#ffc107',
                        confirmButtonText:  'OK'
                    }).then(function () { location.reload(); });
                }
            },
            error: function (xhr) {
                var err = JSON.parse(xhr.responseText);
                $('#edit_repo_alert_error').removeClass('d-none').text(err.message);
            }
        });
    });
});

// ── Buka Modal Edit Master Repository ──────────────────────────────────────
function openEditRepoModal(kode, nama, fungsi, id_fungsi, lvl_pos, id_lvl_pos,
                            lvl_train, id_lvl_train, comp, id_comp) {
    $('#edit_kode_training').val(kode);
    $('#edit_nama_training').val(nama);
    $('#edit_fungsi').val(fungsi);
    $('#edit_id_fungsi').val(id_fungsi);
    $('#edit_level_posisi').val(lvl_pos);
    $('#edit_id_level_posisi').val(id_lvl_pos);
    $('#edit_level_training').val(lvl_train);
    $('#edit_id_level_training').val(id_lvl_train);
    $('#edit_competency').val(comp);
    $('#edit_id_competency_level').val(id_comp);
    $('#edit_repo_alert_error').addClass('d-none');
    new bootstrap.Modal(document.getElementById('editRepoModal')).show();
}

// ── Konfirmasi Hapus Master Repository ─────────────────────────────────────
function confirmDeleteRepo(kode, nama) {
    if (confirm('Apakah Anda yakin ingin menghapus Master Training [' + kode + ' - ' + nama + ']?\n\nCatatan: Semua jadwal batch COE yang berhubungan juga akan terhapus.')) {
        $.post('/delete-repository/' + kode, function (res) {
            if (res.success) location.reload();
        }).fail(function (xhr) {
            var err = JSON.parse(xhr.responseText);
            alert('Gagal menghapus: ' + err.message);
        });
    }
}
