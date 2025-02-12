# A Django Company App with Custom User Model and Company Model

## Overviews

This project is a Django application that demonstrates:

- A custom user model using email as the primary identifier.
- A Company model for managing company info.
- Standard authentication features (login, registration, logout) and profile management.
- standard users are only allowed to update their profile information
- Admin users are allowed to modify all company information and users information
- Token-based authentication and REST API endpoints for both the User and Company models.
- All the company information and users information are stored in sqlite(default) database


## How to Run the Application

Follow these steps to clone the repository, set up a virtual environment, install dependencies, and run the Django development server.

### 1. Clone the Repository and Navigate to directory

```bash
git clone https://github.com/bishnoipk01/assignment
cd assignment/P2-django_app
```

### 2. Create and Activate a Virtual Environment

For macOS/Linux:

```bash
python3 -m venv virtualenv
source virtualenv/bin/activate
```

For Windows:
```bash
python -m venv virtualenv
virtualenv\Scripts\activate
```

### 3. Navigate to the Project Directory

```bash
cd company_project
```

### 4. Install Dependencies

Install the required packages from requirements.txt:
```bash
pip install -r requirements.txt
```

### 5. Run the Django Development Server

Start the server with:
```bash
python manage.py runserver [port] (optional, default: 8000)
```

now open the application at http://localhost:[port]

### 6. Running tests

 To ensure that the core functionality is correct and handles various scenarios, a suite of tests has been provided. These tests verify the correct behavior of core functions.

 **Run the tests using:**

    ```bash
    python manage.py test
    ```



## Approach

1. **Custom Models**  
   - **User Model:** Created a custom user model (extending `AbstractBaseUser` and `PermissionsMixin`) that uses email for login. Added extra fields (first name, last name, phone number, bio) to support profile details.
   - **Company Model:** Developed a model to store company details (name, address, description).

2. **Authentication & API**  
   - Implemented user registration, login, and logout views using Django's built-in authentication along with custom forms.
   - Set up token-based authentication with Django REST Framework's authtoken module.
   - Created REST API endpoints to perform CRUD operations on both the User and Company models.


3. **User Profile Management**  
   - Developed views and forms to display and edit user profiles.
   - Restricted email changes by excluding the email field from profile edit forms, allowing only other fields (like first name, last name, phone number, and bio) to be updated.

4. **Project Organization**  
   - Organized code into logical directories: models, views, forms, static files, and templates.
   - Kept reusable components (like the navbar) in their own template files to avoid duplication.
   - Provided clear styling for forms to ensure they are user-friendly on all devices.


 ## API Endpoints

The project exposes a set of RESTful API endpoints for both the Company and User models. All endpoints require token-based authentication (using the token obtained via `POST /api-token-auth/`). Include the token in your request headers as follows:

Authorization: Token <your_token_here>

Alternatively, you can also see API documentation at [API_DOCS](https://documenter.getpostman.com/view/18134011/2sAYX9kfH8)

**Companies API:**

- **GET /api/companies/**  
  List all companies.

- **POST /api/companies/**  
  Create a new company (admin only).

- **GET /api/companies/<int:pk>/**  
  Retrieve details for a specific company.

- **PUT/PATCH /api/companies/<int:pk>/**  
  Update a specific company (admin only).

- **DELETE /api/companies/<int:pk>/**  
  Delete a specific company (admin only).

**Users API:**

- **GET /api/users/**  
  List all users.

- **POST /api/users/**  
  Create a new user (admin only).

- **GET /api/users/<int:pk>/**  
  Retrieve details for a specific user.

- **PUT/PATCH /api/users/<int:pk>/**  
  Update a specific user (admin or the user themselves).

- **DELETE /api/users/<int:pk>/**  
  Delete a specific user (admin or the user themselves).

**Token Authentication:**

- **POST /api-token-auth/**  
  Submit credentials (email and password) to obtain an authentication token.

