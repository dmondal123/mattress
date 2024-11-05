from dotenv import load_dotenv, find_dotenv


def set_credentials():
    _ = load_dotenv(find_dotenv())