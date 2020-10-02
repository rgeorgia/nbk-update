#!/usr/bin/env /usr/pkg/bin/python3.8
import argparse

import sys
import json
import platform
import urllib
from shutil import copy2
from pathlib import Path

from nbkhelper import Download, DownloadException

config_file = f"{str(Path.home())}/.nbkupdate.json"


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
    parser.add_argument(
        "--withkey",
        type=str,
        choices=["MD5", "md5", "SHA512", "sha512"],
        help="Name of new kernel, defaults to current",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    parser.add_argument("-y", "--yes", action="store_true", help="Automatically add yes to questions.")
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


def download_kernel(url: str, kern_name: str, download_target: str, url_tail: str):
    arch = platform.machine()
    print(
        f"Downloading {url}{arch}/{url_tail}{kern_name} to {download_target}/{kern_name}"
    )
    urllib.request.urlretrieve(
        f"{url}{arch}/{url_tail}{kern_name}", f"{download_target}/{kern_name}"
    )


def list_urls():
    pass


def list_kernels():
    pass


def create_ini():
    with open(config_file, "w") as cf:
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

        for line in file_content:
            cf.write(f"{line}\n")


def create_nbk_profile():
    data = {
        "url_tail": "binary/kernel/",
        "url": "http://nyftp.netbsd.org/pub/NetBSD-daily/HEAD/latest/",
        "newkernel": "current",
        "oldkernel": "occurent",
        "default-download": "/tmp",
        "kernel": "netbsd-GENERIC.gz",
    }

    with open(config_file, "w") as cf:
        json.dump(data, cf)


def copy_kernel(src_dir: str, kern_name: str, new_kern_name: str, verbose: bool = False, location: str = None, ):
    if location is None:
        location = f"/{new_kern_name}"
    else:
        location = f"{location}/{new_kern_name}"

    if verbose:
        print(f"[INFO] Copying {src_dir}/{kern_name} to {location}")

    try:
        copy2(f"{src_dir}/{kern_name}", f"{location}", )
    except PermissionError:
        print(
            f"Looks like you do not have permission to copy the file. "
            f"You will need to run as root or sudo.", file=sys.stderr
        )
        return False
    except Exception as e:
        print(f"Error copying file: {e}", file=sys.stderr)
        return False
    return True


def main(args: argparse.Namespace):
    main_exit_code = 0

    if not Path(config_file).is_file():
        create_nbk_profile()

    with open(config_file, "r") as data_file:
        cfg_data = json.load(data_file)

    k_file = Download(download_target=cfg_data.get("default-download"), url=cfg_data.get("url"),
                      url_tail=cfg_data.get("url_tail"), kern_name=cfg_data.get("kernel"), )
    if args.verbose:
        print(f'Downloading {cfg_data.get("kernel")} from {cfg_data.get("url")}, please wait...')

    try:
        k_file.download_kernel()
    except DownloadException as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    # unpack_kernel(kern_name=args.newkern, download_target=k_file.download_target)

    if args.withkey:
        k_file.hash_key_type = args.withkey.upper()

        if args.verbose:
            print(f'Downloading {args.withkey.upper()} from {cfg_data.get("url")}, please wait...')

        k_file.download_key()

        if not k_file.good_check_sum() and not args.yes:
            cont = input(
                f"WARNING: Checksum of {cfg_data.get('kernel')} does not match what was downloaded.\n"
                f"Would you like to continue? [y/N]"
            )
            if cont.upper() == "N" or cont == "":
                return 1

    try:
        if k_file.is_same_file():
            if args.verbose:
                print(f"Looks like the latest version is already installed")
            return 1
    except FileNotFoundError:
        pass

    except Exception as e:
        print(f"You need root permission to verify files: {e}", file=sys.stderr)
        return 1
    # cp /kern_name to old_kern_name
    src_dir = args.custom if args.custom else ""
    if not copy_kernel(src_dir=src_dir, kern_name=args.newkern, new_kern_name=f"{args.oldkern}",
                       location=args.custom, verbose=args.verbose, ):
        return 1
    # cp new kernel to /kern_name
    if not copy_kernel(src_dir=cfg_data.get("default-download"), kern_name=cfg_data.get("kernel"),
                       new_kern_name=f"{args.newkern}", location=args.custom, verbose=args.verbose, ):
        return 1

    if not is_in_boot_cfg(data=read_boot_cfg(), current_name=args.newkern):
        print("Warning: not in /boot.cfg, you may not be able to boot off your new kernel.", file=sys.stderr)
        return 1

    k_file.clean_up()
    return main_exit_code


if __name__ == "__main__":
    all_args = read_args()
    sys.exit(main(args=all_args))
