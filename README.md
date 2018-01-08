# Obras

Stateless, distributed, reliable computing.

Obras is a system for running recipes concurrently on workers. It uses:

- **RabbitMQ** to implement a task queue
- **Redis** to implement a message bus a.k.a. logging black hole
- **MongoDB** to implement a state DB
- **hocon** for config files

---

- Workers are **spawned** by a `Spawner`
- Tasks are **enqueued** by a `Manager`.

## TODO

- More Spawners
    - Kubernetes spawner, for example
- Log on proper topics
- State logging on the DB is recipe specific. However, the configs for the MongoDB
connection have to be passed in the task payload
