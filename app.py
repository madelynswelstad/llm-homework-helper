from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

# create a flask application instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory where uploaded files are saved

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Dictionary to store class titles as keys and lists of file paths as values
class_files = {}

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

# create a flask application instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory where uploaded files are saved

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Dictionary to store class titles as keys and lists of file paths as values
class_files = {}

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
        class_title = request.form.get('class_title', 'No Class Assigned')  # get the class title
        # Ensure the class title key exists in the dictionary
        if class_title not in class_files:
            class_files[class_title] = []
        # Save the file if it has a PDF extension
        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            class_files[class_title].append(file.filename)  # Add the file under the class title
            return redirect(url_for('upload'))  # Redirect to the upload page after submission
    return render_template('upload.html', class_files=class_files)

@app.route('/delete/<class_title>/<filename>', methods=['POST'])  # define a route to handle file deletion
def delete_file(class_title, filename):
    # Construct the file path
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Remove the file from the dictionary and delete it from disk
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the file from the uploads directory
    if class_title in class_files and filename in class_files[class_title]:
        class_files[class_title].remove(filename)  # Remove the file reference from the dictionary
        # If the class has no files left, remove the class key
        if not class_files[class_title]:
            del class_files[class_title]
    return redirect(url_for('upload'))  # Redirect back to the upload page


# run the app when this file is executed directly
# accessible locally at: http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=True)
    