from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    date = db.Column(db.String(10))
    time = db.Column(db.String(5))

class ReservationForm(FlaskForm):
    name = StringField('名前', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired()])
    date = StringField('予約日', validators=[DataRequired()])
    time = StringField('予約時間', validators=[DataRequired()])
    submit = SubmitField('予約する')

@app.route('/', methods=['GET', 'POST'])
def form():
    form = ReservationForm()
    if form.validate_on_submit():
        new_reservation = Reservation(
            name=form.name.data, 
            email=form.email.data, 
            date=form.date.data, 
            time=form.time.data
        )
        db.session.add(new_reservation)
        db.session.commit()
        return redirect(url_for('confirm', id=new_reservation.id))
    return render_template('form.html', form=form)

@app.route('/confirm')
def confirm():
    reservation_id = request.args.get('id')
    reservation = Reservation.query.get(reservation_id)
    return render_template('confirm.html', reservation=reservation)

@app.route('/reservations')
def reservations():
    all_reservations = Reservation.query.all()
    return render_template('reservations.html', reservations=all_reservations)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']

    new_reservation = Reservation(name=name, email=email, date=date, time=time)
    db.session.add(new_reservation)
    db.session.commit()

    return redirect(url_for('confirm', id=new_reservation.id))

# @app.route('/users/<int:page_num>', defaults={'page_num': 1})
# @app.route('/users/<int:page_num>')
# def users(page_num):
#     all_users = Reservation.query.paginate(per_page=10, page=page_num, error_out=True)
#     return render_template('users.html', users=all_users)

@app.route('/users/<int:page_num>')
def users(page_num=1):
    users_pagination = Reservation.query.paginate(per_page=10, page=page_num, error_out=True)
    return render_template('users.html', users=users_pagination)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
