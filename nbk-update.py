#!/usr/pkg/bin/python3.7
import argparse
import sys
import configparser
import urllib.request
import platform
from pathlib import Path

config_file = f"{str(Path.home())}/.nbkupdate.ini"


def read_args():
    parser = argparse.ArgumentParser(description="Download and update NetBSD kernel.")
    parser.add_argument(
        "--newkern",
        type=str,
        default="current",
        help="Name of new kernel, defaults to current",
    )
    parser.add_argument(
        "--oldkern",
        type=str,
        default="ocurrent",
        help="Name of new kernel, defaults to current",
    )
    parser.add_argument(
        "--custom", type=str, help="Set a custom target directory to install new kernel"
    )
    parser.add_argument("--force", action="store_true", help="Force an update")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Download kern to temp dir and display the kernel version, "
        "but do not replace the default kernel.",
    )

    return parser.parse_args()


def read_boot_cfg() -> str:
    with open("/boot.cfg") as bcfg:
        boot_cfg_data = bcfg.readlines()

    return boot_cfg_data


def is_in_boot_cfg(data: str) -> bool:
    return False


def download_kernel(url: str, kern_name: str, download_target: str, url_tail: str):
    arch = platform.machine()
    print(
        f"Dowloading {url}{arch}/{url_tail}{kern_name} to {download_target}/{kern_name}"
    )
    urllib.request.urlretrieve(
        f"{url}{arch}/{url_tail}{kern_name}", f"{download_target}/{kern_name}"
    )


def list_urls():
    pass


def list_kernels():

    pass


def create_ini():
    file_content = [
        "[urls]",
        "nyftp = http://nyftp.netbsd.org/pub/NetBSD-daily/HEAD/latest/",
        "nycdn = http://nycdn.netbsd.org/pub/NetBSD-daily/HEAD/latest/",
        "urltail = binary/kernel/",
        "[defaults]",
        "default-url = http://nyftp.netbsd.org/pub/NetBSD-daily/HEAD/latest/",
        "default-src = current",
        "default-tgt = occurent",
        "default-download = /tmp",
        "default-kernel = netbsd-GENERIC.gz",
    ]

    with open(config_file, "w") as cf:
        for line in file_content:
            cf.write(f"{line}\n")


def read_config():
    # if .nbkern.ini is not present, create one in home directory
    # else, read the file
    if not Path(config_file).is_file():
        create_ini()

    config = configparser.ConfigParser()
    config.read(config_file)

    return config


def report_update():
    pass


def main():
    main_exit_code = 0
    default_cfg = read_config()
    args = read_args()

    download_kernel(
        download_target=default_cfg.get("defaults", "default-download"),
        url=default_cfg.get("defaults", "default-url"),
        kern_name=default_cfg.get("defaults", "default-kernel"),
        url_tail=default_cfg.get("urls", "urltail"),
    )

    if not is_in_boot_cfg(data=read_boot_cfg()):
        print("Waring: not in /boot.cfg")

    return main_exit_code


if __name__ == "__main__":
    sys.exit(main())
