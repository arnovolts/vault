import base64
import os
import sqlite3
import hashlib
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def init():
   # Create database
   con = sqlite3.connect("vault.db")

   #cursor
   cursor = con.cursor()

   # Create tables 
   crendentials_table = """
      CREATE TABLE IF NOT EXISTS Credentials(
         username TEXT NOT NULL,
         platform TEXT NOT NULL,
         password BLOB NOT NULL,
         salt BLOB NOT NULL
      );
   """

   user_table = """ 
      CREATE TABLE IF NOT EXISTS User(
         username TEXT NOT NULL,
         password BLOB NOT NULL,
         salt BLOB NOT NULL,
         UNIQUE(username)
      );
   """

   cursor.execute(crendentials_table)
   cursor.execute(user_table)

   # ask for master password 
   print("Create app user")
   while True:
      username = input("username")
      password = getpass("Master password: ")
      confirm_password = getpass("Confirm password: ")

      if password == confirm_password: 
         salt = os.urandom(32)
         key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
         break


   cursor.execute(""" 
      INSERT INTO User VALUES(?, ?, ?);
   """, (username, key,salt))
   
   con.commit()

   # Close connection to the database
   con.close()

def encrypt(masterPwd, password):
   salt = os.urandom(16)
   kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt,
      iterations=100000,
   )

   key = base64.urlsafe_b64encode(kdf.derive(masterPwd))
   f = Fernet(key)
   encryptedPass = f.encrypt(bytes(password,encoding="utf-8"))

   return {"encryptedPass" : encryptedPass,"salt": salt}

def decrypt(masterPwd, salt, password):
   kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt,
      iterations=100000,
   )

   key = base64.urlsafe_b64encode(kdf.derive(masterPwd))
   f = Fernet(key)

   return f.decrypt(password)

def write(data):

   con = sqlite3.connect("vault.db")
   cursor = con.cursor()
      
   # Insert data into database
   cursor.execute("INSERT INTO Credentials VALUES (?, ?, ?, ?)", (data["username"], data["platform"], data["password"], data["salt"]))  
      
   # Save the changes
   con.commit()

   con.close()


def search_platform(platform):
   con = sqlite3.connect("vault.db")
   con.row_factory = sqlite3.Row
   cursor = con.cursor()

   rows = cursor.execute("SELECT * FROM Credentials WHERE platform = ?", (platform,)).fetchone()
   con.close()
   return rows


def search_username(username):
   con = sqlite3.connect("vault.db")
   con.row_factory = sqlite3.Row
   cursor = con.cursor()

   rows = cursor.execute("SELECT * FROM Credentials WHERE username = ?", (username,)).fetchone()
   con.close()
   return rows

def update_username(username, platform, new_username):
   con = sqlite3.connect("vault.db")
   con.row_factory = sqlite3.Row
   cursor = con.cursor()

   rows = cursor.execute(""" 
      UPDATE Credentials 
      SET username = ? 
      WHERE username = ? AND platform = ?""", (new_username, username, platform,))
      
   con.commit()
   con.close()

def update_password(username, platform, new_password, new_salt):
   con = sqlite3.connect("vault.db")
   con.row_factory = sqlite3.Row
   cursor = con.cursor()

   rows = cursor.execute("""
      UPDATE Credentials 
      SET password = ?, 
         salt = ?
      WHERE username = ? AND platform = ?""", (new_password, new_salt,username, platform,))

   con.commit()
   con.close()

def update_masterpass(new_pass, new_salt, username, old_master):
   con = sqlite3.connect("vault.db")
   con.row_factory = sqlite3.Row
   cursor = con.cursor()

   rows = cursor.execute("UPDATE user set password = ? , salt = ? WHERE username = ?", (new_pass, new_salt,username)).fetchone()

   old_data = cursor.execute("SELECT * FROM Credentials")

   for row in old_data:
      salt = row["salt"]
      old_encrypt_pass = str(decrypt(old_master, salt, row["password"]))
      new_encrypt = encrypt(new_pass, old_encrypt_pass)
      cursor.execute(""" 
         UPDATE Credentials
         SET password = ?,
             salt = ?
         WHERE username = ? AND platform = ?
      
      """,( new_encrypt["encryptedPass"], 
            new_encrypt["salt"],
            row["username"],
            row["platform"]
         ))

   con.commit()
   con.close()

def checkDB():
   """
   code found at  
   https://careerkarma.com/blog/python-check-if-file-exists/ """
   return os.path.isfile("vault.db")


def check_user(password, username):
   """ 
      Source : 

      https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    """
   con = sqlite3.connect("vault.db")
   con.row_factory = sqlite3.Row
   cursor = con.cursor()

   rows = cursor.execute("SELECT * FROM User WHERE username = ?", (username,)).fetchone()

   salt = rows["salt"]

   key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

   if key == rows["password"] and username == rows["username"]:
      return key

   return None

