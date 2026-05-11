"""Connection to YaDisk"""
import yadisk
import os



class Disk:
    """Connection to Yandex Disk"""
    def __init__(self):
        with open(os.path.join(os.getcwd(), '.token'), 'r') as file:
            token = file.readline().strip()
        self.client = yadisk.Client(token=token)
        
        
    def listdir(self, path: str) -> list[str]:
        """List directory"""
        try:
            return [(file.name, file.modified, file.type) for file in self.client.listdir(path)]
        except yadisk.exceptions.PathNotFoundError as e:
            return f'Path not found!\n{e}'
        except Exception as e:
            return f'ERROR: {type(e).__name__}: {e}'