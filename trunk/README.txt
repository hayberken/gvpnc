1. Install the vpnc command which you must download separately.

2. In the /etc/vpnc directory, take the sample vpnc file I have provided here 
  and save it as 'gvpnc.conf'.

3. Edit /etc/vpnc/gvpnc.conf per the group id, group password, and user id that 
  you have been given by your VPN admin at your office.

4. Install Python and PyGTK if your distribution of Linux does not already
  include this.
  
5. Edit the gvpnc Bash script file where it says FIX ME. You need to put in a
  'cd' statement to change the directory to the location where this gvpnc.py
  file is located.
  
6. Run the gvpnc command. If it fails, it could be one of several things, but
  it just might be that your distribution of Linux puts files in different
  places than my Ubuntu Linux.
  


YES!!! Please update this code if you can do it better, by all means. I really
just don't have the time right now to do this better. And if you can port it
as an XUL application that uses xulrunner to load (see simplexul project on 
code.google.com), that would be even cooler.

