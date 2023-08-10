import bcrypt
from flask import Flask, render_template, url_for, redirect, session, request
import db

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.secret_key='secret_key'
salt = bcrypt.gensalt()

@app.route('/')
def home():

    projects = [
        {"title": "A", "image":"https://images.unsplash.com/photo-1542395975-d6d3ddf91d6e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "source": "/"},
        {"title": "A", "image":"https://images.unsplash.com/photo-1542395975-d6d3ddf91d6e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "source": "/"},
        {"title": "A", "image":"https://images.unsplash.com/photo-1542395975-d6d3ddf91d6e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "source": "/"},
        {"title": "A", "image":"https://images.unsplash.com/photo-1542395975-d6d3ddf91d6e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "source": "/"},
        {"title": "A", "image":"https://images.unsplash.com/photo-1542395975-d6d3ddf91d6e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "source": "/"}
    ]
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('home.html', logged_in=True, projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    else:
        error = None

        if request.method == 'POST':
            try:
                email = request.form['email']
                password = request.form['password']
            except KeyError:
                error='Missing form input'

            if (email == "" or password == ""):
                error = 'Please fill all the fields'
            else:
                cxn = db.sqlite3.connect('credentials.db')
                cursor = cxn.cursor()
                cursor.execute('SELECT password_hash FROM users WHERE email = ?',(email,))
                result = cursor.fetchone()
                cxn.close()

                if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
                    session['email'] = email
                    return redirect(url_for('home'))
                else:
                    error = 'Invalid email or password'
        return render_template('login.html', error=error, logged_in=False)

@app.route('/register', methods=['GET', 'POST']) 
def register():
    if 'email' in session:
        return redirect(url_for('home'))
    else:
        error = None

        if request.method == 'POST':
            try:
                email = request.form['email']
                password = request.form['password']
            except KeyError:
                error = 'Missing form input'
                return render_template('register.html', error=error)
            if (email == "" or password == ""):
                error = 'Please fill all the fields'
            else:
                cxn = db.sqlite3.connect('credentials.db')
                cursor = cxn.cursor()
                cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
                result = cursor.fetchone()
                if result:
                    error = 'User already exists'
                else:
                    password_hash= bcrypt.hashpw(password.encode('utf-8'), salt)
                    cursor.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, password_hash))
                    cxn.commit()
                    cxn.close()
                    session['email'] = email
                    return redirect(url_for('home'))

        return render_template('register.html', error=error)

@app.route('/about')
def about():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('about.html', logged_in=True)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)