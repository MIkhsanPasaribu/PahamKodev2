# 🚀 Panduan Deployment PahamKode ke Azure VM

Panduan lengkap untuk deploy dan troubleshoot aplikasi **PahamKode Streamlit** di Azure Virtual Machine.

---

## 📋 Prerequisites

Sebelum deploy, pastikan sudah setup:

1. ✅ **Azure VM B1s** (Ubuntu 22.04 LTS)
2. ✅ **Azure Cosmos DB** (MongoDB API) - dengan connection string
3. ✅ **GitHub Token** - untuk GitHub Models (AI)
4. ✅ **SSH Access** ke VM
5. ✅ **Domain** (optional - bisa pakai IP VM)

---

## 🔧 Initial Server Setup (First Time Only)

### Step 1: Install Dependencies di VM

SSH ke VM dan install required packages:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install Nginx (reverse proxy)
sudo apt install -y nginx

# Install Git
sudo apt install -y git

# Install build tools (untuk compile dependencies)
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

### Step 2: Clone Repository

```bash
# Clone ke home directory
cd ~
git clone https://github.com/MIkhsanPasaribu/PahamKodev2.git
cd PahamKodev2
```

### Step 3: Setup Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy .env.example atau buat .env baru
nano .env
```

Isi dengan konfigurasi production:

```bash
# Database - Azure Cosmos DB (MongoDB API)
DATABASE_URL=mongodb://pahamkode-cosmos:YOUR_KEY@pahamkode-cosmos.mongo.cosmos.azure.com:10255/pahamkode-db?ssl=true&retrywrites=false&replicaSet=globaldb

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AI Provider - GitHub Models (FREE)
USE_GITHUB_MODELS=true
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_MODEL_NAME=gpt-4o-mini

# Application Settings
ENVIRONMENT=production
LOG_LEVEL=INFO
STREAMLIT_PORT=8501
```

**⚠️ PENTING**: Ganti `YOUR_KEY` dan `your_github_token_here` dengan credentials asli!

### Step 5: Install Systemd Service

```bash
# Copy service file
sudo cp deployment/pahamkode.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (auto-start on boot)
sudo systemctl enable pahamkode

# Start service
sudo systemctl start pahamkode

# Check status
sudo systemctl status pahamkode
```

**Expected Output:**

```
● pahamkode.service - PahamKode Streamlit App
     Loaded: loaded (/etc/systemd/system/pahamkode.service; enabled)
     Active: active (running) since ...
```

### Step 6: Configure Nginx

```bash
# Copy nginx config
sudo cp deployment/nginx-pahamkode.conf /etc/nginx/sites-available/pahamkode

# Create symlink untuk enable site
sudo ln -s /etc/nginx/sites-available/pahamkode /etc/nginx/sites-enabled/

# Remove default nginx config (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### Step 7: Open Firewall Ports

```bash
# Allow HTTP (port 80)
sudo ufw allow 80/tcp

# Allow HTTPS (port 443) - untuk SSL nanti
sudo ufw allow 443/tcp

# Allow Streamlit port (8501) - optional, hanya untuk direct access
sudo ufw allow 8501/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### Step 8: Verify Deployment

```bash
# Check service status
sudo systemctl status pahamkode

# View logs
sudo journalctl -u pahamkode -f

# Test local access
curl http://localhost:8501

# Test via nginx
curl http://localhost
```

Buka browser dan akses:

- **Direct**: `http://YOUR_VM_IP:8501`
- **Via Nginx**: `http://YOUR_VM_IP` (port 80)

---

## 🔄 Update Deployment (Subsequent Deploys)

Untuk update code setelah push ke GitHub:

### Option 1: Automated Deploy Script

```bash
cd ~/PahamKodev2
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

Script akan otomatis:

1. ✅ Backup .env
2. ✅ Pull latest code
3. ✅ Restore .env
4. ✅ Update dependencies
5. ✅ Restart services
6. ✅ Verify deployment

### Option 2: Manual Deploy

```bash
cd ~/PahamKodev2

# Backup .env
cp .env .env.backup

# Pull latest code
git pull origin main

# Restore .env
cp .env.backup .env

# Activate venv & update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart pahamkode

# Check status
sudo systemctl status pahamkode
```

---

## 🐛 Troubleshooting

### Problem 1: 502 Bad Gateway

**Symptoms:**

- Nginx menampilkan "502 Bad Gateway"
- Service status: `Active: active (running)` tapi app tidak respond

**Root Cause:**

- Service running uvicorn (FastAPI) instead of Streamlit
- Wrong service configuration

**Fix:**

```bash
# 1. Stop old service
sudo systemctl stop pahamkode

# 2. Update service file
sudo cp deployment/pahamkode.service /etc/systemd/system/

# 3. Reload systemd
sudo systemctl daemon-reload

# 4. Start service
sudo systemctl start pahamkode

# 5. Verify
sudo systemctl status pahamkode
# Should show: ExecStart=.../streamlit run app/main.py

# 6. Check logs
sudo journalctl -u pahamkode -n 50
```

### Problem 2: Service Failed to Start

**Check logs:**

```bash
sudo journalctl -u pahamkode -xe
```

**Common Issues:**

**A) Module not found:**

```
ModuleNotFoundError: No module named 'streamlit'
```

**Fix:**

```bash
cd ~/PahamKodev2
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart pahamkode
```

**B) Database connection error:**

```
Failed to connect to database
```

**Fix:**

```bash
# Check .env DATABASE_URL
nano .env

