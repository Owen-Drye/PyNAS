import os
import shutil
from flask import Flask, render_template, url_for, send_from_directory, redirect, request, flash
from flask_headers import headers
import mimetypes

app = Flask(__name__)

app.config['DIRECTORY'] = "files"
app.config['SECRET_KEY'] = os.urandom(24)

extensions_dict = {'aac': 'Windows audio file', 'adt': 'Windows audio file', 'adts': 'Windows audio file',
                   'accdb': 'Microsoft Access database file', 'accde': 'Microsoft Access execute-only file',
                   'accdr': 'Microsoft Access runtime database', 'accdt': 'Microsoft Access database template',
                   'aif': 'Audio Interchange File format file', 'aifc': 'Audio Interchange File format file',
                   'aiff': 'Audio Interchange File format file', 'aspx': 'ASP.NET Active Server page',
                   'avi': 'Audio Video Interleave movie or sound file', 'bat': 'PC batch file',
                   'bin': 'Binary compressed file', 'bmp': 'Bitmap file', 'cab': 'Windows Cabinet file',
                   'cda': 'CD Audio Track', 'csv': 'Comma-separated values file',
                   'dif': 'Spreadsheet data interchange format file', 'dll': 'Dynamic Link Library file',
                   'doc': 'Microsoft Word document before Word 2007', 'docm': 'Microsoft Word macro-enabled document',
                   'docx': 'Microsoft Word document', 'dot': 'Microsoft Word template before Word 2007',
                   'dotx': 'Microsoft Word template',
                   'eml': 'Email file created by Outlook Express, Windows Live Mail, and other programs',
                   'eps': 'Encapsulated Postscript file', 'exe': 'Executable program file',
                   'flv': 'Flash-compatible video file', 'gif': 'Graphical Interchange Format file',
                   'htm': 'Hypertext markup language page', 'html': 'Hypertext markup language page',
                   'ini': 'Windows initialization configuration file', 'iso': 'ISO-9660 disc image',
                   'jar': 'Java architecture file', 'jpg': 'Joint Photographic Experts Group photo file',
                   'jpeg': 'Joint Photographic Experts Group photo file', 'm4a': 'MPEG-4 audio file',
                   'mdb': 'Microsoft Access database before Access 2007',
                   'mid': 'Musical Instrument Digital Interface file',
                   'midi': 'Musical Instrument Digital Interface file', 'mov': 'Apple QuickTime movie file',
                   'mp3': 'MPEG layer 3 audio file', 'mp4': 'MPEG 4 video',
                   'mpeg': 'Moving Picture Experts Group movie file', 'mpg': 'MPEG 1 system stream',
                   'msi': 'Microsoft installer file', 'mui': 'Multilingual User Interface file',
                   'pdf': 'Portable Document Format file', 'png': 'Portable Network Graphics file',
                   'pot': 'Microsoft PowerPoint template before PowerPoint 2007',
                   'potm': 'Microsoft PowerPoint macro-enabled template', 'potx': 'Microsoft PowerPoint template',
                   'ppam': 'Microsoft PowerPoint add-in',
                   'pps': 'Microsoft PowerPoint slideshow before PowerPoint 2007',
                   'ppsm': 'Microsoft PowerPoint macro-enabled slideshow', 'ppsx': 'Microsoft PowerPoint slideshow',
                   'ppt': 'Microsoft PowerPoint format before PowerPoint 2007',
                   'pptm': 'Microsoft PowerPoint macro-enabled presentation',
                   'pptx': 'Microsoft PowerPoint presentation', 'psd': 'Adobe Photoshop file',
                   'pst': 'Outlook data store', 'pub': 'Microsoft Publisher file',
                   'rar': 'Roshal Archive compressed file', 'rtf': 'Rich Text Format file',
                   'sldm': 'Microsoft PowerPoint macro-enabled slide', 'sldx': 'Microsoft PowerPoint slide',
                   'swf': 'Shockwave Flash file', 'sys': 'Microsoft DOS and Windows system settings and variables file',
                   'tif': 'Tagged Image Format file', ' tiff': 'Tagged Image Format file', 'tmp': 'Temporary data file',
                   'txt': 'Unformatted text file', 'vob': 'Video object file',
                   'vsd': 'Microsoft Visio drawing before Visio 2013', 'vsdm': 'Microsoft Visio macro-enabled drawing',
                   'vsdx': 'Microsoft Visio drawing file', 'vss': 'Microsoft Visio stencil before Visio 2013',
                   'vssm': 'Microsoft Visio macro-enabled stencil', 'vst': 'Microsoft Visio template before Visio 2013',
                   'vstm': 'Microsoft Visio macro-enabled template', 'vstx': 'Microsoft Visio template',
                   'wav': 'Wave audio file', 'wbk': 'Microsoft Word backup document', 'wks': 'Microsoft Works file',
                   'wma': 'Windows Media Audio file', 'wmd': 'Windows Media Download file',
                   'wmv': 'Windows Media Video file', 'wmz': 'Windows Media skins file',
                   'wms': 'Windows Media skins file', 'wpd': 'WordPerfect document', ' wp5': 'WordPerfect document',
                   'xla': 'Microsoft Excel add-in or macro file', 'xlam': 'Microsoft Excel add-in after Excel 2007',
                   'xll': 'Microsoft Excel DLL-based add-in', 'xlm': 'Microsoft Excel macro before Excel 2007',
                   'xls': 'Microsoft Excel workbook before Excel 2007',
                   'xlsm': 'Microsoft Excel macro-enabled workbook after Excel 2007',
                   'xlsx': 'Microsoft Excel workbook after Excel 2007',
                   'xlt': 'Microsoft Excel template before Excel 2007',
                   'xltm': 'Microsoft Excel macro-enabled template after Excel 2007',
                   'xltx': 'Microsoft Excel template after Excel 2007', 'xps': 'XML-based document',
                   'zip': 'Compressed file', 'py': "Python File"}


