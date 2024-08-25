from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = '###'  #provide your mail username ex : mine was = tharun132213@gmail.com 
app.config['MAIL_PASSWORD'] = '####' # provide your app password ,you have to create it on your google apps ex for mine : uxtz stck **** ****          
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'tharun132213@gmail.com'  



mail = Mail(app)



UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'zip', 'pdf', 'docx', 'pptx','folders'}






def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       email TEXT NOT NULL,
                       project_title TEXT NOT NULL,
                       description TEXT NOT NULL,
                       file_path TEXT,
                       link TEXT,
                       submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_project', methods=['POST'])
def submit_project():
    name = request.form['name']
    email = request.form['email']
    project_title = request.form['project_title']
    Intern_ID = request.form['Intern_ID']
    description = request.form['description']
    file = request.files['file']
    link = request.form.get('link') 
    file_path = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projects (name, email, project_title,Intern_Id, description, file_path, link) VALUES (?, ?, ?, ?, ?, ?,?)',
                   (name, email, project_title,Intern_ID, description, file_path, link))
    conn.commit()
    conn.close()

    



    msg = Message('Project Submission Confirmation', recipients=[email])
    msg.body = f" INTERN ID : {Intern_ID}      Dear {name},\n\nThank you for submitting your project titled '{project_title}'. We have received your submission and will review it shortly.\n\nBest regards,\nProject Team"
    mail.send(msg)

    flash('Project submitted successfully and email confirmation sent.', 'success')
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)
