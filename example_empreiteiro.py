from obras.manager import Manager
from obras.utils import load_config

conf = load_config("./config/example_manager.conf")
job = load_config("./config/example_job.conf")

empreiteiro = Manager(conf)
empreiteiro.deploy(job)
