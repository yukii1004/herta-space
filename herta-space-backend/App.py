from flask import Flask, render_template, url_for, redirect, session, request
 
app = Flask(__name__)

@app.route('/')
def warp():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)