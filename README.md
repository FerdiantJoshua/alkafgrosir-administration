# Alkafgrosir Administration

![GitHub repo size](https://img.shields.io/github/repo-size/FerdiantJoshua/belajar_online) ![GitHub issues](https://img.shields.io/github/issues/FerdiantJoshua/belajar_online) ![GitHub](https://img.shields.io/github/license/FerdiantJoshua/belajar_online) ![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/FerdiantJoshua/belajar_online?include_prereleases)

An administration web to help automating Alkafgrosir's (an online seller) administration process.
Built using [Django](https://github.com/django/django) 3.0.8.

## Requirement

- [Python](https://www.python.org/) 3.6 or higher (tested in Python 3.7)

## Installation

1. Clone the project  
    using SSH:
    ```bash
    $ git clone git@github.com:FerdiantJoshua/alkafgrosir-administration.git
    ```
    or using HTTPS:
    ```bash
    $ git clone https://github.com/FerdiantJoshua/alkafgrosir-administration.git
    ```
2. Change to the directory
    ```bash
    cd alkafgrosir-administration
    ```

3. Create project environtment using `virtualenv`
    ```bash
    $ python -m virtualenv venv
    ```
    
4. Activate the virtual environment  
    Windows
    ```bash
    $ venv/Scripts/activate.bat
    ```    
    Linux or Mac
    ```bash
    $ source venv/bin/activate
    ```

5. Install dependency
    ```bash
    $ pip install -r requirements.txt
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
    ```
7. Migrate the database
    ```bash
    $ python manage.py migrate
    ```

8. Run the server
    ```bash
    $ python manage.py runserver 0.0.0.0:8000
    ```

## Environment Variables
1. Rename `.env.example` to `.env`
2. Modify and adjust any variables according to your configuration 

## Contributor
- Author: [FerdiantJoshua](https://github.com/FerdiantJoshua)

## License

[MIT](LICENSE)

## Check our shop out at marketplaces:
1. [Shopee](https://shopee.co.id/alkafgrosir) 
2. [Tokopedia](https://tokopedia.com/alkafgrosir/) 
3. [Bukalapak](https://www.bukalapak.com/u/rumahanduk/products)
