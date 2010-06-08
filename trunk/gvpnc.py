#!/usr/bin/python2.2
#

# gvpnc v. 1.01
# Copyright © 2007, Super Mike

# A GUI for the vpnc command (distributed separately)

# You may change and re-release as commercial and customized versions per the license. See artistic license.


# the imports below I just pulled from boilerplate from redhat control panels
# and then added others as I received errors
import sys;
import os;
import string;
import popen2;
import pygtk;
pygtk.require('2.0');
import gtk;
import gobject;
import gtk.gdk;
import gtk.glade;
from gtk import TRUE, FALSE;

# assign our globals
global txtResultFont;
global window;

# our signal handling (mostly in menu order)
def on_Run(*args):
	sCmd = 'cat /etc/vpnc/gvpnc.conf | grep "gateway" | cut -d " " -f 3 | tr -d "\n"';
	sResult = RunBash(sCmd);
	if (StrDoesNotContain(sResult, 'cat: ')):
		SetWidgetText('run_server',sResult);
		Widget('run_password').grab_focus();
		sCmd = 'cat /etc/vpnc/gvpnc.conf | grep "IPSec ID" | cut -d " " -f 3 | tr -d "\n"';
		sResult = RunBash(sCmd);
		SetWidgetText('run_groupname',sResult);
		sCmd = 'cat /etc/vpnc/gvpnc.conf | grep "IPSec secret" | cut -d " " -f 3 | tr -d "\n"';
		sResult = RunBash(sCmd);
		SetWidgetText('run_grouppassword',sResult);
		sCmd = 'cat /etc/vpnc/gvpnc.conf | grep "Xauth username" | cut -d " " -f 3 | tr -d "\n"';
		sResult = RunBash(sCmd);
		SetWidgetText('run_username',sResult);
	SetWidgetText('run_password','');
	ShowWindow('run_command');
	
def on_Quit(*args):
	sCmd = "killall buildrunconf.sh";
	RunBash(sCmd);
	QuitAll();

def on_About(*args):
	MessageBox("\n\n\tGnome Cisco VPN Connector GUI (gvpnc)\t\t\n\tCopyright © 2007, Super Mike, v. 1.01\t\t\n\n\tThe component vpnc is required and\n\tis not shippped with this GUI. As of\n\tthis build, vpnc copyrights were listed\n\tas: Copyright (C) 2002-2004 Geoffrey\n\tKeating, Maurice Massar. Without their\n\tefforts, gvpnc could not be possible.\n\t\t\n\n\tThis GUI is distributed on the Artistic License.\n\t\t");	
	
# and now the ancillary signals

def on_RunNow(*args):
	sServer = GetWidgetText('run_server');
	sGroup = GetWidgetText('run_groupname');
	sGroupPass = GetWidgetText('run_grouppassword');
	sUser = GetWidgetText('run_username');
	sPass = GetWidgetText('run_password');
	sCmd = '/bin/bash buildrunconf.sh "' + sServer + '" "' + sGroup + '" "' + sGroupPass + '" "' + sUser + '" "' + sPass + '"';
	HideWindow('run_command');
	Refresh();
	Refresh();
	sResult = RunBash(sCmd);
	if (StrDoesNotContain(sResult, 'vpnc: ')):
		Status('Server: ' + sServer + ' CONNECTED');
	else:
		Status('Server: ' + sServer + ' Disconnected');
	SetWidgetText('txtResult', sResult);
	
def on_Stop(*args):
	sServer = GetWidgetText('run_server');
	sCmd = 'vpnc-disconnect';
	sResult = RunBash(sCmd);
	if (StrDoesNotContain(sResult, 'vpnc: ')):
		Status('Server: ' + sServer + ' Disconnected');	
	SetWidgetText('txtResult', sResult);
	
def on_RunCancel(*args):
	HideWindow('run_command');

def on_AboutClose(*args):
	HideWindow('about');
	
# and now our functions to make life easier
	
def DoNothing():
	print('test');

def GetWidgetText(sName):
	sResult = '';
	try: # for ordinary text fields
		sResult = Widget(sName).get_text();
	except:
		try: # for scrolling textboxes
			c1 = Widget(sName).get_buffer().get_start_iter();
			c2 = Widget(sName).get_buffer().get_end_iter();
			sResult = Widget(sName).get_buffer().get_slice(c1,c2,TRUE);
		except:
			a = '';
	if (sResult == ''):
		try: # for scrolling textboxes
			c1 = Widget(sName).get_buffer().get_start_iter();
			c2 = Widget(sName).get_buffer().get_end_iter();
			sResult = Widget(sName).get_buffer().get_slice(c1,c2,TRUE);
		except:
			sResult = '';
	return sResult;
	