# Verify connection string format:
# mongodb://USER:PASSWORD@HOST:10255/DATABASE?ssl=true&...

# Restart service
sudo systemctl restart pahamkode
```

**C) Permission denied:**

```
Permission denied: '/home/ikhsan/PahamKodev2'
```

**Fix:**

```bash
# Fix ownership
sudo chown -R ikhsan:ikhsan ~/PahamKodev2

# Fix permissions
chmod +x deployment/deploy.sh
```

### Problem 3: Streamlit Not Responding

**Check if Streamlit is running:**

```bash
# Check process
ps aux | grep streamlit

# Check port
sudo netstat -tlnp | grep 8501

# Test local access
curl http://localhost:8501
```

**If not running:**

```bash
# Restart service
sudo systemctl restart pahamkode

# Watch logs untuk error
sudo journalctl -u pahamkode -f
```

### Problem 4: Nginx Configuration Error

**Test nginx config:**

```bash
sudo nginx -t
```

**If error:**

```bash
# View error details
sudo nginx -t 2>&1

# Common fixes:
# 1. Check syntax errors
sudo nano /etc/nginx/sites-available/pahamkode

# 2. Verify symlink exists
ls -la /etc/nginx/sites-enabled/

# 3. Recreate symlink if missing
sudo ln -sf /etc/nginx/sites-available/pahamkode /etc/nginx/sites-enabled/

# 4. Restart nginx
sudo systemctl restart nginx
```

### Problem 5: WebSocket Connection Failed

**Symptoms:**

- App loads tapi tidak interactive
- Error di browser console: "WebSocket connection failed"

**Fix - Update Nginx Config:**

```bash
sudo nano /etc/nginx/sites-available/pahamkode
```

Pastikan ada WebSocket headers:

```nginx
location / {
    proxy_pass http://localhost:8501;
    proxy_http_version 1.1;

    # WebSocket support (CRITICAL!)
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    proxy_buffering off;
}
```

Restart nginx:

```bash
sudo systemctl restart nginx
```

---

## 📊 Monitoring & Logs

### View Real-time Logs

```bash
# Follow service logs
sudo journalctl -u pahamkode -f

# Last 100 lines
sudo journalctl -u pahamkode -n 100

# Logs from specific time
sudo journalctl -u pahamkode --since "1 hour ago"

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### Check Service Status

```bash
# Service status
sudo systemctl status pahamkode

# Is service active?
sudo systemctl is-active pahamkode

# Is service enabled (auto-start)?
sudo systemctl is-enabled pahamkode
```

### Check Resource Usage

```bash
# Memory usage
free -h

# CPU usage
top -bn1 | grep "Cpu(s)"

# Disk usage
df -h

# Process info
ps aux | grep streamlit
```

---

## 🔒 Security Best Practices

### 1. Firewall Configuration

```bash
# Only allow necessary ports
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Secure .env File

```bash
# Restrict .env permissions
chmod 600 ~/.env
```

### 3. Regular Updates

```bash
# Update system packages weekly
sudo apt update && sudo apt upgrade -y

# Update Python dependencies
cd ~/PahamKodev2
source venv/bin/activate
pip install --upgrade pip
pip list --outdated
```

### 4. Setup SSL with Let's Encrypt (HTTPS)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (ganti YOUR_DOMAIN)
sudo certbot --nginx -d YOUR_DOMAIN.com -d www.YOUR_DOMAIN.com

# Auto-renewal test
sudo certbot renew --dry-run
```

---

## 📝 Useful Commands Cheat Sheet

| Task               | Command                              |
| ------------------ | ------------------------------------ |
| Start service      | `sudo systemctl start pahamkode`     |
| Stop service       | `sudo systemctl stop pahamkode`      |
| Restart service    | `sudo systemctl restart pahamkode`   |
| View status        | `sudo systemctl status pahamkode`    |
| Enable auto-start  | `sudo systemctl enable pahamkode`    |
| Disable auto-start | `sudo systemctl disable pahamkode`   |
| View logs (live)   | `sudo journalctl -u pahamkode -f`    |
| View last 50 logs  | `sudo journalctl -u pahamkode -n 50` |
| Restart nginx      | `sudo systemctl restart nginx`       |
| Test nginx config  | `sudo nginx -t`                      |
| Reload systemd     | `sudo systemctl daemon-reload`       |
| Deploy latest code | `./deployment/deploy.sh`             |

---

## ✅ Deployment Checklist

Before marking deployment as complete, verify:

- [ ] Service status: `Active: active (running)`
- [ ] App responds on `http://localhost:8501`
- [ ] Nginx forwards correctly (no 502)
- [ ] WebSocket connection works (interactive UI)
- [ ] Database connection successful
- [ ] AI (GitHub Models) working
- [ ] Login/Register functional
- [ ] No errors in logs (`journalctl -u pahamkode -n 50`)
- [ ] Firewall allows HTTP/HTTPS
- [ ] .env file secured (permissions 600)
- [ ] SSL configured (optional but recommended)

---

## 🆘 Support

Jika masih ada masalah setelah mengikuti panduan ini:

1. **Check Logs First**: `sudo journalctl -u pahamkode -xe`
2. **Verify Service File**: `sudo systemctl cat pahamkode`
3. **Test Streamlit Manually**:
   ```bash
   cd ~/PahamKodev2
   source venv/bin/activate
   streamlit run app/main.py
   ```
4. **Create GitHub Issue**: [PahamKodev2 Issues](https://github.com/MIkhsanPasaribu/PahamKodev2/issues)

---

**Good luck with deployment! 🚀**
