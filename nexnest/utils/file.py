from nexnest import app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def isPDF(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() == 'pdf'
