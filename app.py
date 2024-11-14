from flask import Flask, render_template, request, redirect, url_for
import os

# create a flask application instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory where uploaded files are saved

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/') # define a route to the homepage (ie the root url)
def home():
    query = None  # initialize query variable
    if request.method == 'POST':  # check if the request method is POST
        query = request.form.get('query')  # retrieve the 'query' from the form data
    return render_template('index.html', query=query)  # pass the query to the template

@app.route('/upload', methods=['GET', 'POST'])  # define a route for the upload page
def upload():
    if request.method == 'POST':  # if the request method is POST, handle the file upload
        file = request.files.get('file')  # get the file from the request
        # check if a file is uploaded and if it has a PDF extension
        if file and file.filename.endswith('.pdf'):
            # save the file to the specified upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # after uploading, redirect to the homepage
            return redirect(url_for('home'))
    # render the upload page when the request method is GET
    return render_template('upload.html')

# run the app when this file is executed directly
# accessible locally at: http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=True)
<<<<<<< HEAD

"""
Used chatgpt to see what would need to be changed to allow for textbox
@app.route('/', methods=['GET', 'POST'])  # allow both GET and POST requests
def home():
    query = None  # initialize query variable
    if request.method == 'POST':  # check if the request method is POST
        query = request.form.get('query')  # retrieve the 'query' from the form data
    return render_template('index.html', query=query)  # pass the query to the template

# run the app when this file is executed directly
# accessible locally at: http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=True)
"""
=======
>>>>>>> 0d644771f9d09076317110ecb2f8f499611bbb50
