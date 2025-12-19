"""
WSGI Entry Point for Production Deployment
Import FastAPI app from main.py
"""
from main import app

# This is the application object that gunicorn/uvicorn will use
# For uvicorn: uvicorn wsgi:app --host 0.0.0.0 --port 8000
# For gunicorn: gunicorn -w 4 -k uvicorn.workers.UvicornWorker wsgi:app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
