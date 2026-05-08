#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Website.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        sys.stderr.write(
            "\nCouldn't import Django. Are you sure it's installed and\n"
            "available on your PYTHONPATH environment variable?\n" 
            "Did you forget to activate a virtual environment?\n"
        )
        sys.exit(0)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()