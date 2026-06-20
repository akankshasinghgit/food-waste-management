import mysql.connector

conn = mysql.connector.connect(
    host="mysql-33eeeee5-akan2004-71e3.i.aivencloud.com",
    port=19245,
    user="avnadmin",
    password="AVNS_czTAWhuQe7C3JC6lFtu",
    database="defaultdb",
    ssl_disabled=False
)

cursor = conn.cursor()

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