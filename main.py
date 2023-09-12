import yaml
import Web
import GRBLTools

with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f, Loader=yaml.FullLoader)
