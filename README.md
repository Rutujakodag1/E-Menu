# 🍴 Mini Food Ordering System

The Mini Food Ordering System is a **web-based platform** designed to streamline restaurant operations. It allows **customers, kitchen staff, and counter staff** to manage orders and payments efficiently, reducing errors and improving workflow. Built with **Django, HTML, CSS, and SQLite**, it demonstrates role-based access and organized order management.

---


## 🚀 Features

- **Table User**
  - View digital menu
  - Place new orders
  - Track order status

- **Kitchen User**
  - Receive and manage orders
  - Update cooking progress
  - Notify when ready

- **Counter User**
  - Handle payments
  - Generate receipts
  - Monitor overall system

---

## 🛠️ Tech Stack

- **Backend**: Django  
- **Frontend**: HTML, CSS  
- **Database**: SQLite  

---
## 🚀 Methodology

<img width="769" height="910" alt="7f55b3d1-26b3-4874-878c-641a250888a3" src="https://github.com/user-attachments/assets/d4678fc5-1f51-4ac1-9403-bdd0346c1c45" />



## 📸 Screenshots

### 🍽️ Table User
![Table User Screenshot](screenshots/table1.png) 
![Table User Screenshot](screenshots/table2.png)  
![Table User Screenshot](screenshots/table3.png)  
![Table User Screenshot](screenshots/table4.png)    

### 👨‍🍳 Kitchen User
![Kitchen User Screenshot](screenshots/kitchen.png)    

### 💰 Counter User
![Counter User Screenshot](screenshots/counter1.png)  
![Counter User Screenshot](screenshots/counter2.png)  

---

## ⚡ How to Run Locally

```bash
# Clone repo
git clone https://github.com/Rutujakodag1/miniProject.git
cd miniProject

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations and start the server
python manage.py migrate
python manage.py runserver
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to use the app.

