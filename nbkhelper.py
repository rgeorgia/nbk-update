import sys
import urllib.request
import platform
import hashlib
from enum import Enum
from pathlib import Path
from dataclasses import dataclass


class DownloadException(Exception):
    pass


class HashPath(Enum):
    md5: str = "/usr/bin/md5"
    sha512sum: str = "/usr/pkg/emul/linux/usr/bin/sha512sum"


@dataclass
class KernelFile:
    name: str
    download_location: str
    current_kern_location: str
    backup_kern_location: str
    root_location: str
    hash_key: HashPath


class Download:
    def __init__(self, url: str, kern_name: str, download_target: str, url_tail: str):
        self.url = url
        self.kern_name = kern_name
        self.download_target = download_target
        self.url_tail = url_tail
        self.arch = platform.machine()

    def download_kernel(self):
        urllib.request.urlretrieve(
            f"{self.url}{self.arch}/{self.url_tail}{self.kern_name}",
            f"{self.download_target}/{self.kern_name}",
        )

    def download_key(self, hash_key: str = None):
        if hash_key == "MD5" or hash_key is None:
            h_key = "MD5"
        else:
            h_key = "SHA512"

        urllib.request.urlretrieve(
            f"{self.url}{self.arch}/{self.url_tail}{h_key}",
            f"{self.download_target}/{h_key}",
        )

    def good_check_sum(self, hash_type) -> bool:
        readable_hash = None
        if hash_type == "MD5":
            with open(f"{self.download_target}/{self.kern_name}", "rb") as kf:
                bytes = kf.read()
                readable_hash = hashlib.md5(bytes).hexdigest()

        # return readable_hash


        return False
