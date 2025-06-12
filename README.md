# 🛍️ Cloud-Based Retail Inventory & Sales Analytics Dashboard

A real-time inventory and sales analytics dashboard built with **Streamlit**, designed for retail businesses. It visualizes key performance indicators, manages inventory, predicts stockouts, and automatically triggers restock alerts with integrated image support.

---

## 📌 Features

- 📦 **Inventory Overview** with images, stock, and reorder levels
- 📊 **Sales Analytics** using Plotly for visual insights
- 🚨 **Restock Alerts** for low-stock items
- 🔄 **Auto-Refresh** every 60 seconds for live updates
- 📁 **Image Uploading & Validation** for product entries
- 💌 **Email Notifications** for critical alerts (via AWS SES)
- ☁️ **Cloud-integrated** (AWS RDS, S3, Lambda compatible)

---

## 🚀 Demo

![Inventory Screenshot](assets/screenshots/inventory_overview.png)

Live URL (if deployed):  
`https://your-username.streamlit.app/`

---

## 🏗️ Tech Stack

| Technology      | Purpose                         |
|-----------------|----------------------------------|
| Python          | Core programming language        |
| Streamlit       | Web app framework                |
| Pandas          | Data manipulation                |
| Plotly          | Interactive visualizations       |
| MySQL / AWS RDS | Database backend                 |
| S3 (optional)   | Cloud image storage              |
| SES (optional)  | Email alert system               |

---

## 📁 Project Structure

.
├── app.py
├── db.py
├── utils.py
├── assets/
│ └── images/
├── data/
│ └── inventory.csv
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## 🔧 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/retail-dashboard.git
   cd retail-dashboard
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the app

bash
Copy
Edit
streamlit run app.py
🔄 Auto-Refresh Feature
Enabled with streamlit_autorefresh:

python
Copy
Edit
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=60000, key="dashboard_refresh")
📬 Email Alerts Setup (Optional)
To enable stock alert emails:

Configure AWS SES

Store your credentials securely

Use boto3 to send notifications when stock < reorder threshold

📷 Inventory Images
Place product images inside /assets/images/ and reference them in your inventory data as:

python
Copy
Edit
image_path = "assets/images/wireless_mouse.jpg"
st.image(image_path, caption="Wireless Mouse")

