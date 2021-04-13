import click
import db
import pyperclip
import hashlib
import getpass
import sys
import os


@click.group()
def cli():
    """A cli password manager """
    pass


@click.command()
def init_app():
    """ Creates the databases needed for the app and creates a user. """
    
    db.init()
    click.echo("database created, you are ready to go.")


@click.command()
def add_entry():
    """ Allows for adding credentials into the database """
    # Verify that the database exists
    if db.checkDB():
        click.echo("please fill in all the fields.")
        
        # Veriyf user
        username = click.prompt("Master username ")
        masterPwd = getpass.getpass("Master password: ")
        masterPwd = db.check_user(masterPwd, username)
        
        if masterPwd == None:
            click.echo("Wrong password !!")
            sys.exit()

        # Get data from user and store them in db
        while True:
            data = get_entry()

            click.echo("please confirm entry")
            click.echo(data["username"] + ", " +
                       data["platform"])
            confimation = confirm()

            if confimation == 'y':

                encrypt = db.encrypt(masterPwd, data["password"])
                data["password"] = encrypt["encryptedPass"]
                data["salt"] = encrypt["salt"]
                db.write(data)
                click.echo("entry added sucessfully")
                break
    else:
        click.echo("Please run 'vault init-app' to create the database ")


@click.command()
@click.argument("platform")
def search_by_platform(platform):
    """Gets the platform you wish to get the crediantials for."""
    if db.checkDB():
        # Verify user
        Click.echo("Login")
        username = click.prompt("Master username")
        masterPwd =  masterPwd = getpass.getpass("Master password: ")
        masterPwd = db.check_user(masterPwd, username)
        
        if masterPwd == None:
            click.echo("Wrong password !!")
            sys.exit()

        # search for data
        data = db.search_platform(platform)
        if data is not None:
            click.echo("username " + data['username'])

            try:
                password = db.decrypt(
                    masterPwd, data["salt"], data["password"])
               
                # copy password to clipboard
                pyperclip.copy(password.decode())
                
                #  warn user that the password has been copied to the clipboard
                click.echo("Password has been copied into clipboard !")
            except:
                click.echo("Something went wrong :(")

        else:
            click.echo("platform didn't match check your spelling.")
    else:
        click.echo("Please run 'vault init' to create the database ")


@click.command()
@click.argument("username")
def search_by_username(username):
    """Gets the username for the account you wish to get the crediantials for."""
    if db.checkDB():
        # Verify user
        master_username = click.prompt("master username")
        masterPwd = masterPwd = getpass.getpass("Master password: ")
        masterPwd = db.check_user(masterPwd, master_username)
        
        if masterPwd == None:
            click.echo("Wrong password !!")
            sys.exit()

        # search for data
        data = db.search_username(username)

        if data is not None:
            click.echo("Credentials")
            click.echo("Platform: " + data["platform"])
            
            try:
                password = db.decrypt(
                    masterPwd, data["salt"], data["password"])
            except:
                click.echo("Something went wrong :(")

            # copy password to clipboard
            pyperclip.copy(password.decode())

            #  warn user that the password has been copied to the clipboard
            click.echo("Password has been copied into clipboard !")
        else:
            click.echo("Username didn't match check your spelling.")
    else:
        click.echo("Please run 'vault init' to create the database ")

@click.command()
@click.option('-p', default=False, help="If true updates password for an account")
@click.option('-u', default=False, help="If true updates username for an account")
@click.option('-mp', default=False, help="If true updates master password")
def update(p, u, mp):
    """ Allows to update data """
    #Verify user
    master_username = click.prompt("Master username")
    masterPwd = masterPwd = getpass.getpass("Master password: ")
    masterPwd = db.check_user(masterPwd, master_username)

    if masterPwd == None:
        click.echo("Wrong master Password")
        sys.exit()

    if p:
        username = click.prompt("Username")
        platform = click.prompt("platform")
        new_pass = getpass.getpass("New password: ")
        confirm_pass = getpass.getpass("confirm password: ")

        if new_pass == confirm_pass:
            encrypted_data = db.encrypt(masterPwd, new_pass)

            try:
                db.update_password(username, platform, encrypted_data["encryptedPass"], encrypted_data["salt"])
                click.echo("password updated !")
            except:
                click.echo("Something went wrong try again...")
        else: 
            click.echo("Passwords didn't match.")

    elif u: 
        username = click.prompt("Old username ")
        platform = click.prompt("platform ")
        new_username = click.prompt("New username")
        try:
            db.update_username(username, platform, new_username)
            click.echo("username updated !")
        except:
            click.echo("Something went wrong trya again...")
    
    elif mp:
        password = getpass.getpass("new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        
        if password == confirm_password: 
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

            try: 
                db.update_masterpass(key, salt, master_username,masterPwd)

            except:
                click.echo("Something went wrong try again...")

        else:
            click.echo("Passwords didn't match.")
            sys.exit()



def get_entry():
    while True:
        username = input("username: ")
        platform = input("platform: ")
        password = getpass.getpass()
        confirm_password = getpass.getpass('confirm password:')

        if password == confirm_password:
            break
        else: 
            click.echo("Passwords did not match :(")

    return {
        "username": username,
        "platform": platform,
        "password": password
    }


def confirm():
    while True:
        answer = input("y/n: ").lower()

        if answer in ['y', 'n']:
            break

    return answer


cli.add_command(init_app)
cli.add_command(add_entry)
cli.add_command(search_by_platform)
cli.add_command(search_by_username)
cli.add_command(update)