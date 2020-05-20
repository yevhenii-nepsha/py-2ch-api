class TOP_METHODS:
    VIEWS = "views"
    SCORE = "score"
    POSTS = "posts"


class MEDIA_TYPE:
    JPEG = ["jpeg"]
    PNG = ["png"]
    GIF = ["gif"]
    WEBM = ["webm"]
    MP4 = ["mp4"]
    VIDEO = ["mp4", "gif", "webm"]
    IMAGES = ["jpeg", "png"]
    ALL = ["ALL"]


class FILE_TYPE:
    TYPES = {
        1: "jpeg",
        2: "png",
        4: "gif",
        6: "webm",
        10: "mp4",
        100: "png",
    }

    def get(self, value: int = None):
        return self.TYPES.get(value)


class ConsoleColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
