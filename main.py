from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import matplotlib.pyplot as plt
# product_id = "P001"
# product_name = "Rice"
# category = "Grocery"
# price = 60
# quantity = 50

# print(product_id)
# print(product_name)
# print(category)
# print(price)
# print(quantity)

products = [
    {"id": "P001", "name": "Rice", "category": "Grocery", "price": 60, "quantity": 50},
    {"id": "P002", "name": "Wheat Flour", "category": "Grocery", "price": 45, "quantity": 40},
    {"id": "P003", "name": "Cooking Oil", "category": "Grocery", "price": 140, "quantity": 25},
    {"id": "P004", "name": "Sugar", "category": "Grocery", "price": 50, "quantity": 35},
    {"id": "P005", "name": "Salt", "category": "Grocery", "price": 25, "quantity": 30},

    {"id": "P006", "name": "Milk", "category": "Dairy", "price": 30, "quantity": 20},
    {"id": "P007", "name": "Butter", "category": "Dairy", "price": 55, "quantity": 15},
    {"id": "P008", "name": "Cheese", "category": "Dairy", "price": 100, "quantity": 12},
    {"id": "P009", "name": "Curd", "category": "Dairy", "price": 40, "quantity": 18},
    {"id": "P010", "name": "Paneer", "category": "Dairy", "price": 90, "quantity": 10},

    {"id": "P011", "name": "Bread", "category": "Bakery", "price": 40, "quantity": 18},
    {"id": "P012", "name": "Cake", "category": "Bakery", "price": 250, "quantity": 7},
    {"id": "P013", "name": "Bun", "category": "Bakery", "price": 20, "quantity": 25},
    {"id": "P014", "name": "Cookies", "category": "Bakery", "price": 80, "quantity": 20},
    {"id": "P015", "name": "Donut", "category": "Bakery", "price": 50, "quantity": 14},

    {"id": "P016", "name": "Biscuit", "category": "Food", "price": 20, "quantity": 40},
    {"id": "P017", "name": "Noodles", "category": "Food", "price": 25, "quantity": 30},
    {"id": "P018", "name": "Chips", "category": "Food", "price": 20, "quantity": 45},
    {"id": "P019", "name": "Chocolate", "category": "Food", "price": 50, "quantity": 25},
    {"id": "P020", "name": "Ketchup", "category": "Food", "price": 90, "quantity": 15},

    {"id": "P021", "name": "Soap", "category": "Personal Care", "price": 35, "quantity": 22},
    {"id": "P022", "name": "Shampoo", "category": "Personal Care", "price": 120, "quantity": 12},
    {"id": "P023", "name": "Toothpaste", "category": "Personal Care", "price": 90, "quantity": 16},
    {"id": "P024", "name": "Face Wash", "category": "Personal Care", "price": 150, "quantity": 9},
    {"id": "P025", "name": "Hand Wash", "category": "Personal Care", "price": 100, "quantity": 13},

    {"id": "P026", "name": "Detergent", "category": "Household", "price": 110, "quantity": 10},
    {"id": "P027", "name": "Dishwash Liquid", "category": "Household", "price": 85, "quantity": 14},
    {"id": "P028", "name": "Floor Cleaner", "category": "Household", "price": 120, "quantity": 8},
    {"id": "P029", "name": "Tea", "category": "Beverage", "price": 180, "quantity": 8},
    {"id": "P030", "name": "Coffee", "category": "Beverage", "price": 250, "quantity": 6}
]
sales_history = []

#print(products)

#print(products)
def display_products():
    for product in products:
        print("Product Id:",product ["id"])
        print("Product Name:",product["name"])
        print("Product Category:",product["category"])
        print("Product price:",product["price"])
        print("Product Quantity:",product["quantity"])
# display_products()
# def add_products():
    # product_id  = input("Enter Product id")
    # product_name = input("Enter Product Name")
    # product_category = input("Enter Product category")
    # product_price = float(input("Enter Product Price"))
    # product_quantity = int(input("Enter Product Quantity"))

    # new_product = {
    #     "id": product_id,
    #     "name": product_name,
    #     "category": product_category,
    #     "price": product_price,
    #     "quantity": product_quantity
    # }

    # products.append(new_product)
    # print("product added succesfully!")
# add_products()
# display_products()

def search_product():
    search_id = input("Enter Product Id search")
    found = False
    for product in products:
        if product["id"] == search_id:
            print("product found!")
            print("Product Id:",product["id"])
            print("Product Name:",product["name"])
            print("Category:",product["category"])
            print("Price:",product["price"])
            print("Quantity:",product["quantity"])
            found = True
            break

    if found == False:
        print("Product not found!")  

