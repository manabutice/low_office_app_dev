from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションデータの暗号化に使用

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']

        if not name or not email or not date or not time:
            flash('すべてのフィールドを入力してください。')
            return redirect(url_for('form'))

        return redirect(url_for('confirm', name=name, email=email, date=date, time=time))

@app.route('/confirm')
def confirm():
    name = request.args.get('name')
    email = request.args.get('email')
    date = request.args.get('date')
    time = request.args.get('time')
    return render_template('confirm.html', name=name, email=email, date=date, time=time)

if __name__ == '__main__':
    app.run(debug=True)
