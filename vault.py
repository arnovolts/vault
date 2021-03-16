import click
import db
import pyperclip

@click.group()
def cli():
    pass

@click.command()
def init_app():
    db.init()

@click.command()
def add_entry():
    db.decrypt()
    click.echo("please fill in all the fields.")

    while True:
        data = get_entry()

        click.echo("please confirm entry")
        click.echo(data[0] + ", " + data[1] + ", " + data[2])
        confimation = confirm()

        if confimation == 'y':
            db.write(data)
            db.encrypt()
            break


@click.command()
@click.option("--platform", prompt="which platform",
            help="The platform you wish to get the crediantials for.")
def get_data(platform):
    db.decrypt()

    # search for data
    data =  db.read(platform)
    if data == -1:
      click.echo("not found.")
    else:
       click.echo(data["username"] + ", " + data["platform"])

       #copy password to clipboard 
       pyperclip.copy(data["password"])

       # warn user that the password has been copied to the clipboard
       click.echo("Password has been copied into clipboard")

    db.encrypt()

def get_entry():
    username = input("username: ")
    platform = input("platform: ")
    password = input("password: ")

    return [username, platform, password]


def confirm():
    while True:
        answer = input("y/n: ").lower()
        print(answer)

        if answer in ['y', 'n']:
            break

    return answer

cli.add_command(init_app)
cli.add_command(add_entry)
cli.add_command(get_data)