def add_products():
    product_id = input("Enter product id: ").strip().upper()
    for product in products:
        if product["id"] == product_id:
            print("Product already exists")
            return

    product_name = input("Enter Product Name: ")
    product_category = input("Enter Product category: ")

    while True:
        try:
            product_price = float(input("Enter Product Price: "))
            if product_price <= 0:
                print("Price must be greater than 0")
                continue
            break
        except ValueError:
            print("Invalid price! Please enter a number")

    while True:
        try:
            product_quantity = int(input("Enter Product Quantity: "))
            if product_quantity < 0:
                print("Quantity cannot be negative")
                continue
            break
        except ValueError:
            print("Invalid quantity! Please enter a valid number")

    new_product = {
        "id": product_id,
        "name": product_name,
        "category": product_category,
        "price": product_price,
        "quantity": product_quantity
    }

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO products (id, name, category, price, quantity) VALUES (%s, %s, %s, %s, %s)",
            (product_id, product_name, product_category, product_price, product_quantity)
        )
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print("Database error:", error)
        return

    products.append(new_product)
    save_products()
    print("Product added successfully!")
        
# display_products()
#add products()

def update_products():
    search_id = input("Enter Product ID To Update: ")
    found = False

    for product in products:
        if product["id"] == search_id:
            found = True
            print("Product Found")
            print("1. Update Price")
            print("2. Update Quantity")
            choice = input("Enter Your choice: ")

            if choice == "1":
                while True:
                    try:
                        new_price = float(input("Enter A New Price: "))
                        if new_price < 0:
                            print("Price must be 0 or greater")
                            continue
                        break
                    except ValueError:
                        print("Invalid price! Please enter a number.")

                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE products SET price = %s WHERE id = %s",
                    (new_price, search_id)
                )
                connection.commit()
                cursor.close()
                connection.close()

                product["price"] = new_price
                save_products()
                print("Product price updated successfully")

            elif choice == "2":
                while True:
                    try:
                        new_quantity = int(input("Enter New Quantity: "))
                        if new_quantity < 0:
                            print("Quantity cannot be negative")
                            continue
                        break
                    except ValueError:
                        print("Invalid quantity! Please enter a whole number.")

                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE products SET quantity = %s WHERE id = %s",
                    (new_quantity, search_id)
                )
                connection.commit()
                cursor.close()
                connection.close()

                product["quantity"] = new_quantity
                save_products()
                print("Product quantity updated successfully")

            else:
                print("Invalid choice")

            return

    if not found:
        print("No Product Found")

#update_products() 
def delete_product():
    search_id= input("Enter Product Id To Delete:")
    for product in products:
        if product["id"] == search_id:
            products.remove(product)
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (search_id,))
            connection.commit()
            cursor.close()
            connection.close()
            save_products()
            print("Product Delete Succesfully")
            return
    print("product not found")

def record_sale():
    search_id = input("Enter Product Id to sell: ").strip().upper()
    try:
        sale_quantity = int(input("Enter quantity to sell: "))
    except ValueError:
        print("Invalid quantity!")
        return
    if sale_quantity <= 0:
        print("Quantity must be greater than zero")
        return

    for product in products:
        if product["id"] == search_id:
            if sale_quantity > product["quantity"]:
                print("Not enough stock")
                return

            total = product["price"] * sale_quantity
            product["quantity"] -= sale_quantity

            sale_record = {
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": sale_quantity,
                "total": total
            }
            sales_history.append(sale_record)

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE products SET quantity = %s WHERE id = %s",
                (product["quantity"], product["id"])
            )
            connection.commit()
            cursor.close()
            connection.close()

            save_products()
            save_sales_history()
            save_sale_to_mysql(sale_record)

            print("Sale recorded successfully")
            print("Product:", product["name"])
            print("Quantity sold:", sale_quantity)
            print("Total Sale Amount:", total)
            print("Remaining Stock:", product["quantity"])
            return

    print("Product not found")

def display_sales_history():
    if not sales_history:
        print("No sales_history")
        return
    for sale in sales_history:
        print("Product Id:",sale["id"])
        print("Product Name:",sale["name"])
        print("Price:",sale["price"])
        print("Quantity Sold:",sale["quantity"])
        print("Total:",sale["total"])
