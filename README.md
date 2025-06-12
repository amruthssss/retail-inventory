🛒 Retail Inventory & Auto-Restock System
A real-time retail inventory monitoring and auto-restock dashboard built using Streamlit, MySQL, and Plotly, deployed on the cloud. It provides visual insights, low-stock alerts, auto-refreshing data, and auto-reordering capabilities to streamline inventory operations.

<!-- Add this if you have a demo screenshot -->

🔧 Features
✅ Real-time inventory and sales dashboards
✅ Auto-refresh and Lottie animations for live monitoring
✅ Low-stock alert panel
✅ Auto-reorder logic for critical inventory levels
✅ Admin panel with secure login
✅ Visual analytics with Plotly
✅ Export options and automated notifications (coming soon)

🚀 Live Demo
🌍 Access the dashboard:
👉 https://retail-inventory-project-2025.streamlit.app/

🗂️ Project Structure
graphql
Copy
Edit
retail-inventory-dashboard/
│
├── app.py                    # Main Streamlit app
├── db.py                     # DB connection & data fetching logic
├── auth.py                   # Admin login authentication
├── admin_panel.py            # Admin management functions
├── product_images.py         # Product image mapping
│
├── assets/                   # Product images and logos
├── data/                     # Optional: sample CSV data for testing
│
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore                # Ignore sensitive and unnecessary files
🛠️ Tech Stack
Frontend/UI: Streamlit

Database: MySQL (cloud-hosted via Google Cloud SQL)

Visualization: Plotly

Hosting: Streamlit Cloud

Languages: Python 3

📊 Key Visuals
📦 Inventory Levels with Conditional Coloring

💰 Daily & Monthly Sales Line Charts

🚨 Alerts for Low Stock Products

🔐 Admin-only controls for product and inventory management

⚙️ How to Run Locally
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/retail-inventory-dashboard.git
cd retail-inventory-dashboard
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Configure your database:

Set up your MySQL instance (locally or on Google Cloud SQL).

Update db.py with your DB connection credentials.

Run the app:

bash
Copy
Edit
streamlit run app.py

✅ Example Use Cases
🏪 Small-to-medium retail shops tracking product inventory

🛒 Auto-restocking system for ecommerce vendors

📉 Visual alerts for declining stock trends

👨‍💻 Admin dashboard for product management

📬 Upcoming Features
📤 Export inventory/sales reports (CSV, PDF)

✉️ Email notifications via AWS SES or SMTP

📱 Mobile optimization

🔍 Advanced filters & search

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss.

