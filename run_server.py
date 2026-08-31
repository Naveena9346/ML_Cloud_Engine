import os
import sys
import uvicorn

# Set sys.path
root_dir = os.path.abspath(os.path.dirname(__file__))
backend_dir = os.path.join(root_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

if __name__ == "__main__":
    print("Starting MLCloudEngine Server...")
    print("Open Swagger UI Documentation at: http://localhost:8000/docs")
    print("Open Health Check at: http://localhost:8000/health")
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
