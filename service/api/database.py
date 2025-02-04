from motor.motor_asyncio import AsyncIOMotorClient
import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_INITDB_DATABASE = os.getenv("MONGO_INITDB_DATABASE")


async def connect_to_db(app: FastAPI):
    """Connects to MongoDB and stores it in app.state."""
    try:
        print("🔄 Attempting to connect to MongoDB...")

        # Ensure attributes exist before accessing them
        if not hasattr(app.state, "mongo_client"):
            app.state.mongo_client = None
        if not hasattr(app.state, "db"):
            app.state.db = None

        if app.state.mongo_client:
            print("✅ Already connected to MongoDB.")
            return

        client = AsyncIOMotorClient(MONGO_URI)

        # Ping MongoDB to verify connection
        await client.admin.command("ping")

        # Store the client and database in app.state
        app.state.mongo_client = client
        app.state.db = client[MONGO_INITDB_DATABASE]

        print("✅ Successfully connected to MongoDB.")

    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        raise ConnectionError(f"MongoDB connection error: {e}")


async def close_db_connection(app: FastAPI):
    """Closes the MongoDB connection when shutting down."""
    if hasattr(app.state, "mongo_client") and app.state.mongo_client:
        print("⚠️ Closing MongoDB connection...")
        app.state.mongo_client.close()
        app.state.mongo_client = None
        app.state.db = None
        print("✅ MongoDB connection closed.")

def parse_obj_id(item):
    """Convert MongoDB ObjectId to string and rename `_id` to `id`."""
    if isinstance(item, list):
        return [{**doc, "id": str(doc.pop("_id"))} for doc in item]  # Rename `_id` to `id`
    elif isinstance(item, dict):
        item["id"] = str(item.pop("_id"))  # Rename `_id` to `id`
        return item
    return item
   
# Lifespan gerador assíncrono
async def lifespan(app: FastAPI):
    # Executa na inicialização
    await connect_to_db(app)
    yield  # Permite que a aplicação execute
    # Executa no encerramento
    await close_db_connection(app)
