from pony.orm import Database, PrimaryKey, Required


db = Database()


class SelectedTextChannel(db.Entity):
    id = PrimaryKey(int, auto=True)
    channel_id = Required(str)


class Tweet(db.Entity):
    id = PrimaryKey(int, auto=True)
    tweet_id = Required(str)
    status = Required(str)
    create_time = Required(int)