def SetWidgetText(sName, sText):
	if (sText == ''):
		try:
			aReset = string.split('\n', "\n");
			Widget(sName).set_popdown_strings(aReset);
		except:
			a = '';	
	try:
		Widget(sName).get_buffer().set_text(sText);
	except:
		try:
			Widget(sName).set_text(sText);
		except:
			return;			
		
def Widget(sName):
	return MyWindows.get_widget(sName);		
		
def ShowWindow(thewindow):
    Widget(thewindow).show();
    
def HideWindow(thewindow):
    Widget(thewindow).hide();

def Destroy(thewindow):
    Widget(thewindow).destroy();
	
def SetResultFont(*args):
	o = args[0].get_buffer();
	c1 = o.get_start_iter();
	c2 = o.get_end_iter();
	o.apply_tag(txtResultFont,c1,c2);
	pass;

def Status(sMsg):
	Widget('statusbar1').pop(0);
	Widget('statusbar1').push(0,sMsg);

def MessageBox(sMsg):
	global window;
	dialog = gtk.MessageDialog(
		window, 
		gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
		gtk.MESSAGE_INFO, 
		gtk.BUTTONS_OK, 
		sMsg
	);
	dialog.run();
	dialog.destroy();

def ErrorBox(sMsg):
	global window;
	dialog = gtk.MessageDialog(
		window, 
		gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
		gtk.MESSAGE_WARNING, 
		gtk.BUTTONS_OK, 
		sMsg
	);
	dialog.run();
	dialog.destroy();

def QuestionYesNoBox(sMsg):
	global window;
	dialog = gtk.MessageDialog(
		window, 
		gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
		gtk.MESSAGE_QUESTION, 
		gtk.BUTTONS_YES_NO, 
		sMsg
	);
	response = dialog.run();
	dialog.destroy();
	return response;

def QuestionOKCancelBox(sMsg):
	global window;
	dialog = gtk.MessageDialog(
		window, 
		gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
		gtk.MESSAGE_QUESTION, 
		gtk.BUTTONS_OK_CANCEL, 
		sMsg
	);
	response = dialog.run();
	dialog.destroy();
	return response;

def RunBash(sBash):
	output, err = popen2.popen4(sBash);
	sResult = output.read();
	output.close();
	return sResult;

def SpawnBash(sBash):
	if (sBash[-1] != '&'):
		sBash = sBash + ' &';
	output, err = popen2.popen4(sBash);
	output.close();
	return;
	
def PrepareOpenFile(sTitleMessage):
	sFile = '';
	fb = gtk.FileSelection(sTitleMessage);
	fb.set_position(gtk.WIN_POS_CENTER);
	fb.set_filename(gsHomeDir);
	fb.show_all();
	result = fb.run();
	fb.hide();
	if (result == gtk.RESPONSE_OK):
		sFile = fb.get_filename();
		sFile = StrTrim(sFile);
		if ((StrRight(sFile, 1) == '/') or (sFile == '') or (sFile == '/')):
			MessageBox('No filename entered. Nothing opened.');
			return;		
	return sFile;	
	
def PrepareSaveFile(sTitleMessage, sFileExtension, bRootHomeSafety):
	fb = gtk.FileSelection(sTitleMessage);
	fb.set_position(gtk.WIN_POS_CENTER);
	fb.set_filename(gsHomeDir);
	fb.show_all();
	result = fb.run();
	fb.hide();
	if (result == gtk.RESPONSE_OK):
		sFile = fb.get_filename();
		sFile = StrTrim(sFile);
		if ((StrRight(sFile, 1) == '/') or (sFile == '') or (sFile == '/')):
			MessageBox('No filename entered. Nothing saved.');
			return;
		sFileExtension = StrLCase(sFileExtension);			
		if (StrLeft(sFileExtension, 1) != '.'):
			sFileExtension = '.' + sFileExtension;
		if (StrLCase(StrRight(sFile, 4)) != sFileExtension):
			sFile = sFile + sFileExtension;
		if (bRootHomeSafety):
			if ((StrLeft(sFile, 6) != '/root/') and (StrLeft(sFile, 6) != '/home/')):
				MessageBox('For your safety, this program can only save to \n/root and /home subdirectories.');
				return;
		sCmd = 'file "' + sFile + '"';
		sResult = RunBash(sCmd);
		if (StrDoesNotContain(sResult, "can't stat")):
			result = QuestionYesNoBox("Do you wish to overwrite\n'" + sFile + "' ?");
			if (result != gtk.RESPONSE_YES):
				return;
		return sFile;

