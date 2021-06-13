from flask import Flask, render_template, make_response, abort, request, url_for, redirect
import smtplib

from werkzeug.utils import redirect

from AzureDB import AzureDB

from flask_dance.contrib.github import make_github_blueprint, github
import secrets
import os

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
github_blueprint = make_github_blueprint(
    client_id="438c05d891ef57925e22",
    client_secret="76a99c755f5322f3500318bacb59fe6565509ab4")
app.register_blueprint(github_blueprint, url_prefix='/login')

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/aboutme')
def aboutme():
    return app.send_static_file('aboutme.html')


@app.route('/gallery')
def gallery():
    return app.send_static_file('gallery.html')


@app.route('/contact')
def contact():
    return app.send_static_file('contact.html')


@app.route('/error_denied')
def error_denied():
    abort(401)


@app.route('/error_internal')
def error_internal():
    return render_template('template.html', name='ERROR 505'), 505


@app.route('/error_not_found')
def error_not_found():
    response = make_response(render_template('template.html', name='ERROR 404'), 404)
    response.headers['X-Something'] = 'A value'
    return response


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.route('/form', methods=["POST"])
def form():
    email = request.form.get("email")
    description = request.form.get("description")

    message = "You have message"
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.starttls()
    server.login("address@email.com", "")
    server.sendmail("address@email.com", email, message, description)

    if not email or not description:
        error_statement = "All form fields required..."
        return render_template('contact.html')


@app.route('/guestbook')
def guestbook():
    with AzureDB() as a:
        data = a.azureGetData()
    return render_template('guestbook.html', data=data)


@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    text = request.form['text']
    date = request.form['date']
    with AzureDB()as b:
        b.azureAddData(name, text, date)
        data = b.azureGetData()
    return redirect(url_for('guestbook'))

    if __name__ == '__main__':
        app.run(debug=True)


@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    with AzureDB() as c:
        c.azureDeleteData(id)
    return redirect(url_for('guestbook'))

@app.route('/git-login')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
    if account_info.ok:
        account_info_json = account_info.json()
    return '<h1>Your Github name is {}'.format(account_info_json['login'])
    return render_template('index.html')
    return '<h1>Request failed!</h1>'

    if __name__ == "__main__":
        app.run(debug=True)