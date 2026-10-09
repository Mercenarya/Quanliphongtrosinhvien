# AI Rules and Skills for Room Rental Contract Management System

This document summarizes the AI rules and skills created for the Django-based room rental contract management system.

## Created Files

### Rules
- `.claude/rules/project-identity.md` - Defines project identity, technical details, and development guidelines

### Skills
- `.claude/skills/django-contract-management.md` - Django development guidance specific to this contract management system
- `.claude/skills/rental-workflow.md` - Focuses on rental business logic and workflows
- `.claude/skills/ajax-api-integration.md` - Guidance for AJAX/API integration patterns used in the system
- `.claude/skills/testing-quality-assurance.md` - Testing and quality assurance practices
- `.claude/skills/project-setup.md` - Setup and configuration guidance for development and deployment

### Project Configuration
- `CLAUDE.md` - Main Claude Code configuration file referencing the rules and skills
- `.claude/settings.local.json` - Existing permissions configuration (enhanced with project-specific details)

## Purpose
These rules and skills help Claude Code understand and work effectively with this Django project by providing:
1. Context about the project's purpose and technical structure
2. Specialized guidance for common development tasks
3. Best practices for maintaining code quality and consistency
4. Guidance on testing, setup, and deployment
5. Specific advice for the rental business logic and workflows

## Usage
When working on this project with Claude Code:
1. The CLAUDE.md file provides overall guidance
2. Refer to specific rules and skills based on your task type
3. Follow the conventions and patterns outlined in the documentation
4. Use the skills as references when implementing features, fixing bugs, or improving the system

## Project Background
This is a Django 6.0.6 web application for managing room rentals featuring:
- Room and Contract models with proper relationships
- CRUD operations for contracts with room availability checking
- Bootstrap 5 frontend with vanilla JavaScript
- AJAX/API integration for dynamic user experience
- CSRF protection and proper HTTP method usage
- Responsive design for room and contract management

The system allows users to:
- View available and rented rooms
- Create new rental contracts with validation
- View existing contracts
- Delete contracts (which updates room status to available)
- Track tenant information and contract details

Each skill provides targeted guidance to help maintain consistency, quality, and effectiveness when working on this specific project.