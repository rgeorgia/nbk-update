
import urllib.request
import platform
import hashlib
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path


class DownloadException(Exception):
    pass


class HashType(Enum):
    MD5:str = 'MD5'
    SHA512:str = 'SHA512'

class Download:
    def __init__(self, url: str, kern_name: str, download_target: str, url_tail: str):
        self.url = url
        self.kern_name = kern_name
        self.download_target = download_target
        self.url_tail = url_tail
        self.arch = platform.machine()

    def download_kernel(self):
        if Path(f"{self.download_target}/{self.kern_name}").is_file():
            Path(f"{self.download_target}/{self.kern_name}").unlink()

        try:
            urllib.request.urlretrieve(
                f"{self.url}{self.arch}/{self.url_tail}{self.kern_name}",
                f"{self.download_target}/{self.kern_name}",
            )
        except Exception as e:
            raise DownloadException(f'Error downloading {self.kern_name}: {e}')

    def download_key(self, hash_key: str = None):
        if hash_key == "MD5" or hash_key is None:
            h_key = "MD5"
        else:
            h_key = "SHA512"

        if Path(f"{self.download_target}/{hash_key}").is_file():
            Path(f"{self.download_target}/{hash_key}").unlink()

        try:
            urllib.request.urlretrieve(
                f"{self.url}{self.arch}/{self.url_tail}{h_key}",
                f"{self.download_target}/{h_key}",
            )
        except Exception as e:
            raise DownloadException(f'Error downloading {h_key}: {e}')

    def hash_of_file(self, hash_type) -> str:
        readable_hash = None
        if hash_type == "MD5":
            with open(f"{self.download_target}/{self.kern_name}", "rb") as kf:
                bytes = kf.read()
                readable_hash = hashlib.md5(bytes).hexdigest()
        else:
            with open(f"{self.download_target}/{self.kern_name}", "rb") as kf:
                bytes = kf.read()
                readable_hash = hashlib.sha512(bytes).hexdigest()

        return readable_hash


    def good_check_sum(self)->bool:
        return True