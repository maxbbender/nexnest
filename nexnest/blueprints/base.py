from flask import Blueprint, send_from_directory

base = Blueprint('base', __name__, template_folder='../templates/base')


@base.route('/uploads/<path:path>')
def serve_upload(path):
    # print(path)
    return send_from_directory('uploads/', path)
