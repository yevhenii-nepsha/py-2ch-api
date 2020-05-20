import os
from typing import List

from addict import Dict


class Board:
    def __init__(self, board_data: Dict = None):
        self.bump_limit = board_data.bump_limit
        self.category = board_data.category
        self.default_name = board_data.default_name
        self.enable_names = board_data.enable_names
        self.enable_sage = board_data.enable_sage
        self.board_id = board_data.id
        self.info = board_data.info
        self.last_num = board_data.last_num
        self.name = board_data.name
        self.speed = board_data.speed
        self.threads = board_data.threads
        self.unique_posters = board_data.unique_posters
        self.enable_dices = board_data.enable_dices
        self.enable_flags = board_data.enable_flags
        self.enable_icons = board_data.enable_icons
        self.enable_likes = board_data.enable_likes
        self.enable_oekaki = board_data.enable_oekaki
        self.enable_posting = board_data.enable_posting
        self.enable_shield = board_data.enable_shield
        self.enable_subject = board_data.enable_subject
        self.enable_thread_tags = board_data.enable_thread_tags
        self.enable_trips = board_data.enable_trips
        self.icons = board_data.icons
        self.pages = board_data.pages

    def __repr__(self):
        return f"<Settings: {self.board_id}>"


class Thread:
    def __init__(self, thread_data: Dict = None):
        self.comment = thread_data.comment
        self.lasthit = thread_data.lasthit
        self.num = thread_data.num
        self.posts_count = thread_data.posts_count
        self.score = thread_data.score
        self.subject = thread_data.subject
        self.timestamp = thread_data.timestamp
        self.views = thread_data.views
        self.opening_post = Post(thread_data)

    def __repr__(self):
        return f"<Thread: {self.num}"


class Post:
    def __init__(self, post):
        """
        Create object from dict with post info
        :param post: dict with post info
        """
        self.banned = post.banned
        self.closed = post.closed
        self.comment = post.comment
        self.date = post.date
        self.email = post.email
        self.endless = post.endless
        self.files = [File(Dict(file)) for file in post.files]
        self.lasthit = post.lasthit
        self.name = post.name
        self.num = post.num
        self.number = post.number
        self.op = post.op
        self.parent = post.parent
        self.sticky = post.sticky
        self.subject = post.subject
        self.tags = post.tags
        self.timestamp = post.timestamp
        self.trip = post.trip

    def __repr__(self):
        return f"<Post: {self.num}>"


class File:
    def __init__(self, file):
        """
            Create file object from dict of file params
            :param file: dict of file params
            """
        self.displayname = file.displayname
        self.fullname = file.fullname
        self.height = file.height
        self.md5 = file.md5
        self.name = file.name
        self.nsfw = file.nsfw
        self.path = file.path
        self.size = file.size
        self.thumbnail = file.thumbnail
        self.tn_height = file.tn_height
        self.tn_width = file.tn_width
        self.type = file.type
        self.width = file.width
        self.duration = file.duration if file.duration else None
        self.duration_secs = file.duration_secs if file.duration_secs else None

    def __repr__(self):
        return f"<File: {self.name}>"


class Message:
    def __init__(
        self,
        board_id: str = None,
        thread_id: str = None,
        comment: str = "",
        email: str = "",
        subject: str = "",
        name: str = "",
        sage: bool = False,
        files: List[str] = None,
    ):
        self.board_id = board_id
        self.thread_id = thread_id
        self.comment = comment
        self.email = email
        self.subject = subject
        self.name = name
        self.sage = sage
        self.files = files
        self._files_data = {}

        self._generate_payload()
        self._generate_files_payload()

    def _generate_payload(self):
        self.payload = Dict(
            {
                "json": 1,
                "task": "post",
                "board": self.board_id,
                "thread": self.thread_id,
                "email": self.email,
                "name": self.name,
                "subject": self.subject,
                "comment": self.comment,
                "sage": 1 if self.sage else 0,
            }
        )

    def _generate_files_payload(self):
        if self.files and len(self.files) <= 8:
            self.filesize = {"size": 0}

            try:
                for file_name in self.files:
                    with open(file_name, "rb") as current_file:
                        self._files_data[
                            current_file.name
                        ] = current_file.read()

                    self.filesize["size"] += (
                        os.path.getsize(file_name) / 1000000
                    )
            except Exception as e:
                print(f"IO Error: {e}")

        else:
            self._files_data = {"": ""}
