# Click and Collect

A initail Click and Collect Web Application to demonstrating Flask and SQL usage.

# Getting Started

## VS Code

- You must install the VS Code [python extension](https://code.visualstudio.com/docs/languages/python).
- You must install the [Python Virtual Environments in VSCode](https://code.visualstudio.com/docs/python/environments).

## Copy the Code

You must have a copy of the code on your local machine.
Either clone the repository or download a ZIP archive of the code.

To clone it use the VScode source control tools with the repository URL `https://github.com/5579096/clickandcollect2-main`.
You will be asked for a target directory. After the clone is complete you should have a folder `clickandcollect2-main` in the target directory.
Open this directory in VScode before proceeding to the next steps.

To download a ZIP archive go to [the repository](https://github.com/5579096/clickandcollect2-main) Select the green `code` button. Then select the `Download ZIP` option at the bottom of the dropdown menu. This will download a file `clickandcollect2-main.zip` to your local disk. Move the file `clickandcollect2-main.zip` to a target directory and unpack it. Unpacking may result in a folder with subfolder `PMA/clickandcollect2-main` or just a folder `clickandcollect2-main` in your target directory. Whatever the results of unpacking the ZIP file you want to open the folder `clickandcollect2-main` in VSCode before proceeding to the next steps.

## Copy the Database

There is a ready made database in the code repository. It is in the file `site.db`. VSCode cannot read this file but it can copy the file. You must copy the file `site.db` to `/instance/site.db` which is the name of the database file the flask application expects. Having a working copy `app.db` and a backup copy `backup_site.db` means we can restore the working copy if we make a mistake when examining the database.

## Install SQLite Studio

SQLiteStudio is a GUI application which allows you to explore the database and make changes to it. We will use this to do just that.

Follow this link [SQLite Studio](https://sqlitestudio.pl/) and download the appropriate package for your computer.
On a Mac you need to open the package then right-click on the contents and choose install. This will give you the option to install despite the package being unsigned.

## Creating the database

Our web application needs to store information about customers, products etc. We use a database for this. We don't want to embed information about, for exampe, products in our code because that will be changing all of the time and we don't want to re-release the application every time we add or remove a product. Similarly a key feature of a shopping cart is for customers to add and remove and eventually buy the contents. A shopping cart is dynamic information which changes all the time and is therefore best kept in a datastore.

## Preparing project before implement to server

Initially, the application must be prepared for production by setting 'DEBUG' to 'False', configuring a robust production database like PostgreSQL or MySQL, securing session and cookie keys, and freezing dependencies with pip freeze > requirements.txt to ensure environment consistency. Logging mechanisms should be established to capture critical errors and information, complemented by comprehensive testing—unit, integration, and system tests—to identify any potential issues pre-deployment.

## Released note

- version 1 - Keep order item in session
- version 2.1 - Add log in account for editing Food Item CRUD
- version 2.2 - Add timestamp to order table
- version 2.3 - Add testing 'test-int.py' and 'test-unit.py'

## User-End funtion

User

- Create order
- Update quantity in the basket
- Store cart item in the same session when come back the item will stay the same as where the user left
- Payment and confirm order number

Admin go to '/admin' to enter login page

- Login (Username: admin , Password: adminpass )
- CRUD Food item

####

# Known Problems

Please refer to [Known Problems](docs/known_problems.md)
