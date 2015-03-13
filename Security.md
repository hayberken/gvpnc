# Introduction #

Well it's a VPN, so there's got to be some security issues, right?


# Details #

Firstly, gvpnc only supports Xauth/PSK authentication, which is known to be insecure.  It would be nice to support certificates, but vpnc only partly supports them, so that is unlikely to happen fully.

Second, the original gvpnc ran entirely as 'root' and read/wrote to the /etc/vpnc
directory.  I've already changed that so that it reads/writes to the user's .config
directory and only runs 'vpnc' itself as root.

The next thing to do is to not write passwords into the .conf files.  I've got some ideas on how to do that.