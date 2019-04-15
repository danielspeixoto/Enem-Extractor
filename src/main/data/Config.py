import yaml

class YAMLConfig:

    def __init__(self, input_path: str):
        self.config = yaml.load_all(open(input_path, "r"))