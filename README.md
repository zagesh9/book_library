# Book Library Management System

## Project Overview
A comprehensive web application for managing a book library with web scraping capabilities, role-based access control, and advanced book management features.

## Features

### User Roles
1. **Super Admin**
   - Full system access
   - Complete CRUD operations on books

2. **Admin**
   - Add, view, and edit book details
   - Web scraping functionality
   - Cannot delete books

3. **User**
   - View book catalog
   - Filter books by category

### Core Functionalities
- Book management (Add, View, Update, Delete)
- Web scraping from books.toscrape.com
- Category-based book filtering
- User authentication and authorization

## Default Credentials
- **Super Admin**
  - Username: superadmin
  - Password: super

- **Admin**
  - Username: admin
  - Password: admin

### Steps
1. Clone the repository
   ```bash
   git clone https://github.com/zagesh9/book_library.git
   cd book_library
   ```

2. Create virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create the admin and superadmin
   ```bash
   python create_users.py
   ```

5. Run the application
   ```bash
   python manage.py runserver
   ```

## Web Scraping
- Scrape book details from books.toscrape.com
- Extract: Title, Genre, Price, Description
- Admin can trigger scraping via dedicated interface
