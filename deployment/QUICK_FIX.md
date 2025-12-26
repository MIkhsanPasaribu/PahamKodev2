# 🔧 Quick Fix untuk 502 Bad Gateway

## 🚨 Masalah

```
502 Bad Gateway
Service running: uvicorn (FastAPI) ❌
Should be: streamlit (Streamlit app) ✅
```

## ⚡ Quick Fix (Run di Server)

SSH ke VM dan jalankan commands ini:

```bash
# 1. Stop service yang salah
sudo systemctl stop pahamkode

# 2. Backup .env (PENTING!)
cd ~/PahamKodev2
cp .env .env.backup

# 3. Pull latest code (dengan fix deployment)
git pull origin main

# 4. Restore .env
cp .env.backup .env

# 5. Update systemd service
sudo cp deployment/pahamkode.service /etc/systemd/system/
sudo systemctl daemon-reload

# 6. Update nginx
sudo cp deployment/nginx-pahamkode.conf /etc/nginx/sites-available/pahamkode
sudo nginx -t

# 7. Restart everything
sudo systemctl restart pahamkode
sudo systemctl restart nginx

# 8. Verify
sudo systemctl status pahamkode
```

## ✅ Expected Result

Service status harus menunjukkan:

```
● pahamkode.service - PahamKode Streamlit App
     Active: active (running)

ExecStart=/home/ikhsan/PahamKodev2/venv/bin/streamlit run app/main.py
```

Bukan lagi:

```
❌ ExecStart=.../uvicorn app.main:app  (OLD/WRONG)
```

## 🧪 Test

```bash
# Test 1: Check service
sudo systemctl status pahamkode

# Test 2: Check logs
sudo journalctl -u pahamkode -n 20

# Test 3: Test local access
curl http://localhost:8501

# Test 4: Open browser
# http://YOUR_VM_IP:8501
```

## 📋 Apa yang Berubah?

| File                              | Changes                                   |
| --------------------------------- | ----------------------------------------- |
| `deployment/pahamkode.service`    | ✅ Fixed: uvicorn → streamlit             |
| `deployment/nginx-pahamkode.conf` | ✅ Added WebSocket support                |
| `deployment/deploy.sh`            | ✅ New: Automated deployment script       |
| `.streamlit/config.toml`          | ✅ New: Production Streamlit settings     |
| `deployment/DEPLOYMENT_GUIDE.md`  | ✅ New: Complete deployment documentation |

## 🆘 Jika Masih Error

1. **Check Logs**:

   ```bash
   sudo journalctl -u pahamkode -xe
   ```

2. **Test Manual**:

   ```bash
   cd ~/PahamKodev2
   source venv/bin/activate
   streamlit run app/main.py
   ```

3. **Verify Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Check .env**:
   ```bash
   cat .env
   # Pastikan DATABASE_URL dan GITHUB_TOKEN ada!
   ```

---

**Full Documentation**: Lihat `deployment/DEPLOYMENT_GUIDE.md`