def StrTrim(sInput):
	return string.strip(sInput);
				
def StrLCase(sInput):
	return string.lower(sInput);
	
def StrUCase(sInput):
	return string.upper(sInput);
									
def StrLeft(sInput, nIndex):
	return sInput[:nIndex];
	
def StrRight(sInput, nIndex):
	return sInput[(nIndex * -1):];

def StrContains(sHaystack, sNeedle):
	if (string.find(sHaystack, sNeedle) != -1):
		return TRUE;
	else:
		return FALSE;
		
def StrDoesNotContain(sHaystack, sNeedle):
	if (string.find(sHaystack, sNeedle) == -1):
		return TRUE;
	else:
		return FALSE;		
			
def ReadFile(sFile):
	sCmd = 'cat "' + sFile + '"';
	sResult = RunBash(sCmd);
	return sResult;
	
def RemoveFile(sFile):
	if (sFile == ''):
		return;
	try:
		sCmd = 'rm -f "' + sFile + '"';
		RunBash(sCmd);
	except:
		return;
	
def SaveFile(sFile, sContents):
	if (sFile == ''):
		return;
	try:
		sCmd = 'echo -en "' + sContents + '" > "' + sFile + '"';
		RunBash(sCmd);
	except:
		return;
	
def TranslateApproxFolderPath(sFolderPath):
	if ((sFolderPath[-1] == '*') or (sFolderPath[-1] == '/')):
		sFolderPath = sFolderPath[:-1];
	sCmd = 'cd ' + sFolderPath + '*; pwd | tr -d "\n"';
	sResult = RunBash(sCmd);
	return sResult;

def GetHomeDir():
	sCmd = 'cd ~; pwd | tr -d "\n"';
	sResult = RunBash(sCmd);
	return sResult + '/';

def OpenMozilla(sProtocol, sURL):
	sCmd = 'mozilla ' + sProtocol + '://' + sURL;
	SpawnBash(sCmd);		
	
def DisableWidget(sName):
	Widget(sName).set_property('sensitive',FALSE);	

def EnableWidget(sName):
	Widget(sName).set_property('sensitive',TRUE);
	
def GetUser():
	sCmd = 'whoami | tr -d "\n"';
	sResult = RunBash(sCmd);
	return sResult;
	
def RemoveMenuItems(sMenu, nAfterMenuItem):
	i = 1;
	for m in Widget(sMenu).get_children():
		if (i > nAfterMenuItem):
			Widget(sMenu).remove(m);
		i += 1;
		
def AddMenuItem(sMenu, sLabel, sName, sImage, oSignal):
	mnu = gtk.ImageMenuItem(sLabel);
	mnu.set_name(sName);
	mnu.connect('activate', oSignal);
	Widget(sMenu).add(mnu);	
	img = gtk.Image();
	img.set_from_file(sImage);
	mnu.set_image(img);	
	img.show();
	mnu.show();
	return mnu;

def AddSeparatorMenuItem(sMenu):
	mnu = gtk.SeparatorMenuItem();
	Widget(sMenu).add(mnu);
	mnu.show();	
	
def gtk_main_quit(*args):
    gtk.main_quit();

def Refresh():
    while gtk.events_pending():
        gtk.mainiteration(FALSE);

def QuitAll():
	Destroy('main');
	sCmd = 'vpnc-disconnect';
	sResult = RunBash(sCmd);
	# Destroy('run_command');
	gtk.main_quit();
	
PROGNAME = 'Bash UI';

# load our Glade2 file with the GUI
MyWindows = gtk.glade.XML('gvpnc.glade',None,domain=PROGNAME);

# g var initizialization
window = None;

# change whole app's font
Widget('main').get_settings().set_string_property('gtk-font-name', 'sans normal 9','');

# change font on the two main text fields
o = Widget('txtResult').get_buffer();
txtResultFont = o.create_tag('txtResultFont');
txtResultFont.set_property('font', 'Luxi Mono 8');

# connect our signals to our glade file object
MyWindows.signal_autoconnect(locals());


# show our main window and go into main loop
ShowWindow('main');
Widget('statusbar1').grab_focus();
sCmd = 'whoami | tr -d "\n"';
sResult = RunBash(sCmd);
if (StrDoesNotContain(sResult, 'root')):
	ErrorBox('This tool requires that it be run as root user.');
	QuitAll();
gtk.main();
