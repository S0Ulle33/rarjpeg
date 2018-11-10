import argparse
import logging
import pathlib

from src.rarjpeg_class import Rarjpeg


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S %d.%m.%Y')
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(usage="%(prog)s TARGET [-e]",
                                 description="Checks TARGET image or folder for rarjpeg(-s).")
parser.add_argument('target', help='name of the FILE or DIRECTORY to check')
parser.add_argument('-e', '--extract', action='store_true', default=False,
                    help='extract files from found rarjpegs')


def check(rarjpeg_path, extract=False):

    rarjpeg = Rarjpeg(rarjpeg_path)
    valid = rarjpeg.check()
    logging.info(f"{rarjpeg.name} is {'valid' if valid else 'invalid'}")

    if extract:
        extracted, msg = rarjpeg.extract()
        logging.info(
            f"{rarjpeg.archive} {'was extracted' if extracted else 'was not extracted,'} {msg}\n")


def main():
    args = parser.parse_args()

    if args.target:
        path = pathlib.Path.cwd() / args.target.lstrip('/')
        if path.is_file():
            check(path, args.extract)
        elif path.is_dir():
            for image in path.iterdir():
                if image.suffix == '.jpg':
                    check(image, args.extract)
        else:
            logger.error('Something went wrong!\n')
            parser.print_help()


if __name__ == '__main__':
    main()
