#!/usr/bin/env python3

from asyncio import get_event_loop, as_completed
from functools import wraps
from getpass import getuser
from logging import getLogger, INFO, basicConfig
from pathlib import Path
from time import time, strftime, gmtime
from urllib.parse import urlparse

from aiohttp import ClientSession, ClientResponse, ClientConnectionError
from requests import head, Response

basicConfig(level=INFO)
logger = getLogger(name="bruter")


def timer(function):
    """
    Timer that used to count runtime
    of different functions. Simple.
    :param function: wrapping function
    :return: wrapped function
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        print(
            f"Function '{function.__name__}' is running... Args: {args}, Kwargs: {kwargs}",
            flush=True,
        )
        start = time()
        result = function(*args, **kwargs)
        end = time()
        seconds = round(end - start, 2)
        print(
            f"Done in {seconds}s ({str(strftime('%H:%M:%S', gmtime(seconds)))})",
            flush=True,
        )
        return result

    return wrapper


def show_function_meta(please_lie_to_me: bool = False) -> callable:
    """
    Wrap function to show some info
    :param please_lie_to_me: <3 if you like liars
    :return: wrapped function
    """

    def wrap(function):
        def wrapped_function(*args, **kwargs):
            if please_lie_to_me:
                logger.warning(
                    msg=f"Nothing is permanent, everything is permitted, {getuser()}!"
                )
                return
            logger.info(
                f"Function '{function.__name__}' is running... Args: {args}, Kwargs: {kwargs}"
            )
            return function(*args, **kwargs)

        return wrapped_function

    return wrap


class Defaults:
    FILE_DIR: Path = Path("src/assets/")
    FILE_NAME: str = "fuzz.txt"


class BruterException(Exception):
    def __init__(self, error_args: Exception or str):
        super().__init__(self)
        self._error_args = error_args

    @property
    def error_args(self):
        return self._error_args

    def __str__(self):
        return f"Error occured in Bruter module: {self._error_args}"


class Bruter:
    def __init__(self, host: str = None, limit: int or None = None):
        """
        Initialize the base class with some values
        :param host: host to use as a target server
        :param limit: limit of payloads to send
        """
        self.__host = host
        self.__limit = limit
        self.fuzz_list = []

    def __repr__(self) -> str:
        """
        Print class instances
        :return: return string representation
        """
        dump = dict(host=self.__host, limit=self.__limit, payloads=self.fuzz_list)
        return f"Class {self.__class__.__name__}, " f"values: {dump}"

    @property
    def host(self) -> str:
        """
        Get host property. Look, it's private btw!
        :return: host
        """
        return self.__host

    @host.setter
    def host(self, host: str) -> None:
        """
        Set host
        :param host: host to set
        :return: None
        """
        if not host:
            raise BruterException("You should put here the right host, buddy!")
        self.__host = host

    def open_file(
        self, filename: str = Defaults.FILE_NAME, limit: int or None = None
    ) -> None:
        """
        Open file with the payloads, read lines from it and return
        list of entities (like brute elements, you can call it as you wish.)
        :param filename: name of the file to open
        :param limit: limit to get lines, payloads limit
        :return: None
        """
        _limit = limit or self.__limit
        with open(
            file=f"{Defaults.FILE_DIR.joinpath(filename)}", mode="r"
        ) as fuzz_file:
            fuzz_list = fuzz_file.read().splitlines()
            if _limit:
                self.fuzz_list = fuzz_list[:_limit]
            else:
                self.fuzz_list = fuzz_list

    @staticmethod
    def log(filename: str, status: int, url: str, length: int or None) -> None:
        """
        Log response to the stdout with logging module
        :param filename: filename
        :param status: status code
        :param url: URL of the file
        :param length: response length
        :return: None
        """
        logger.info(
            msg=f"file: {filename}, status: {status}, url: {url}, length: {length}"
        )

    @staticmethod
    def process(
        results: list, filename: str, status: int, url: str, length: int or None
    ) -> None:
        """
        Process results, append them to 'results' list
        :param results: all results
        :param filename: name of the file
        :param status: response code status
        :param url: URL of the file
        :param length: length of the HTTP response ('content-length' field)
        :return: None
        """
        results.append(dict(file=filename, status=status, url=url, length=length))

    def brute(self, *args, **kwargs) -> None:
        """
        Base brute method. It is not implemented, bruh >:(
        :param args: some args
        :param kwargs: some kwargs
        :return: None, but raises an error!
        """
        raise NotImplementedError("This method is not implemented")


class ThreadBruter(Bruter):
    """
    Yay, that's cool! But what about deadlocks, race conditions, memory corruptions and so on?
    Are you ready for it?
    """

    ...


class MultiprocessingBruter(Bruter):
    """
    Are you sure bruh?
    """

    ...


class AsyncBruter(Bruter):
    """
    Define Asynchronous bruter.
    Should be best solution.
    """

    def __init__(self, *args, **kwargs):
        """
        Re-init the base class.
        Append argument 'results' to class.
        """
        super().__init__(*args, **kwargs)
        self.session = None
        self.results = []

    @staticmethod
    async def __check_file(
        session: ClientSession, file_url: str, filename: str
    ) -> (ClientResponse or None, str or None, str or None):
        """
        Check if file exists or not?
        :param file_url: URL to check file existence
        :return: response + checked URL
        """
        try:
            async with await session.head(file_url) as resp:
                return (
                    (resp, file_url, filename)
                    if resp.status == 200
                    else (None, None, None)
                )
        except ClientConnectionError:
            logger.info("Connection error while trying to access", filename)
            return None, None, None

    # @show_function_meta()
    async def __brute(self, host: str = None) -> None:
        """
        Async brute directories and files
        :param host: host to brute
        :return: None
        """
        if not self.fuzz_list:
            self.open_file()
        target = urlparse(host or self.host)
        session = ClientSession()
        futures = [
            self.__check_file(
                session, f"{target.scheme}://{target.hostname}/{filename}", filename
            )
            for filename in self.fuzz_list
        ]
        for future in as_completed(futures):
            response, file_url, filename = await future
            if not response:
                continue
            result = (
                filename or "-",
                response.status,
                file_url,
                response.headers.get("Content-Length"),
            )
            self.log(*result)
            self.process(self.results, *result)
        await session.close()

    @timer
    def brute(self, host: str = None) -> None:
        """
        Start asyncio event loop
        """
        ioloop = get_event_loop()
        ioloop.run_until_complete(self.__brute(host))
        ioloop.close()

    def get_results(self) -> list:
        """
        Return results from the class instance
        :return: list of the results
        """
        return self.results


class SyncBruter(Bruter):
    """
    Define Synchronous bruter.
    It's slow and not optimized, but can show you
    the basics of python structures.
    """

    def __init__(self, *args, **kwargs):
        """
        Append one additional argument to this class, 'results'.
        Re-init the base class here too.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.results = []

    @staticmethod
    def __check_file(file_url: str) -> (Response or None, str or None):
        """
        Check if file exists or not?
        :param file_url: URL to check file existence
        :return: response + checked URL
        """
        response = head(file_url)
        if response.status_code != 200:
            return None, None
        return response, file_url

    # @show_function_meta(please_lie_to_me=False)
    @timer
    def brute(self, host: str = None) -> None:
        """
        Brute directories and files
        :param host: host to brute
        :return: None
        """
        if not self.fuzz_list:
            self.open_file()
        target = urlparse(host or self.host)
        for filename in self.fuzz_list:
            response, file_url = self.__check_file(
                file_url=f"{target.scheme}://{target.hostname}/{filename}"
            )

            if not response:
                continue
            result = (
                filename,
                response.status_code,
                file_url,
                response.headers.get("content-length"),
            )
            self.log(*result)
            self.process(self.results, *result)

    def get_results(self) -> list:
        """
        Return results from the class instance
        :return: list of the results
        """
        return self.results
