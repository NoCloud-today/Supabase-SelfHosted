import requests
import subprocess
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

    subprocess.run(['mkdir', 'env_bkp'])

    subprocess.run(['docker', 'compose', 'pull'])
    subprocess.run(['docker', 'compose', 'up', '-d', 'admin', 'caddy'])

    print(f'Admin run on https://{ip}')

    subprocess.run(['chmod', '+x', 'restarter.sh'])

    try:
        subprocess.run(['./restarter.sh'])
    except KeyboardInterrupt:
        pass
