from os import path
import config
from tornado import gen
from tornado import ioloop
import motor


@gen.coroutinne
def main():
    client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGDB_CONN,
                                                    config.MONGDB_PORT)
    db = client.sotool
    col = db.cache
    for subdir, dirs, files in path.walk(config.CACHE_DIR):
        for file in files:
            full_path = path.join(subdir, file)
            with open(full_path) as f:
                file_content = f.read()
            yield col.insert_one({"file_content": file_content})
    ioloop.IOLoop.current().stop()


if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(main)
