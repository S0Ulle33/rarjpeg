import pathlib
import platform
import re
import zipfile

import rarfile


if platform.system() == 'Windows':
    UNRAR_PATH = pathlib.Path().cwd() / 'UnRar.exe'
else:
    UNRAR_PATH = pathlib.Path().cwd() / 'unrar'

if not pathlib.Path(UNRAR_PATH).is_file():
    raise FileNotFoundError(
        f"Can not find unrar at {UNRAR_PATH}, make sure you download it")
rarfile.UNRAR_TOOL = str(UNRAR_PATH)


SIGNATURES = {
    'ZIP_NORMAL': b'PK\x03\x04', 'ZIP_EMPTY': b'PK\x05\x06',
    'ZIP_SPANNED': b'PK\x07\x08',
    'RAR_1.50': b'Rar!\x1a\x07\x00', 'RAR_5.0': b'Rar!\x1a\x07\x01\x00'
}
FOLDER_TO_EXTRACT = 'extracted_rarjpegs'


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

    @property
    def is_valid(self):
        if not self._is_valid:
            self._check()

        return self._is_valid

    def __repr__(self):
        return f"Rarjpeg('{self.path}')"

    def _find_signature(self):

        self._bytes = self.path.read_bytes()

        for name, signature in SIGNATURES.items():
            found_signature = re.search(signature, self._bytes)
            if found_signature:
                self.type = name.split("_")[0]
                self._offset = found_signature.start()
                return

    def _check_archive(self):

        self.archive.write_bytes(self._bytes[self._offset:])

        if (zipfile.is_zipfile(str(self.archive)) or
                rarfile.is_rarfile(str(self.archive))):
            self._is_valid = True
            self.archive.unlink()
            return

        self.archive.unlink()
        self._is_valid = False
        return

    def _check(self):

        self._find_signature()
        self._check_archive()

    def extract(self):

        if not self._is_valid:
            return False, "there is no archive"

        self.archive.write_bytes(self._bytes[self._offset:])

        path_to_extract = str(pathlib.Path.cwd() / FOLDER_TO_EXTRACT /
                              self.name.with_suffix(''))

        func = {'RAR': rarfile.RarFile,
                'ZIP': zipfile.ZipFile}

        try:
            archive = func[self.type](str(self.archive))
            archive.extractall(path=path_to_extract)
        except Exception as e:
            return False, "requires password"
        finally:
            archive.close()
            self.archive.unlink()

        return True, "successfully"
