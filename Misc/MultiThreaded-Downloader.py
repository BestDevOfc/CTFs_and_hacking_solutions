# NOT MADE BY ME, just saved as a backup

#! /usr/bin/env python3
import click
import requests
import concurrent.futures as fut
import logging
import hashlib  
import sys


__author__ = "Akshay D. Nehe <anehe@cs.stonybrook.edu>"
__purpose__ = "A Multi-threading supported download utility"


def validate_thread_count(ctx, param, value):
    """
    Checks whether user input value for number_of_threads argument is a positive integer.
    """
    if type(value) is not int or value < 1:
        raise click.BadParameter('Should be a positive integer.')
    return value


def handler(t_name, start, end, url, filename):
    """
    The file chunk (from "start" to "end" bytes gets downloaded in this function
    from the "url" and is written into "filename" by thread ("t_name").
    Returns exit code 1 if some error encountered.
    TODO: Can be extended to resume partial download.
    """
    logging.debug("Thread %s: starting", t_name)
    headers = {'Range': 'bytes=%d-%d' % (start, end)}

    try:
        r = requests.get(url, headers=headers, stream=True)
    except requests.exceptions.ConnectionError as e:
        logging.error(e)
        return 1
    try:
        with open(filename, "r+b") as fp:
            fp.seek(start)
            fp.write(r.content)
    except Exception as e:
        logging.error(e)
        return 1
    logging.info("Chunk %s: finished download", t_name)
    logging.debug("Thread %s: Finished", t_name)
    return 0


@click.command(help="Script to download the file at specified URL")
@click.option('--number_of_threads', default=2, callback=validate_thread_count,
              help="Number of Threads")
@click.option('--name', type=click.Path(), help="Name of the file with extension")
@click.argument('url_of_file', type=click.Path())
def download_file(url_of_file, name, number_of_threads):
    """
    It is determined whether "utl_of_file" allows partial download and accordingly
    proceeds to download on main thread or spawned threads ("number_of_threads").
    The function exits when the entire file has been written to local disk.
    """
    multi_thread_possible = False
    exit_status = 0
    try:
        r = requests.head(url_of_file)
    except requests.exceptions.ConnectionError as e:
        logging.error(e)
        logging.error("Failed to establish connection so exiting.")
        return 1
    try:
        file_size = int(r.headers['content-length'])
    except (AttributeError, KeyError):
        logging.error("Invalid/Inaccessible URL: %s", url_of_file)
        return

    if name:
        file_name = name
    else:
        file_name = url_of_file.split('/')[-1]
        logging.info("Filename not provided. File will be named: %s", file_name)

    try:
        accept_ranges = str(r.headers['accept-ranges'])
        # Either field ACCEPT-RANGES is absent or set to "none" in response
        if accept_ranges == "none":
            raise KeyError
    except (AttributeError, KeyError):
        logging.warning("URL does not allow range access. Running on Main Thread.")
    else:
        multi_thread_possible = True
        logging.debug("URL allows partial download in %s", accept_ranges)

    if number_of_threads == 1:
        multi_thread_possible = False

    if multi_thread_possible:
        chunk_size = int(file_size) // number_of_threads
        fp = open(file_name, "wb")
        fp.seek(file_size - 1)
        fp.write(b"\0")
        fp.close()

        logging.debug("Part size: %d", chunk_size)

        list_of_tasks = [[i, chunk_size * i, chunk_size * (i + 1),
                          url_of_file, file_name] for i in range(number_of_threads)]
        # In some cases, the last few bytes of file do not get selected because we chose
        # integral division to determine chunk_size hence setting the last task's end as
        # the last byte
        list_of_tasks[-1][2] = file_size
        logging.info("Starting download in multi-threaded mode "
                     "with: %s threads", number_of_threads)
        # Using thread pool to manage spawned threads for each chunk
        with fut.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
            results = executor.map(lambda p: handler(*p), list_of_tasks)

        # Check if any of the threads failed at it's task
        for result in results:
            if result != 0:
                exit_status = 1
                break
    else:
        logging.info("Starting download in single-thread mode ")
        exit_status = handler("Main", 0, file_size, url_of_file, file_name)

    if exit_status == 0:
        logging.info('%s downloaded', file_name)
        with open(file_name, 'rb') as f:
            content = f.read()
        sha = hashlib.sha256()
        sha.update(content)
        logging.info("SHA256 Hash of downloaded file is: %s", sha.hexdigest())
    else:
        logging.error('ERROR: %s download failed', file_name)
    return exit_status


if __name__ == '__main__':
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Started")
    sys.exit(download_file(obj={}))
