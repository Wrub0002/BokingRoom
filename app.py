from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    features = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    slot = db.Column(db.String(50), nullable=False)

def create_dummy_data():
    if Room.query.count() == 0:
        rooms = [
            Room(name="Deluxe Room", image_url="room1.jpg", features="WiFi, TV, AC", price=50.00),
            Room(name="Suite", image_url="room2.jpg", features="WiFi, TV, AC, Mini Bar", price=80.00)
        ]
        db.session.add_all(rooms)
        db.session.commit()

@app.route('/')
def home():
    rooms = Room.query.all()
    return render_template('index.html', rooms=rooms)

@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        date = request.form['date']
        slot = request.form['slot']
        new_booking = Booking(room_id=room_id, date=date, slot=slot)
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('book.html', room=room)

@app.route('/success')
def success():
    return "Booking successful! Your room is reserved."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_dummy_data()
    app.run(debug=True)
