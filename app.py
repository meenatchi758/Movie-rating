from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

# Initialize DB
db = SQLAlchemy(app)

# ------------------ MODELS ------------------
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

# ------------------ FORMS ------------------
class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired()])
    rating = IntegerField('Rating (1 to 10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Submit')

# ------------------ ROUTES ------------------
@app.route('/')
def home():
    movies = Movie.query.order_by(Movie.rating.desc()).all()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        new_movie = Movie(
            title=form.title.data,
            director=form.director.data,
            rating=form.rating.data
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_movie.html', form=form)

@app.route('/delete/<int:id>')
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

# ------------------ MAIN ------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
