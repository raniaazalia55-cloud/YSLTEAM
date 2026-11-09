from flask import Blueprint, render_template, request, jsonify
from ..models import training as training_model
from ..utils.decorators import login_required, hcd_required

repository_bp = Blueprint('repository', __name__)


@repository_bp.route('/repository')
@login_required
def repository():
    try:
        master_data = training_model.get_all_repository()
    except Exception as e:
        return f'<h3>Terjadi Error Database:</h3><p>{str(e)}</p>'

    return render_template('repository.html', master_data=master_data, current_page='repository')


@repository_bp.route('/add-repository', methods=['POST'])
@hcd_required
def add_repository():
    try:
        kode         = request.form.get('kode_training')
        nama         = request.form.get('nama_training')
        fungsi       = request.form.get('fungsi', '-')
        id_fungsi    = request.form.get('id_fungsi', '-')
        lvl_pos      = request.form.get('level_posisi', '-')
        id_lvl_pos   = request.form.get('id_level_posisi', '-')
        lvl_train    = request.form.get('level_training', 'Teknis')
        id_lvl_train = request.form.get('id_level_training', '-')
        comp         = request.form.get('competency', '-')
        id_comp      = request.form.get('id_competency_level', '-')

        training_model.add_repository(
            kode, nama, fungsi, id_fungsi, lvl_pos, id_lvl_pos,
            lvl_train, id_lvl_train, comp, id_comp
        )
        return jsonify({'success': True, 'message': 'Master Training baru berhasil disimpan di Repository!'})
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@repository_bp.route('/update-repository', methods=['POST'])
@hcd_required
def update_repository():
    """Route ini sebelumnya TIDAK ADA di app.py lama — sekarang sudah diperbaiki."""
    try:
        kode         = request.form.get('kode_training')
        nama         = request.form.get('nama_training')
        fungsi       = request.form.get('fungsi', '-')
        id_fungsi    = request.form.get('id_fungsi', '-')
        lvl_pos      = request.form.get('level_posisi', '-')
        id_lvl_pos   = request.form.get('id_level_posisi', '-')
        lvl_train    = request.form.get('level_training', 'Teknis')
        id_lvl_train = request.form.get('id_level_training', '-')
        comp         = request.form.get('competency', '-')
        id_comp      = request.form.get('id_competency_level', '-')

        training_model.update_repository(
            kode, nama, fungsi, id_fungsi, lvl_pos, id_lvl_pos,
            lvl_train, id_lvl_train, comp, id_comp
        )
        return jsonify({'success': True, 'message': 'Master Training berhasil diperbarui!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@repository_bp.route('/delete-repository/<string:kode_training>', methods=['POST'])
@hcd_required
def delete_repository(kode_training):
    try:
        training_model.delete_repository(kode_training)
        return jsonify({
            'success': True,
            'message': f'Master Training {kode_training} berhasil dihapus dari Repository!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
