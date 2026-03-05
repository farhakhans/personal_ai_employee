---
title: Personal AI Employee
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# 🤖 Personal AI Employee

Complete AI-powered employee management system deployed on Hugging Face Spaces.

## Features

- 🔐 User Authentication (JWT)
- 📊 Multi-tier Dashboards (Bronze/Silver/Gold/Platinum)
- 👥 Customer Management
- 💼 Employee Management
- 💰 Payment Tracking
- 📱 Notifications
- ⚙️ Settings Management

## Default Login Credentials

| Email | Password | Tier |
|-------|----------|------|
| `admin@employee.ai` | `Admin@2026!` | Platinum |
| `manager@employee.ai` | `Manager@2026!` | Gold |
| `user@employee.ai` | `User@2026!` | Bronze |

## Tech Stack

- **Backend:** Flask (Python 3.12)
- **Database:** SQLite
- **Authentication:** JWT
- **Deployment:** Docker on Hugging Face Spaces

## Running Locally

```bash
# Clone the repository
git clone https://github.com/farhakhans/personal_ai_employee.git
cd personal_ai_employee

# Install dependencies
pip install -r requirements.txt

# Run the application
python api_routes.py
```

Access at: `http://localhost:5000`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key | Auto-generated |
| `VAULT_PATH` | Vault storage path | `/tmp/vault` |
| `ANTHROPIC_API_KEY` | AI API key (optional) | - |

## License

MIT License
