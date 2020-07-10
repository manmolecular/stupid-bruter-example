#!/usr/bin/env python3

from src.core.bruter import Bruter, SyncBruter, BruterException
from pprint import pprint


class Values:
    HOST = "http://www.your_host_here.com/"
    LIMIT = None


def brute_example() -> None:
    """
    Just an example
    :return: None
    """
    base_bruter = Bruter(host=Values.HOST)
    print(f"'base_bruter' is {base_bruter}")

    try:
        base_bruter.host = ""
    except BruterException as wrong_host:
        print(f"Oops, what are you doing here? Error: {wrong_host}")

    try:
        base_bruter.brute()
    except Exception as unexp_error:
        print(f"Something gone wrong: {unexp_error}")

    bruter_sync = SyncBruter(host=Values.HOST, limit=Values.LIMIT)
    print(f"'bruter_sync' is {bruter_sync}")

    bruter_sync.brute()
    results = bruter_sync.get_results()
    pprint(results)


if __name__ == "__main__":
    try:
        brute_example()
    except KeyboardInterrupt:
        exit(0)
