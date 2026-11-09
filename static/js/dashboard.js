/**
 * dashboard.js — Logic JavaScript untuk halaman Integrated Database Training
 * Dipisah dari template HTML untuk kemudahan maintenance
 */

$(document).ready(function () {

    // ── Inisialisasi DataTable ──────────────────────────────────────────────
    var table = $('#trainingTable').DataTable({
        pageLength: 10,
        lengthMenu: [5, 10, 25, 50],
        language: {
            search:     'Cari Global:',
            lengthMenu: 'Tampilkan _MENU_ entri',
            info:       'Showing _START_ to _END_ of _TOTAL_ entries',
            infoFiltered: '(filtered from _MAX_ total entries)',
            paginate:   { previous: 'Sebelumnya', next: 'Selanjutnya' }
        },
        initComplete: function () {
            // Dropdown filter untuk kolom Fungsi (index 1) dan Status Planning (index 15)
            this.api().columns([1, 15]).every(function () {
                var column = this;
                var select = $('<select class="form-select form-select-sm my-1"><option value="">-- Semua --</option></select>')
                    .appendTo($(column.header()))
                    .on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex($(this).val());
                        column.search(val ? '^' + val + '$' : '', true, false).draw();
                    });
                column.data().unique().sort().each(function (d) {
                    select.append('<option value="' + d + '">' + d + '</option>');
                });
            });
        }
    });

    // ── Submit: Tambah Jadwal Batch COE Baru ───────────────────────────────
    $('#addCoeForm').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            url:  '/add-coe-schedule',
            type: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                if (res.success) {
                    $('#addCoeModal').modal('hide');
                    Swal.fire({
                        title: 'Berhasil!',
                        text:  'Data batch COE baru berhasil ditambahkan',
                        icon:  'success',
                        confirmButtonColor: '#198754',
                        confirmButtonText:  'OK'
                    }).then(function (result) {
                        if (result.isConfirmed) location.reload();
                    });
                }
            },
            error: function (xhr) {
                var err = JSON.parse(xhr.responseText);
                $('#coe_alert_error').removeClass('d-none').text(err.message);
            }
        });
    });

    // ── Submit: Edit / Reschedule Jadwal COE ───────────────────────────────
    $('#editForm').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            url:  '/update-schedule',
            type: 'POST',
            data: $(this).serialize(),
            success: function (response) {
                if (response.success) location.reload();
            },
            error: function (xhr) {
                var err = JSON.parse(xhr.responseText);
                $('#alert_error').removeClass('d-none').text(err.message);
            }
        });
    });
});

// ── Buka Modal Edit ─────────────────────────────────────────────────────────
function openEditModal(id, kode, nama, batch, ren_m, ren_s, rea_m, rea_s, status) {
    $('#edit_id_coe').val(id);
    $('#edit_info_training').text(kode + ' - ' + nama + ' (' + batch + ')');
    $('#edit_ren_mulai').val(ren_m);
    $('#edit_ren_selesai').val(ren_s);
    $('#edit_rea_mulai').val(rea_m);
    $('#edit_rea_selesai').val(rea_s);
    $('#edit_status_coe').val(status);
    $('#alert_error').addClass('d-none');
    new bootstrap.Modal(document.getElementById('editModal')).show();
}

// ── Konfirmasi Hapus Jadwal COE ─────────────────────────────────────────────
function confirmDelete(id_coe) {
    if (confirm('Apakah Anda yakin ingin menghapus jadwal COE ini? Tindakan ini tidak dapat dibatalkan.')) {
        $.post('/delete-schedule/' + id_coe, function (res) {
            if (res.success) location.reload();
        });
    }
}
