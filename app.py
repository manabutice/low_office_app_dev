from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    date = db.Column(db.String(10))
    time = db.Column(db.String(5))

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']

        new_reservation = Reservation(name=name, email=email, date=date, time=time)
        db.session.add(new_reservation)
        db.session.commit()

        return redirect(url_for('confirm', id=new_reservation.id))

    return render_template('form.html')

@app.route('/confirm')
def confirm():
    reservation_id = request.args.get('id')
    reservation = Reservation.query.get(reservation_id)
    return render_template('confirm.html', reservation=reservation)

@app.route('/reservations')
def reservations():
    all_reservations = Reservation.query.all()
    return render_template('reservations.html', reservations=all_reservations)
# エラーのため追加
@app.route('/submit', methods=['POST'])
def submit():
    # 予約送信の処理
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']

    new_reservation = Reservation(name=name, email=email, date=date, time=time)
    db.session.add(new_reservation)
    db.session.commit()

    return redirect(url_for('confirm', id=new_reservation.id))
# 登録されたユーザーの一覧を表示
@app.route('/users')
def users():
    all_users = Reservation.query.all()
    return render_template('users.html', users=all_users)

def method_name():
    pass
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
