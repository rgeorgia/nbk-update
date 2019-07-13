# Update NetBSD Kernel

requires python 3.7+

### Brownlee Points:
This was totally inspired by [David Brownlee's update-netbsd-kernel](https://github.com/abs0/update-netbsd-kernel)

## Summary:

* Download kernel from NetBSD-daily/HEAD/latest/ to /tmp directory (or to different target dir: future)
* Fetch MD5 or SHA512 hash file, depending on with _withkey_ option is used
* Verify downloaded file against hash
* If everything checks out, check the current /current version against what was just downloaded. If they are the same, quit. (unless the -f or _force_ option is present)
* Copy /current to /ocurrent
* Copy downloaded file from /tmp to /current.
* Check /boot.cfg. if current is not present, alert the user
* Clean up /tmp

## Some Initial Thoughts For Features

1. Use ini file to keep some config data
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
* optional path to kernels (optional --custom)
* withkey: pulls down hash file, either MD5 or SHA512
* provide --configure option to setup .nbkupdate.json file

## Future options?

* target: name of target directory to download kernel to. **defaults** to **/tmp**
* remote: allow user to enter different url
* list: list remote kernel available. This will allow other architectures
* kern: allow user to download a specific kernel from the server


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
WARNING: $kernel_file_name not found in /boot.cfg. 
You may not be able to boot using your new kernel.
```



