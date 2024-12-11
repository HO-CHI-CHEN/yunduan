from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# 預設圖片上傳資料夾
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 設定允許的檔案格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 檢查檔案格式是否允許
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 主頁面，顯示圖片上傳表單
@app.route('/')
def upload_form():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Image Upload</title>
        </head>
        <body>
            <h1>Upload an image to get a hello message</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file">
                <button type="submit">Upload</button>
            </form>
        </body>
        </html>
    ''')


# 處理圖片上傳的 POST 請求
@app.route('/', methods=['POST'])
def upload_image():
    # 檢查是否有檔案
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    # 檢查檔案是否有名稱
    if file.filename == '':
        return 'No selected file'

    # 檢查檔案格式是否允許
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return 'hello'  # 返回 "hello" 訊息

    return 'Invalid file format'


if __name__ == '__main__':
    # 如果資料夾不存在，創建它
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(host='0.0.0.0', port=5000)
