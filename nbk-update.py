#!/usr/pkg/bin/python3.7
import argparse
import sys
import configparser
import urllib.request
import platform
import hashlib
from pathlib import Path
from enum import Enum
import nbkhelper

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
    parser.add_argument(
        "--withkey",
        type=str,
        choices=["MD5", "SHA512"],
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

    if not Path(f"{download_target}/{kern_name}").is_file():
        nbkhelper.download_kernel(
            download_target=download_target,
            url=url,
            kern_name=kern_name,
            url_tail=url_tail,
        )
    if args.withkey:
        nbkhelper.download_key(
            download_target=download_target,
            url=url,
            hash_key=args.withkey,
            url_tail=url_tail,
        )

        if not nbkhelper.good_check_sum(kern_name=kern_name, hash_type=args.withkey):
            print(
                f"WARNING: Checksum of {kern_name} does not match what was downloaded"
            )

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
