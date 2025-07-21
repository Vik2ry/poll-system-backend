# 🗳️ Online Poll System Backend  
By Olusegun Banji
## 📌 Overview  

This project focuses on developing a **scalable and efficient backend** for an online poll system. The backend provides APIs for **poll creation, user voting, and real-time result computation** while ensuring **optimized database performance and detailed API documentation**.  

This project highlights key aspects of **real-time data processing**, including:  
- 📡 **Building scalable APIs** for a voting system.  
- ⚡ **Optimizing database queries** for frequent operations.  
- 📜 **Providing clear and accessible API documentation** using Swagger.  

---

## 🎯 Project Goals  

The primary objectives of this backend system are:  

✅ **API Development** – Design RESTful APIs for poll management, voting, and fetching results.  
✅ **Database Efficiency** – Implement a schema optimized for real-time vote count computation.  
✅ **Comprehensive Documentation** – Use **Swagger** to provide detailed API references.  

---

## 🛠️ Technologies Used  

- **🐍 Django & Django Rest Framework (DRF)** – Backend framework for building APIs.  
- **🛢️ PostgreSQL** – Relational database for storing api data.
- **📜 Swagger (drf-yasg)** – API documentation.  

---

## 🚀 Key Features  

### 📊 **Poll Management**  
- APIs to **create, update, and manage polls** with multiple options.  
- Polls include metadata such as **creation date, expiration date**, and status.  

### 🎯 **Voting System**  
- Secure API allowing **authenticated users** to vote.  
- Prevent **duplicate voting** to maintain fairness.  

### 📈 **Real-Time Result Computation**  
- Automatically calculates **vote counts per option**.  
- **Optimized queries** for handling large datasets efficiently.  

### 📜 **API Documentation**  
- Fully documented API using **Swagger**.  
- Accessible at `/api/docs` for easy testing.  

---

## ⚙️ Installation & Setup  

### 1️⃣ **Prerequisites**  
- **Python 3.8+** installed  
- **Virtualenv** (or use Python’s built-in `venv`)  
- **PostgreSQL** (default database, but SQLite is also supported)  

### 2️⃣ **Clone the Repository**  

```bash
git clone https://github.com/your-username/online-poll-system.git
cd online-poll-system
```

3️⃣ Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux  
venv\Scripts\activate    # Windows  
pip install -r requirements.txt
```

4️⃣ Set Up Environment Variables

Create a `.env` file in the root directory and add the following:

```plaintext
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST= your_db_host
DATABASE_PORT=your_db_port
```

5️⃣ Apply Migrations, create a superuser and run the server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API will be accessible at: 📍 ```http://127.0.0.1:8000/api/```


## 📡 API Endpoints
 
- All endpoints except vote submission require **admin authentication**.
- Vote submission requires **participant authentication**.

### 🔹 Polls

* `GET /polls/` → Retrieve all polls
* `POST /polls/` → Create a new poll
* `GET /polls/{id}/` → Retrieve a poll
* `PUT /polls/{id}/` → Update a poll
* `PATCH /polls/{id}/` → Partially update a poll
* `DELETE /polls/{id}/` → Delete a poll
* `POST /polls/{id}/cast-vote/` → Submit a vote for a poll
* `GET /polls/{id}/options/` → Retrieve the list of options for a poll
* `POST /polls/{id}/options/` → Add a new option to a poll
* `PATCH /polls/{id}/options/{option_id}/` → Update an option in a poll
* `DELETE /polls/{id}/options/{option_id}/` → Delete an option in a poll
* `GET /polls/{id}/results/` → Retrieve the results of a poll

### 🔹 Users (Administrators and Participants)

* `GET /users/` → List all users
* `POST /users/` → Create a new user
* `GET /users/{id}/` → Retrieve a user
* `PUT /users/{id}/` → Update a user
* `PATCH /users/{id}/` → Partially update a user

## 📜 API Documentation

The API documentation is available at: 📍```http://127.0.0.1:8000/api/docs/```


## Author

👤 [8srael](https://www.github.com/vik2ry)