from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import boto3
import os
import logging
from typing import List, Dict, Optional, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------- CONFIGURATION ----------
DB_USER = 'root'
DB_PASSWORD = os.getenv("DB_PASSWORD", "Amruth%408050")
DB_NAME = 'retail_system'
DB_HOST = '34.93.172.75'
DB_PORT = 3306

SES_REGION = 'us-east-1'
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "amruths604@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "vddywbeuafhopmrw")  # Use an App Password, not your main password!
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "amruthsharma49@example.com")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

PRODUCTS_TABLE = "products"
INVENTORY_TABLE = "inventory"
SALES_TABLE = "sales"
RESTOCK_ALERTS_TABLE = "restock_alerts"

# ---------- CONNECT TO DB ----------
DB_URL = os.getenv("DB_URL")
if DB_URL:
    engine = create_engine(DB_URL)
else:
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ---------- UTILITY ----------
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
def log(msg: str, level: str = "info"):
    getattr(logging, level)(msg)

# ---------- DB OPERATIONS ----------
def test_connection() -> None:
    """Test DB connection and print available tables."""
    try:
        tables = pd.read_sql("SHOW TABLES;", engine)
        log("✅ Connected. Tables found:")
        log(tables.to_string(), "info")
    except Exception as e:
        log(f"❌ DB connection failed: {e}", "error")

def clear_tables() -> None:
    """Clear all main tables for a fresh start."""
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM restock_alerts;"))
        conn.execute(text("DELETE FROM sales;"))
        conn.execute(text("DELETE FROM inventory;"))
        conn.execute(text("DELETE FROM products;"))
    log("🧹 Tables cleared to prevent duplication.")

def insert_sample_data() -> None:
    """Insert sample products, inventory, and sales data."""
    try:
        with engine.begin() as conn:
            # Insert all products
            conn.execute(text(f"""
                INSERT INTO {PRODUCTS_TABLE} (product_name, category, supplier_name, unit_price, reorder_level) VALUES
                ('Wireless Mouse', 'Electronics', 'TechWare', 599.99, 20),
                ('LED Bulb 9W', 'Lighting', 'BrightLite', 89.50, 50),
                ('Notebook A5', 'Stationery', 'OfficeMart', 45.00, 100),
                ('Desk Chair', 'Furniture', 'HomeComfort', 3499.00, 10),
                ('Bluetooth Speaker', 'Electronics', 'SoundMax', 1299.00, 15),
                ('Table Lamp', 'Lighting', 'BrightLite', 499.00, 25),
                ('Gel Pen', 'Stationery', 'OfficeMart', 15.00, 200),
                ('Office Desk', 'Furniture', 'HomeComfort', 5999.00, 5),
                ('USB-C Cable', 'Electronics', 'TechWare', 199.00, 40),
                ('Sticky Notes', 'Stationery', 'OfficeMart', 25.00, 150),
                ('Floor Lamp', 'Lighting', 'BrightLite', 1599.00, 8),
                ('Bookshelf', 'Furniture', 'HomeComfort', 2499.00, 7)
            """))

        # Retrieve actual product_ids
        df = pd.read_sql("SELECT product_id, product_name FROM products", engine)
        product_map = {row['product_name']: row['product_id'] for _, row in df.iterrows()}

        # Insert inventory for all products
        with engine.begin() as conn:
            conn.execute(text(f"""
                INSERT INTO {INVENTORY_TABLE} (product_id, quantity_in_stock) VALUES
                (:mouse, 30), (:bulb, 120), (:notebook, 90), (:chair, 5),
                (:speaker, 18), (:lamp, 40), (:pen, 300), (:desk, 8),
                (:cable, 60), (:notes, 200), (:floorlamp, 10), (:bookshelf, 6)
            """), {
                "mouse": product_map['Wireless Mouse'],
                "bulb": product_map['LED Bulb 9W'],
                "notebook": product_map['Notebook A5'],
                "chair": product_map['Desk Chair'],
                "speaker": product_map['Bluetooth Speaker'],
                "lamp": product_map['Table Lamp'],
                "pen": product_map['Gel Pen'],
                "desk": product_map['Office Desk'],
                "cable": product_map['USB-C Cable'],
                "notes": product_map['Sticky Notes'],
                "floorlamp": product_map['Floor Lamp'],
                "bookshelf": product_map['Bookshelf']
            })

            # Define sales data (add more if you want sales for all products)
            sales_data = [
                {"product_id": product_map['Wireless Mouse'], "quantity_sold": 3, "sale_date": '2025-06-01'},
                {"product_id": product_map['Wireless Mouse'], "quantity_sold": 2, "sale_date": '2025-06-03'},
                {"product_id": product_map['LED Bulb 9W'], "quantity_sold": 20, "sale_date": '2025-06-01'},
                {"product_id": product_map['Notebook A5'], "quantity_sold": 25, "sale_date": '2025-06-01'},
                {"product_id": product_map['Notebook A5'], "quantity_sold": 10, "sale_date": '2025-06-05'},
                {"product_id": product_map['Desk Chair'], "quantity_sold": 6, "sale_date": '2025-06-04'},
                # Add more sales records for other products as needed
            ]
            validate_sales_data(sales_data)

            conn.execute(
                text(f"""
                    INSERT INTO {SALES_TABLE} (product_id, quantity_sold, sale_date)
                    VALUES (:product_id, :quantity_sold, :sale_date)
                """),
                sales_data
            )

        log("📦 Sample data inserted successfully using dynamic product IDs.")
    except Exception as e:
        log(f"❌ Failed to insert sample data: {e}", "error")

