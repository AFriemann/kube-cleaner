#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, tempfile, yaml
import click, pykube

def generate_config(host, token):
    return {
        "clusters": [
            {
                "name": "default",
                "cluster": {
                    "server": host,
                }
            }
        ],
        "contexts": [
            {
                "name": "default",
                "context": {
                    "cluster": "default",
                    "namespace": "kube-system",
                    "user": "default",
                }
            }
        ],
        "users": [
            {
                "name": "default",
                "user": { "token": token } if token is not None else {},
            }
        ],
        "current-context": "default",
    }
    # return """
    # apiVersion: v1
    # kind: Config
    # clusters:
    # - name: default
    #   cluster:
    #     api-version: v1
    #     server: {host}
    # users:
    # - name: default
    #   user:
    #     token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkZWZhdWx0LXRva2VuLXN2a3c0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImRlZmF1bHQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiIxZmRkNDJmNi01MzI2LTExZTYtODdmYi0wNjQ2NWUxOTY1ZmIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06ZGVmYXVsdCJ9.WU8Y7LHQ-lEmcfGPd1rhcOUhXSswB-ewcgBqPWEyu2FFPwtcGXq-v51sxI4Rzt--as6XbIoaFZWZ0CHC3XhO37taflFHOTvYP-kklJoiRqZPA1_BHoA6ruCD16esAYb5DOCUY7k70XTxx84-c1R1d_gB3yvHKFmNHrxiiqlhrIOfv5JXoPg_-D8A5gixMj1Q4dWybWf7eJblIOVA6hJdOt0Fv_Xjsr2y9H7NVSxEIPrc6bbqjVQZzDqi-pti1ttktKDOBBH1AwWxhPa0lfdkKmMiohHqopojaOt18ie_tpWWjhzRfOv3PL4mz88k3BSlwy8GNkO6O_RrkgjZ1b6J1Q
    # contexts:
    # - name: default
    #   context:
    #     cluster: default
    #     namespace: kube-system
    #     user: default
    # current-context: default
    # """.format(host=host)

def get_nodes(api):
    for node in pykube.Node.objects(api):
        yield node

@click.command()
@click.option('--use-host-certs/--no-host-certs', default=True)
@click.option('--insecure/--secure', default=False)
@click.option('--token')
@click.option('-s', '--api-server')
def main(use_host_certs, insecure, token, api_server):
    """main"""
    if api_server is not None:
        config = pykube.KubeConfig(generate_config(api_server, token))
    else:
        config = pykube.KubeConfig.from_service_account()

    api = pykube.HTTPClient(config)

    for node in get_nodes(api):
        print(10*'-' + str(node) + 10*'-')
        print(dir(node))
        print(node.annotations)



if __name__ == '__main__':
    exit(main())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
