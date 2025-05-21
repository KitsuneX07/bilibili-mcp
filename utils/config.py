import os
from dotenv import load_dotenv, find_dotenv

DEFAULT_CONFIG = {"CONSOLE_LOG_LEVEL": "INFO", "FILE_LOG_LEVEL": "DEBUG", "LOG_DIR": "logs"}


def create_default_env(default_config: dict, env_path: str = ".env"):
	"""
	Create a default .env file if it does not exist.

	Args:
	    default_config (dict): A dictionary containing the default configurations.
	    env_path (str): The path to the .env file, defaults to ".env".
	"""
	if not os.path.exists(env_path):
		with open(env_path, "w") as f:
			for key, value in default_config.items():
				f.write(f"{key}={value}\n")

		print(f"Created default configuration file: {env_path}")
	else:
		print(f"Configuration file already exists: {env_path}")


def load_config(default_config: dict = DEFAULT_CONFIG, env_path: str = ".env") -> None:
	"""
	Load the configuration, first try to load from the .env file, and create a default configuration if the file does not exist.

	Returns:
	    dict: A dictionary containing the configuration.
	"""
	# Find the .env file, use the default path if not found
	dotenv_path = find_dotenv(env_path, raise_error_if_not_found=False)

	# If the .env file is not found, create a default file
	if not dotenv_path:
		print(f".env file not found at {env_path}, creating a default one.")
		create_default_env(default_config, env_path)
		dotenv_path = env_path
	else:
		print(f".env file found at {dotenv_path}")

	print(f"Loading configuration from: {os.path.abspath(dotenv_path)}")
	load_dotenv(dotenv_path)
