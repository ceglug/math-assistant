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

class manageconf(wx.Panel):
    """
    This class is used to perform profile creation and removal operations.
    when a profile is created it is added with default settings.
    """

    def __init__(self, parent,profiles,frame):
        """
        Constructor method for this class.
        
        @param parent    : Parent class of the object
        @param profiles  : profiles list in current directory
        @param frame     : MainFrame class object

        """
        wx.Panel.__init__(self, parent)

        self.config = ConfigParser.RawConfigParser()    #: ConfigParser class instance
        self.config.add_section('dict')
        self.config.add_section('options')
        self.config.add_section('settings')
        self.config.add_section('color')

        self.profile = None             #: current profile name
        self.remindex = None            #: index no for the profile to remove in the list
        self.remlabel = None            #: profile name to remove in the list
        self.frame = frame              #: MainFrame class object
        
        #t = wx.StaticText(self, -1, "This is a PageTwo object", (40,40))
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.rmtext = wx.StaticText(self, -1 , " Select a profile to Remove ")
        self.crtext = wx.StaticText(self, -1 , " Type a profile name to Create(without .ext) ")
        self.tc = wx.TextCtrl(self, -1, size=(125, -1) )
        self.lc = wx.ListBox(self,10,(-1, -1),(170, 130),choices = profiles,style=wx.LB_SINGLE)
        self.add = wx.Button(self , 1 , ' ADD ')
        self.remove = wx.Button(self , 2 , ' REMOVE ')
        self.cancel = wx.Button(self, 3, ' CLOSE ')
        self.line = wx.StaticLine(self)
        self.tc.SetFocus()
    
        vbox.Add(self.crtext ,0, wx.TOP|wx.ALIGN_CENTER , 30)
        hbox1.Add(self.tc ,0,wx.RIGHT,10)
        hbox1.Add(self.add ,0)
        vbox.Add(hbox1,0,wx.ALL|wx.ALIGN_CENTRE,20)
        vbox.Add(self.line,0,wx.TOP|wx.EXPAND,10)
        vbox.Add(self.rmtext ,0, wx.TOP|wx.ALIGN_CENTER , 30)
        vbox.Add(self.lc , 0 ,wx.ALL|wx.ALIGN_CENTER , 20)
        hbox2.Add(self.remove ,0,wx.RIGHT,10) 
        hbox2.Add(self.cancel ,0) 
        vbox.Add(hbox2,0,wx.ALL|wx.ALIGN_CENTER , 30)
        
        self.add.Enable(False)
        self.lc.SetSelection(0)
        self.Bind(wx.EVT_TEXT, self.Ontext,self.tc)
        self.Bind(wx.EVT_BUTTON, self.Onadd, id=1)
        self.Bind(wx.EVT_BUTTON, self.Onremove, id=2)
        self.Bind(wx.EVT_BUTTON, self.Oncancel, id=3)
        self.Bind(wx.EVT_LISTBOX, self.Onlistselect ,self.lc)
        
        self.SetSizerAndFit(vbox)
        self.Centre()
        self.Show(True)
    
    def Onadd(self, event):
        """
        This method adds a new profile when clicked ADD button
        """
        self.profile = self.tc.GetValue() + '.cfg'
        self.defaultprofilecreate()
        try:
            with open(self.profile, 'wb') as configfile:
                self.config.write(configfile)
            self.lc.Append(self.profile)
            self.add.Enable(False)
            self.tc.SetValue('')
        except:
            print 'File creation error..Try again!'
            pass

    def Onremove(self, event):
        """
        This method removes an existing profile when clicked REMOVE button
        """

        if( self.remindex is None or self.remlabel is None or self.remlabel == '' ):
            pass
        else:
            self.removeconfigfile()
            self.lc.Delete(self.remindex)
  
    def Oncancel(self, event):
        """
        This method closes the ManageProfile notebook dialog
        """
        self.frame.Close()
    
    def Ontext(self,event):
        """
        Event handler function for the textcontrol used in this dialog
        enable/disables add button when a name is provided or not.
        """
        i = len(event.GetString())
        if(i > 0 ):
            self.add.Enable(True)
        else:
            self.add.Enable(False)

    def Onlistselect(self, event):
        """
        Event handler function for the list contorl
        stores the name of the profile to remove when selected an item
        """
        self.remindex = event.GetSelection()
        self.remlabel = event.GetString()

    def removeconfigfile(self):
        """
        This method removes a profile stored in remlabel variable on current directory
        """
        try:
            fname = os.path.join(os.curdir,self.remlabel)
            os.remove(fname)
            #print 'remove file name',fname
            
        except:
            print 'File remove error..Try again!'
            pass
        

    def defaultprofilecreate(self):
        """
        This method creates new profile settings on config variable
        """
        self.butList1 = range(12)       #: Menugroup 1
        self.butList2 = range(12)       #: Menugroup 2
        self.butList3 = range(12)       #: Menugroup 3

        self.butList1[0] = '9'
        self.butList1[1] = '8'
        self.butList1[2] = '7'
        self.butList1[3] = '6'
        self.butList1[4] = '5'
        self.butList1[5] = '4'
        self.butList1[6] = '3'
        self.butList1[7] = '2'
        self.butList1[8] = '1'
        self.butList1[9] = '0'
        self.butList1[10] = '<---'
        self.butList1[11] = 'NEXT'

        self.butList2[0] = ' + '
        self.butList2[1] = ' -- '
        self.butList2[2] = ' * '
        self.butList2[3] = ' / '
        self.butList2[4] = ' = '
        self.butList2[5] = 'NEXT'
        self.butList2[6] = 'PREV'
        self.butList2[7] = 'UP'
        self.butList2[8] = 'NEXTT'
        self.butList2[9] = 'LEFT'
        self.butList2[10] = 'DOWN'
        self.butList2[11] = 'RIGHT'
                
        self.butList3[0] = 'DIV'
        self.butList3[1] = 'LCM'
        self.butList3[2] = 'BY'
        self.butList3[3] = 'CROSS'
        self.butList3[4] = 'DOT'
        self.butList3[5] = 'DEL'
        self.butList3[6] = ' ( '
        self.butList3[7] = ' ) '
        self.butList3[8] = ' , '
        self.butList3[9] = ' | '
        self.butList3[10] = ' % '
        self.butList3[11] = 'NEXT'

        self.Sound = False              #: sound option
        self.Bclick = True              #: Button click option
        self.Lclick = True              #: Left click option
        self.Showgrid = False           #: show gridlines option
        self.Sbar = True                #: show statusbar option
        self.Mbspeed = 5                #: Menubox speed option
        self.Mispeed = 2                #: Menuitem speed option
        self.Zoomlevel = 2              #: Zoom level option
        self.paneltype = 'VERTICAL'     #: Paneltype option
        self.panelnos  = '3'            #: Panel nos option
        self.Bpcolor =   (128, 255, 255, 255)   #: Background panel color option
        self.Hlcolor =   (255, 0, 0, 255)       #: Highlighting color option
                
        self.config.set('dict' ,'butlist1',repr(self.butList1))
        self.config.set('dict' ,'butlist2',repr(self.butList2))
        self.config.set('dict' ,'butlist3',repr(self.butList3))

        self.config.set('options' ,'sound',self.Sound)
        self.config.set('options' ,'bclick',self.Bclick)
        self.config.set('options' ,'lclick',self.Lclick)
        self.config.set('options' ,'showgrid',self.Showgrid)
        self.config.set('options' ,'sbar',self.Sbar)
        
        self.config.set('settings' ,'mbspeed',self.Mbspeed)
        self.config.set('settings' ,'mipeed',self.Mispeed)
        self.config.set('settings' ,'zoomlevel',self.Zoomlevel)
        self.config.set('settings' ,'Paneltype',self.paneltype)
        self.config.set('settings' ,'Panelnos',self.panelnos)

        self.config.set('color' ,'bpcolor',repr(self.Bpcolor))
        self.config.set('color' ,'hlcolor',repr(self.Hlcolor))

    
class MainFrame(wx.Frame):
    """
    This class used to show the notebook dialog for ManageProfile  
    """
    def __init__(self):
        """
        Constructor method for this class.
        Finds configuration files in current directory and invokes manageconf class
        """
        wx.Frame.__init__(self, None, title="Profile Settings")

        p = wx.Panel(self, -1)                      #: main panel instance
        nb = wx.Notebook(p,-1, style=wx.BK_DEFAULT) #: notebook instance

        self.profiles = []              #: profiles list (.cfg files) in current directory
        ext = '.cfg'
        for root, dirs, files in os.walk('./'):
            for name in files:       
                filename = os.path.join(root, name)
                if os.path.splitext(filename)[1] == ext:
                    self.profiles.append(name)
                    #print name
        
        self.manage = manageconf(nb ,self.profiles,self)
        nb.AddPage(self.manage, "Manage Profile")
        
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
        self.Center()
        self.Show()