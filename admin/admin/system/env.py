import os
import shutil
from dotenv import dotenv_values

env_file_path = os.getenv('ENV_FILE_PATH')
env_bkp_dir = os.getenv('ENV_BKP_DIR')


def load_env_dict(version: int | None = None) -> dict:
    if version is None:
        return dotenv_values(dotenv_path=env_file_path)
    else:
        target_env_file_path = os.path.join(env_bkp_dir, f'.evn.v{version}')
        return dotenv_values(dotenv_path=target_env_file_path)


def get_last_version() -> int:
    files = [
        f for f in os.listdir(env_bkp_dir)
        if f.startswith('.env.v') and os.path.isfile(os.path.join(env_bkp_dir, f))
    ]

    return int(max(map(lambda f: f[6:], files)))


def create_backup() -> int:
    version = get_last_version() + 1
    dst = os.path.join(env_bkp_dir, f'.env.v{version}')
    shutil.copy(env_file_path, dst)

    return version


def load_backup(version: int | None = None) -> int:
    if version is None:
        version = get_last_version()

    src = os.path.join(env_bkp_dir, f'.env.v{version}')
    shutil.copy(src, env_file_path)

    return create_backup()


def get_all_backups() -> dict:
    files = [
        f for f in os.listdir(env_bkp_dir)
        if f.startswith('.env.v') and os.path.isfile(os.path.join(env_bkp_dir, f))
    ]

    version_to_config = dict()
    for f in files:
        version = int(f[6:])
        version_to_config[version] = load_env_dict(version)

    return version_to_config


def set_new_env(config: dict) -> int:
    with open(env_file_path, 'w') as f:
        for key, value in config:
            f.write(f'{key}={value}\n')

    return create_backup()
