# Deployment Guide for Sentiment Analysis App on AWS EC2

This guide documents the steps to deploy the Sentiment Analysis Flask application to an AWS EC2 instance using Docker.

## Prerequisites
- An active AWS EC2 instance (Amazon Linux 2023 or similar).
- Key pair file (`.pem` or `.ppk`) for authentication.
- **WinSCP** installed for file transfer.
- **PuTTY** (or a terminal) installed for SSH access.
- Local project files ready in `deploy on aws/`.

## Step 0: Configure EC2 Security Group (Inbound Rules)

Before you can access your app or connect to the server, you must allow specific traffic in your EC2 Security Group.

1.  Go to the **AWS Console** > **EC2** > **Instances**.
2.  Select your instance and click the **Security** tab.
3.  Click the **Security Group ID** (e.g., `sg-01234...`).
4.  Click **Edit inbound rules** and ensure the following rules exist:

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| **HTTP** | TCP | **80** | **0.0.0.0/0** | Allows public access to your website |
| **SSH** | TCP | **22** | **My IP** (or 0.0.0.0/0) | Allows you to connect via PuTTY/WinSCP |

5.  Click **Save rules**.

---

## Step 1: File Transfer using WinSCP

1.  **Open WinSCP**.
2.  **New Session**:
    - **Host name**: Your EC2 Public IP (e.g., `13.60.76.117`).
    - **User name**: `ec2-user`.
    - **Advanced** > **SSH** > **Authentication**: Select your Private Key file.
    - Click **Login**.
3.  **Transfer Files**:
    - Navigate to the remote directory (default is `/home/ec2-user/`).
    - Drag and drop the contents of your local `deploy on aws` folder to the remote server.
    - **Important**: Ensure the `models` folder (containing `.pkl` files) is uploaded.

**Files to upload:**
- `app.py`
- `data_processing_and_features.py` (Critical: Helper functions)
- `Dockerfile`
- `requirements.txt`
- `models/` (Folder)
- `templates/` (Folder)

---

## Step 2: Server Setup & Deployment (PuTTY / SSH)

Connect to your instance using PuTTY or your terminal.

### 1. Initial Setup (First Time Only)
If this is a fresh instance, install Docker:

```bash
# Update the system
sudo yum update -y

# Install Docker
sudo yum install docker -y

# Start Docker service
sudo service docker start

# Enable Docker to start on boot
sudo systemchk config docker on

# Add ec2-user to the docker group (avoids using 'sudo' for docker commands)
sudo usermod -a -G docker ec2-user
```
*Note: After running the `usermod` command, you must **logout and log back in** for permissions to take effect.*

### 2. Deployment Commands (For Updates/Redeployment)

Run these commands whenever you update code or requirements.

**A. Stop and Remove Existing Container**
If a version of the app is already running, stop it first to free up Port 80.

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker rm $(docker ps -a -q)
```

**B. Build the Docker Image**
This packages your application and installs dependencies from `requirements.txt`.

```bash
# Build the image with the tag 'sentiment-app'
docker build -t sentiment-app .
```

**C. Run the Container**
This starts the application in the background (`-d`) on Port 80.
We add `--restart always` so the app restarts automatically if the server reboots.

```bash
docker run -d --restart always -p 80:80 sentiment-app
```

---

## Step 3: Verification & Troubleshooting

### Check if the container is running
```bash
docker ps
```
You should see `sentiment-app` listed with status "Up".

### View Application Logs
If the app isn't working, check the logs for errors (e.g., missing files, python errors).
```bash
# Replace <container_id> with the ID from 'docker ps'
docker logs <container_id>
```

### Access the App
Open your browser and visit: `http://<YOUR_EC2_PUBLIC_IP>/`

---

## Important Notes

1.  **Public IP Changes**: If you **Stop** and **Start** your EC2 instance, your Public IP address will change. You will need to use the new IP to access the site.
    - *Solution*: Allocate an **Elastic IP** in AWS Console and associate it with your instance for a permanent IP.
2.  **AWS Costs**: Remember to **Terminate** (delete) or **Stop** your instance when you are done to avoid unexpected charges.
3.  **Missing Files**: Always ensure `data_processing_and_features.py` is uploaded, or the app will fail to start.
