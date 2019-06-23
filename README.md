# Update NetBSD Kernel

requires python 3.7+

### NOTE:
This was totally inspired by [David Brownlee's update-netbsd-kernel](https://github.com/abs0/update-netbsd-kernel)

## Some initial thoughts for features

1. use toml or ini file to keep some config data
    1. Things like urls for kernels
    1. backup location
1. use url to list available kernels to download
    1. default to netbsd-GENERIC.gz
1. Read /boot.cfg and 
    1. alert user if the "new" name is not found
    1. alert user if the "old" name is not found
1. Compare freshly downloaded kernel version to "current" kernel version.
1. Requires sudo permissions to update /current and /ocurrent

## Options

* new kernel name: **defaults** to **current** (optional first param)
* name of "old kernel": **defaults** to **ocurrent** (optional second param)
* optional path to kernels (optional --custpath)
* force an update (optional --force)
* provide dry-run option (optional --dryrun)
* provide --configure option to setup ini or toml file


## Usage

```bash
$ nbk-update 
```
This uses the default **/current** for the new kernel name and **/ocurrent** for a place to store the old kernel. Download the GENERIC kernel from the url to a templocation. Compare the freshly downloaded kernel with **/current** (and maybe **/netbsd**?). If they downloaded kernel is newer than the **/current**, then copy **/current** to **/ocurrent** and then copy new kernel to **/current**. Print out status.

```bash
current:  version 8.99.49
ocurrent: version 8.99.47
netbsd:   version 8.1
```

Check /boot.cfg and search for new kernel name. If it's not there, alert the user only. No need to edit the file, that's what vi is for.

```bash
WARNING: $kernel_file_name not found in /boot.cfg. You may not be able to boot using your new kernel
```



