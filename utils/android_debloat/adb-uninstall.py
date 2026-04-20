#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Usage: adb-uninstall.py <package-list>
#

import re
import sys
from subprocess import run, PIPE, STDOUT

def adb_clear(app):
    proc = run(f"adb shell pm clear --user 0 {app}".split(), capture_output=True, text=True)
    if proc.returncode:
        print(f"Failed: could not clear app data of '{app}'")
        return proc.returncode
    else:
        print(f"Success: cleared app data '{app}'")
        return 0

def adb_disable(app):
    proc = run(f"adb shell pm disable-user --user 0 {app}".split(), capture_output=True, text=True)
    if proc.returncode:
        print(f"Failed: could not disable '{app}'")
        return proc.returncode
    else:
        print(f"Success: disabled '{app}'")
        return 0

def adb_uninstall(app):
    proc = run(f"adb shell pm uninstall -k --user 0 {app}".split(), capture_output=True, text=True)
    if proc.returncode:
        print(f"Failed: could not uninstall '{app}'")
        return proc.returncode
    else:
        print(f"Success: uninstalled '{app}'")
        return 0

def adb_list_packages():
    stdout = run("adb shell pm list packages".split(), text=True, capture_output=True).stdout
    stdout = stdout.split("\n")

    installed = []
    for line in stdout:
        try:
            line = line.strip()
            line = line.split(":")[1]
            installed.append(line)
        except IndexError:
            continue

    return set(installed)

def read_package_list(name):
    with open(name) as fd:
        lines = fd.readlines()

    packages = []
    for line in lines:
        line = re.sub(r"#.*", "", line)
        line = line.strip()
        if line:
            packages.append(line)

    return set(packages)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <package-list>")
        sys.exit()

    installed = adb_list_packages()
    remove = read_package_list(sys.argv[1])
    remove = installed & remove

    # Clear cache, disable, and uninstall app.
    # Sometimes, uninstallation is shown as successful, but
    # the app remains accessible.  In these situations,
    # disabling can sometimes work.
    for app in remove:
        adb_clear(app)
        adb_disable(app)
        adb_uninstall(app)
        print()
