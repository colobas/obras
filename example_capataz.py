from obras.spawner import CPUSpawner
from obras.utils import load_config

conf = load_config("./config/example_spawner.conf")
spawner = CPUSpawner(conf)

spawner.spawn()
