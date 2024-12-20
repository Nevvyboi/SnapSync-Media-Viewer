import sqlite3
import hashlib
import os

def getBasePath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def getDatabasePath(fileName) -> str:
    components_folder = os.path.join(getBasePath(), "Database")
    return os.path.join(components_folder, fileName)

class MediaDatabase:
    def __init__(self):
        self.databasePath = getDatabasePath("media.db")
        self.createDatabaseAndTables()

    def createDatabaseAndTables(self) -> None:
        try:
            with sqlite3.connect(self.databasePath) as conn:
                conn.execute("""
                CREATE TABLE IF NOT EXISTS media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('image', 'video')),
                    path TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    resolution TEXT,
                    duration REAL,
                    hash TEXT UNIQUE,
                    processedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS likedMedia (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        mediaID INTEGER NOT NULL,
                        mediaType TEXT NOT NULL,
                        filePath TEXT NOT NULL,
                        LikedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        except Exception as e:
            print(e)

    def generateFileHashCode(self, filePath : str) -> str:
        try:
            hashCode = hashlib.sha256()
            with open(filePath, "rb") as f:
                while chunk := f.read(8192):
                    hashCode.update(chunk)
            return hashCode.hexdigest()
        except Exception as e:
            print(e)

    def isDuplicateMedia(self, fileHash: str) -> bool:
        try:
            with sqlite3.connect(self.databasePath) as conn:
                cursor = conn.execute("SELECT 1 FROM media WHERE hash = ?", (fileHash,))
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            print(e)
            return False

    def insertMediaIntoDatabase(self, name : str, mediaType, path, size, resolution = None, duration = None, fileHashCode = None) -> bool:
        try:
            if self.isDuplicateMedia(fileHashCode):
                print(f"Duplicate found: {path}. Skipping...")
                return False
            with sqlite3.connect(self.databasePath) as conn:
                conn.execute("""
                    INSERT INTO media (name, type, path, size, resolution, duration, hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, mediaType, path, size, resolution, duration, fileHashCode))
                print(f"Inserted: {path}")
                return True
        except Exception as e:
            print(e)
