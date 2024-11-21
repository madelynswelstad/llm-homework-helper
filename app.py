from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import main
import openai
from openai import OpenAI

# create a flask application instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory where uploaded files are saved

collection_name = "llm-collection2.0"
currId = 0

# Initialize OpenAI client
openai_client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Dictionary to store class titles as keys and lists of file paths as values
class_files = {}
conversation_list = []

# home method is called when user loads root url, reloads page, or submits a form or performs an action
@app.route('/', methods=['GET', 'POST']) # define a route to the homepage (ie the root url) and call function below
def home():
    query = None
    response = None
    if request.method == 'POST':
        query = request.form.get('query')
        response = main.process_query(query)
        conversation_list.insert(0, [query, response])  # Save query and response 

    # check if collection already exists
    
    # main.find_collections(collection_name)

    # query = None  # initialize query variable
    # response = None  # initialize response variable for ChatGPT
    # if request.method == 'POST':  # check if the request method is POST (when data like forms or actions are sent to the server)
    #     query = request.form.get('query')  # retrieve the 'query' from the form data

    #     if query:  # If a query is provided
    #         print(query)
    #         Send the query to ChatGPT
    #         try:
    #             response = openai.chat.completions.create(
    #                 model="gpt-3.5-turbo",
    #                 messages=[{"role": "user", "content": "Your query here"}]
    #             ).choices[0].message.content
    #             queries.append({"query": query, "response": response})  # Save query and response
    #             print(response)
    #         except Exception as e:
    #             print(e)
    #             response = f"Error communicating with ChatGPT: {str(e)}"
    print(response)
    return render_template('index.html', conversation_list=conversation_list)  # pass queries for display

@app.route('/upload', methods=['GET', 'POST'])  # define a route for the upload page
def upload():
    global currId
    error_message = None  # Initialize the error message

    if request.method == 'POST':  # if the request method is POST, handle the file upload
        file = request.files.get('file')  # get the file from the request
        class_title = request.form.get('class_title', 'No Class Assigned')  # get the class title
        
        # if the class title key does not exist in the dictionary, add it
        if class_title not in class_files:
            class_files[class_title] = []
        
        # Save the file if it has a PDF extension
        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            class_files[class_title].append(file.filename)  # Add the file under the class title

            # Process and prepare the documents
            text_chunks = main.get_text_from_pdf(file_path)  # Get text as a list of strings
            documents = [{"id": i, "text": chunk} for i, chunk in enumerate(text_chunks, start=currId)]
            currId += len(documents) 

            # Insert documents into the collection
            main.insert_documents(documents, collection_name)

            return redirect(url_for('upload'))  # Redirect to the upload page after submission
        
        else:
            # Set the error message if the file is not a PDF
            error_message = "Incorrect file type. Please upload a PDF."

    return render_template('upload.html', class_files=class_files, error_message=error_message)

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

@app.route('/speech-to-text', methods=['GET'])
def call_speech():
    query = main.speech_to_text()
    print(query)
    return {"text": query}, 200
# run the app when this file is executed directly
# accessible locally at: http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=True)
