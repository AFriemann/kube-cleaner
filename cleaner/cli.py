#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, tempfile, yaml, datetime, logging
import click, pykube

logger = logging.getLogger(__name__)

def get_nodes(api):
    for node in pykube.Node.objects(api):
        yield node

def delete_node(api, node_object):
    pykube.Node(api, node_object).delete()

@click.command()
@click.option('--use-host-certs/--no-host-certs', default=True)
@click.option('--insecure/--secure', default=False)
@click.option('--token')
@click.option('-s', '--api-server')
@click.option('--time-shift', type=int, default=0, help='time shift between servers in seconds')
def main(use_host_certs, insecure, token, api_server, time_shift):
    """main"""
    if api_server is not None:
        config = pykube.KubeConfig.from_url(api_server)
    else:
        config = pykube.KubeConfig.from_service_account()

    api = pykube.HTTPClient(config)

    for node in get_nodes(api):
        node_object = node.obj
        for condition in node_object.get('status').get('conditions'):
            if condition.get('type') != 'Ready': continue
            if condition.get('status') == 'True': continue

            last_heartbeat = datetime.datetime.strptime(condition.get('lastHeartbeatTime'), '%Y-%m-%dT%H:%M:%SZ')
            shifted_heartbeat = last_heartbeat + datetime.timedelta(seconds=time_shift)
            difference = (datetime.datetime.now() - shifted_heartbeat).seconds

            if difference < 3600: continue

            logger.info('deleting node %s', node_object.get('metadata').get('name'))
            delete_node(api, node_object)

if __name__ == '__main__':
    exit(main())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
