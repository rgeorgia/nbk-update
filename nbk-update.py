#!/usr/pkg/bin/python3.7
import argparse
import sys
import configparser
import urllib.request
import platform
import hashlib
from pathlib import Path
from enum import Enum
from nbkhelper import Download

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
        "--withkey",
        type=str,
        choices=["MD5", "md5","SHA512", "sha512"],
        help="Name of new kernel, defaults to current",
    )
    return parser.parse_args()


def read_boot_cfg() -> list:
    try:
        with open("/boot.cfg") as bcfg:
            boot_cfg_data = bcfg.readlines()
    except FileNotFoundError as ffe:
        print(
            f"That's strange, the /boot.cfg file seems to be missing: {ffe.args[1]} -> {ffe.filename}"
        )
        boot_cfg_data = [ffe.errno]

    return boot_cfg_data


def is_in_boot_cfg(data: list, current_name: str) -> bool:
    for line in data:
        if current_name in line:
            return True
    return False

def list_urls():
    pass


def list_kernels():

    pass


def create_json():
    file_content = {
  "url_tail": "binary/kernel/",
  "url": "http://nyftp.netbsd.org/pub/NetBSD-daily/HEAD/latest/",
  "newkernel": "current",
  "oldkernel": "occurent",
  "default-download": "/tmp",
  "kernel": "netbsd-GENERIC.gz"
}

    with open(config_file, "w") as cf:
        for line in file_content:
            cf.write(f"{line}\n")


def read_config():
    if not Path(config_file).is_file():
        create_ini()

    config = configparser.ConfigParser()
    config.read(config_file)

    return config


def report_update():
    pass


def main(args):
    main_exit_code = 0
    default_cfg = read_config()

    download_target = default_cfg.get("defaults", "default-download")
    url = default_cfg.get("defaults", "default-url")
    kern_name = default_cfg.get("defaults", "default-kernel")
    url_tail = default_cfg.get("urls", "urltail")

    k_file = Download(download_target=download_target, url=url, url_tail=url_tail, kern_name=kern_name)
    k_file.download_kernel()

    if args.withkey:
        k_file.download_key(hash_key=args.withkey)

        if not k_file.good_check_sum():
            print(
                f"WARNING: Checksum of {kern_name} does not match what was downloaded"
            )

    print(k_file.hash_of_file(hash_type=args.withkey))
    # cp /kern_name to old_kern_name
    # cp new kernel to /kern_name

    if not is_in_boot_cfg(data=read_boot_cfg(), current_name=args.newkern):
        print(
            "Warning: not in /boot.cfg, you may not be able to boot off your new kernel."
        )

    return main_exit_code


if __name__ == "__main__":
    args = read_args()
    sys.exit(main(args))