def get_files(directory):
    files_paths = []
    directory_paths = []

    for filename in os.listdir(directory):
        if os.path.isdir(f"{directory}/{filename}"):
            directory_paths.append(f'{filename}')
        else:
            files_paths.append(f'{filename}')

    return files_paths, directory_paths


@app.route("/storage", methods=['GET', 'POST'])
def storage():
    return render_template('index.html', files=get_files(f"{app.config['DIRECTORY']}"), extensions_dict=extensions_dict,
                           root='')


@app.route("/storage/<path:path>")
def storage_folder(path):
    try:
        return render_template('index.html', files=get_files(f"{app.config['DIRECTORY']}/{path}"),
                               extensions_dict=extensions_dict, root=path)
    except FileNotFoundError:
        return redirect(url_for('storage'))


@app.route("/file/<path:filename>")
def download(filename):
    return send_from_directory(directory=app.config['DIRECTORY'], path=filename)


@app.route("/file-preview/<path:filename>")
def preview(filename):
    for i in os.listdir("static/buffer"):
        os.remove("static/buffer/" + i)

    buffer_file_path = f"static/buffer/{filename.split('/')[-1]}"
    shutil.copy(f"{app.config['DIRECTORY']}/{filename}", buffer_file_path)

    return render_template('preview.html', filename=buffer_file_path.replace('static/', ''))


@app.route('/upload/<path:current_url>', methods=["GET", "POST"])
def file_upload(current_url):
    if request.method == "POST":
        file = request.files['file']

        new_filename = file.filename
        num = 1
        if file:
            while new_filename in os.listdir(app.config['DIRECTORY'] + current_url.replace('storage', '')):

                if file.filename.split('.')[0] != file.filename:
                    new_filename = file.filename.split('.')[0] + ' copy' + f".{file.filename.split('.')[1]}"

                else:
                    new_filename = file.filename + ' copy'

            file.save(app.config['DIRECTORY'] + current_url.replace('storage', '') + '/' + new_filename)

        return redirect(request.referrer)


@app.route('/delete/<path:current_url>', methods=["GET", "POST"])
def delete_files(current_url):
    if request.method == "POST":
        dir_path = current_url.replace('storage', app.config['DIRECTORY'])

        for f in get_files(dir_path)[0]:

            file_path = current_url.replace('storage', app.config['DIRECTORY']) + '/' + f
            form_id = file_path.replace('files/', '')

            if request.form.get(form_id) == 'on':
                os.remove(file_path)

        for directory in get_files(dir_path)[1]:

            dir_path = current_url.replace('storage', app.config['DIRECTORY']) + '/' + directory
            form_id = dir_path.replace('files/', '')

            if request.form.get(form_id) == 'on':
                shutil.rmtree(dir_path)

    return redirect(request.referrer)


@app.route('/new-folder/<path:dir_path>', methods=["GET", "POST"])
def new_folder(dir_path):
    if request.method == 'POST':
        dir_name = request.form.get('dir_name')
        if dir_name != '':
            os.mkdir(dir_path.replace('storage', app.config['DIRECTORY'] + '/') + '/' + dir_name)

    return redirect(request.referrer)


@app.route('/rename/<path:file_path>', methods=["GET", "POST"])
def rename(file_path):
    if request.method == 'POST':
        new_file_name = request.form.get('file_name')
        real_file_path = file_path.replace('storage', app.config['DIRECTORY'])
        current_file_name = real_file_path.split('/')[-1]
        extension = os.path.splitext(current_file_name)[1]

        if new_file_name != '':
            try:
                os.rename(real_file_path, real_file_path.replace(current_file_name, new_file_name + extension))
            except FileExistsError:
                flash('File exists, choose a different name')

    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
