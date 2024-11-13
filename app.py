from flask import Flask, render_template, request

# create a flask application instance
app = Flask(__name__)
 
@app.route('/') # define a route to the homepage (ie the root url)
def home():
    return render_template('index.html') # renders an html template in the templates folder

# run the app when this file is executed directly
# accessible locally at: http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=True)