import click
import db
import pyperclip


@click.group()
def cli():
    """A cli password manager """
    pass


@click.command()
def init_app():
    """ Creates the databases needed for the app. """
    db.init()
    click.echo("database created, you are ready to go.")


@click.command()
def add_entry():
    """ Allows for adding credentials into the database """
     # Verify that the database exists
    if db.checkDB():
        click.echo("please fill in all the fields.")
        while True:
            data = get_entry()

            click.echo("please confirm entry")
            click.echo(data["username"] + ", " +
                       data["platform"] + ", " + data["password"])
            confimation = confirm()

            if confimation == 'y':
                masterPwd = click.prompt("Enter master Password")
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
def get_platform(platform):
    """Gets the platform you wish to get the crediantials for."""
    if db.checkDB():

        # search for data
        data = db.search_platform(platform)
        if data is not None:
            # click.echo("username " + data['username'])
            masterPwd = click.prompt("Enter master password")
            try:
                password = db.decrypt(
                    masterPwd, data["salt"], data["password"])
            except:
                click.echo("The master password is incorrect.")

            # copy password to clipboard
            pyperclip.copy(password.decode())

            #  warn user that the password has been copied to the clipboard
            click.echo("Password has been copied into clipboard !")
        else:
            click.echo("platform didn't match check your spelling.")
    else:
        click.echo("Please run 'vault init' to create the database ")


@click.command()
@click.argument("username")
def get_username(username):
    """Gets the username for the account you wish to get the crediantials for."""
    if db.checkDB():
        # search for data
        data = db.search_username(username)
        if data is not None:
            click.echo("username " + data['username'])
            masterPwd = click.prompt("Enter master password")

            try:
                password = db.decrypt(
                    masterPwd, data["salt"], data["password"])
            except:
                click.echo("The master password is incorrect.")

            # copy password to clipboard
            pyperclip.copy(password.decode())

            #  warn user that the password has been copied to the clipboard
            click.echo("Password has been copied into clipboard !")
        else:
            click.echo("Username didn't match check your spelling.")
    else:
        click.echo("Please run 'vault init' to create the database ")

def get_entry():
    username = input("username: ")
    platform = input("platform: ")
    password = input("password: ")

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
cli.add_command(get_platform)
cli.add_command(get_username)
