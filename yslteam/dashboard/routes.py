from flask import Blueprint, render_template, request, jsonify
from ..models import training as training_model
from ..models import coe as coe_model
from ..utils.decorators import login_required, hcd_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        rows = training_model.get_all_training_with_schedule()
        repository_list = training_model.get_repository_list()
    except Exception as e:
        return f'<h3>Terjadi Error Database:</h3><p>{str(e)}</p>'

    trainings = []
    for r in rows:
        rec = dict(r)
        if rec.get('tgl_realisasi_mulai') and rec.get('tgl_realisasi_selesai'):
            ren_m = str(rec['tgl_rencana_mulai'])
            rea_m = str(rec['tgl_realisasi_mulai'])
            ren_s = str(rec['tgl_rencana_selesai'])
            rea_s = str(rec['tgl_realisasi_selesai'])

            if ren_m == rea_m and ren_s == rea_s:
                rec['status_planning'] = 'Sesuai'
                rec['flag_class']      = 'bg-success text-white'
            else:
                rec['status_planning'] = 'Tidak Sesuai (Rescheduled)'
                rec['flag_class']      = 'bg-danger text-white'
        else:
            rec['status_planning'] = 'Belum Realisasi'
            rec['flag_class']      = 'bg-warning text-dark'
        trainings.append(rec)

    return render_template(
        'dashboard.html',
        trainings=trainings,
        repository_list=repository_list,
        current_page='dashboard'
    )


@dashboard_bp.route('/add-coe-schedule', methods=['POST'])
@hcd_required
def add_coe_schedule():
    try:
        kode       = request.form.get('kode_training_select')
        batch      = request.form.get('batch')
        ren_m      = request.form.get('tgl_rencana_mulai')
        ren_s      = request.form.get('tgl_rencana_selesai')
        partisipan = request.form.get('jumlah_partisipan', 0)
        pic        = request.form.get('pic', '-')
        status     = request.form.get('status_coe', 'Pending')

        if ren_s < ren_m:
            return jsonify({
                'success': False,
                'message': 'Tanggal Rencana Selesai tidak boleh lebih awal dari Rencana Mulai!'
            }), 400

        coe_model.add_coe_schedule(kode, batch, status, ren_m, ren_s, partisipan, pic)
        return jsonify({'success': True, 'message': 'Jadwal Batch COE berhasil ditambahkan!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@dashboard_bp.route('/update-schedule', methods=['POST'])
@hcd_required
def update_schedule():
    id_coe               = request.form.get('id_coe')
    tgl_realisasi_mulai  = request.form.get('tgl_realisasi_mulai')
    tgl_realisasi_selesai = request.form.get('tgl_realisasi_selesai')
    status_coe           = request.form.get('status_coe')

    if tgl_realisasi_mulai and tgl_realisasi_selesai:
        if tgl_realisasi_selesai < tgl_realisasi_mulai:
            return jsonify({
                'success': False,
                'message': 'Validasi Gagal: Tanggal Selesai tidak boleh lebih awal dari Tanggal Mulai!'
            }), 400

    try:
        coe_model.update_coe_schedule(id_coe, tgl_realisasi_mulai, tgl_realisasi_selesai, status_coe)
        return jsonify({'success': True, 'message': 'Jadwal berhasil diperbarui!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@dashboard_bp.route('/delete-schedule/<int:id_coe>', methods=['POST'])
@hcd_required
def delete_schedule(id_coe):
    try:
        coe_model.delete_coe_schedule(id_coe)
        return jsonify({'success': True, 'message': 'Jadwal COE berhasil dihapus.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
