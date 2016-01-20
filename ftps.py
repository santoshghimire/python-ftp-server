#!/usr/bin/env python

"""
An RFC-4217 asynchronous FTPS server supporting both SSL and TLS.
Requires PyOpenSSL module (http://pypi.python.org/pypi/pyOpenSSL).
"""

from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
import yaml
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
import sys


class S3Upload():
    """ This class uploads the given files to S3 Bucket.
    """

    def upload_to_s3(self, file_name, path=None):
        print("Uploading file to s3")
        conn = S3Connection()
        bucket_name = 'BUCKET_NAME'
        try:
            bucket = conn.create_bucket(bucket_name)
        except:
            bucket = conn.get_bucket(bucket_name)

        print('Uploading %s to Amazon S3 bucket %s' % (file_name, bucket_name))

        k = Key(bucket)
        if path:
            full_path = os.path.join(path, file_name)
        else:
            full_path = file_name
        k.key = full_path
        k.set_contents_from_filename(
            full_path,
            cb=self.percent_cb, num_cb=10
        )
        full_path_dir = '/'.join(full_path.split('/')[:-1])
        full_path_dir = full_path_dir[1:] if full_path_dir.startswith('/') else full_path
        keys = bucket.list(full_path_dir)
        user = full_path.split('/')[-2]
        for k in keys:
            newkeyname = 'ftp/' + user + '/' + k.name.partition(full_path_dir)[2]
            bucket.copy_key(newkeyname, k.bucket.name, k.name)
            k.delete()
        print('done')
        
    def percent_cb(self, complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()


class MyHandler(TLS_FTPHandler):
    """
    Custom TLS_FTPHandler that uploads the file received on ftp server to s3 bucket.
    """
    def on_file_received(self, file):
        # when a file has been received, upload to s3 bucket
        # just comment out this method if you don't want the files to be uploaded to s3
        s3 = S3Upload()
        s3.upload_to_s3(file)


def main():
    """
    Main ftp server code
    """
    with open("ABSOLUTE_PATH_OF_config.yaml", 'r') as stream:
        config = yaml.load(stream)
        authorizer = DummyAuthorizer()
        if config.get('user'):
            for each_user in config['user']:
                if not os.path.exists(each_user['details']['home_directory']):
                    os.makedirs(each_user['details']['home_directory'])
                authorizer.add_user(
                    each_user['details']['username'],
                    each_user['details']['password'],
                    each_user['details']['home_directory'],
                    perm=each_user['details']['permission']
                )
        authorizer.add_anonymous('.')
        handler = MyHandler
        handler.certfile = config['certfile']
        handler.authorizer = authorizer
        handler.masquerade_address = config['masquerade_address']
        # requires SSL for both control and data channel
        handler.tls_control_required = True
        handler.tls_data_required = True
        handler.passive_ports = range(60000, 60099)
        server = FTPServer(('', 21), handler)
        server.serve_forever()

if __name__ == '__main__':
    main()