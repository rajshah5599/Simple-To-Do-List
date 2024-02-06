from flask import Flask, render_template, request, redirect, url_for
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os

app = Flask(__name__)
executor = ThreadPoolExecutor()

# Create a 'data' folder if it doesn't exist
data_folder = 'data'
os.makedirs(data_folder, exist_ok=True)

def process_text_background(text, user):
    # Get the current time in hh:mm:ss format
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # Create the file name with the format hh:mm:ss_user.txt and include the 'data' folder
    file_name = os.path.join(data_folder, f'{current_time}_{user}.txt')
    
    # Pad the text to make it 512 bytes
    padded_text = text.ljust(512, ' ')
    
    # Write the padded text to the file
    with open(file_name, 'w') as file:
        file.write(padded_text)

@app.route('/')
def index():
    # Read all text files in the 'data' folder
    file_contents = []
    for file_name in os.listdir(data_folder):
        if file_name.endswith('.txt'):
            with open(os.path.join(data_folder, file_name), 'r') as file:
                content = file.read()
                user = file_name.split('_')[-1].split('.')[0]
                file_contents.append({'user': user, 'file_name': file_name, 'content': content})

    return render_template('index.html', file_contents=file_contents)

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        text_input = request.form['text']
        user_identifier = request.form['user']  # Assuming user identifier is submitted in the form
        # Start a background task to process the text
        executor.submit(process_text_background, text_input, user_identifier)
        return redirect(url_for('index'))  # Redirect to the index page

@app.route('/deleteFile', methods=['POST'])
def delete_file():
    file_name = request.form['file_name']
    file_path = os.path.join(data_folder, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return 'File deleted successfully'
    else:
        return 'File not found', 404


if __name__ == '__main__':
    app.run(debug=True)