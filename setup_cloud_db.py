import mysql.connector
import pandas as pd

# Connect to Aiven Cloud MySQL
conn = mysql.connector.connect(
    host="mysql-33eeeee5-akan2004-71e3.i.aivencloud.com",
    port=19245,
    user="avnadmin",
    password="AVNS_czTAWhuQe7C3JC6lFtu",
    database="defaultdb",
    ssl_disabled=False
)

cursor = conn.cursor()
print("✅ Connected to Aiven Cloud MySQL!")

# ============ CREATE TABLES ============
cursor.execute("DROP TABLE IF EXISTS claims")
cursor.execute("DROP TABLE IF EXISTS food_listings")
cursor.execute("DROP TABLE IF EXISTS receivers")
cursor.execute("DROP TABLE IF EXISTS providers")

cursor.execute("""
CREATE TABLE providers (
    Provider_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    Address VARCHAR(255),
    City VARCHAR(100),
    Contact VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE receivers (
    Receiver_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    City VARCHAR(100),
    Contact VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE food_listings (
    Food_ID INT PRIMARY KEY,
    Food_Name VARCHAR(255),
    Quantity INT,
    Expiry_Date DATE,
    Provider_ID INT,
    Provider_Type VARCHAR(100),
    Location VARCHAR(100),
    Food_Type VARCHAR(100),
    Meal_Type VARCHAR(100),
    FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
)
""")

cursor.execute("""
CREATE TABLE claims (
    Claim_ID INT PRIMARY KEY,
    Food_ID INT,
    Receiver_ID INT,
    Status VARCHAR(50),
    Timestamp DATETIME,
    FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
)
""")

conn.commit()
print("✅ Tables created!")

# ============ LOAD CSV DATA ============
providers_df = pd.read_csv(r"C:\Users\akan2\Downloads\providers_data.csv")
receivers_df = pd.read_csv(r"C:\Users\akan2\Downloads\receivers_data.csv")
food_df = pd.read_csv(r"C:\Users\akan2\Downloads\food_listings_data.csv")
claims_df = pd.read_csv(r"C:\Users\akan2\Downloads\claims_data.csv")

# Fix date format
food_df['Expiry_Date'] = pd.to_datetime(food_df['Expiry_Date'], dayfirst=True).dt.strftime('%Y-%m-%d')

for _, row in providers_df.iterrows():
    cursor.execute("INSERT IGNORE INTO providers VALUES (%s, %s, %s, %s, %s, %s)", tuple(row))

for _, row in receivers_df.iterrows():
    cursor.execute("INSERT IGNORE INTO receivers VALUES (%s, %s, %s, %s, %s)", tuple(row))

for _, row in food_df.iterrows():
    cursor.execute("INSERT IGNORE INTO food_listings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", tuple(row))

for _, row in claims_df.iterrows():
    cursor.execute("INSERT IGNORE INTO claims VALUES (%s, %s, %s, %s, %s)", tuple(row))

conn.commit()
print("✅ All data loaded to Aiven Cloud MySQL!")

cursor.execute("SELECT COUNT(*) FROM providers")
print(f"Providers: {cursor.fetchone()[0]} rows")
cursor.execute("SELECT COUNT(*) FROM receivers")
print(f"Receivers: {cursor.fetchone()[0]} rows")
cursor.execute("SELECT COUNT(*) FROM food_listings")
print(f"Food Listings: {cursor.fetchone()[0]} rows")
cursor.execute("SELECT COUNT(*) FROM claims")
print(f"Claims: {cursor.fetchone()[0]} rows")

cursor.close()
conn.close()