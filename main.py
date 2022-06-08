from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

BEER_CHOICES = ['-', '🍺', '🍺🍺', '🍺🍺🍺️', '🍺🍺🍺🍺', '🍺🍺🍺🍺🍺']
OUTSIDE_CHOICES = ['-', '✅', '❌']
FOOSBALL_CHOICES = ['-', '✅', '❌']
RATING_CHOICES = ['-', '⭐️', '⭐️⭐️', '⭐️⭐️⭐️', '⭐️⭐️⭐️⭐️', '⭐️⭐️⭐️⭐️⭐️']

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL_QL", "sqlite:///pubs_bars.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class PubsBars(db.Model):
    __tablename__ = "pubs_bars"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    url = db.Column(db.String(250), nullable=False)
    open_time = db.Column(db.String(250), nullable=False)
    close_time = db.Column(db.String(250), nullable=False)
    beer_rating = db.Column(db.String(250), nullable=False)
    outside_tables = db.Column(db.String(250), nullable=False)
    foosball = db.Column(db.String(250), nullable=False)
    overall_rating = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

#db.create_all()


class AddForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    url = StringField(label='Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField(label='Opening Time e.g. 5PM', validators=[DataRequired()])
    close_time = StringField(label='Closing Time e.g. 2:30AM', validators=[DataRequired()])
    beer_rating = SelectField(label='Beer Rating', choices=BEER_CHOICES, validators=[DataRequired()])
    outside_tables = SelectField(label='Outside Tables', choices=OUTSIDE_CHOICES, validators=[DataRequired()])
    foosball = SelectField(label='Foosball', choices=FOOSBALL_CHOICES, validators=[DataRequired()])
    overall_rating = SelectField(label='Overall Rating', choices=RATING_CHOICES, validators=[DataRequired()])
    submit = SubmitField(label='Submit')


# Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_place():
    form = AddForm()
    if form.validate_on_submit():
        new_place = PubsBars(
            name=form.name.data,
            url=form.url.data,
            open_time=form.open_time.data,
            close_time=form.close_time.data,
            beer_rating=form.beer_rating.data,
            outside_tables=form.outside_tables.data,
            foosball=form.foosball.data,
            overall_rating=form.overall_rating.data,
        )
        db.session.add(new_place)
        db.session.commit()
        return redirect(url_for('pubs_bars'))
    return render_template('add.html', form=form)


@app.route('/pubs-bars')
def pubs_bars():
    places = PubsBars.query.all()
    return render_template('pubs_bars.html', places=places)


# API endpoints below
# Get all places
@app.route("/all-pubs-bars")
def get_all():
    results = []
    all_pubs_bars = db.session.query(PubsBars).all()
    print(all_pubs_bars)
    for each in all_pubs_bars:
        results.append(each.to_dict())
    return jsonify(places=results)


# Get places with specified parameters
@app.route("/search")
def search():
    all_pubs_bars = db.session.query(PubsBars).all()
    results = all_pubs_bars.copy()

    if request.args.get("foosball") == "1":
        for each in all_pubs_bars:
            if each.foosball != "✅":
                results.remove(each)
    all_pubs_bars = results.copy()
    if request.args.get("outdoor") == "1":
        for each in all_pubs_bars:
            if each.outside_tables != "✅":
                results.remove(each)
    all_pubs_bars = results.copy()
    if request.args.get("best-beer") == "1":
        for each in all_pubs_bars:
            if each.beer_rating != "🍺🍺🍺🍺🍺":
                results.remove(each)

    results = [each.to_dict() for each in results]
    if len(results) != 0:
        return jsonify(places=results)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a Pub or a Bar that matches all your criteria in our "
                                           "database."}), 404


# Update beer rating and/or overall rating
@app.route("/update/<int:place_id>", methods=["PATCH"])
def update(place_id):
    api_key = request.args.get("api-key")
    place = db.session.query(PubsBars).get(place_id)
    if api_key == os.environ.get('API_KEY'):
        if place:
            if request.args.get("new-beer-rating"):
                place.beer_rating = request.args.get("new-beer-rating")
            if request.args.get("new-overall-rating"):
                place.overall_rating = request.args.get("new-overall-rating")
            db.session.commit()
            return jsonify(response={"Success": "Successfully updated Pub or Bar info."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry, no Pub or Bar with that id found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct API key."}), 403


# Delete a place from database
@app.route("/delete/<int:place_id>", methods=["DELETE"])
def delete(place_id):
    api_key = request.args.get("api-key")
    if api_key == os.environ.get('API_KEY'):
        place = PubsBars.query.get(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
            return jsonify(response={"Success": "Successfully deleted the Pub or Bar from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry, no Pub or Bar with that id found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct API key."}), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
