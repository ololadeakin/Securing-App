
# CST8919 Lab 1 - Flask + Auth0 Login

## Setup Instructions

### 1. Clone and Install
```bash
git clone https://github.com/ololadeakin/oauth.git
cd oauth

pip3 install -r requirements.txt
```
### 2. Set Environment Variables
Create a .env file:

```bash
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_secret
AUTH0_DOMAIN=your-tenant.auth0.com
APP_SECRET_KEY=your_random_secret_keyy

```
### 3. Run the App
```bash

python3 server.py
```
### 4. Navigate to:
http://127.0.0.1:3000 - Home

http://127.0.0.1:3000/protected - Protected Page

### 🎥 Demo Video
[Watch Demo](https://youtu.be/utiNm8-J8_U)

## What I Learned
How to integrate Auth0 with Flask

How to protect routes using session-based authentication