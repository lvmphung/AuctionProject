from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/AuctionProject'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    start_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    items = db.relationship('Item', backref='user', lazy=True)


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False)
    bid_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


db.drop_all()
db.create_all()
db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.form:
        user = User(username=request.form.get("username"), password=request.form.get("password"),
                    created_at=datetime.now())
        db.session.add(user)
        db.session.commit()
        return render_template("index.html")
    else:
        users = User.query.all()
        return render_template('signup.html', users=users)


@app.route('/items', methods=["GET", "POST"])
def item():
    if request.form:
        item = Item(name=request.form.get("name"), description=request.form.get("description"),
                    created_at=datetime.now(), start_time=request.form.get("start_time"),
                    created_by=request.form.get("created_by"),
                    )
        db.session.add(item)
        db.session.commit()
        return render_template("index.html")
    else:
        items = Item.query.all()
        return render_template('item.html', items=items)


@app.route('/bids', methods=["GET", "POST"])
def bid():
    if request.form:
        bid = Bid(price=request.form.get("price"), bid_by=request.form.get("bid_by"),
                  created_at=datetime.now(), item_id=request.form.get("item_id")
                  )
        db.session.add(bid)
        db.session.commit()
        return render_template("index.html")
    else:
        bids = Bid.query.all()
        return render_template('bid.html', bids=bids)


@app.route('/showbid', methods=["GET", "POST"])
def showbid():
    if request.form:
        bids = Bid.query.filter_by(item_id=int(request.form.get("item_id"))).order_by("price desc")
        return render_template('showbid.html', bids=bids)
    else:
        return render_template('showbid.html')


if __name__ == '__main__':
    app.run(debug=True)
