# Quick Trip: Intercity Transportation System
Overview
Quick Trip is a comprehensive intercity transportation system designed to streamline travel between cities. It offers a robust platform for managing passengers, vehicles, and drivers, ensuring a secure, efficient, and reliable travel experience. With both web and mobile applications, Quick Trip aims to provide seamless access and management for all stakeholders.

# Features
Quick Trip provides a wide range of functionalities to support its intercity transportation operations:

User Management:

Registration: Allows new passengers, drivers, and sub-admins to register.

Management & Modification: Comprehensive tools for administrators to manage and modify vehicle, driver, and sub-admin accounts.

Vehicle Management: Registration and management of various vehicle types.

Driver Management: Detailed profiles and management for drivers.

Location Tracking: Real-time tracking of vehicles and trips for enhanced security and operational oversight using Google Maps.

National ID Verification: Integration for verifying national IDs to ensure user authenticity and compliance.

Payment & Payroll System: Secure processing of payments for trips and efficient management of driver payroll.

Analytics Dashboard: A centralized dashboard providing key insights into operations, performance, and trends.

Reporting: Generation of detailed reports for various aspects of the transportation system.

Account Management: Tools for users to manage their personal profiles, trip history, and preferences.

Notifications: Real-time notifications for trip updates, payments, and administrative alerts.

Ticket Managment : Ticket purchasing , tracking , and keeping track of travel history for passengers .

On site functionalities : Vehicle Queueing , payment verification and Exit slip generation .

# Technology Stack
Quick Trip is built using a modern and scalable technology stack:

# Backend:

Django: A high-level Python web framework that encourages rapid development and clean, pragmatic design. Utilized for its robust ORM (Object-Relational Mapping) and simplified model management, minimizing database setup and complex algorithm integration with its MVC (Model-View-Controller) architecture.

Django REST Framework: For building powerful and flexible REST APIs.

Simple JWT: For secure and efficient token-based authentication.

# Frontend:

React: A JavaScript library for building user interfaces. Used for both the web application and potentially the mobile application (via React Native if applicable).

# Database:

PostgreSQL: A powerful, open-source object-relational database system known for its reliability, feature robustness, and performance.

# Mapping & Location Services:

Google Maps API: Integrated for location tracking, route planning, and geographical data visualization.

# API Testing:

Postman: Used for API development, testing, and documentation.

# Unit Testing:

Pytest: A Python testing framework used for writing simple, scalable, and efficient unit tests for the backend.

# Getting Started
To get a local copy of Quick Trip up and running, follow these steps.

# Prerequisites
    Python 3.8+
    React npm (vite)
    PostgreSQL
    Git
    AWS EC2 instance (for deployment)
    Google Maps API Key

# Installation
Clone the Repository:
git clone https://github.com/BOLT4L/Quicktrip/

# Backend Setup (Django):

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.text


# Run database migrations
python backend/manage.py migrate

# Create a superuser (for admin access)
python backend/manage.py createsuperuser

# Run the Django development server
python backend/manage.py runserver

The backend will typically run on http://localhost:8000

Frontend Setup (React):

cd frontend

# Install dependencies
npm install  or yarn install

# Change api gateway 
Inside the .env fiel change url ot = http://localhost:8000
  
# Run the React development server
npm run dev or yarn start

The frontend will typically run on http://localhost:5173/ 


Deployment to AWS EC2
Refer to the Implementing HTTPS for Your Web Application on AWS EC2 guide for detailed steps on deploying your Django backend to EC2 and securing it with HTTPS using Nginx/Apache or an Application Load Balancer (ALB). Remember to configure CORS on your Django backend to allow requests from your frontend's domain.

Collaboration & Contribution
We welcome contributions! If you're interested in improving Quick Trip, please fork the repository, create a new branch, and submit a pull request with your changes. Ensure your code adheres to our style guidelines and passes all tests.

