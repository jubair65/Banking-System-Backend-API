# Banking System Backend API

A secure RESTful banking backend built with **Django REST Framework and MySQL**. The system simulates core banking operations including customer registration, JWT authentication, bank account management, deposits, withdrawals, account-to-account transfers, transaction history, and administrator controls.

This project was developed as part of the **Sqrock IT Solutions Backend Development Internship — Project Phase 1**.

## Features

### Authentication & User Management

* Customer and Admin roles
* User signup and login
* JWT-based authentication
* Secure password hashing
* Protected API endpoints
* Role-based access control
* Customers cannot assign themselves the Admin role

### Bank Account Management

* Create a bank account
* Automatic account number generation
* Savings and Current account types
* View own account details
* View current balance
* Active and Blocked account status
* One bank account per customer

### Banking Transactions

* Deposit money
* Withdraw money
* Transfer money to another account
* Automatic balance updates
* Transaction records for all operations
* Insufficient-balance protection
* Negative balance prevention
* Atomic transaction processing
* Account status validation

### Transaction History

* View account transaction history
* Filter by transaction type
* Filter by date range
* Combined type and date filtering
* Incoming and outgoing transfer history
* Customer transaction isolation

### Admin Features

* View all users
* View all bank accounts
* View individual accounts
* View all transactions
* View transactions for a specific account
* Block accounts
* Unblock accounts
* Admin-only route protection

## Technologies Used

* **Python**
* **Django**
* **Django REST Framework**
* **Simple JWT**
* **MySQL**
* **mysqlclient**
* **python-dotenv**
* **Postman**
* **Git & GitHub**

## API Endpoints

### Authentication

| Method | Endpoint              | Access        | Description                  |
| ------ | --------------------- | ------------- | ---------------------------- |
| POST   | `/api/signup/`        | Public        | Register a customer          |
| POST   | `/api/login/`         | Public        | Login and receive JWT tokens |
| POST   | `/api/token/refresh/` | Public        | Refresh access token         |
| GET    | `/api/profile/`       | Authenticated | View logged-in user profile  |

### Account APIs

| Method | Endpoint               | Access   | Description           |
| ------ | ---------------------- | -------- | --------------------- |
| POST   | `/api/account/create/` | Customer | Create bank account   |
| GET    | `/api/account/me/`     | Customer | View own bank account |

### Transaction APIs

| Method | Endpoint             | Access   | Description              |
| ------ | -------------------- | -------- | ------------------------ |
| POST   | `/api/deposit/`      | Customer | Deposit money            |
| POST   | `/api/withdraw/`     | Customer | Withdraw money           |
| POST   | `/api/transfer/`     | Customer | Transfer money           |
| GET    | `/api/transactions/` | Customer | View transaction history |

### Transaction Filters

```text
GET /api/transactions/?type=deposit
GET /api/transactions/?type=withdraw
GET /api/transactions/?type=transfer
```

Date filtering:

```text
GET /api/transactions/?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
```

Combined filtering:

```text
GET /api/transactions/?type=transfer&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
```

### Admin APIs

| Method | Endpoint                                | Access | Description               |
| ------ | --------------------------------------- | ------ | ------------------------- |
| GET    | `/api/admin/users/`                     | Admin  | View all users            |
| GET    | `/api/admin/accounts/`                  | Admin  | View all accounts         |
| GET    | `/api/admin/accounts/<id>/`             | Admin  | View specific account     |
| GET    | `/api/admin/transactions/`              | Admin  | View all transactions     |
| GET    | `/api/admin/transactions/<account_id>/` | Admin  | View account transactions |
| POST   | `/api/admin/accounts/<id>/block/`       | Admin  | Block account             |
| POST   | `/api/admin/accounts/<id>/unblock/`     | Admin  | Unblock account           |

## Database Design

### Users

The custom user model stores:

```text
User
├── id
├── username
├── email
├── password
├── first_name
├── last_name
├── role
└── date_joined
```

Supported roles:

```text
customer
admin
```

### Bank Accounts

```text
BankAccount
├── id
├── user
├── account_number
├── account_type
├── balance
├── status
└── created_at
```

Account types:

```text
savings
current
```

Account statuses:

```text
active
blocked
```

### Transactions

```text
Transaction
├── id
├── from_account
├── to_account
├── amount
├── type
└── timestamp
```

Transaction types:

```text
deposit
withdraw
transfer
```

## Transaction Rules

### Deposit

```text
Current Balance + Deposit Amount = New Balance
```

### Withdrawal

A withdrawal is allowed only when:

```text
Withdrawal Amount <= Current Balance
```

### Transfer

For a successful transfer:

```text
Sender Balance - Transfer Amount
Receiver Balance + Transfer Amount
```

Both balance changes are processed atomically.

The system also prevents:

* Negative amounts
* Zero-value transactions
* Transfers to nonexistent accounts
* Transfers to the sender's own account
* Transfers from blocked accounts
* Transfers to blocked accounts
* Withdrawals exceeding available balance

## Security

The backend implements several security controls:

### Password Security

Passwords are securely hashed through Django's authentication system.

### JWT Authentication

Protected endpoints require a valid JWT access token.

Example:

```http
Authorization: Bearer <access_token>
```

### Role-Based Access Control

Admin APIs are restricted using a dedicated Admin permission class.

Customers attempting to access admin endpoints receive:

```text
403 Forbidden
```

### Account Ownership

Customer operations automatically use the authenticated user's account rather than accepting arbitrary account ownership from the request.

### Balance Protection

Customers cannot directly submit or modify their account balance through the API.

### Atomic Transactions

Deposit, withdrawal, and transfer operations use database transactions and row locking to protect balance integrity during concurrent operations.

## Project Structure

```text
Banking-System-Backend-API/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── banking/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jubair65/Banking-System-Backend-API.git
cd Banking-System-Backend-API
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Open MySQL and create:

```sql
CREATE DATABASE banking_db;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

DB_NAME=banking_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

Do not commit the real `.env` file to GitHub.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create an admin user

```bash
python manage.py createsuperuser
```

After creation, assign the user's application role as:

```text
admin
```

through Django Admin if necessary.

### 8. Run the development server

```bash
python manage.py runserver
```

API base URL:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

## Postman Testing

The API was tested using Postman through a complete end-to-end audit.

### Final Audit Result

```text
Requests: 39
Tests: 66
Passed: 66
Failed: 0
Pass Rate: 100%
```

The audit covered:

```text
Signup
Login
JWT authentication
Profile
Account creation
Account details
Deposits
Withdrawals
Overdraft protection
Transfers
Self-transfer protection
Transaction history
Transaction type filtering
Date filtering
Admin users
Admin accounts
Admin transactions
Role-based access control
Account blocking
Account unblocking
```

## Example Banking Flow

A typical customer workflow is:

```text
Signup
   ↓
Login
   ↓
Receive JWT
   ↓
Create Bank Account
   ↓
Deposit Money
   ↓
Withdraw Money
   ↓
Transfer Money
   ↓
View Transaction History
```

An administrator can additionally:

```text
View Users
   ↓
View Accounts
   ↓
View Transactions
   ↓
Block / Unblock Accounts
```



## 👨‍💻 Author

**Jubair Bin Hasan**

Computer Science & Engineering
University of Asia Pacific

---

## 📄 License

This project was developed for educational and internship purposes.