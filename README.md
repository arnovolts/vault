A CLI password manager built with python

# Implementation

This program uses a sqlite3 database to store
data. There are 2 tables: 

- 1 table is used to store data related to the user of 
  of the application
- The other table stores the various crendentials of
  the application user 
  
The tables are named User and Credentials respectively. 

The password field in the Crendentials table is encrypted using the Cryptography library, the encryption is derived by the master password. Without it the passwords can't be decrypted. 

The User table is used to authenticate the user 
the password associated with the user is hashed using pythons hashlib

# Installation
After cloning this repository create a virtual environment.
```
python3 -m venv venv
```

Activate it with: 
``` 
source venv/bin/activate 
```

And then install the module with: 
``` 
pip install vault
```

In editable mode
```
pip install -e vault
```

# Usage
After installing the app it needs to be initialized that can be done using the command 
```
vault init-app
```

There are two commands that allow the user to query the
database:
1. Searching by platform 
```
vault search-by-platform <name of platform>
```

2. Searching by username
```
vault search-by-username <username>
```

The application allows updating the data of previously 
added information. The command associated with this is 

```
vault update <option> <value>
```

The available options are: 

- -p with a value of true allows for updating 
  the password of a specific field. 
  
- -u with a value of true allows for updating 
  the username of a specific field. 
  
- -mp with a value of true allows for updating
  the master password. 