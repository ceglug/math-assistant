"""
System configuration is one of the most important issues for making this tool more convenient for users.
By handling multiple profiles, we can edit, manage and load the profiles for our system.
By giving more choices for configuration, this makes our tool dynamic and easy to use.
Also configurations can be saved and reused on other systems by means of the profile handling mechanism.

Manage profile is used to perform profile creation and removal operations.
Edit profile is used to edit the default or predefined settings and saves these settings in the configuration files.
Load profile loads the specified configuration file, and assigns the saved settings to the current math assistant object.
All these operations are based on the configuration files in current directory.


@license: Math Assistant is a free software;
You can redistribute it and/or modify it under
the terms of the GNU General Public License 
as published by the Free Software Foundation; 
@copyright: GNU General Public License version 3.0
@author: MURALI KUMAR. M
@contact: U{murali.au@gmail.com}

"""

import wx
import wx.lib.colourselect as  csel
import os
import ConfigParser
import sys

class loadconf(wx.Panel):
    """
    This class is used to load selected profile and applies the settings in the profiles 
    to the current math assistant object through callbacks.  
    """
    def __init__(self, parent,profiles,frame,mathob):
        """
        Constructor method for this class.
        This method shows the dialog when mathob.loaddefault variable is None.
        else it loads the specified profile.
        
        @param parent    : Parent class of the object
        @param profiles  : profiles list in current directory
        @param frame     : MainFrame class object
        @param mathob    : MathAssistant class object

        """

        wx.Panel.__init__(self, parent)
        
        self.mathob = mathob                            #: MathAssistant class instance
        self.frame = frame                              #: MainFrame class instance
        self.profile = None                             #: current profile
        self.config = ConfigParser.RawConfigParser()    #: configParser instance variable


        #t = wx.StaticText(self, -1, "This is a PageOne object", (20,20))
        #for files in os.listdir(os.getcwd()):
        #    for name in files:       
        #        if os.path.splitext(name)[1] == ext:
        #            print name 
        if (mathob.loaddefault is None or mathob.loaddefault == ''):
            vbox = wx.BoxSizer(wx.VERTICAL)
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            
            self.cbtext = wx.StaticText(self, -1 , " Select a profile ")
            self.cb = wx.ComboBox(self, -1 , size =(150, -1) , choices = profiles , style = wx.CB_READONLY)
            self.load = wx.Button(self , 1 , ' LOAD ')
            self.cancel = wx.Button(self, 2, ' CLOSE ')

            vbox.Add(self.cbtext ,0, wx.TOP|wx.ALIGN_CENTER , 50)
            vbox.Add(self.cb ,0,wx.ALL|wx.ALIGN_CENTER , 10)
            hbox.Add(self.load ,0,wx.RIGHT,10) 
            hbox.Add(self.cancel ,0) 
            vbox.Add(hbox,0,wx.ALL|wx.ALIGN_CENTRE,30)
            
            self.load.Enable(False)
            self.Bind(wx.EVT_BUTTON, self.Onload, id=1)
            self.Bind(wx.EVT_BUTTON, self.Oncancel, id=2)
            self.Bind(wx.EVT_COMBOBOX, self.OnSelect , self.cb)

            self.SetSizerAndFit(vbox)
            self.Centre()
            self.Show(True)
        else:
            self.profile = self.mathob.loaddefault
            self.loadprofile()
            self.Close()

    def Onload(self, event):
        """
        This method Loads a profile when LOAD button is clicked
        """
        if (self.profile != ''):
            self.load.Enable(False)
            self.loadprofile()
           # self.mathob.Enable(True)
            self.frame.Close()
        else:
            pass

    def Oncancel(self, event):
        """
        This method closes the LoadProfile notebook dialog
        """

       # self.mathob.Enable(True)
        self.frame.Close()

    def OnSelect(self, event):
        """
        Event handler function for the list control in this dialog
        It stores the selected profile in profile variable to load
        """

        self.profile = event.GetString()
        self.load.Enable(True)
        print 'profile',self.profile

    def loadprofile(self):
        """
        This method is called by OnLoad event handler
        It is used to read and apply the configuration settings stored in the profile
        to the current MathAssistant class object.
        """
        self.config.read(self.profile)

        self.blist1 = self.config.get('dict' , 'butlist1')
        self.blist1 = eval(self.blist1)
        self.blist2 = self.config.get('dict' , 'butlist2')
        self.blist2 = eval(self.blist2)
        self.blist3 = self.config.get('dict' , 'butlist3')
        self.blist3 = eval(self.blist3)
                
        self.mathob.soundflag = self.config.getboolean('options' ,'sound')
        self.Bclick     = self.config.getboolean('options' ,'bclick')
        self.Lclick     = self.config.getboolean('options' ,'lclick')
        self.Showgrid   = self.config.getboolean('options' ,'showgrid')
        self.Sbar       = self.config.getboolean('options' ,'sbar')
        self.Mbspeed    = int(self.config.get('settings' ,'mbspeed'))
        self.Mispeed    = int(self.config.get('settings' ,'mipeed'))
        self.Zoomlevel  = int(self.config.get('settings' ,'zoomlevel'))
        self.paneltype  = self.config.get('settings' ,'Paneltype')
        self.panelnos   = self.config.get('settings' ,'Panelnos')
        self.Bpcolor    = self.config.get('color' ,'bpcolor')
        self.Hlcolor    = self.config.get('color' ,'hlcolor')
        
        for i in range(12):
            self.mathob.butList1[i].SetLabel(self.blist1[i])
            self.mathob.butList2[i].SetLabel(self.blist2[i])
            self.mathob.butList3[i].SetLabel(self.blist3[i])
            
        self.mathob.chkbc.Check(self.Bclick)
        self.mathob.Onchkbc(None)

        self.mathob.chklc.Check(self.Lclick)
        self.mathob.Onchklc(None)

        self.mathob.chksb.Check(self.Sbar)
        self.mathob.Onchksb(None)

        self.mathob.paneltype = self.paneltype
        self.mathob.panelnos  = self.panelnos

        self.mathob.menuspeed = self.Mbspeed * 1000
        self.mathob.butspeed  = self.Mispeed * 1000
        
        self.mathob.setpanelbgcolor(eval(self.Bpcolor))
        self.mathob.sethighlightcolor(eval(self.Hlcolor))

        if(self.Showgrid):
            self.mathob.grid.EnableGridLines(True)
        else:
            self.mathob.grid.EnableGridLines(False)
        
        self.mathob.makechoicepanel2()

            
class MainFrame(wx.Frame):
    """
    This class used to show the notebook dialog for LoadProfile  
    """
    def __init__(self,mathob):
        """
        Constructor method for this class.
        Finds configuration files in current directory and invokes loadconf class

        @param mathob    : MathAssistant class object
        """

        wx.Frame.__init__(self,mathob, title="Profile Settings")

        if (mathob.loaddefault is None or mathob.loaddefault == ''):
            p = wx.Panel(self, -1)
            nb = wx.Notebook(p,-1, style=wx.BK_DEFAULT)

            self.profiles = []          #: profiles list in current directory
            ext = '.cfg'
            for root, dirs, files in os.walk('./'):
                for name in files:       
                    filename = os.path.join(root, name)
                    if os.path.splitext(filename)[1] == ext:
                        self.profiles.append(name)
                        #print name
            
            self.load = loadconf(nb ,self.profiles,self,mathob)
            nb.AddPage(self.load, "Load Profile")
            
            sizer = wx.BoxSizer()
            sizer.Add(nb, 1, wx.EXPAND)
            p.SetSizer(sizer)
           # mathob.Enable(False)
           # self.MakeModal()
            self.Center()
            self.Show()
        else:
            self.load = loadconf(self,None,self,mathob)
            self.Close()
            