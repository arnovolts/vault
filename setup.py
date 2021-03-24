from setuptools import setup

setup(
    name="vault",
    version="0.1",
    py_modules="vault",
    install_requires=[
        'Click',
        'pyperclip',
        'cryptography'
    ],
    entry_points='''
        [console_scripts]
        vault=vault:cli    
    ''',
)