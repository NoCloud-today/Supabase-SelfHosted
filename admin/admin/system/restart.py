from admin.system import upload_env_dict

import subprocess
import os

restart_flag_file = os.getenv('RESTART_FLAG_FILE') or '/supabase/docker/restart.txt'


def restart(config: dict[str, str]):
    config['CADDY_NETWORK_MODE'] = ''
    config['CADDY_CONFIG_FILE'] = './volumes/caddy/Caddyfile'
    config['ADMIN_DOMAIN'] = 'admin.${BASE_DOMAIN}'
    config['ADMIN_BASIC_USER'] = ''
    config['ADMIN_BASIC_PASS'] = ''
    upload_env_dict(config)

    run_docker_compose()


def run_docker_compose():
    subprocess.run(['touch', restart_flag_file])
