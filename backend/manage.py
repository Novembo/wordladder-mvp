#!/usr/bin/env python
import sys
import uvicorn
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py [runserver|migrate|test]")
        sys.exit(1)

    command = sys.argv[1]
    
    # Ensure we are in the backend directory
    backend_dir = Path(__file__).parent.resolve()
    
    if command == "runserver":
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    
    elif command == "migrate":
        subprocess.run(["alembic", "upgrade", "head"], cwd=backend_dir)
        
    elif command == "test":
        subprocess.run(["pytest"], cwd=backend_dir)
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
