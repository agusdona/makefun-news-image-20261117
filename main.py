"""Decode entry.png.b64 next to this script into <output>/entry.png.

Usage: MAKEFUN_OUTPUT_DIR=/path/to/out python3 main.py
Output dir defaults to /output. Standard library only; never writes into
the repository directory.
"""
import base64
import binascii
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png.b64")
MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not os.path.isfile(SRC):
        sys.exit("missing entry.png.b64 next to %s" % __file__)
    with open(SRC, "rb") as f:
        data = f.read()
    try:
        png = base64.b64decode(b"".join(data.split()), validate=True)
    except (binascii.Error, ValueError, TypeError) as e:
        sys.exit("entry.png.b64 is not valid base64: %s" % e)
    if not png.startswith(MAGIC) or png[-8:-4] != b"IEND":
        sys.exit("decoded data is not a complete PNG")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(png)
    print("wrote %s (%d bytes)" % (dst, len(png)))


if __name__ == "__main__":
    main()
