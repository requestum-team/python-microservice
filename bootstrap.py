import os
import dotenv


# init configuration
root_dir = os.path.dirname(os.path.abspath(__file__))
dotenv.load_dotenv(dotenv_path=root_dir+'/.env')


# helper functions
def path(*rel):
    return os.path.abspath(os.path.join(root_dir, *rel))


def text(rel):
    with open(path(rel), 'r') as file:
        data = file.read()

    return data


# environment
ENV = str(os.getenv('ENV') or 'prod')
SERVER_PORT = int(os.getenv('SERVER_PORT') or 8000)