import yaml
from pathlib import Path

# To load this config the following function is provided
def load_yaml(filepath: str) -> dict:
    """
    Load chip configuration from yaml file

    :param filepath: Path to the configuration file to be loaded
    :return: Dictionary containing configuration
    """
    path = Path(filepath)
    if path.exists():
        with open(path, 'r', encoding='utf-8') as config_file:
            configuration = yaml.safe_load(config_file.read())
    else:
        print(f'File {path.absolute()} not found')
    return configuration