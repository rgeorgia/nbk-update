import filecmp
import urllib.request
import platform
import hashlib
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path


class DownloadException(Exception):
    pass


class HashType(Enum):
    MD5: str = "MD5"
    SHA512: str = "SHA512"


class Download:
    def __init__(
        self,
        url: str,
        kern_name: str,
        download_target: str,
        url_tail: str,
        hash_key_type: str = None,
    ):
        self.url = url
        self.kern_name = kern_name
        self.download_target = download_target
        self.url_tail = url_tail
        self.arch = platform.machine()
        self._hash_key_type = hash_key_type
        self._hash_of_file = None

    @property
    def hash_key_type(self):
        return self._hash_key_type

    @hash_key_type.setter
    def hash_key_type(self, hash_type):
        self._hash_key_type = hash_type

    @property
    def hash_of_file(self):

        if self.hash_key_type == "MD5":
            with open(f"{self.download_target}/{self.kern_name}", "rb") as kf:
                bytes = kf.read()
                self._hash_of_file = hashlib.md5(bytes).hexdigest()
        else:
            with open(f"{self.download_target}/{self.kern_name}", "rb") as kf:
                bytes = kf.read()
                self._hash_of_file = hashlib.sha512(bytes).hexdigest()

        return self._hash_of_file


    def is_same_version(self):

        return True


    def is_same_file(self):
        try:
            filecmp.cmp("/current",f"{self.download_target}/{self.kern_name}")
        except PermissionError as pe:
            raise pe


    def download_kernel(self):
        if Path(f"{self.download_target}/{self.kern_name}").is_file():
            Path(f"{self.download_target}/{self.kern_name}").unlink()

        try:
            urllib.request.urlretrieve(
                f"{self.url}{self.arch}/{self.url_tail}{self.kern_name}",
                f"{self.download_target}/{self.kern_name}",
            )
        except Exception as e:
            raise DownloadException(f"Error downloading {self.kern_name}: {e}")

    def download_key(self):
        if self.hash_key_type is None:
            self.hash_key_type = "MD5"

        if Path(f"{self.download_target}/{self.hash_key_type}").is_file():
            Path(f"{self.download_target}/{self.hash_key_type}").unlink()

        try:
            urllib.request.urlretrieve(
                f"{self.url}{self.arch}/{self.url_tail}{self.hash_key_type}",
                f"{self.download_target}/{self.hash_key_type}",
            )
        except Exception as e:
            raise DownloadException(f"Error downloading {self.hash_key_type}: {e}")

    def good_check_sum(self) -> bool:
        key_value = None
        with open(f"{self.download_target}/{self.hash_key_type}") as cksum_file:
            for line in cksum_file:
                if self.kern_name in line:
                    key_value = line.split("=")[1].strip()
        if key_value == self.hash_of_file:
            return True
        else:
            return False

    def clean_up(self):
        if Path(f"{self.download_target}/{self.hash_key_type}").is_file():
            Path(f"{self.download_target}/{self.hash_key_type}").unlink()

        if Path(f"{self.download_target}/{self.kern_name}").is_file():
            Path(f"{self.download_target}/{self.kern_name}").unlink()



