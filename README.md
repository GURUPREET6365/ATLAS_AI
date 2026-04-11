# ATLAS AI

ATLAS AI is my personal backend project for building an assistant that brings together AI, Telegram automation, expense tracking, and hardware automation in one system.

I built this project to learn by making something genuinely useful for myself instead of creating isolated demo apps. The idea is simple: one assistant that can help me through chat, keep track of expenses, monitor my laptop battery, and trigger real-world device actions when needed.

## Overview

This repository is the backend for ATLAS AI. Right now the server runs on my own machine, and it is built with FastAPI to handle:

- Telegram bot webhook processing
- user verification
- expense management APIs
- Gemini-based AI response integration
- battery monitoring
- MQTT-based hardware control
- authentication utilities
- database management with SQLAlchemy and Alembic

This is an active personal project, so some parts are more complete than others. The goal is to keep improving it into a practical everyday assistant.

## Why I Made This

I wanted one project where I could combine several things I was learning and interested in:

- backend development
- API design
- database modeling
- Telegram bot workflows
- AI integration
- automation
- hardware communication

Instead of building separate practice projects for each topic, I decided to connect them into one system with a personal use case.

## Features

### Telegram bot integration

ATLAS AI receives Telegram webhook events and responds to bot commands after verifying the user.

Commands currently represented in the code include:

- `/start`
- `/add_expense`
- `/battery`
- `/view_expense`
- `/add_user`
- `/turn_switch_on`

### Expense tracking

The assistant can store and manage expense entries through API endpoints. This part of the project is meant to make personal expense logging simpler through Telegram and related web flows.

Supported flows in the backend:

- add expenses
- view filtered expenses
- delete expenses

### AI integration

The project includes a Gemini integration layer for generating AI responses from text prompts.

### Battery monitoring

When the app starts, it launches a background task that monitors my laptop battery level and charging state. Based on the conditions, it can notify through Telegram and trigger hardware-related actions.

### Servo motor charging automation

To keep charging regular on my machine, I connected the system to a servo motor setup. The backend communicates using MQTT and sends messages that make the servo motor turn the charging switch on when needed.

So in practice, this project is not only a software assistant, but also a small automation system connected to my real charging setup.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Telegram Bot API
- Google Gemini API
- MQTT
- FastAPI Mail
- Uvicorn

## Project Structure

```text
ATLAS_API/
  app/
    main.py
    database/
    frontend_endpoint/
    micro_controller/
    telegram/
    utilities/
alembic/
requirements.txt
```

### Folder summary

- `ATLAS_API/app/main.py` contains the FastAPI app and router registration
- `database/` contains the DB connection, ORM models, and pydantic models
- `telegram/` contains Telegram webhook logic and web-related expense endpoints
- `frontend_endpoint/` contains login and auth-related endpoints/utilities
- `micro_controller/` contains MQTT and hardware-related code
- `utilities/` contains helper modules like LLM calls, battery monitoring, and email alerts
- `alembic/` contains migration files for database schema changes

## How It Works

At a high level, the system works like this:

1. Telegram sends events to the webhook endpoint.
2. The backend verifies whether the user is allowed to interact with the assistant.
3. Commands and requests are processed depending on the message type.
4. Expense data is stored and fetched from the database.
5. Utility services handle AI calls, email warnings, battery checks, and MQTT publishing.
6. MQTT messages are used to communicate with a servo motor that physically turns the switch on for charging control.

## Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/atlas_ai

TELEGRAM_BOT_API_TOKEN=your_telegram_bot_token
ADMIN_CHAT_ID=your_telegram_chat_id

SECRET_KEY=your_jwt_secret
ALGORITHM=HS256

CLIENT_ID_MQTT=atlas-ai-client
BROKER_MQTT=broker.hivemq.com

MAIL_USERNAME=your_email
ATLAS_APP_PASSWORD=your_app_password
MAIL_FROM=your_email
MAIL_TO=your_alert_email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_FROM_NAME=Atlas Bot
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
USE_CREDENTIALS=true
VALIDATE_CERTS=true

ADMIN_FIRST_NAME=your_first_name
ADMIN_LAST_NAME=your_last_name
ADMIN_EMAIL=your_email
ADMIN_ROLE=admin
ADMIN_PASSWORD=your_password
ADMIN_PHONE_NUMBER=your_phone_number
```

These are the main variables currently referenced in the codebase.

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ATLAS_AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add the required values.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Create the admin user if needed

```bash
python -m ATLAS_API.app.frontend_endpoint.utilities.create_admin
```

### 7. Start the server

```bash
uvicorn ATLAS_API.app.main:app --reload
```

The API should then be available at:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## Main API Routes

### Core

- `GET /` - health/message route

### Telegram

- `POST /telegram/webhook` - Telegram webhook receiver
- `POST /telegram/web/expense` - fetch filtered expenses
- `POST /telegram/web/add/expense` - add expenses
- `DELETE /telegram/web/expense/delete` - delete an expense

### Auth

- `POST /api/login` - login endpoint
- `GET /api/me` - get current authenticated user

## Current Status

This project is functional in parts and still evolving in others. It already shows the main architecture and direction of the assistant, but there are still areas that need cleanup and refinement.

The current version runs on my own machine and is designed around my personal workflow, including the MQTT-connected servo motor charging setup.

Some parts are experimental because this is a personal build-first, improve-next project.

## Future Improvements

- improve authentication and user management
- clean up incomplete or rough modules
- add better error handling
- improve logging and observability
- expand AI assistant features
- improve Telegram web app workflows
- add automated tests
- make deployment smoother

## What This README Should Contain

For a personal project, a strong `README.md` should usually include:

- project name
- short project summary
- why you built it
- main features
- tech stack
- installation steps
- environment variables
- how to run the project
- important routes or usage examples
- current status or limitations
- future plans

That combination helps people quickly understand both the technical side of the project and the story behind it.