def main():
    while True:
        print("\n=====INVENTORY SALES SYSTEM=====")
        print("1.Display Products")
        print("2.Add Products")
        print("3.Search Products")
        print("4.Update Products")
        print("5.Delete Products")
        print("6.Record Sale")
        print("7.Display Sales History")
        print("8.low stock alert")
        print("9.Show Stock Chart")
        print("10.Exit")
        choice = input("Enter your Choice")
        if choice =="1":
            print("Display The Products")
            display_products()
            input("Press Enter To Continue...")
        elif choice =="2":
            add_products()
        elif choice =="3":
            search_product()
        elif choice =="4":
            update_products()
            input("Press Enter to continue")
        elif choice == "5":
            delete_product()
        elif choice =="6":
            record_sale()
        elif choice == "7":
            print("Testing sales_history")
            display_sales_history()
            input("Press Enter  To Continue...")
        elif choice == "8":
            print("Testing Low Stock Alert")
            low_stock_alert()
            input("Press Enter To Continue...")
        elif choice =="9":
            show_stock_chart()
            input("Press Enter Continue")
        
        elif choice == "10":
          print("Thank You!")
          break
        else:
            print("Invalid Choice!")
def low_stock_alert():
    # print("LO STOCK FUNCTION STARTED")
    found = False
    for product in products:
        if product["quantity"] <=5:
            print("Low Stack Product")
            print("Product Id:",product["id"])
            print("Product Name:",product["name"])
            print("Remaining Quantity:",product["quantity"])
            found = True
    if not found:
        print("No Low Stock Products")                    

def sales_report():
    total_sales = 0
    total_quantity = 0
    for sale in sales_history:
        total_sales += sale["total"]
        total_quantity +=sale["quantity"]
    print("Total Sale Amount:",total_sales)
    print("Total Product Sold:",total_quantity)
    print("Number of Sales:",len(sales_history))

import json
def load_products():
    global products
    try:
        with open("products.json","r") as file :
            products = json.load(file)
    except FileNotFoundError:
        pass
def save_products():
    with open("products.json","w") as file:
        json.dump(products,file,indent = 4)
# load_products()       
# main()
def save_sales_history():
    with open("sales_history.json","w") as file:
        json.dump(sales_history,file,indent = 4)
def load_sales_history():
    global sales_history
    try:
        with open("sales_history.json","r") as file:
            sales_history = json.load(file)
    except FileNotFoundError:
        pass
load_products()
load_sales_history()

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
try:
    connection = get_connection()
    print("MySQL connection successful!")
    connection.close()
except mysql.connector.Error as error:
    print("MySQL connection failed:", error)
def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("USE inventory_db")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL
)
""")

    # cursor.execute("USE inventory_db")
    #     CREATE TABLE IF NOT EXISTS products (
    #         id VARCHAR(20) PRIMARY KEY,
    #         name VARCHAR(100) NOT NULL,
    #         category VARCHAR(50),
    #         price DECIMAL(10, 2) NOT NULL,
    #         quantity INT NOT NULL
    #     )
    # """)

    # cursor.execute("""
    #      CREATE TABLE IF NOT EXISTS sales (
    #         sale_id INT AUTO_INCREMENT PRIMARY KEY,
    #         product_id VARCHAR(20),
    #         product_name VARCHAR(100),
    #         price DECIMAL(10, 2),
    #         quantity INT,
    #         total DECIMAL(10, 2),
    #         sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #     )
    # """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(20),
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    quantity INT,
    total DECIMAL(10,2),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

    connection.commit()
    cursor.close()
    connection.close()


def save_products_to_mysql():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("USE inventory_db")
    
    print("Products to save:",len(products))

    for product in products:
        cursor.execute("""
            INSERT INTO products (id, name, category, price, quantity)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                category = VALUES(category),
                price = VALUES(price),
                quantity = VALUES(quantity)
        """, (
            product["id"],
            product["name"],
            product.get("category", ""),
            product["price"],
            product["quantity"]
        ))

    connection.commit()
    cursor.close()
    connection.close()

create_tables()
save_products_to_mysql()

# def save_products_to_mysql():
#     connection = get_connection()
#     cursor = connection.cursor()

#     for product in products:
#         cursor.execute(
#             """
#             INSERT INTO products (id, name, category, price, quantity)
#             VALUES (%s, %s, %s, %s, %s)
#             ON DUPLICATE KEY UPDATE
#                 name = VALUES(name),
#                 category = VALUES(category),
#                 price = VALUES(price),
#                 quantity = VALUES(quantity)
#             """,
#             (
#                 product["id"],
#                 product["name"],
#                 product.get("category", ""),
#                 product["price"],
#                 product["quantity"]
#             )
#         )

