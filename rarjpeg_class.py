import re
import os
import pathlib
import zipfile

import rarfile

SIGNATURES = {
    'ZIP_NORMAL': b'PK\x03\x04', 'ZIP_EMPTY': b'PK\x05\x06',
    'ZIP_SPANNED': b'PK\x07\x08',
    'RAR_1.50': b'Rar!\x1a\x07\x00', 'RAR_5.0': b'Rar!\x1a\x07\x01\x00'
}
EXTRACT_FOLDER = 'extracted_rarjpegs'


class Rarjpeg:

    __slots__ = ('path', 'name', 'archive', 'type',
                 '_bytes', '_offset', '_is_valid')

    def __init__(self, path):

        self.path = pathlib.Path(path)
        self.name = pathlib.Path(self.path.name)
        self.archive = self.name.with_suffix('.rar')
        self.type = None

        self._bytes = None
        self._offset = None
        self._is_valid = None

    def _find_signature(self):

        with open(self.path, 'rb') as f:
            self._bytes = f.read()

        for name, signature in SIGNATURES.items():
            found_signature = re.search(signature, self._bytes)
            if found_signature:
                self.type = name.split("_")[0]
                self._offset = found_signature.start()
                return

    def _check_archive(self):

        with open(self.archive, 'wb') as f:
            f.write(self._bytes[self._offset:])

        if (zipfile.is_zipfile(str(self.archive)) or
                rarfile.is_rarfile(str(self.archive))):
            self._is_valid = True

        os.remove(self.archive)
        self._is_valid = False
        return

    def extract(self):

        if not self._is_valid:
            return False, "there is no archive"

        with open(self.archive, 'wb') as f:
            f.write(self._bytes[self._offset:])

        path_to_extract = str(pathlib.Path.cwd() / EXTRACT_FOLDER /
                              self.name.with_suffix(''))

        func = {'RAR': rarfile.RarFile,
                'ZIP': zipfile.ZipFile}

        try:
            archive = func[self.type](str(self.archive))
            archive.extractall(path=path_to_extract)
        except Exception:
            return False, "requires password"
        finally:
            os.remove(self.archive)
            archive.close()

        return True, "successfully"

    def check(self):

        self._find_signature()
        self._check_archive()

        return self._is_valid
