import redis

pubsub = redis.Redis().pubsub()
pubsub.subscribe(["um_canal"])

for item in pubsub.listen():
    try:
        print(item["data"].decode("utf-8"))
    except:
        print(item["data"])
