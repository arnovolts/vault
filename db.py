import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sqlite3

def init():
   # Create database
   con = sqlite3.connect("vault.db")

   #cursor
   cursor = con.cursor()

   # Create table 
   table = """
      CREATE TABLE IF NOT EXISTS Credentials(
         username TEXT NOT NULL,
         platform TEXT NOT NULL,
         password BLOB NOT NULL,
         salt BLOB NOT NULL
      );
   """

   cursor.execute(table)
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

   masterPwd = bytes(masterPwd, encoding="utf-8")
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

   masterPwd = bytes(masterPwd, encoding="utf-8")
   key = base64.urlsafe_b64encode(kdf.derive(masterPwd))
   f = Fernet(key)

   return f.decrypt(password)

def write(data):

   con = sqlite3.connect("vault.db")
   cursor = con.cursor()
      
   # Insert data into database
   cursor.execute("INSERT INTO Credentials VALUES (?, ?, ?, ?)", (data[0], data[1], data[2], data[3]))  
      
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


def checkDB():
   """
   code found at  
   https://careerkarma.com/blog/python-check-if-file-exists/ """
   return os.path.isfile("vault.db")