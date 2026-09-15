# Blog & Article Management System

A dynamic, multi-user blogging platform built with Django and Bootstrap. This application supports full article lifecycle management, automated media optimization, nested comment threads, user dashboards, and visitor feedback mechanisms.

---

## Key Features

* Complete CRUD support for blog posts with category and tag relationships.
* Automated image processing: Cover photos are resized and cropped to 520x450 via Pillow using the Lanczos resampling filter.
* AJAX-driven endpoints for instant deletion of articles and cover media without page reload.
* Supports multi-level replies via self-referential relations for nested comments.
* Asynchronous AJAX toggle for liking/unliking comments.
* Custom user model (Account) extending Django's AbstractUser with support for custom avatars.
* Private user control panel displaying author-specific articles with pagination.
* Public author profiles showing personal bios and published posts.
* Asynchronous profile picture reset to default avatar.
* Text-based full search (Q lookups on title and body).
* Taxonomy filtering by category slugs and tag slugs.
* Global sidebar populated across templates using a Django Context Processor.
* Visitor feedback module via the Contact Us form.

---

## Tech Stack

* Backend: Python, Django
* Database: SQLite (development)
* Media & Image Processing: Pillow (PIL)
* Frontend: HTML5, CSS3, JavaScript (AJAX/Fetch), Bootstrap
* Architecture: Modular Django Apps (blog, authentication, main)

---

## Project Structure

```text
blog_project/
├── authentication/       # User authentication, custom Account model, profile views
├── blog/                 # Articles, tags, categories, nested comments, and AJAX likes
├── main/                 # Landing page, about page, and contact form handling
├── blog_project/         # Project configuration, settings, and main URL router
├── templates/            # Global HTML templates and includes
├── assets/               # Static assets (CSS, JS, Fonts, Vendor libraries)
├── media/                # Uploaded article covers and user avatars
├── manage.py
├── requirements.txt
└── README.md
```
## Application Routes and Endpoints

### Blog & Articles

| Route / Endpoint | HTTP Method | Access Level | Description |
| :--- | :---: | :---: | :--- |
| `/all-posts/` | GET | Public | Paginated list of articles with search, category, and tag filtering |
| `/article-detail/<slug>/` | GET | Public | Displays full article content, comments, and user interaction state |
| `/article/create/` | GET, POST | Logged-in | Renders form and processes new article creation |
| `/article/<id>/edit/` | GET, POST | Author Only | Renders form and updates an existing article |
| `/article/<id>/comment/add/` | POST | Logged-in | Submits a new comment or a nested reply to an article |
| `/comment/<id>/delete/` | POST | Author Only | Permanently deletes a specific comment |
| `/comment/<id>/like/` | POST | Logged-in | AJAX endpoint to toggle like/unlike on a comment |
| `/article/<id>/delete-cover/` | POST | Author Only | AJAX endpoint to remove only the cover image from storage |
| `/article/<id>/delete/` | POST | Author Only | AJAX endpoint to permanently delete an article and its media |

### Authentication & User Management

| Route / Endpoint | HTTP Method | Access Level | Description |
| :--- | :---: | :---: | :--- |
| `/register/` | GET, POST | Public | User account registration and automatic session login |
| `/login/` | GET, POST | Public | User authentication and session creation |
| `/logout/` | GET | Logged-in | Terminates the current authenticated session |
| `/user/panel/` | GET, POST | Logged-in | Personal dashboard to update profile info and manage user's articles |
| `/user/<username>/` | GET | Public | Public author profile showing published articles |
| `/profile/delete-image/` | POST | Logged-in | AJAX endpoint to remove profile picture and reset to default |

### General Pages

| Route / Endpoint | HTTP Method | Access Level | Description |
| :--- | :---: | :---: | :--- |
| `/` | GET | Public | Landing homepage showing banner articles and recent posts feed |
| `/about-us/` | GET | Public | Informational static page about the blog |
| `/contact-us/` | GET, POST | Public | Visitor feedback and contact inquiry form |

## Installation and Setup

Follow these steps to set up and run the project locally on your machine.

### Prerequisites

* Python (v3.10 or higher recommended)
* Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/Mohammad-RFE/blog_project.git
cd blog_project
```

### 2. Create and Activate a Virtual Environment
Windows:
```DOS
python -m venv venv
venv\Scripts\activate
```
Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an Administrator Account

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```
Open your browser and navigate to:
Web Application: http://127.0.0.1:8000/
Admin Dashboard: http://127.0.0.1:8000/admin/
