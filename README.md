# 🛒 Retail Inventory & Auto-Restock System

A **real-time cloud-based retail inventory dashboard** powered by **Streamlit**, **MySQL**, and **Plotly**. It features low-stock alerts, automatic restocking triggers, and beautiful interactive charts for a smarter retail experience.

![Dashboard Demo](assets/demo_screenshot.png)

---

## 🚀 Live Project

👉 **Try it here**: [https://retail-inventory-project-2025.streamlit.app/](https://retail-inventory-project-2025.streamlit.app/)

---

## 🎯 Key Features

- 📦 **Live Inventory Monitoring** – Track product stock in real-time  
- 📊 **Interactive Sales Charts** – Visualize daily and monthly trends  
- 🔁 **Auto-Refresh Dashboard** – Keeps data updated automatically  
- 🔔 **Low Stock Alerts** – Flags products needing restocking  
- 🔒 **Admin Login Panel** – Secure management interface  
- 🧠 **Auto-Restock Logic** – Automatically flags or simulates reorders  
- 📤 **Upcoming:** Export to CSV & Email Alerts via SES  

---

## 🛠️ Tech Stack

| Layer         | Technology                 |
|---------------|----------------------------|
| **Frontend**  | Streamlit, Plotly, Lottie  |
| **Backend**   | Python, MySQL (Cloud SQL)  |
| **Hosting**   | Streamlit Cloud            |
| **Cloud**     | Google Cloud Platform (SQL)|
| **Notifications** | AWS SES *(planned)* |

---

## 📂 Project Structure

retail-inventory-dashboard/
│
├── app.py # 🎯 Streamlit app entrypoint
├── db.py # 🔗 MySQL connection & queries
├── auth.py # 🔐 Admin authentication
├── admin_panel.py # ⚙️ Admin tools
├── product_images.py # 🖼️ Maps product names to images
│
├── assets/ # 📁 Product images and animations
├── data/ # 📊 Optional sample CSVs
│
├── requirements.txt # 📦 Python dependencies
├── .gitignore # 🚫 Ignore sensitive files
└── README.md # 📘 This file

yaml
Copy
Edit

---

## 🧪 How to Run Locally

> 🐍 **Python 3.9+** and **MySQL** required

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/yourusername/retail-inventory-dashboard.git
cd retail-inventory-dashboard
📦 2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🛢️ 3. Configure MySQL
Update your MySQL credentials in db.py:

python
Copy
Edit
connection = mysql.connector.connect(
    host="your-db-host",
    user="your-username",
    password="your-password",
    database="your-database"
)
▶️ 4. Run the App
bash
Copy
Edit
streamlit run app.py
📈 Dashboard Visuals
✅ Total Inventory Value & Sales Today

📉 Low Stock Alerts (Table with Highlights)

📆 Daily and Monthly Sales Charts (Plotly)

👤 Admin Panel (Login, Product Update Functions)

♻️ Auto-refresh every minute using streamlit_autorefresh

🔐 Admin Panel Access
Allows secure product management

Modify prices, update stock, or restock items

Simple login system via auth.py

📤 Upcoming Features
📨 Automated emails via AWS SES

🗃️ Export reports to CSV or PDF

🧠 Advanced analytics & forecasting

📱 Mobile-friendly UI

📸 Screenshot

![image](https://github.com/user-attachments/assets/b0891c44-8f66-4ba7-8b80-86e211086b41)
!![image](https://github.com/user-attachments/assets/85e7812c-cbb5-4246-b54b-2b5d476d62a9)
![image](https://github.com/user-attachments/assets/4b272059-2eb4-4fca-a48c-de239080525a)



📌 Use Cases
🏪 Small businesses managing physical inventory

🛒 E-commerce platforms tracking sales & stock

🧾 Inventory teams needing automated restocking logic

📉 Retailers analyzing daily/monthly sales patterns
