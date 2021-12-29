import yaml

class Config:
    """Configuration for tests."""
    def __init__(self):
        """Initialise."""
        #self._config = None
        with open('config.yaml', 'r') as config:
           self._config = yaml.safe_load(config)

        self.source_bucket_name = self._config["source_bucket_name"]
        self.source_object_name = self._config["source_object_name"]
        self.part_no = self._config["part_no"]
