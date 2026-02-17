from sqlalchemy import create_engine, text
import urllib.parse

# Original from .env
# user: postgres
# pass: Deenasadhak@2004 (presumed)
# host: db.vtvojbkstrhsnbytdkxm.supabase.co
# port: 5432
# db: postgres

password = urllib.parse.quote_plus("Deenasadhak@2004")
db_url = f"postgresql://postgres:{password}@db.vtvojbkstrhsnbytdkxm.supabase.co:5432/postgres"

print(f"Testing connection with URL: {db_url.replace(password, '******')}")

try:
    engine = create_engine(db_url)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection successful!", result.scalar())
except Exception as e:
    print(f"Connection failed: {e}")