#     connection.commit()
#     cursor.close()
#     connection.close()
# create_tables()
# save_products_to_mysql()
def save_sale_to_mysql(sale):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO sales (product_id, product_name, price, quantity, total)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (sale["id"], sale["name"], sale["price"], sale["quantity"], sale["total"])
    )
    connection.commit()
    cursor.close()
    connection.close()
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def show_stock_chart():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT name, quantity FROM products ORDER BY quantity")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    if not rows:
        print("No products to display.")
        return

    names = [r[0] for r in rows]
    qty = [r[1] for r in rows]
    colors = ["#e74c3c" if q <= 5 else "#f39c12" if q <= 15 else "#2ecc71"
              for q in qty]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 9))
    bars = ax.barh(names, qty, color=colors, edgecolor="white", height=0.7)

    for bar, q in zip(bars, qty):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                str(q), va="center", fontsize=9, fontweight="bold")

    ax.set_title("Current Stock by Product", fontsize=16,
                 fontweight="bold", pad=15)
    ax.set_xlabel("Quantity in Stock", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(handles=[
        Patch(color="#e74c3c", label="Low (≤5)"),
        Patch(color="#f39c12", label="Medium (6–15)"),
        Patch(color="#2ecc71", label="Good (>15)")],
        loc="lower right")

    plt.tight_layout()
    plt.show()
app = Flask(__name__, template_folder="templates")    
import os

print("CURRENT DIRECTORY:", os.getcwd())
print("TEMPLATE PATH:", app.template_folder)
print("CHART EXISTS:", os.path.exists("templates/chart.html"))
print("TEMPLATE FILES:", os.listdir("templates"))

@app.route("/")
def home():
    
    print("HOME ROUTE STARTED")

    connection = get_connection()
    print("MYSQL CONNECTED")

    
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, category, price, quantity FROM products"
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    products = []

    for row in rows:

        product = {
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "price": float(row[3]),
            "quantity": row[4]
        }

        products.append(product)

    total_products = len(products)

    total_units = sum(
        product["quantity"] for product in products
    )

    stock_value = sum(
        product["price"] * product["quantity"]
        for product in products
    )

    low_stock = sum(
        1 for product in products
        if product["quantity"] <= 5
    )

    categories = sorted(set(
        product["category"] for product in products
        if product["category"]
    ))

    return render_template(
        "index.html",
        products=products,
        total_products=total_products,
        total_units=total_units,
        stock_value=stock_value,
        low_stock=low_stock,
        categories=categories
    )

@app.route("/add_product", methods=["POST"])
def add_product_web():

    product_id = request.form.get("product_id")
    name = request.form.get("name")
    category = request.form.get("category")
    price = request.form.get("price")
    quantity = request.form.get("quantity")

    if not all([product_id, name, category, price, quantity]):
        return "Please fill all fields", 400

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO products (id, name, category, price, quantity)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (product_id, name, category, float(price), int(quantity))
        )

        connection.commit()

    except mysql.connector.Error as error:
        return f"Database Error: {error}", 400

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("home"))

@app.route("/update_product/<product_id>", methods=["POST"])
def update_product_web(product_id):

    name = request.form.get("name")
    category = request.form.get("category")
    price = request.form.get("price")
    quantity = request.form.get("quantity")

    if not all([name, category, price, quantity]):
        return "Please fill all fields", 400

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE products
            SET name = %s,
                category = %s,
                price = %s,
                quantity = %s
            WHERE id = %s
            """,
            (name, category, float(price),
             int(quantity), product_id)
        )

        connection.commit()

    except mysql.connector.Error as error:
        return f"Database Error: {error}", 400

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("home"))

@app.route("/chart")
def chart():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT name, quantity FROM products ORDER BY quantity DESC"
        )
        rows = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    chart_data = []

    max_quantity = max([row[1] for row in rows], default=1)

    for row in rows:
        chart_data.append({
            "name": row[0],
            "quantity": row[1],
            "percentage": (row[1] / max_quantity) * 100
        })

    return render_template(
        "chart.html",
        chart_data=chart_data
    )
if __name__ == "__main__":
    app.run(debug=True)      # website চালাতে এটা
    # main()                 # terminal menu চালাতে এটা (একবারে একটাই)
# main()


    
    
                
            
            


