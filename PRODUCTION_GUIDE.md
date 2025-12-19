# 🚀 Production Deployment Guide

## ✅ Files Created

- **wsgi.py** - WSGI entry point for production servers
- **gunicorn** - Production-grade HTTP server installed

---

## 🖥️ Running Options

### **Development (Current)**
```bash
python main.py
```
- ✅ Auto-reload on code changes
- ✅ Easy debugging
- ❌ Single worker (not for production)

---

### **Production - Option 1: Uvicorn**
```bash
uvicorn wsgi:app --host 0.0.0.0 --port 8000 --workers 4
```
- ✅ Works on Windows
- ✅ Multiple workers for better performance
- ✅ Already installed

---

### **Production - Option 2: Gunicorn (Linux/Mac Only)**

⚠️ **Note**: Gunicorn doesn't work on Windows! Use Linux or WSL.

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker wsgi:app --bind 0.0.0.0:8000
```

**Explanation:**
- `-w 4` = 4 worker processes
- `-k uvicorn.workers.UvicornWorker` = Use uvicorn worker class
- `wsgi:app` = Import app from wsgi.py
- `--bind 0.0.0.0:8000` = Listen on all interfaces, port 8000

---

### **Production - Option 3: Waitress (Windows)**

If you need a production server on Windows:

```bash
pip install waitress
waitress-serve --host 0.0.0.0 --port 8000 wsgi:app
```

---

## 📊 Recommended Setup

### **For Windows (Current System)**
```bash
# Option 1: Uvicorn with workers
uvicorn wsgi:app --host 0.0.0.0 --port 8000 --workers 4

# Option 2: Waitress
pip install waitress
waitress-serve --host 0.0.0.0 --port 8000 wsgi:app
```

### **For Linux/Mac Production Servers**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker wsgi:app --bind 0.0.0.0:8000
```

---

## 🔧 Configuration Tips

### **Number of Workers**
Calculate based on CPU cores:
```
workers = (2 × CPU_CORES) + 1
```

For 4 cores: `workers = 9`

### **With Logs**
```bash
gunicorn -w 4 \
  -k uvicorn.workers.UvicornWorker \
  wsgi:app \
  --bind 0.0.0.0:8000 \
  --access-logfile access.log \
  --error-logfile error.log
```

### **Background Process (Linux)**
```bash
gunicorn -w 4 \
  -k uvicorn.workers.UvicornWorker \
  wsgi:app \
  --bind 0.0.0.0:8000 \
  --daemon
```

---

## 🌐 Deployment Checklist

Before going to production:

- [ ] Set `DEBUG=False` in `.env`
- [ ] Use strong `SECRET_KEY` (64+ characters)
- [ ] Configure proper CORS origins in `main.py`
- [ ] Set up SSL/HTTPS (use nginx reverse proxy)
- [ ] Configure firewall (allow port 8000 or 80/443)
- [ ] Set up database backups
- [ ] Monitor server logs
- [ ] Use process manager (systemd, supervisor, or PM2)

---

## 📝 Example Systemd Service (Linux)

Create `/etc/systemd/system/cyberanytime.service`:

```ini
[Unit]
Description=Cyber Anytime API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/backend/venv/bin"
ExecStart=/path/to/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker wsgi:app --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable cyberanytime
sudo systemctl start cyberanytime
sudo systemctl status cyberanytime
```

---

## ✅ Quick Start Production (Windows)

Right now, you can run:

```bash
uvicorn wsgi:app --host 0.0.0.0 --port 8000 --workers 4
```

This gives you production-level performance on Windows!

---

## 🆘 Troubleshooting

### Gunicorn not working on Windows?
- **Solution**: Use `uvicorn` or `waitress` instead (both work on Windows)

### Port already in use?
```bash
# Change port to 8080
uvicorn wsgi:app --host 0.0.0.0 --port 8080
```

### Workers not starting?
- Reduce worker count: `--workers 2`
- Check available RAM (each worker uses memory)

---

**Your backend is now production-ready!** 🎉
