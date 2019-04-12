import Nymph.settings as settings
import twitter


class Nymph:

    def __init__(self):
        self.__apis = [
            NymphTwitter()
        ]

    def post(self, status, options=None):
        for api in self.__apis:
            api.post(status, options)


class ApiService:

    def post(self, status, options=None):
        raise NotImplemented


class NymphTwitter(ApiService):

    def __init__(self):
        self.__api = twitter.Api(
            consumer_key=settings.CONSUMER_API_KEY,
            consumer_secret=settings.CONSUMER_API_KEY_SECRET,
            access_token_key=settings.ACCESS_TOKEN,
            access_token_secret=settings.ACCESS_TOKEN_SECRET
        )

    def post(self, status, options=None):
        self.__api.PostUpdate(status)


class NymphDiscord(ApiService):
    pass
