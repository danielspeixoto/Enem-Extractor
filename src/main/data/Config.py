import yaml

class YAMLConfig:

    def __init__(self, input_path: str):
        self.config = yaml.safe_load(open(input_path, "r"))