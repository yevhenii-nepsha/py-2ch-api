from typing import Optional

import requests


class RequestError(Exception):
    def __init__(
        self,
        r: requests.Response,
        expected_status_code: int,
        *,
        reason: Optional[str] = None,
    ) -> None:
        self.status_code = r.status_code
        reason = reason or r.reason
        self.error_text = (
            f"Status code mismatch: {r.status_code} "
            f"!= {expected_status_code}. "
            f"Reason: {reason}. Text: {r.text.strip()}."
        )
        super().__init__(self.error_text)


class BoardNotFound(Exception):
    pass


class PasscodeNotProvidedError(Exception):
    pass


class ExtraFilesError(Exception):
    def __init__(self, files_len: int = None, passcode: bool = None):

        passcode_status = "enabled" if passcode else "disabled"

        super().__init__(
            self,
            f"The maximum number of files has been exceeded.\n"
            f"You transfer - {files_len} files, passcode - {passcode_status}.\n"
            f"The maximum number of files with a passcode is 8, and without it, 4.",
        )


class FileSizeError(Exception):
    def __init__(self, files_size, passcode):
        passcode_status = "enabled" if passcode else "disabled"

        super().__init__(
            self,
            f"File size limit exceeded.\n"
            f"The total file size is {files_size}, the passcode is {passcode_status}.\n"
            f"The maximum file size with a passcode is 40-60 Mb, without it - 20 Mb.",
        )
