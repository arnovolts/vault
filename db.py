import csv
import subprocess

def init():
   # Create CSV file
   with open("vault.csv", "w") as file:
      writer = csv.writer(file, delimiter=",")
      writer.writerow(["username", "platform", "password"])

   encrypt()

def encrypt():
   # encrypt file using ccrypt
   subprocess.run(["ccrypt", "-e", "vault.csv"])


def decrypt():
   # decrypt file using ccrypt
   subprocess.run(["ccrypt", "-d", "vault.csv.cpt"])

def write(data):
   # write an entry into the file
   with open("vault.csv", "a") as file:
      writer = csv.writer(file, delimiter=",")
      writer.writerow(data)

def read(platform):
   # get data
   with open("vault.csv", "r") as file:
      reader = csv.DictReader(file)
      for row in reader:
         if row["platform"] == platform:
            return row
      return - 1

