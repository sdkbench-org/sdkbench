"""Run P1b with the shared strict campaign lifecycle."""
from ..p1a.cli import main as campaign_main


def main(argv=None):
    return campaign_main(argv, suite='p1b')


if __name__ == '__main__':raise SystemExit(main())
