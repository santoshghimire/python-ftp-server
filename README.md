# python-ftp-server
Simple ftps server in python using pyftpdlib

## PRE-INSTALLATION INSTRUCTIONS

Before installing anything, follow these steps:
1.  Rename config_sample.yaml file inside the source directory to config.yaml

2.  Change a few things in the config.yaml file.
  1.  Replace the value of masquerade_address with the public ip address of the server.
  2.  Replace the value of certfile with the absolute path of the certificate file keycert.pem
  3.  Add users with username, password and their home directory, and permissions.
    1.  Read permissions:
      -  "e" = change directory (CWD command)
      -  "l" = list files (LIST, NLST, MLSD commands)
      -  "r" = retrieve file from the server (RETR command)

    2.  Write permissions:
      -  "a" = append data to an existing file (APPE command)
      -  "d" = delete file or directory (DELE, RMD commands)
      -  "f" = rename file or directory (RNFR, RNTO commands)
      -  "m" = create directory (MKD command)
      -  "w" = store a file to the server (STOR, STOU commands)

## INSTALLATION INSTRUCTIONS
For debian server:

1.  `sudo apt-get update`
2.  `sudo apt-get install python-pip`
3.  `sudo apt-get install build-essential libssl-dev libffi-dev python-dev`
4.  `sudo pip install pyftpdlib`
5.  `sudo pip install cryptography`
6.  `sudo pip install pyopenssl`
7.  `sudo pip install pyyaml`

8.  (If the ftps server is an EC2 instance, before running the script, we need to open some ports for ftp)
  1.  In Amazon EC2 console, on the left, click on Security group.
  2.  Select security group of the ec2 instance.
  3.  Click on inbound tab and click edit.
  4.  Add two tcp rules shown in the screenshot tcp.png

## Upstart configuration:
1.  Paste the upstart config file pyftplib.conf to `/etc/init/` (it requires admin privilage to paste so use sudo).
2.  Make the script ftps.py and ftps.sh exucetable by the following command.
  1.  `chmod u+x ftps.py`
  2.  `chmod u+x ftps.sh`

## RUNNING THE FTP SERVER
`sudo service pyftpdlib start`

That's it !! The ftps server is now ready !