def validate_sales_data(sales_data: List[Dict[str, Any]]) -> None:
    """Validate sales data before insertion."""
    for sale in sales_data:
        if sale["quantity_sold"] < 0:
            raise ValueError(f"Negative quantity in sales data: {sale}")
        if not sale["product_id"]:
            raise ValueError(f"Missing product_id in sales data: {sale}")

def update_inventory(product_id: int, new_stock: int) -> None:
    """Update inventory for a product."""
    try:
        with engine.begin() as conn:
            conn.execute(
                text(f"UPDATE {INVENTORY_TABLE} SET quantity_in_stock = :stock WHERE product_id = :pid"),
                {"stock": new_stock, "pid": product_id}
            )
        log(f"🔄 Inventory updated for product_id {product_id}: {new_stock}")
    except Exception as e:
        log(f"❌ Failed to update inventory: {e}", "error")

def delete_product(product_id: int) -> None:
    """Delete a product and its related records."""
    try:
        with engine.begin() as conn:
            conn.execute(text(f"DELETE FROM {INVENTORY_TABLE} WHERE product_id = :pid"), {"pid": product_id})
            conn.execute(text(f"DELETE FROM {SALES_TABLE} WHERE product_id = :pid"), {"pid": product_id})
            conn.execute(text(f"DELETE FROM {RESTOCK_ALERTS_TABLE} WHERE product_id = :pid"), {"pid": product_id})
            conn.execute(text(f"DELETE FROM {PRODUCTS_TABLE} WHERE product_id = :pid"), {"pid": product_id})
        log(f"🗑️ Product {product_id} and related records deleted.")
    except Exception as e:
        log(f"❌ Failed to delete product: {e}", "error")

