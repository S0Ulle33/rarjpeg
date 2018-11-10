import re
import os
import zipfile
import rarfile

SIGNATURES = {
    'ZIP_NORMAL': b'PK\x03\x04', 'ZIP_EMPTY': b'PK\x05\x06',
    'ZIP_SPANNED': b'PK\x07\x08',
    'RAR_1.50': b'Rar!\x1a\x07\x00', 'RAR_5.0': b'Rar!\x1a\x07\x01\x00'
}


def is_valid(byte_str, offset):

    with open('test.rar', 'wb') as f:
        f.write(byte_str[offset:])

    if (zipfile.is_zipfile('test.rar') or
            rarfile.is_rarfile('test.rar')):
        os.remove('test.rar')
        return True

    os.remove('test.rar')
    return False


def is_rarjpeg(rarjpeg):

    with open(rarjpeg, 'rb') as f:
        byte_str = f.read()

    for name, signature in SIGNATURES.items():
        search = re.search(signature, byte_str)
        if search:
            offset = search.start()
            return is_valid(byte_str, offset)
