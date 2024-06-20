import os
import requests
from dotenv import dotenv_values


def get_self_ip_address() -> str:
    url = 'https://api.ipify.org/?format=json'
    return requests.get(url).json()['ip']


if __name__ == "__main__":
    env: dict[str, str] = dotenv_values(dotenv_path='.env.example', interpolate=False)
    ip = get_self_ip_address()

    env['ADMIN_DOMAIN'] = ip

    with open('.env', 'w') as f:
        for key, value in env.items():
            f.write(f'{key}=\"{value}\"\n')

    os.system('docker compose up -d admin caddy')

    print(f'Admin run on https://{ip}')
