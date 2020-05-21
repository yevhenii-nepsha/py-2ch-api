import os
import sys
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List, Optional

import wget

from py_2ch_api.constants import (
    TOP_METHODS,
    MEDIA_TYPE,
    FILE_TYPE,
)
from py_2ch_api.exceptions import (
    BoardNotFound,
    PasscodeNotProvidedError,
)
from py_2ch_api.logger import Logger
from py_2ch_api.models import Board, Thread, Post, File
from py_2ch_api.session import GenericRequestProvider


class ChAPI(GenericRequestProvider):
    def __init__(
        self,
        board: str = "b",
        base_url: str = "https://2ch.hk",
        passcode: str = None,
        proxies: Dict = None,
        use_threads: bool = False,
        workers: int = 10,
        debug: bool = False,
    ):
        super().__init__(base_url, proxies)

        self._boards = self.get_all_board_settings()

        self.board = board
        self.use_threads = use_threads
        self.workers = workers
        self.passcode = passcode
        self.passcode_data = None
        self._logger = Logger(
            "py-2ch-api", logger_level="DEBUG" if debug else "INFO"
        )

    def get_all_board_settings(self) -> Dict[str, Board]:
        boards = {}

        all_settings = self.get(path="/makaba/mobile.fcgi?task=get_boards")
        user_boards = self.get(path="userboards.json")

        for key in all_settings.keys():
            for settings in all_settings[key]:
                boards[settings["id"]] = Board(settings)

        for key in user_boards.keys():
            if key != "is_index":
                for settings in user_boards[key]:
                    boards[settings["id"]] = Board(settings)

        return boards

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, board):
        if board in self._boards.keys():
            self.__board = self._boards[board]
        else:
            raise BoardNotFound(f"Board {board} not found")

    def _is_board_exist(self, board: str = None) -> bool:
        return board in self._boards.keys()

    def auth_passcode(self, passcode: str = None) -> Optional[str]:

        passcode = self.passcode if self.passcode else passcode

        if not passcode:
            raise PasscodeNotProvidedError("Please provide actual passcode")

        payload = {
            "task": "auth",
            "usercode": passcode,
            "json": 1,
        }

        response_data = self.get("/makaba/makaba.fcgi", data=payload)

        self.passcode_data = response_data.hash

        return self.passcode_data

    def get_board_threads(
        self,
        board: Board = None,
        tag: str = None,
        subject: str = None,
        limit: int = 1,
    ) -> List[Thread]:
        """
        Get all threads from board

        tag: filter by tag
        subject: filter by subject
        """

        if not (board and self._is_board_exist(board)):
            board = self.board.board_id

        threads_response = self.get(f"/{board}/catalog.json").threads
        threads = [Thread(thread_data) for thread_data in threads_response]

        if tag:
            filtered_results = list(
                filter(lambda thread: tag in thread.opening_post.tags, threads)
            )
            return filtered_results[:limit]

        if subject:
            filtered_results = list(
                filter(lambda thread: subject in thread.subject, threads)
            )
            return filtered_results[:limit]

        return threads

    def get_thread(self, thread: Optional[Thread] = None, board: Board = None):
        if isinstance(thread, Thread):
            thread = thread.num

        if not (board and self._is_board_exist(board)):
            board = self.board.board_id

        posts = self.get(f"/{board}/res/{thread}.json").threads

        return [Post(post) for post in posts[0].posts]

    def get_top_threads(
        self,
        board: Board = None,
        method: TOP_METHODS = TOP_METHODS.VIEWS,
        limit: int = 5,
    ):
        if not (board and self._is_board_exist(board)):
            board = self.board.board_id

        threads = self.get_board_threads(board=board)

        if method == TOP_METHODS.VIEWS:
            threads = sorted(
                threads,
                key=lambda thread: (thread.views, thread.score),
                reverse=True,
            )
        elif method == TOP_METHODS.POSTS:
            threads = sorted(
                threads,
                key=lambda thread: (thread.posts_count, thread.views),
                reverse=True,
            )
        elif method == TOP_METHODS.SCORE:
            threads = sorted(
                threads,
                key=lambda thread: (thread.score, thread.views),
                reverse=True,
            )
        else:
            return []

        return threads[:limit]

    def send_post(self):
        raise NotImplementedError

    def get_all_media_from_thread(
        self,
        thread: Thread = None,
        media_type: Optional[MEDIA_TYPE] = MEDIA_TYPE.MP4,
    ):
        posts = self.get_thread(thread)

        media = [
            item
            for sublist in [post.files for post in posts if post.files]
            for item in sublist
        ]

        if media_type:
            media = [
                file
                for file in media
                if FILE_TYPE().get(file.type) in media_type
            ]

        return media

    def download_all_media_from_thread(self):
        raise NotImplementedError

    def download_all_media_from_post(
        self,
        post: Post = None,
        out_dir: str = "downloads",
        media_type: MEDIA_TYPE = MEDIA_TYPE.ALL,
    ):

        result = []

        if post.files:

            files_to_download = post.files

            if media_type != MEDIA_TYPE.ALL:
                files_to_download = [
                    file
                    for file in post.files
                    if FILE_TYPE().get(file.type) in media_type
                ]

            if files_to_download:

                try:
                    os.makedirs(out_dir)
                except FileExistsError:
                    pass

                if self.use_threads:
                    pool = ThreadPoolExecutor(max_workers=self.workers)

                    for file in files_to_download:
                        pool.submit(
                            self.download_file_from_post, file, out_dir
                        )

                        out_path = os.path.join(out_dir, file.name[:64])

                        result.append(out_path)

                    pool.shutdown(wait=True)
                else:
                    for file in files_to_download:

                        out_path = self.download_file_from_post(
                            file=file, out_dir=out_dir
                        )

                        result.append(out_path)

                return result

    def download_file_from_post(
        self, file: File = None, out_dir: str = "downloads"
    ) -> Optional[str]:

        out_path = os.path.join(out_dir, file.name[:64])
        url = self.build_url(file.path)

        self._logger.info(f"Downloading: {url}")

        wget.download(url=url, out=out_path)
        sys.stdout.flush()
        sys.stdout.write("\n")

        return out_path
