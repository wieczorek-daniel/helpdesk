# Helpdesk
## Introduction
An application that is an implementation of a helpdesk system built using Django.

## Setup
First download the project folder or clone the repository using the following command:
```shell
git clone https://github.com/wieczorek-daniel/helpdesk.git
```
Then create and run the virtual environment. Depending on your operating system the commands may vary.

### Linux and OS X
```shell
python3 -m venv venv
. venv/bin/activate
```

### Windows
```shell
python -m venv venv
venv\Scripts\activate
```

Later install the dependencies (required packages) using the following command:
```shell
pip install -r requirements.txt
```
In the project directory also create an `.env` file containing environment variables based on the `.env.example` file.
```shell
cp .env.example .env # for Linux
copy .env.example .env # for Windows
```
The next step is to configure the `.env` file:
- `SECRET_KEY` contains the generated value of the secret key.
- `DEBUG` specifies whether debugging mode is enabled or not.
- `DATABASE_URL` is the URL containing the configuration data of the previously created database.
- The remaining variables (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PAGE_DOMAIN`) are related to the configuration of sending emails. When using Gmail, remember that the `EMAIL_HOST_PASSWORD` is the password for the created and configured application available when two-step verification is enabled, not the password for your Google account.

An example of the `.env` file contents is shown below:
```shell
SECRET_KEY={generated_secret_key}
DEBUG=False
DATABASE_URL=postgres://{user}:{password}@{hostname}:{port}/{database_name}
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=password
EMAIL_PAGE_DOMAIN=https://application-domain.com
```
Before running the application migrate the data using the following commands:
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```
To start the application use the following command:
```shell
python3 manage.py runserver
```

## Live demo
Heroku deployment: https://niejestessam.herokuapp.com

## Basic accounts (available after migrate operation)
| Username | Password     | Account type  |
| :---:    | :---:        | :---:         |
| Admin    | Helpdesk.123 | Administrator |
| Staff    | Helpdesk.123 | Staff user    |
| User     | Helpdesk.123 | User          |

