import configparser
import boto3
from flask import Flask, render_template, request, redirect

# Configuración de AWS
config = configparser.ConfigParser()
config.read('config.ini')
s3 = boto3.client('s3',
                  aws_access_key_id=config['aws']['aws_access_key_id'],
                  aws_secret_access_key=config['aws']['aws_secret_access_key'])

# Configuración de Flask
app = Flask(__name__)

# index.html para listar las imágenes
@app.route('/')
def index():
    images = get_images_from_s3()
    return render_template('index.html', images=images)

# ruta POST para subir las imágenes
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        file = request.files['image']
        image_path = upload_image_to_s3(file)
        return redirect('/')
    return render_template('add.html')

# obtener las imágenes
def get_images_from_s3():
    bucket_name = 'lab09nubes2'
    response = s3.list_objects_v2(Bucket=bucket_name)
    images = []
    if 'Contents' in response:
        for obj in response['Contents']:
            image_path = f"https://{bucket_name}.s3.amazonaws.com/{obj['Key']}"
            images.append(image_path)
    return images

# subir imagen
def upload_image_to_s3(file):
    bucket_name = 'lab09nubes2'
    filename = file.filename
    s3.upload_fileobj(file, bucket_name, filename)
    image_path = f'https://{bucket_name}.s3.amazonaws.com/{filename}'
    return image_path

if __name__ == '__main__':
    app.run(debug=True)
