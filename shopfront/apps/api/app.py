import os
import logging
from fastapi import FastAPI, Response, status
import psycopg2

# Configure basic logging for our DevOps pipelines to capture
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(title="Shopfront API Backend")

# Read database connection parameters from environment variables
# Note: The defaults point to localhost, which aligns with the sidecar proxy!
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "shopfront")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "changeme")

def get_db_connection():
    """Helper function to open a secure database connection."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3
    )

@app.get("/healthz")
def healthz():
    """Liveness probe: Just checks if the Python process is alive."""
    return {"status": "alive"}

@app.get("/readyz")
def readyz(response: Response):
    """Readiness probe: Actually checks if the database is responding before accepting traffic."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")  # Minimal query to test connectivity
        cur.close()
        conn.close()
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unready", "reason": "database unavailable"}

@app.get("/api/v1/search")
def search_products(q: str = ""):
    """Queries real products from the Cloud SQL database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # In a real retail-AI app, this would query embeddings. Here we use a simple SQL search.
        query = "SELECT id, name, score FROM products WHERE name ILIKE %s LIMIT 5;"
        cur.execute(query, (f"%{q}%",))
        rows = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # Map the SQL rows to a clean JSON response
        products = [{"id": r[0], "name": r[1], "score": float(r[2])} for r in rows]
        return {
            "query": q,
            "engine": "cloud-sql-postgres",
            "products": products
        }
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        return {"error": "failed_to_retrieve_data", "details": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)