# Project Identity: Room Rental Contract Management System

## Overview

This is a Django-based web application for managing room rentals and contracts. The system allows users to:

- View and manage rooms (available/rented)
- Create, view, and delete rental contracts
- Track tenant information and contract details

## Key Technical Details

- **Framework**: Django 6.0.6
- **Database**: SQLite3 (rental.db)
- **Frontend**: Bootstrap 5.3.3 with vanilla JavaScript
- **Authentication**: Django built-in auth system
- **Security**: CSRF protection enabled

## Core Models

1. **Room**: Represents a rental room with fields for ID, name, area, price, and status (FREE/RENTED)
2. **Contract**: Represents a rental agreement with fields for ID, room (foreign key), tenant name, ID card, contract date, and duration

## Key Features

- Contract creation with validation (room availability, duplicate contract ID prevention)
- Contract deletion with automatic room status update
- Room listing with filtering by availability
- Responsive design using Bootstrap
- REST-like API endpoints for AJAX interactions
- Form validation and error handling

## Development Guidelines

1. Follow Django conventions and best practices
2. Maintain CSRF protection for all state-changing operations
3. Use proper HTTP methods (POST for creates, DELETE for deletes, GET for lists, PUT for Update )
4. Validate all user input both client-side and server-side
5. Handle database transactions properly for data consistency
6. Keep frontend code clean and maintainable
7. Follow existing code patterns in the project
8. Ensure proper error handling and user feedback
