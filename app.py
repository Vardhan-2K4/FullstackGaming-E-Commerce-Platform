from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game/<game_name>')
def game_page(game_name):
    return render_template(f'{game_name}.html')

# New route to handle the form data
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # For this project, we just print the data to the terminal
        print(f"Form Submission Received:\nName: {name}\nEmail: {email}\nMessage: {message}")

        # Redirect to the success page
        return redirect(url_for('success'))

# New route to display the success page
@app.route('/success')
def success():
    return render_template('success.html')

# Sidebar demo routes mapped to navbar
@app.route('/left-sidebar')
def left_sidebar():
    return render_template('left-sidebar.html')

@app.route('/right-sidebar')
def right_sidebar():
    return render_template('right-sidebar.html')

@app.route('/no-sidebar')
def no_sidebar():
    return render_template('no-sidebar.html')

if __name__ == '__main__':
    app.run(debug=True)