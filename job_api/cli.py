# The MIT License (MIT)
# Copyright (c) 2020 by the xcube development team and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json
import sys
from pprint import pprint

import click
from job_api.version import version


@click.command(name="create")
@click.option('--cube-conf', '-c',
              help="Submit a job using a config file")
def create(cube_conf: str):
    """
    Start the service.
    """

    from job_api.jobapi import JobApi
    api = JobApi()
    with open(cube_conf, 'r') as f:
        pprint(api.create(json.load(f)))


@click.command(name="list",
               help="List your jobs")
def lst():
    """
    Stop the service.
    """

    from job_api.jobapi import JobApi
    api = JobApi()
    pprint(api.list())


@click.command(name="status")
@click.option('--job-id', '-j',
              help="Get a job status")
def status(job_id: str):
    """
    Start the service.
    """

    from job_api.jobapi import JobApi
    api = JobApi()
    pprint(api.status(job_id))


@click.command(name="delete")
@click.option('--job-id', '-j',
              help="Delete a job")
def delete(job_id: str):
    """
    Start the service.
    """

    from job_api.jobapi import JobApi
    api = JobApi()
    pprint(api.delete(job_id))


# noinspection PyShadowingBuiltins,PyUnusedLocal
@click.group(name="xcube-gen")
@click.version_option(version)
def cli():
    """
    xcube data cube generation service.
    """


cli.add_command(create)
cli.add_command(status)
cli.add_command(lst)
cli.add_command(delete)


def main(args=None):
    # noinspection PyBroadException
    try:
        exit_code = cli.main(args=args, standalone_mode=False)
    except click.ClickException as e:
        e.show()
        exit_code = 1
    except Exception as e:
        import traceback
        traceback.print_exc()
        exit_code = 2
        print(f'Error: {e}')
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
