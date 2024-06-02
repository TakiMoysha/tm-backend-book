#!/usr/bin/env python

# running python module


def main():
    import sys

    from app_protocols.cli import runserver

    try:
        exit_status = runserver()
        sys.exit(exit_status)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
