#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# detox-contract.py is a Python 3 script to clean up filenames by
# removing spaces and special characters.  It restricts the filenames to
# [a-z0-9.-_].  detox's functionality is very similar to the detox
# program by Doug Harple, although the implementation is much more
# rudimentary and simpler.  The basic usage is
#
#   detox-contract.py <file>...
#
# Compared to the original detox script, this script safely converts
# English contractions as well.  For more details about detox's options,
# run
#
#   detox-contract.py --help
#

import argparse
import os
import re
import sys
import unicodedata


WORDS = [
    " s",
    "ain t",
    "amn t",
    "aren t",
    "can t",
    "could ve",
    "couldn t",
    "couldn t ve",
    "daren t",
    "daresn t",
    "dasn t",
    "didn t",
    "doesn t",
    "don t",
    "everyone s",
    "gon t",
    "hadn t",
    "hasn t",
    "haven t",
    "he d",
    "he ll",
    "he s",
    "he ve",
    "how d",
    "how ll",
    "how re",
    "how s",
    "i d",
    "i ll",
    "i m",
    "i ve",
    "isn t",
    "it d",
    "it ll",
    "it s",
    "let s",
    "ma am",
    "mayn t",
    "may ve",
    "mightn t",
    "might ve",
    "mustn t",
    "mustn t ve",
    "must ve",
    "needn t",
    "oughtn t",
    "shalln t",
    "shan t",
    "she d",
    "she ll",
    "she s",
    "should ve",
    "shouldn t",
    "shouldn t ve",
    "somebody s",
    "someone s",
    "something s",
    "so re",
    "that ll",
    "that re",
    "that s",
    "that d",
    "there d",
    "there ll",
    "there re",
    "there s",
    "these re",
    "they d",
    "they ll",
    "they re",
    "they ve",
    "this s",
    "those re",
    "wasn t",
    "we d",
    "we d ve",
    "we ll",
    "we re",
    "we ve",
    "weren t",
    "what d",
    "what ll",
    "what re",
    "what s",
    "what ve",
    "when s",
    "where d",
    "where re",
    "where s",
    "where ve",
    "which s",
    "who d",
    "who d ve",
    "who ll",
    "whom st",
    "whom st d ve",
    "who re",
    "who s",
    "who ve",
    "why d",
    "why re",
    "why s",
    "won t",
    "would ve",
    "wouldn t",
    "y all",
    "y all d ve",
    "you d",
    "you ll",
    "you re",
    "you ve",
]

REGEXES = []
for w in WORDS:
    REGEXES.append([re.compile(r"\b{}\b".format(w)), w.replace(" ", "")])


def rename(root, name, dry=False):
    """Rename a file with the given root directory and name."""
    src = os.path.join(root, name)

    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore")
    name = name.decode("ascii")

    if os.path.isfile(src):
        name = re.sub(r"[_\W]+\.([^.]*)$", r".\1", name)

    name = re.sub(r"^(?!\.)[_\W^.]+", "", name)
    name = re.sub(r"[_\W]+$", "", name)
    name = re.sub(r"[\"']+", "", name)
    name = re.sub(r"[^\w.-]+", "_", name)
    name = name.replace("_", " ")
    name = name.lower()

    for regex, sub in REGEXES:
        name = regex.sub(sub, name)

    name = name.replace(" ", "_")
    dst = os.path.join(root, name)

    if src == dst:
        pass
    elif os.path.exists(dst):
        print("{} exists".format(dst), file=sys.stderr)
    else:
        print("{} -> {}".format(src, dst), file=sys.stderr)
        if not dry:
            try:
                os.replace(src, dst)
            except Exception as e:
                print(e, file=sys.stderr)


def detox(files, recurse=False, dry=False):
    """Detox a list of files."""
    for name in files:
        if os.path.isdir(name) and recurse:
            for root, dirs, files in os.walk(name, topdown=False):
                for f in files + dirs:
                    rename(root, f, dry)
        else:
            rename(os.path.dirname(name), os.path.basename(name), dry)

def arg_parser_valid(name):
    """Check if the file is valid and can be accessed."""
    if not os.path.isfile(name) and not os.path.isdir(name):
        raise argparse.ArgumentTypeError("{} is not a valid path".format(name))
    else:
        return os.path.normpath(name)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(prog="detox-contract.py",
        description="clean up filenames")
    arg_parser.add_argument("-r", "--recurse", action="store_true",
        default=False, help="recurse into directories")
    arg_parser.add_argument("-n", "--dry-run", action="store_true",
        default=False, help="dry run")
    arg_parser.add_argument("files", type=arg_parser_valid, nargs="+",
        help="input files")

    args = arg_parser.parse_args()
    sys.exit(detox(args.files, recurse=args.recurse, dry=args.dry_run))
