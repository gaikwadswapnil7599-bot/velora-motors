from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from pathlib import Path
from datetime import datetime
import secrets

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


CARS = [
    {"id": 1, "brand": "Ferrari", "name": "SF90 Stradale", "price": 72500000,
     "engine": "4.0L V8 Hybrid", "power": "986 HP", "zero": "2.5 sec", "speed": "340 km/h",
     "type": "Supercar",
     "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",
     "description": "A breathtaking hybrid supercar combining Ferrari V8 performance with advanced electric power."},
    {"id": 2, "brand": "Lamborghini", "name": "Revuelto", "price": 88900000,
     "engine": "6.5L V12 Hybrid", "power": "1,001 HP", "zero": "2.5 sec", "speed": "350 km/h",
     "type": "Supercar",
     "image": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&w=1200&q=80",
     "description": "A V12 hybrid flagship created for dramatic design, extreme performance and an unforgettable drive."},
    {"id": 3, "brand": "Porsche", "name": "911 GT3 RS", "price": 35000000,
     "engine": "4.0L Flat-6", "power": "525 HP", "zero": "3.2 sec", "speed": "296 km/h",
     "type": "Performance",
     "image": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1200&q=80",
     "description": "A road-legal performance icon engineered around aerodynamics, precision and driver connection."},
    {"id": 4, "brand": "McLaren", "name": "750S", "price": 59100000,
     "engine": "4.0L V8", "power": "750 PS", "zero": "2.8 sec", "speed": "332 km/h",
     "type": "Supercar",
     "image": "https://images.unsplash.com/photo-1553440569-bcc63803a83d?auto=format&fit=crop&w=1200&q=80",
     "description": "Lightweight engineering and explosive acceleration define this focused McLaren supercar."},
    {"id": 5, "brand": "Bugatti", "name": "Chiron", "price": 150000000,
     "engine": "8.0L W16", "power": "1,479 HP", "zero": "2.4 sec", "speed": "420 km/h",
     "type": "Supercar",
     "image": "https://images.unsplash.com/photo-1494905998402-395d579af36f?auto=format&fit=crop&w=1200&q=80",
     "description": "A hypercar icon that blends outrageous speed, engineering mastery and unmistakable presence."},
    {"id": 6, "brand": "Bentley", "name": "Continental GT", "price": 52300000,
     "engine": "4.0L V8 Hybrid", "power": "782 PS", "zero": "3.2 sec", "speed": "335 km/h",
     "type": "Grand Tourer",
     "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",
     "description": "A luxurious grand touring experience where handcrafted comfort meets effortless performance."},
    {"id": 7, "brand": "Toyota", "name": "Supra", "price": 36500000,
     "engine": "2.0L Turbo", "power": "382 HP", "zero": "3.9 sec", "speed": "250 km/h",
     "type": "Performance",
     "image": "https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?auto=format&fit=crop&w=1200&q=80",
     "description": "A modern legend blending classic rear-drive attitude with thrilling performance and sharp styling."},
    {"id": 8, "brand": "BMW", "name": "M5 CS", "price": 44500000,
     "engine": "4.4L V8 Twin-Turbo", "power": "627 HP", "zero": "3.4 sec", "speed": "250 km/h",
     "type": "Performance",
     "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1200&q=80",
     "description": "An executive performance sedan with brutal straight-line speed and daily-driver practicality."},
    {"id": 9, "brand": "Pagani", "name": "Huayra", "price": 96900000,
     "engine": "6.0L Twin-Turbo V12", "power": "764 HP", "zero": "3.3 sec", "speed": "350 km/h",
     "type": "Supercar",
     "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1200&q=80",
     "description": "A hand-built Italian masterpiece with exotic design, astonishing grip and an unmistakable presence."},
]


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            pincode TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            total INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Confirmed',
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            car_id INTEGER NOT NULL,
            car_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    """)
    conn.commit()
    conn.close()


def find_car(car_id):
    return next((car for car in CARS if car["id"] == car_id), None)


def cart_items():
    raw = session.get("cart", {})
    items = []
    total = 0
    for car_id, quantity in raw.items():
        car = find_car(int(car_id))
        if car:
            quantity = int(quantity)
            subtotal = car["price"] * quantity
            items.append({**car, "quantity": quantity, "subtotal": subtotal})
            total += subtotal
    return items, total


@app.context_processor
def globals_for_templates():
    items, total = cart_items()
    return {"cart_count": sum(i["quantity"] for i in items), "cart_total": total}


@app.route("/")
def index():
    return render_template("index.html", featured=CARS[:4])


@app.route("/shop")
def shop():
    q = request.args.get("q", "").strip().lower()
    brand = request.args.get("brand", "").strip()
    car_type = request.args.get("type", "").strip()
    sort = request.args.get("sort", "featured")

    results = CARS[:]
    if q:
        results = [
            c for c in results
            if q in f"{c['brand']} {c['name']} {c['type']}".lower()
        ]
    if brand:
        results = [c for c in results if c["brand"] == brand]
    if car_type:
        results = [c for c in results if c["type"] == car_type]

    if sort == "low":
        results.sort(key=lambda c: c["price"])
    elif sort == "high":
        results.sort(key=lambda c: c["price"], reverse=True)
    elif sort == "name":
        results.sort(key=lambda c: c["name"])

    brands = sorted({c["brand"] for c in CARS})
    types = sorted({c["type"] for c in CARS})
    return render_template("shop.html", cars_list=results, brands=brands, types=types,
                           q=request.args.get("q", ""), selected_brand=brand,
                           selected_type=car_type, selected_sort=sort)


@app.route("/product/<int:car_id>")
def product(car_id):
    car = find_car(car_id)
    if not car:
        return render_template("base.html", page_error="Vehicle not found."), 404
    return render_template("product.html", car=car)


@app.post("/cart/add/<int:car_id>")
def add_to_cart(car_id):
    if not find_car(car_id):
        return redirect(url_for("shop"))
    cart = session.get("cart", {})
    key = str(car_id)
    cart[key] = int(cart.get(key, 0)) + 1
    session["cart"] = cart
    return redirect(request.form.get("next") or url_for("cart"))


@app.get("/cart")
def cart():
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total)


@app.post("/cart/update")
def update_cart():
    cart = session.get("cart", {})
    for key, value in request.form.items():
        if key.startswith("qty_"):
            car_id = key[4:]
            try:
                qty = max(0, min(5, int(value)))
            except ValueError:
                qty = 1
            if qty == 0:
                cart.pop(car_id, None)
            else:
                cart[car_id] = qty
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.post("/cart/remove/<int:car_id>")
def remove_from_cart(car_id):
    cart = session.get("cart", {})
    cart.pop(str(car_id), None)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_items()
    if not items:
        return redirect(url_for("shop"))

    if request.method == "POST":
        required = ["name", "email", "phone", "address", "city", "state", "pincode", "payment"]
        data = {field: request.form.get(field, "").strip() for field in required}
        if not all(data.values()):
            return render_template("checkout.html", items=items, total=total, error="Please complete all required fields.")

        order_number = "VL-" + datetime.now().strftime("%Y%m%d") + "-" + secrets.token_hex(2).upper()
        conn = db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders
            (order_number, customer_name, email, phone, address, city, state, pincode,
             payment_method, total, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (order_number, data["name"], data["email"], data["phone"], data["address"],
              data["city"], data["state"], data["pincode"], data["payment"], total,
              "Confirmed", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        order_id = cur.lastrowid 
        for item in items:
            cur.execute("""
                INSERT INTO order_items (order_id, car_id, car_name, price, quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, item["id"], f'{item["brand"]} {item["name"]}',
                  item["price"], item["quantity"]))
        conn.commit()
        conn.close()

        session["cart"] = {}
        session["last_order"] = {
            "order_number": order_number,
            "name": data["name"],
            "email": data["email"],
            "total": total,
            "payment": data["payment"],
            "order_items": [{"name": f'{i["brand"]} {i["name"]}', "quantity": i["quantity"]} for i in items]
        }
        return redirect(url_for("success"))

    return render_template("checkout.html", items=items, total=total, error=None)


@app.get("/success")
def success():
    order = session.get("last_order")
    if not order:
        return redirect(url_for("shop"))
    return render_template("success.html", order=order)


@app.errorhandler(404)
def not_found(_error):
    return render_template("base.html", page_error="Page not found."), 404


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
