# Alkafgrosir Administration

![GitHub repo size](https://img.shields.io/github/repo-size/FerdiantJoshua/alkafgrosir-administration) ![GitHub issues](https://img.shields.io/github/issues/FerdiantJoshua/alkafgrosir-administration) ![GitHub](https://img.shields.io/github/license/FerdiantJoshua/alkafgrosir-administration) ![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/FerdiantJoshua/alkafgrosir-administration?include_prereleases)

An administration web to help automating Alkafgrosir's (an online seller) administration process.
Built using [Django](https://github.com/django/django) 4.1.2.

## Requirement

- [Python](https://www.python.org/) 3.8 or higher (tested in Python 3.9, and 3.10)

## Installation

1. Clone the project  
    using SSH:

    ```bash
    git clone git@github.com:FerdiantJoshua/alkafgrosir-administration.git
    ```

    or using HTTPS:

    ```bash
    git clone https://github.com/FerdiantJoshua/alkafgrosir-administration.git
    ```

2. Change to the directory

    ```bash
    cd alkafgrosir-administration
    ```

3. Create project environtment using `virtualenv`

    ```bash
    python -m virtualenv venv
    ```

4. Activate the virtual environment  
    Windows

    ```bash
    venv/Scripts/activate.bat
    ```

    Linux or Mac

    ```bash
    source venv/bin/activate
    ```

5. Install dependency

    ```bash
    pip install -r requirements.txt
    ```

6. Create your .env file (check for [.env.example](.env.example))

    for example:

    ```.env
    ALLOWED_HOSTS = localhost,127.0.0.1
    DEBUG = False
    DB_NAME = alkaf_administration
    DB_USER = root
    DB_PASSWORD = password
    DB_HOST = 127.0.0.1
    DB_PORT = 3306
    DEV_MODE = False
    SECRET_KEY = {your_secret_key}
    ```

7. Create your own secret key

    ```shell script
    python manage.py shell
    ```

    You will run a Django shell, then run this script inside the Django shell:

    ```python
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    exit()
    ```

8. Put the printed secret key in SECRET_KEY variable in .env

9. Migrate the database

    ```bash
    python manage.py migrate
    ```

10. Run the server

    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

## Environment Variables

1. Rename `.env.example` to `.env`
2. Modify and adjust any variables according to your configuration

## Contributor

- Author: [FerdiantJoshua](https://github.com/FerdiantJoshua)

## License

[MIT](LICENSE)

## Check our shop out at marketplaces

1. [Shopee](https://shopee.co.id/alkafgrosir)
2. [Tokopedia](https://tokopedia.com/alkafgrosir/)
3. [Bukalapak](https://www.bukalapak.com/u/rumahanduk/products)
