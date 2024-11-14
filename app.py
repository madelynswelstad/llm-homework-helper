from flask import Flask, render_template, request

# create a flask application instance
app = Flask(__name__)
 
@app.route('/') # define a route to the homepage (ie the root url)
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