import jwt
import os
import random
import string
import requests
import subprocess
from dotenv import dotenv_values
from datetime import datetime, timedelta


def get_self_ip_address() -> str:
    url = 'https://api.ipify.org/?format=json'

    return requests.get(url).json()['ip']


def generate_caddy_secrets():
    symbols = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(symbols) for _ in range(30))
    password = ''.join(random.choice(symbols) for _ in range(30))

    subprocess.run(['docker', 'pull', 'caddy:2.7'])
    os.system(f'docker run caddy:2.7 caddy hash-password --plaintext \"{password}\" > caddy_hash_password')
    with open('caddy_hash_password', 'r') as f:
        caddy_hash_password = f.readlines()[0][:-1]

    return username, password, caddy_hash_password


def generate_postgres_password():
    symbols = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(symbols) for _ in range(40))

    return password


def generate_jwt_secrets():
    jwt_headers = {'alg': 'HS256', 'typ': 'JWT'}

    now = datetime.now()
    today = datetime(now.year, now.month, now.day)
    five_years = today + timedelta(days=5 * 365)

    anon_token_payload = {
        'role': 'anon',
        'iss': 'supabase',
        'iat': int(today.timestamp()),
        'exp': int(five_years.timestamp())
    }

    service_token_payload = {
        'role': 'service_role',
        'iss': 'supabase',
        'iat': int(today.timestamp()),
        'exp': int(five_years.timestamp())
    }

    symbols = string.ascii_letters + string.digits
    secret = ''.join(random.choice(symbols) for _ in range(40))
    anon_key = jwt.encode(anon_token_payload, secret, headers=jwt_headers, algorithm='HS256')
    service_role_key = jwt.encode(service_token_payload, secret, headers=jwt_headers, algorithm='HS256')

    return secret, anon_key, service_role_key


if __name__ == "__main__":
    subprocess.run(['mkdir', 'env_bkp'])

    ip = get_self_ip_address()
    caddy_secrets = generate_caddy_secrets()
    postgres_password = generate_postgres_password()
    jwt_secrets = generate_jwt_secrets()

    env: dict[str, str] = dotenv_values(dotenv_path='.env.example', interpolate=False)
    env['ADMIN_DOMAIN'] = ip
    env['ADMIN_BASIC_USER'] = caddy_secrets[0]
    env['ADMIN_BASIC_PASS'] = caddy_secrets[2]
    env['POSTGRES_PASSWORD'] = postgres_password
    env['JWT_SECRET'] = jwt_secrets[0]
    env['ANON_KEY'] = jwt_secrets[1]
    env['SERVICE_ROLE_KEY'] = jwt_secrets[2]
    with open('.env', 'w') as f:
        for key, value in env.items():
            f.write(f"{key}='{value}'\n")

    subprocess.run(['docker', 'compose', 'pull'])
    subprocess.run(['docker', 'compose', 'up', '-d', 'admin', 'caddy'])

    print(f'Admin run on https://{ip}. The browser will consider the connection as insecure, just allow it.')
    print(f'Admin username: {caddy_secrets[0]}')
    print(f'Admin password: {caddy_secrets[1]}')
    print('Save these credentials for yourself:')
    print(f'JWT secret key: {jwt_secrets[0]}')
    print(f'Supabase anon key: {jwt_secrets[1]}')
    print(f'Supabase service role key: {jwt_secrets[2]}')

    subprocess.run(['chmod', '+x', 'restarter.sh'])
    try:
        subprocess.run(['./restarter.sh'])
    except KeyboardInterrupt:
        pass