# ---------- EMAIL ----------
def send_email_alert(product_name: str, stock: int, threshold: int) -> None:
    """Send a restock alert email using Gmail SMTP."""
    subject = f"Restock Alert: {product_name}"
    body = f"""
    Product: {product_name}
    Current Stock: {stock}
    Reorder Threshold: {threshold}
    Action Needed: Please reorder this product.
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        log(f"📧 Email sent for {product_name}")
    except Exception as e:
        log(f"⚠️ Email failed for {product_name}: {e}", "warning")

# ---------- RESTOCK CHECK ----------
def check_inventory_and_restock() -> None:
    """Check inventory and create restock alerts for low stock products."""
    query = f"""
        SELECT p.product_id, p.product_name, i.quantity_in_stock, p.reorder_level
        FROM {PRODUCTS_TABLE} p
        JOIN {INVENTORY_TABLE} i ON p.product_id = i.product_id
        WHERE i.quantity_in_stock < p.reorder_level;
    """
    low_stock_df = pd.read_sql(query, engine)

    for _, row in low_stock_df.iterrows():
        log(f"🚨 {row['product_name']} stock {row['quantity_in_stock']} < reorder {row['reorder_level']}", "warning")
        with engine.begin() as conn:
            conn.execute(text(f"""
                INSERT INTO {RESTOCK_ALERTS_TABLE} (product_id, quantity_in_stock, threshold, alert_sent, sent_at)
                VALUES (:product_id, :quantity_in_stock, :threshold, :alert_sent, :sent_at)
            """), {
                "product_id": row['product_id'],
                "quantity_in_stock": row['quantity_in_stock'],
                "threshold": row['reorder_level'],
                "alert_sent": True,
                "sent_at": datetime.now()
            })
        send_email_alert(row['product_name'], row['quantity_in_stock'], row['reorder_level'])

# ---------- REPORTING ----------
def generate_sales_report() -> None:
    """Generate and log a sales summary report."""
    query = f"""
        SELECT p.product_name, SUM(s.quantity_sold) AS total_quantity_sold,
               SUM(s.quantity_sold * p.unit_price) AS total_revenue
        FROM {SALES_TABLE} s
        JOIN {PRODUCTS_TABLE} p ON s.product_id = p.product_id
        GROUP BY p.product_name;
    """
    df = pd.read_sql(query, engine)
    log("\n📊 Sales Report:")
    log(df.to_string())

def generate_inventory_report() -> None:
    """Generate and log an inventory summary report."""
    query = f"""
        SELECT p.product_name, i.quantity_in_stock, p.reorder_level
        FROM {PRODUCTS_TABLE} p
        JOIN {INVENTORY_TABLE} i ON p.product_id = i.product_id;
    """
    df = pd.read_sql(query, engine)
    log("\n📦 Inventory Report:")
    log(df.to_string())

def generate_restock_alerts() -> None:
    """Generate and log a restock alerts report."""
    query = f"""
        SELECT p.product_name, ra.quantity_in_stock, ra.threshold, ra.sent_at
        FROM {RESTOCK_ALERTS_TABLE} ra
        JOIN {PRODUCTS_TABLE} p ON ra.product_id = p.product_id
        WHERE ra.alert_sent = TRUE;
    """
    df = pd.read_sql(query, engine)
    log("\n🚨 Restock Alerts:")
    log(df.to_string())

# ---------- DATA RETRIEVAL ----------
def get_sales_data(start_date: Optional[str] = None, end_date: Optional[str] = None, category: Optional[str] = None) -> pd.DataFrame:
    """
    Get sales data, optionally filtered by date range and category.
    """
    query = f"""
        SELECT s.sale_date, p.product_name, s.quantity_sold, p.category
        FROM {SALES_TABLE} s
        JOIN {PRODUCTS_TABLE} p ON s.product_id = p.product_id
    """
    filters = []
    params = {}
    if start_date:
        filters.append("s.sale_date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        filters.append("s.sale_date <= :end_date")
        params["end_date"] = end_date
    if category:
        filters.append("p.category = :category")
        params["category"] = category
    if filters:
        query += " WHERE " + " AND ".join(filters)
    query += " ORDER BY s.sale_date DESC"
    return pd.read_sql(text(query), engine, params=params)

def get_inventory_data(category: Optional[str] = None) -> pd.DataFrame:
    """
    Get inventory data, optionally filtered by category.
    """
    query = f"""
        SELECT p.product_name, p.category, i.quantity_in_stock, p.reorder_level
        FROM {INVENTORY_TABLE} i
        JOIN {PRODUCTS_TABLE} p ON i.product_id = p.product_id
    """
    if category:
        query += " WHERE p.category = :category"
        return pd.read_sql(text(query), engine, params={"category": category})
    return pd.read_sql(query, engine)

def get_alert_data() -> pd.DataFrame:
    """
    Get all active restock alerts.
    """
    query = f"""
        SELECT p.product_name, ra.quantity_in_stock, ra.threshold, ra.sent_at
        FROM {RESTOCK_ALERTS_TABLE} ra
        JOIN {PRODUCTS_TABLE} p ON ra.product_id = p.product_id
        WHERE ra.alert_sent = TRUE
        ORDER BY ra.sent_at DESC
    """
    return pd.read_sql(query, engine)

# ---------- MAIN ----------
if __name__ == "__main__":
    log("🔌 Testing DB connection...")
    test_connection()

    log("🧹 Clearing tables...")
    clear_tables()

    log("📥 Inserting sample data...")
    insert_sample_data()

    log("📉 Checking inventory and sending alerts...")
    check_inventory_and_restock()

    log("📄 Generating reports...\n")
    generate_sales_report()
    generate_inventory_report()
    generate_restock_alerts()

    log("✅ All operations completed.")
