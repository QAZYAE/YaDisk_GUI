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
            with self.client:
                return [(file.name, file.modified, file.type) for file in self.client.listdir(path)]
        except yadisk.exceptions.PathNotFoundError as e:
            return f'Path not found!\n{e}'
        except Exception as e:
            return f'ERROR: {type(e).__name__}: {e}'
        
        
    def check_path(self, path: str) -> bool | str:
        """Check if the path exists on the disk"""
        try:
            with self.client:
                return self.client.exists(path)
        except Exception as e:
            return f'ERROR: {type(e).__name__}: {e}'