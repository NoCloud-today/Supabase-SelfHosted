import os
import random
import string
import requests
import subprocess
from dotenv import dotenv_values


def get_self_ip_address() -> str:
    url = 'https://api.ipify.org/?format=json'
    return requests.get(url).json()['ip']


def generate_caddy_secrets():
    symbols = string.ascii_lowercase + '1234567890'
    username = ''.join(random.choice(symbols) for _ in range(30))
    password = ''.join(random.choice(symbols) for _ in range(30))

    subprocess.run(['docker', 'pull', 'caddy:2.7'])
    os.system(f'docker run caddy:2.7 caddy hash-password --plaintext \"{password}\" > caddy_hash_password')
    with open('caddy_hash_password', 'r') as f:
        caddy_hash_password = f.readlines()[0]

    return username, password, caddy_hash_password


if __name__ == "__main__":
    subprocess.run(['mkdir', 'env_bkp'])

    ip = get_self_ip_address()
    caddy_secrets = generate_caddy_secrets()

    env: dict[str, str] = dotenv_values(dotenv_path='.env.example', interpolate=False)
    env['ADMIN_DOMAIN'] = ip
    env['ADMIN_BASIC_USER'] = caddy_secrets[0]
    env['ADMIN_BASIC_PASS'] = caddy_secrets[2]
    with open('.env', 'w') as f:
        for key, value in env.items():
            f.write(f"{key}='{value}'\n")

    subprocess.run(['docker', 'compose', 'pull'])
    subprocess.run(['docker', 'compose', 'up', '-d', 'admin', 'caddy'])

    print(f'Admin run on https://{ip}')
    print(f'Username: {caddy_secrets[0]}')
    print(f'Password: {caddy_secrets[1]}')

    subprocess.run(['chmod', '+x', 'restarter.sh'])
    try:
        subprocess.run(['./restarter.sh'])
    except KeyboardInterrupt:
        pass
