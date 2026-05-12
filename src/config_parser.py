"""Config parser for yandex disk config file"""



class ConfigParser(dict):
    """Config parser for yandex disk config file. Inherits from `dict`"""
    
    exclude_dirs: list
    
    def __init__(self, path_to_config: str, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.path = path_to_config
        # Reading config
        self.read()
        
    
    def read(self, update_self=True):
        """Read config from the file"""
        config = {}
        with open(self.path, 'r') as file:
            for line in file:
                split = line.strip().split('=')
                if update_self:
                    self[split[0]] = split[1].strip('"')
                else:
                    config[split[0]] = split[1].strip('"')
        # Parsing exclude-dirs
        self.exclude_dirs = self['exclude-dirs'].split(',')
        if not update_self:
            return config
                
    
    def write(self):
        """Write config to the file"""
        with open(self.path, 'w') as file:
            for key, val in self.items():
                file.write(f'{key}="{val}"\n')            
        
        
    def change_path_to_config(self, new_path: str):
        """Change path to the config file"""
        self.path = new_path
        
    
    def get_exclude_paths(self) -> list[str]:
        """Get exclude dirs list"""
        return self.exclude_dirs
    
    
    def set_exclude_paths(self, exclude_dirs: str):
        """Set exclude_dirs parameter"""
        self.exclude_dirs = exclude_dirs
        self['exclude-dirs'] = ','.join(exclude_dirs)
        
        
    def compare_with_file(self):
        """Compare current config with file"""
        config = self.read(update_self=False)
        return config == self
