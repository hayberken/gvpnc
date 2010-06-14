#!/bin/bash

PREFIX=/usr/local
APPDIR=gvpnc


echo -n Installing gvpnc into $PREFIX...
mkdir -p $PREFIX/share/$APPDIR

install gvpnc $PREFIX/bin
install -m644 gvpnc.glade README TODO $PREFIX/share/$APPDIR
install -m644 gvpnc.desktop $PREFIX/share/applications

echo Done.
