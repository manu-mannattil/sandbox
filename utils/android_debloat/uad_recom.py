#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Make a list of packages based on uad_list.json that are
# safe to remove from the current device.
#
# Requires uad_lists.json to be in the same directory.
#
# [1] https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation/raw/refs/heads/main/resources/assets/uad_lists.json

import json
from subprocess import run, PIPE, STDOUT

# These apps need to be removed on a case-by-case basis,
# even though some of them are marked as "recommended" by
# UAD.  So avoid automated removal.
unsafe = {
    "com.android.chrome", # Google Chrome
    "com.android.vending", # Play Store
    "com.google.android.apps.maps", # Google Maps
    "com.google.android.apps.messaging", # Messaging
    "com.google.android.apps.nbu.files", # File browser
    "com.google.android.apps.nbu.paisa.user", # Google Pay
    "com.google.android.apps.photos", # Google Photos (gallery app)
    "com.google.android.apps.wellbeing", # Digital Wellbeing
    "com.google.android.backuptransport", # Allow apps to backup to Google servers
    "com.google.android.calculator", # Calculator
    "com.google.android.calendar", # Calendar app
    "com.google.android.contacts", # Contacts
    "com.google.android.dialer", # Phone
    "com.google.android.gm", # Gmail
    "com.google.android.googlequicksearchbox", # Google
    "com.google.android.inputmethod.latin", # Gboard (Google Keyboard)
    "com.google.android.youtube", # YouTube
    "com.google.ar.lens", # Google Lens
    "com.whatsapp", # WhatsApp
    "com.ubercab", # Uber
}

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

with open("uad_lists.json") as fd:
    data = json.load(fd)

recommended = []
for app, info in data.items():
    if info["removal"] == "Recommended":
        recommended.append(app)

installed = adb_list_packages()
recommended = set(recommended)
recommended = installed & recommended - unsafe

with open("uad_recom.conf", "w") as fd:
    fd.write("\n".join(recommended))
    print("List of safe-to-remove apps written to 'uad_recom.conf'")
