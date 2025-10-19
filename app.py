from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bicycles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Bicycle model
class Bicycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    wheel_size = db.Column(db.String(50))
    suspension = db.Column(db.String(50))
    frame = db.Column(db.String(100))
    fork = db.Column(db.String(100))
    transmission = db.Column(db.String(100))
    brakes = db.Column(db.String(100))
    cranks = db.Column(db.String(100))
    price = db.Column(db.String(50))
    pros = db.Column(db.Text)
    cons = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    image_url = db.Column(db.String(255))

# ✅ Create DB and seed only if empty
with app.app_context():
    db.create_all()

    if Bicycle.query.count() == 0:  # 👈 this prevents duplicate rows
        df = pd.read_csv("bicycles.csv")
        for _, row in df.iterrows():
            bicycle = Bicycle(
                brand=row["Производитель"],
                model=row["Модель"],
                wheel_size=row["Размер колес"],
                suspension=row["Подвеска"],
                frame=row["Рама"],
                fork=row["Вилка"],
                transmission=row["Трансмиссия"],
                brakes=row["Тормозная система"],
                cranks=row["Шатуны"],
                price=row["Цена"],
                pros=row["Плюсы"],
                cons=row["Минусы"],
                recommendation=row["Порекомендуете ли вы данный продукт?"],
                image_url=row["Ссылка на фото"]
            )
            db.session.add(bicycle)
        db.session.commit()
        print("✅ Database seeded from bicycles.csv")
    else:
        print("✅ Database already has data, skipping CSV import.")

@app.route('/')
def index():
    bicycles = Bicycle.query.all()
    return render_template('index.html', bicycles=bicycles)

if __name__ == '__main__':
    app.run(debug=True)
