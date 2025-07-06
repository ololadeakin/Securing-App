# 🛡️ Securing and Monitoring an Authenticated Flask App

This project combines Auth0 authentication with Azure App Service deployment and logging to demonstrate a secure, monitored, production-ready Flask application.

## 🔧 Tech Stack

* Flask
* Auth0 (SSO)
* Azure App Service
* Azure Log Analytics + KQL
* Python `logging` module
* GitHub for version control

---

## 🚀 Project Overview

As part of a DevSecOps team, you're tasked with securing a Flask app using SSO (Auth0), deploying it to Azure, and monitoring user behavior through Azure Monitor. This includes logging login events, tracking protected route access, detecting suspicious activity, and configuring alerts.

---

## 🧐 Key Features

* 🔐 **SSO Authentication** via Auth0
* 📊 **Structured Logging** of:

  * Every login (user\_id, email, timestamp)
  * Every `/protected` route access
  * Unauthorized access attempts
* ☁️ **Deployed to Azure App Service**
* 🕵️‍♂️ **KQL Query** to detect high-volume access patterns
* 📣 **Azure Alert** triggers when abnormal behavior is detected

---

## 🛠️ Setup Instructions

### 1. Clone & Create Virtual Environment

```bash
git clone https://github.com/ololadeakin/Securing-App.git
cd Securing-App
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 2. Create `.env` from Template

Create a `.env` file using the provided `.env.example`.

```env
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_DOMAIN=your-domain.auth0.com
APP_SECRET_KEY=your-random-secret-key
PORT=3000
```

---

### 3. Run Locally

```bash
python app.py
```

Navigate to: `http://localhost:3000`

---

### 4. Deploy to Azure App Service

* Create an App Service Plan and Web App via Azure Portal or CLI
* Push to GitHub and connect deployment center to your repo
* Set the **App Settings** (environment variables) in the Azure portal
* Enable **App Service Logs** and **Diagnostic Settings**:

  * AppServiceConsoleLogs
  * Application Logs
  * Platform Logs
  * Send to Log Analytics

---

### 5. Logging Behavior

| Action              | Log Example                                               |
| ------------------- | --------------------------------------------------------- |
| Login Attempt       | `[LOGIN_ATTEMPT] Redirecting to Auth0...`                 |
| Login Success       | `[LOGIN_SUCCESS] user_id=... email=... timestamp=...`     |
| Unauthorized Access | `[UNAUTHORIZED_ACCESS] Attempted access to /protected...` |
| Access Granted      | `[ACCESS_GRANTED] /protected accessed by user_id=...`     |

Logs are emitted to stdout and picked up by AppServiceConsoleLogs.

---

### 6. KQL Query: Suspicious Activity

Detect users accessing `/protected` more than 10 times in 15 mins:

```kusto
AppServiceConsoleLogs
| where TimeGenerated > ago(15m)
| where ResultDescription has "[ACCESS_GRANTED]"
| extend user_id = extract("user_id=(.*?)\\,", 1, ResultDescription)
| summarize count() by user_id
| where count_ > 10
```

---

### 7. Azure Alert

**Alert Criteria**:

* Based on the query above
* Threshold: Access count > 10 in 15 minutes
* Severity: 3 (Low)
* Action: Email alert via Action Group

---

## 📸 Demo Walkthrough (YouTube)

🔗 [Watch the full deployment + monitoring demo](https://youtu.be/wTLWLZfDqSs)

> Includes: Auth0 login, structured logs, KQL detection, and triggered email alert.

---

## 📂 Repo Structure

```
.
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── templates/
│   ├── home.html
│   └── protected.html
└── test-app.http
```

---

## ⚠️ Challenges Faced

| Challenge                           | Solution                                                    |
| ----------------------------------- | ----------------------------------------------------------- |
| Logs not appearing in Log Analytics | Ensured logs were emitted via `StreamHandler(sys.stdout)`   |
| Azure not picking up env vars       | Used Azure App Settings panel instead of `.env`             |
| Log Analytics KQL confusion         | Used `ResultDescription` field from `AppServiceConsoleLogs` |
| Callback URL errors                 | Fixed by correctly updating Auth0 allowed URLs              |
| Alert setup complexity              | Used GUI + custom KQL to link to alert logic                |

---

## ✅ Improvements

* Store logs in Blob for long-term auditing
* Add role-based access for `/protected`
* Integrate with Microsoft Sentinel for enhanced detection

---

## 📋 License

This project is part of CST8919 course work (Summer 2025), for educational purposes only.
