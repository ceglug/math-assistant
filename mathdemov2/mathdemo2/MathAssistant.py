"""
Math Assistant is a Comprehensive tool for speacially enabled children, 
providing a Math Worksheet Environment for easy way of solving simple Math problems.

This module mainly handles,
    - GUI design
    - Event handling 
parts in the math worksheet tool.

@license: Math Assistant is a free software;
You can redistribute it and/or modify it under
the terms of the GNU General Public License 
as published by the Free Software Foundation; 
@copyright: GNU General Public License version 3.0
@author: MURALI KUMAR. M
@contact: U{murali.au@gmail.com}

speech.py is a GNU licensed third party module for python speech API calls. 
You must agree it to use this module in this application.

"""

import wx
import wx.grid
import os
import string
import celleditor as cell
import cellrenderer as render
import loadprofile as loadpf
import manageprofile as managepf
import editprofile as editpf
import wx.lib.evtmgr as em
import wx.lib.inspection
#import speech
import sys
import time

class mathassist(wx.Frame):
    """
    This math assist class used as the main class of the project.
    This class defines GUI design and Event Handling of this tool. 
    """
    def __init__(self, parent, id, title):
        """
        Creates a math assistant object to workout math problems.
        @param parent: Parent class of the object
        @param id    : Instance id of the object
        @param title : Title of the object.
        
        """

        wx.Frame.__init__(self, parent, id, title,size = wx.DisplaySize())
        self.panel = wx.Panel(self, -1) #: main panel instance
      
        menubar = wx.MenuBar()  #: menubar instance
        file = wx.Menu()
        file.Append(11, '&New')
        file.Append(12, '&Open')
        file.Append(13, '&Save')
        file.AppendSeparator()
        file.Append(14, 'E&xit\tCtrl+X')

        config = wx.Menu()
        self.chkps = config.Append(21, 'PlaySound', 'PlaySound', kind=wx.ITEM_CHECK)
        self.chkbc = config.Append(22, 'ButtonClick', 'ButtonClick', kind=wx.ITEM_CHECK)
        self.chklc = config.Append(23, 'LeftClick', 'LeftClick', kind=wx.ITEM_CHECK)
        self.chkhl = config.Append(24, 'Futureuse', 'Futureuse', kind=wx.ITEM_CHECK)
        self.chksb = config.Append(25, 'Show Statusbar', 'Show Statusbar', kind=wx.ITEM_CHECK)
        config.AppendSeparator()
        self.sp    = config.Append(26, 'Speech Input','Speech Input',kind=wx.ITEM_CHECK)
        config.AppendSeparator()
        config.Append(27, '&ClearAll \tCtrl+C')
        config.Check(21, False)
        config.Check(22, True)
        config.Check(23, True)
        config.Check(24, False)
        config.Check(25, True)

        view = wx.Menu()
        view.Append(31, 'Zoom &In\tCtrl++')
        view.Append(32, 'Zoom &Out\tCtrl+-')
        view.AppendSeparator()
        view.Append(33, '&Menu Speed++')
        view.Append(34, 'M&enu Speed--')
        view.AppendSeparator()
        view.Append(35, 'Menu&Item Speed++')
        view.Append(36, 'MenuI&tem Speed--')

        settings = wx.Menu()
        settings.Append(41, '&Load Profile\tCtrl+L')
        settings.Append(42, '&Manage Profile\tCtrl+M')
        settings.AppendSeparator()
        settings.Append(43, '&Edit Profile\tCtrl+E')
        
        help = wx.Menu()
        help.Append(51, '&Manual..')
        help.AppendSeparator()
        help.Append(52, '&About..')

        menubar.Append(file, '&File')
        menubar.Append(config, '&Config')
        menubar.Append(view, '&View')
        menubar.Append(settings, '&Profile Settings')
        menubar.Append(help, '&Help')

        # Menu items event handler bindings
        self.Bind(wx.EVT_MENU, self.OnNew, id=11)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=12)
        self.Bind(wx.EVT_MENU, self.OnSave, id=13)
        self.Bind(wx.EVT_MENU, self.OnExit, id=14)
        
        self.Bind(wx.EVT_MENU, self.Onchkps, id=21)
        self.Bind(wx.EVT_MENU, self.Onchkbc, id=22)
        self.Bind(wx.EVT_MENU, self.Onchklc, id=23)
        self.Bind(wx.EVT_MENU, self.Onchkhl, id=24)
        self.Bind(wx.EVT_MENU, self.Onchksb, id=25)
        self.Bind(wx.EVT_MENU, self.Onconfig, id=26)
        self.Bind(wx.EVT_MENU, self.Onclear, id=27)
        
        self.Bind(wx.EVT_MENU, self.OnZoomin, id=31)
        self.Bind(wx.EVT_MENU, self.OnZoomout, id=32)
        self.Bind(wx.EVT_MENU, self.OnMenuinc, id=33)
        self.Bind(wx.EVT_MENU, self.OnMenudec, id=34)
        self.Bind(wx.EVT_MENU, self.OnMenuiteminc, id=35)
        self.Bind(wx.EVT_MENU, self.OnMenuitemdec, id=36)

        self.Bind(wx.EVT_MENU, self.OnLoadprofile, id=41)
        self.Bind(wx.EVT_MENU, self.OnManageprofile, id=42)
        self.Bind(wx.EVT_MENU, self.OnEditprofile, id=43)
        
        self.Bind(wx.EVT_MENU, self.OnManual, id=51)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=52)

        self.SetMenuBar(menubar)
        
        # Defines font properties 
        self.font=wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT) #: font used for math problems
        self.font.SetPointSize(15)
        self.font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.font.SetFamily(wx.FONTFAMILY_DEFAULT)
        
        
        self.timer=wx.Timer(self)       #: timer instance
        self.soundflag = False          #: To determine whether to play sound or not
        self.sound = None               #: sound object
        self.cellsize = 26              #: Cell size of the grid control
        self.pointsize = 15             #: Point size of the grid control
        self.menuspeed=5000             #: Contains Menu group speed
        self.butspeed=2000              #: Contains Menuitem speed
        self.menubox=-1                 #: To hold current highlighted Menu group
        self.menuboxitem=False          #: To determine whether to highlight the Menu group or Menu items 
        self.buttonid = -1              #: To hold current highlighted button id
        self.butlabel = ''              #: To hold current highlighted button label
        self.topx = 0                   #: top left X-axis position to highlight
        self.topy = 0                   #: top left Y-axis position to highlight
        self.width = 0                  #: width of the window to highlight
        self.height = 0                 #: height of the window to highlight
        self.curcol = 0                 #: Current column of the grid cursor
        self.currow = 0                 #: Current row of the grid cursor
        self.moveflag = True            #: To determine whether retain highlight or not when clicked move buttons
        self.moveid = 5                 #: where To retain highlight when clicked move buttons
        self.hlcolor = wx.RED           #: Highlighting colour
        self.paneltype = 'HORIZONTAL'   #: To hold Panel group type horizontal/vertical
        self.panelnos = '3'             #: To hold No.of panels
        #self.loaddefault = 'default.cfg'       
        self.loaddefault = ''           #: Future- To load default profile
       # self.bpcolor = wx.NullColor
                
        self.vbox = wx.BoxSizer(wx.VERTICAL)     
        
        self.panel1 = wx.Panel(self.panel,-1)   #: grid panel instance
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        wd,ht = wx.DisplaySize()                #: widht and height setting for grid panel
        ht = int((ht * 2)/3) - 80               #: height setting as 2/3 in screen size
        self.grid = wx.grid.Grid(self.panel1,size=(wd,ht))      #: grid instance
        self.grid.CreateGrid(30,50)
        self.grid.SetDefaultRowSize(self.cellsize)
        self.grid.SetDefaultColSize(self.cellsize)
        #grid.SetGridLineColour(wx.WHITE)
        self.grid.EnableGridLines(False)
        self.grid.DisableDragGridSize()
        self.grid.SetRowLabelSize(0)
        self.grid.SetColLabelSize(0)
        
        self.editor=cell.myCellEditor()         #: sets the default custom editor
        self.grid.SetDefaultEditor(self.editor)

        self.grid.SetDefaultCellFont(self.font)  #(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        
       # attr = wx.grid.GridCellAttr()
        #attr.SetRenderer(render.myRenderer())
       # self.grid.SetCellRenderer(2,2,render.mycellrenderer())
       # grid.SetRowAttr(4, attr)
       # for row in range(10):
       #     for col in range(10):
        #       self.grid.SetCellValue(row, col,"c")

        
        #print self.grid.GetDefaultCellAlignment()
           
        print self.grid.GetFont()
        self.sbox1 = wx.StaticBoxSizer(wx.StaticBox(self.panel1, -1, 'WORKSHEET'), orient=wx.VERTICAL)
        self.sbox1.Add(self.grid, 1, wx.ALL|wx.EXPAND , 0)
        vbox1.Add(self.sbox1, 1, wx.EXPAND)
        self.panel1.SetSizer(vbox1)      
        self.vbox.Add(self.panel1, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER | wx.EXPAND, 9)
        
        line = wx.StaticLine(self.panel)
        self.vbox.Add(line, 0, wx.EXPAND)
        
        self.makepanel2()               # To create button panel
        
        """em.eventManager.Register(self.OnChangeCursor , wx.EVT_TIMER , self)
        em.eventManager.Register(self.OnMenuPaint , wx.EVT_PAINT , self.panel2)
        em.eventManager.Register(self.OnLeftClick , wx.EVT_LEFT_DOWN , self.panel1)
        em.eventManager.Register(self.OnLeftClick , wx.EVT_LEFT_DOWN , self.panel2)
        em.eventManager.Register(self.OnLeftClick , wx.EVT_LEFT_DOWN , self.panel)"""

        # Event handler binding
        self.timerevt = self.Bind(wx.EVT_TIMER,self.OnChangeCursor)     #: timer event instance
        self.paintevt = self.panel2.Bind(wx.EVT_PAINT,self.OnMenuPaint) #: paint event instance
        self.lcp1 = self.panel1.Bind(wx.EVT_LEFT_DOWN , self.OnLeftClick) #: Mouse left click Event in panel1
        self.lcp2 = self.panel2.Bind(wx.EVT_LEFT_DOWN , self.OnLeftClick) #: Mouse left click Event in panel2
        self.lcp =  self.panel.Bind(wx.EVT_LEFT_DOWN , self.OnLeftClick)  #: Mouse left click Event in panel
        #self.dcp = wx.EVT_LEFT_DCLICK(self.panel, self.OnLeftDclick) # double click event..
        self.grid.SetFocus()
        
        
        self.vbox.Fit(self)
        self.panel.SetSizerAndFit(self.vbox)
        self.statusbar = self.CreateStatusBar() #: status bar instance
        self.Centre()
        self.ShowFullScreen(True ,wx.FULLSCREEN_NOTOOLBAR)
        self.Show(True)
        self.OnChangeCursor(self)               # timer event handler
        self.grid.SetGridCursor(4,4)
        #self.loaddefaultprofile()              # Future- To load default profile (some bug here..)
   #---------------------------------------------------------------------------- 
    def makepanel2(self):
        """
        Creates the default button panel and binds the event handlers
        """
        if(self.paneltype == 'VERTICAL'):       
            self.grsize = 4                     #: Menugroup gridsizer row size
            self.gcsize = 3                     #: Menugroup gridsizer column size
            self.bwsize = 100                   #: Menuitem Button width
            self.bhsize = 40                    #: Menuitem Button height
        elif(self.paneltype == 'HORIZONTAL'):
            self.grsize = 1
            self.gcsize = 12
            self.bwsize = 85
            self.bhsize = 40
        else:
            pass

        self.panel2 = wx.Panel(self.panel,-1)   #: button panel instance 
                
        self.butList1=range(12)                 #: Menugroup 1
        self.butList2=range(12)                 #: Menugroup 2
        self.butList3=range(12)                 #: Menugroup 3
                    
        self.gbox1 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        
        for i in range(12):
            self.butList1[i]=wx.Button(self.panel2,i,'',size=(self.bwsize,self.bhsize))
            self.butList1[i].SetFont(self.font)
            self.butList1[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)
            self.gbox1.Add(self.butList1[i],0,wx.ALL|wx.EXPAND)
        
        self.butList1[0].SetLabel('9')
        self.butList1[1].SetLabel('8')
        self.butList1[2].SetLabel('7')
        self.butList1[3].SetLabel('6')
        self.butList1[4].SetLabel('5')
        self.butList1[5].SetLabel('4')
        self.butList1[6].SetLabel('3')
        self.butList1[7].SetLabel('2')
        self.butList1[8].SetLabel('1')
        self.butList1[9].SetLabel('0')
        self.butList1[10].SetLabel('<---')
        self.butList1[11].SetLabel('NEXT')
       
        #self.butList1[10].Enable(False)

        self.gbox2 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        
        for i in range(12):
            self.butList2[i]=wx.Button(self.panel2,i+12,'',size=(self.bwsize,self.bhsize))
            self.butList2[i].SetFont(self.font)
            self.butList2[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)                  
            self.gbox2.Add(self.butList2[i],0,wx.ALL|wx.EXPAND)
            
        self.butList2[0].SetLabel(' + ')
        self.butList2[1].SetLabel(' -- ')
        self.butList2[2].SetLabel(' * ')
        self.butList2[3].SetLabel(' / ')
        self.butList2[4].SetLabel(' = ')
        self.butList2[5].SetLabel('NEXT')
        self.butList2[6].SetLabel('PREV')
        self.butList2[7].SetLabel('UP')
        self.butList2[8].SetLabel('NEXTT')
        self.butList2[9].SetLabel('LEFT')
        self.butList2[10].SetLabel('DOWN')
        self.butList2[11].SetLabel('RIGHT')
        
        #self.butList2[6].Enable(False)
        #self.butList2[8].Enable(False)
                
        self.gbox3 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)

        for i in range(12):
            self.butList3[i]=wx.Button(self.panel2,i+24,'',size=(self.bwsize,self.bhsize))
            self.butList3[i].SetFont(self.font)
            self.butList3[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)
            self.gbox3.Add(self.butList3[i],0,wx.ALL|wx.EXPAND)
            
        self.butList3[0].SetLabel('DIV')
        self.butList3[1].SetLabel('LCM')
        self.butList3[2].SetLabel('BY')
        self.butList3[3].SetLabel('CROSS')
        self.butList3[4].SetLabel('DOT')
        self.butList3[5].SetLabel('DEL')
        self.butList3[6].SetLabel(' ( ')
        self.butList3[7].SetLabel(' ) ')
        self.butList3[8].SetLabel(',')
        self.butList3[9].SetLabel(' | ')
        self.butList3[10].SetLabel('%')
        self.butList3[11].SetLabel('NEXT')
        
        if(self.paneltype == 'VERTICAL'):
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(self.gbox1,1,wx.ALL|wx.EXPAND,10)    
            hbox.Add(self.gbox2,1,wx.ALL|wx.EXPAND,10)    
            hbox.Add(self.gbox3,1,wx.ALL|wx.EXPAND,10)    

            self.panel2.SetSizer(hbox)  
        elif(self.paneltype == 'HORIZONTAL'):
            vertbox = wx.BoxSizer(wx.VERTICAL)
            vertbox.Add(self.gbox1,1,wx.ALL|wx.EXPAND,10)    
            vertbox.Add(self.gbox2,1,wx.ALL|wx.EXPAND,10)    
            vertbox.Add(self.gbox3,1,wx.ALL|wx.EXPAND,10)    

            self.panel2.SetSizer(vertbox)  
        else:
            pass

        #self.vbox.Detach(self.panel2)
        self.vbox.Add(self.panel2, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER, 9)

    def makechoicepanel2(self):
        """
        Recreates the button panel when loading a profile
        Mainly it depends two choices.
            1. Paneltype (horizontal/vertical)
            2. No.of panels (1,2,3)
        """
        print 'choicepanel2'
        if(self.paneltype == 'VERTICAL'):
            self.grsize = 4
            self.gcsize = 3
            self.bwsize = 100
            self.bhsize = 40
        elif(self.paneltype == 'HORIZONTAL'):
            self.grsize = 1
            self.gcsize = 12
            self.bwsize = 85
            self.bhsize = 40
        else:
            pass

        #self.panel2 = wx.Panel(self.panel,-1)

        self.gbox1 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        self.gbox2 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        self.gbox3 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox2 = wx.BoxSizer(wx.VERTICAL)


        for i in range(12):
            self.butList1[i].SetSize(wx.Size(self.bwsize,self.bhsize))
            self.butList2[i].SetSize(wx.Size(self.bwsize,self.bhsize))
            self.butList3[i].SetSize(wx.Size(self.bwsize,self.bhsize))

            self.gbox1.Add(self.butList1[i],0,wx.ALL|wx.EXPAND)
            self.gbox2.Add(self.butList2[i],0,wx.ALL|wx.EXPAND)
            self.gbox3.Add(self.butList3[i],0,wx.ALL|wx.EXPAND)
    
        if(self.paneltype == 'VERTICAL'):
            self.hbox2.Add(self.gbox1, 1, wx.ALL|wx.EXPAND,10)
            self.hbox2.Add(self.gbox2, 1, wx.ALL|wx.EXPAND,10)
            self.hbox2.Add(self.gbox3, 1, wx.ALL|wx.EXPAND,10)
        elif(self.paneltype == 'HORIZONTAL'):
            self.vbox2.Add(self.gbox1, 1, wx.ALL|wx.EXPAND,10)
            self.vbox2.Add(self.gbox2, 1, wx.ALL|wx.EXPAND,10)
            self.vbox2.Add(self.gbox3, 1, wx.ALL|wx.EXPAND,10)
        else:
            pass
            
        self.panel2.Layout()
        self.panel.Layout()
        self.panel2.Refresh()
        self.Refresh()
        
        if(self.panelnos == '3'):
            if(self.paneltype == 'VERTICAL'):
                self.hbox2.Show(self.gbox1,True)
                self.hbox2.Show(self.gbox2,True)
                self.hbox2.Show(self.gbox3,True)
                
            elif(self.paneltype == 'HORIZONTAL'):
                self.vbox2.Show(self.gbox1,True)
                self.vbox2.Show(self.gbox2,True)
                self.vbox2.Show(self.gbox3,True)
                
        elif(self.panelnos == '2'):
            if(self.paneltype == 'VERTICAL'):
                self.hbox2.Show(self.gbox1,True)
                self.hbox2.Show(self.gbox2,True)
                self.hbox2.Show(self.gbox3,False)
                
            elif(self.paneltype == 'HORIZONTAL'):
                self.vbox2.Show(self.gbox1,True)
                self.vbox2.Show(self.gbox2,True)
                self.vbox2.Show(self.gbox3,False)

        elif(self.panelnos == '1'):
            if(self.paneltype == 'VERTICAL'):
                self.hbox2.Show(self.gbox1,True)
                self.hbox2.Show(self.gbox2,False)
                self.hbox2.Show(self.gbox3,False)
                
            elif(self.paneltype == 'HORIZONTAL'):
                self.vbox2.Show(self.gbox1,True)
                self.vbox2.Show(self.gbox2,False)
                self.vbox2.Show(self.gbox3,False)

        if(self.paneltype == 'VERTICAL'):
            self.panel2.SetSizerAndFit(self.hbox2,True)  
            self.vbox.Detach(self.panel2)
            self.vbox.Add(self.panel2, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER, 9)
            #self.vbox.Add(self.panel2, 1, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER | wx.EXPAND, 9)

        elif(self.paneltype == 'HORIZONTAL'):
            self.panel2.SetSizerAndFit(self.vbox2,True)  
            self.vbox.Detach(self.panel2)
            self.vbox.Add(self.panel2, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER | wx.EXPAND, 9)
            #self.vbox.Add(self.panel2, 1, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER | wx.EXPAND, 9)

        else:
            pass

        self.panel2.Layout()
        self.panel.Layout()
        self.panel2.Refresh()
        self.Refresh()

#------------------------------------------------------------------------------------------
        
    def OnExit(self, event):
        """
        Exit menu handler or keyboard shortcut Ctrl+X
        Exits from application .
        """
        self.Close()

    def OnNew(self, event):
        """
        Future impl
        """
        pass
    
    def OnOpen(self, event):
        """
        Future impl
        """
        pass
    
    def OnSave(self, event):
        """
        Future impl
        """
        pass

    def Onchkps(self, event):
        """
        Soundplay menu handler.
        Sets the soundflag when enable/disable menu
        """
        if self.chkps.IsChecked():
            self.soundflag = True
        else:
            self.soundflag = False
       # print 'sound', self.soundflag
        
    def Onchkbc(self, event):
        """
        Buttonclick menu handler.
            1. Disable: Disables the button click event and it redirects as leftclick event if Leftclick option is enabled.
            2. Enable : Enables the button click event.
        """
        if self.chkbc.IsChecked():
            for i in range(12):
                self.butList1[i].Unbind(wx.EVT_BUTTON)
                self.butList2[i].Unbind(wx.EVT_BUTTON)
                self.butList3[i].Unbind(wx.EVT_BUTTON)
            for i in range(12):
                self.butList1[i].Bind(wx.EVT_BUTTON, self.OnButtonClick)
                self.butList2[i].Bind(wx.EVT_BUTTON, self.OnButtonClick)
                self.butList3[i].Bind(wx.EVT_BUTTON, self.OnButtonClick)
        else:
            for i in range(12):
                self.butList1[i].Unbind(wx.EVT_BUTTON)
                self.butList2[i].Unbind(wx.EVT_BUTTON)
                self.butList3[i].Unbind(wx.EVT_BUTTON)
            for i in range(12):
                self.butList1[i].Bind(wx.EVT_BUTTON, self.OnButtontoleftclick)
                self.butList2[i].Bind(wx.EVT_BUTTON, self.OnButtontoleftclick)
                self.butList3[i].Bind(wx.EVT_BUTTON, self.OnButtontoleftclick)

    def Onchklc(self, event):
        """
        Leftclick menu handler.
            1. Disable: Disables the left click event and stops highlighting and soundplay.
            2. Enable : Enables the left click event and starts highlighting and soundplay.
        """
        if self.chklc.IsChecked():
            """em.eventManager.Register(self.OnChangeCursor , wx.EVT_TIMER , self)
            em.eventManager.Register(self.OnMenuPaint , wx.EVT_PAINT , self.panel2)
            em.eventManager.Register(self.OnLeftClick , wx.EVT_LEFT_DOWN , self.panel1)
            em.eventManager.Register(self.OnLeftClick , wx.EVT_LEFT_DOWN , self.panel2)
            em.eventManager.Register(self.OnLeftClick , wx.EVT_LEFT_DOWN , self.panel)
            """
            self.timerevt = self.Bind(wx.EVT_TIMER,self.OnChangeCursor)
            self.paintevt = self.panel2.Bind(wx.EVT_PAINT,self.OnMenuPaint)
            self.lcp1 = self.panel1.Bind(wx.EVT_LEFT_DOWN , self.OnLeftClick) # Mouse Event
            self.lcp2 = self.panel2.Bind(wx.EVT_LEFT_DOWN , self.OnLeftClick) # Mouse Event
            self.lcp =  self.panel.Bind(wx.EVT_LEFT_DOWN , self.OnLeftClick)  # Mouse Event
            self.OnChangeCursor(self)
            self.grid.SetFocus()
        else:
            self.timer.Stop()
            """em.eventManager.DeregisterListener(self.OnChangeCursor)
            em.eventManager.DeregisterListener(self.OnMenuPaint)
            em.eventManager.DeregisterListener(self.OnLeftClick)
            """
            if self.Disconnect(-1,-1, wx.wxEVT_TIMER): print 'timer unbinded'
            if self.panel2.Disconnect(-1,-1, wx.wxEVT_PAINT): print 'paint unbinded'
            if self.panel1.Disconnect(-1,-1, wx.wxEVT_LEFT_DOWN): print 'panel1 unbinded'
            if self.panel2.Disconnect(-1,-1, wx.wxEVT_LEFT_DOWN): print 'panel2 unbinded'
            if self.panel.Disconnect(-1,-1, wx.wxEVT_LEFT_DOWN): print 'panel unbinded'
            self.menuboxitem = False
            self.buttonid = -1
            self.butlabel = None
            self.Refresh()
            """
            if self.Unbind(wx.EVT_TIMER):
                print 'timer unbinded'
            if self.panel2.Unbind(wx.EVT_PAINT):
                print 'paint unbinded'
            if self.panel1.Unbind(wx.EVT_LEFT_DOWN):
                print 'panel1 unbinded'
            if self.panel2.Unbind(wx.EVT_LEFT_DOWN):
                print 'panel2 unbinded'
            if self.panel.Unbind(wx.EVT_LEFT_DOWN):
                print 'panel unbinded'
            """
           
            
    def Onchkhl(self, event):
        """
        Future use
        """
        pass
    
    def Onchksb(self, event):
        """
        Show statusbar menu handler.
            1. Disable: hides the status bar
            2. Enable : shows the status bar
        """
        if self.chksb.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def Onconfig(self,event):
        """
        Speech Input menu handler.
            1. Disable: disables the speech input
            2. Enable : enables the speech input and defines response callback function
                - List of operations currently supported:
                  'Zero','One', 'Two', 'Three', 'Four','Five','Six','Seven','Eight','Nine',
                  'DIV','LCM','BY','DOT','CROSS','DEL', 
                  'Plus','Minus','Into','Divide','Equalto','UP','DOWN','LEFT','RIGHT','TURN OFF' 

                - Give speech input after the head phone output as B{Start speaking}
                - When u say B{TURN OFF} head phone will be B{Speech Input Stopped}
                - Supported operations are specified in phraselist variable in this function
        """

        self.numdict = { 'Zero':'0','One':'1', 'Two':'2', 'Three':'3', 'Four':'4','Five':'5','Six':'6','Seven':'7','Eight':'8','Nine':'9' }
        self.opdict = { 'Plus':' + ','Minus':' - ','Into':' * ','Divide':' / ','Equalto':' = ' }
        
        if self.chkbc.IsChecked():
            def response(phrase, listener):
                """
                speech input callback function.
                This function called for each speech input in separate thread to perform corresponding operation.
                """
                self.curcol = self.grid.GetGridCursorCol()
                self.currow = self.grid.GetGridCursorRow()  
                
                if phrase == 'TURN OFF':
                    listener.stoplistening()
                    print 'listener stopped'
                    speech.say('Speech Input stopped')
                else:
                    if(phrase in self.numdict.keys()):
                        self.setcellvalue(self.numdict[phrase])
                    elif(phrase in self.opdict.keys()):
                        self.setcellvalue(self.opdict[phrase])
                    elif(phrase != ''):
                        self.setcellvalue(phrase)
                    else:
                        pass
            
            print 'listener started..'
            phraselist = [ 'Zero','One', 'Two', 'Three', 'Four','Five','Six','Seven','Eight','Nine',
                               'DIV','LCM','BY','DOT','CROSS','DEL', 
                               'Plus','Minus','Into','Divide','Equalto','UP','DOWN','LEFT','RIGHT','TURN OFF'] #: List of supported operation
            
              
            listener = speech.listenfor(phraselist,response)
            speech.say("Start Speaking")

           # while listener.islistening():
           #     time.sleep(1)  

    def Onclear(self, event):
        """
        Clear All menu handler or keyboard shortcut Ctrl+C.
        clears all math worksheet content    
        """
        self.grid.ClearGrid()
        rows = self.grid.GetNumberRows()
        cols = self.grid.GetNumberCols()
        #renderer = self.grid.GetDefaultRenderer()
    
        for i in range(rows):
            for j in range(cols):
                self.grid.SetCellRenderer(i,j,self.grid.GetDefaultRenderer())
        
        self.grid.Refresh()
        
    def OnZoomin(self, event):
        """
        Zoom In menu handler or Keyboard shortcut Ctrl++.
        sets the grid cell size and font point size .        
        """
        self.cellsize = self.cellsize + 2
        self.font.SetPointSize(self.cellsize - 8)
        
        self.grid.SetDefaultRowSize(self.cellsize)
        self.grid.SetDefaultColSize(self.cellsize)
        self.grid.SetDefaultCellFont(self.font)
        self.grid.AdjustScrollbars()
        self.grid.Refresh()
        self.Refresh()
        print 'cell size', self.cellsize
        
    
    def OnZoomout(self, event):
        """
        Zoom Out menu handler or Keyboard shortcut Ctrl+-.
        sets the grid cell size and font point size .        
        """
        if self.cellsize > 15:
            self.cellsize = self.cellsize - 2
            self.font.SetPointSize(self.cellsize - 8)
        
        self.grid.SetDefaultRowSize(self.cellsize)
        self.grid.SetDefaultColSize(self.cellsize)
        self.grid.SetDefaultCellFont(self.font)
        self.grid.AdjustScrollbars()
        self.grid.Refresh()
        self.Refresh()
        print 'cell size', self.cellsize   
        

    def OnMenudec(self, event):
        """
        Menu speed-- menu handler.
        Increases the menugroup highlighting interval .        
        """
        self.menuspeed = self.menuspeed + 1000
        self.Refresh()
        print 'menuspeed', self.menuspeed
    
    def OnMenuinc(self, event):
        """
        Menu speed++ menu handler.
        Decreases the menugroup highlighting interval .        
        """
        if self.menuspeed > 2000:
            self.menuspeed = self.menuspeed - 1000
        else:
            pass
        self.Refresh()
        print 'menuspeed', self.menuspeed
    
    def OnMenuitemdec(self, event):
        """
        Menuitem speed-- menu handler.
        Increases the menuitem highlighting interval .        
        """
        self.butspeed = self.butspeed + 1000
        self.Refresh()
        print 'menuitemspeed', self.butspeed

    def OnMenuiteminc(self, event):
        """
        Menuitem speed++ menu handler.
        decreases the menuitem highlighting interval .        
        """
        if self.butspeed > 1000: 
            self.butspeed = self.butspeed - 1000
        else:
            pass
        self.Refresh()
        print 'menuitemspeed', self.butspeed

    def OnLoadprofile(self, event):
        """
        Load Profile menu handler or keyboard shortcut Ctrl+L
        It shows the Load profile dialog window.
        It applies the selected profile configuration options in current math assistant object.
        """
        loadpf.MainFrame(self)
        self.Refresh()

    def OnManageprofile(self, event):
        """
        Manage Profile menu handler or keyboard shortcut Ctrl+M
        It shows the Manage profile dialog window.
        It used to add/remove profiles.
        """
        managepf.MainFrame()
        self.Refresh()

    def OnEditprofile(self, event):
        """
        Edit Profile menu handler or keyboard shortcut Ctrl+E
        It shows the Edit profile dialog window.
        It shows the selected profile configuration options for editing.
        After editing options, we can save or cancel the editing.
        """
        editpf.MainFrame()
        self.Refresh()

    def OnManual(self,event):
        """
        Manual menu handler 
        Future impl
        """
        pass
    
    def OnAbout(self, event):
        """
        About menu handler
        To show brief info about this project.
        """
        description="""Math Assistant is a Comprehensive tool for speacially enabled children, 
providing a Math Worksheet Environment for easy way of solving simple Math problems.
        """
        license="""     Math Assistant is a free software;
You can redistribute it and/or modify it 
under the terms of the GNU General Public License 
as published by the Free Software Foundation; 
        """
        Mentors="""Mentors:

       Ranjani Parthasarathi            (rp@annauniv.edu)
        Bama S                           (bama@cs.annauniv.edu)
        
        Developer:

        Murali kumar. M                  (murali.au@gmail.com)
        """
        
        info=wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('source/math.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Math Assistant')
        info.SetVersion('2.0')
        info.SetDescription(description)
        info.SetCopyright('GNU General Public License version 3.0')
        info.SetLicence(license)
        info.AddDeveloper(Mentors)
        wx.AboutBox(info)



 #------------------------------------------------------------------------------
    def loaddefaultprofile(self):
        """
        This function loads the default profile specified in default profile variable.
        Future use - implemented with some bugs.
        """
        loadpf.MainFrame(self)
        self.loaddefault = None
        self.Refresh()

    def setpanelbgcolor(self,colour):
        """
        It sets panel background colour in current math assistant object.
        This is called by loadprofile function in loadconf class.
        """
        #self.bpcolor = colour
        self.panel.SetBackgroundColour(colour)
        print 'colour',colour
        self.Refresh()

    def sethighlightcolor(self,colour):
        """
        It sets highlighting colour in current math assistant object.
        This is called by loadprofile function in loadconf class.
        """
        self.hlcolor = colour
        self.Refresh()

    def refresh(self, event):
        """
        Refreshes the application.
        """
        self.grid.Refresh()
        self.Refresh()
        
    def OnMenuPaint(self,event):
        """
        This is paint event handler.
        Used to highlight the buttons.
        """
        paint=wx.PaintDC(self.panel2)
        paint.SetPen(wx.Pen(self.hlcolor))
        paint.SetBrush(wx.Brush(self.hlcolor))
        paint.DrawRoundedRectangle(self.topx,self.topy,self.width,self.height,10)
        
        """  if self.menuboxitem == False:
            print 'menu',self.menubox         
        else:
            print 'button',self.buttonid
        print self.topx, self.topy, self.width, self.height"""
    
    def movenext(self):
        """
        Future impl
        """
        pass
    def moveprev(self):
        """
        Future impl
        """
        pass
    def divsymbol(self):
        """
        B{DIV} menuitem handler.
        It used to draw the division symbol at current grid cursor in grid panel.
        """
        col = self.curcol
        if self.currow > 0 and col > 0 and col + 3 < self.grid.GetNumberCols():
            for i in range(5):
                col = col + 1
                self.grid.SetCellRenderer(self.currow,col,render.myHbyrenderer())
            
            self.grid.SetCellRenderer(self.currow,self.curcol,render.mydivrenderer())
            self.grid.MoveCursorDown(False)
            self.currow = self.currow + 1  
           # if self.currow <= self.grid.GetNumberRows():
            self.grid.SetCellRenderer(self.currow,self.curcol,render.myVbyrenderer())
            self.grid.MoveCursorRight(False)
            
        self.grid.Refresh()
        self.grid.SetFocus()
                    
    def lcmsymbol(self):
        """
        B{LCM} menuitem handler.
        It used to draw the lcm symbol at current grid cursor in grid panel.
        """
        col = self.curcol
        if self.currow > 0 and col > 0 and col + 3 < self.grid.GetNumberCols():  
            for i in range(5):
                col = col + 1
                self.grid.SetCellRenderer(self.currow,col,render.myHbyrenderer())
            self.grid.SetCellRenderer(self.currow,self.curcol,render.mylcmrenderer())
            self.grid.MoveCursorUp(False)
            self.currow = self.currow - 1 
            #if self.currow <= 1:
            self.grid.SetCellRenderer(self.currow,self.curcol,render.myVbyrenderer())
            self.grid.MoveCursorRight(False)
            
        self.grid.Refresh()
        self.grid.SetFocus()
        
    def crosssymbol(self):
        """
        B{CROSS} menuitem handler.
        It used to draw the cross symbol at current grid cursor in grid panel.
        """
        self.grid.SetCellRenderer(self.currow,self.curcol,render.mycrossrenderer())
        self.grid.SetFocus()

    def bysymbol(self):
        """
        B{BY} menuitem handler.
        It used to draw the BY symbol at current grid cursor in grid panel.
        """
        self.grid.SetCellRenderer(self.currow,self.curcol,render.myHtextbyrenderer())
        self.grid.MoveCursorDown(False)
        self.grid.SetFocus()

    def setcellvalue(self,id):
        """
        It used to B{set id value in parameter} at current grid cursor in grid panel.
        
        @param id: It can be symbols or moving operations or digits or letters.
        """
        if (id == '<---'):
            pass
            
        elif (id == 'PREV'):
            pass
            
        elif (id == 'NEXTT'):
            pass
            
        elif (id == 'NEXT'):

            self.timer.Stop()
            self.menuboxitem = False
            self.buttonid = -1
            self.butlabel = ''
            self.Refresh()
            self.OnChangeCursor(self)

        elif (id == 'UP'):

            # self.grid.DisableCellEditControl()
            self.grid.MoveCursorUp(False)
            self.grid.SetFocus()

        elif (id == 'DOWN'):

            success = self.grid.MoveCursorDown(False)
            
            if not success:
                newRow = self.grid.GetGridCursorRow() + 1
                if newRow <= 50:
                    if newRow >= self.grid.GetNumberRows(): 
                        self.grid.AppendRows(1,False)
                    self.grid.SetGridCursor(newRow, self.curcol)
                    self.grid.MakeCellVisible(newRow, self.curcol)

            self.grid.SetFocus()

        elif (id == 'LEFT'):

            self.grid.MoveCursorLeft(False)
            self.grid.SetFocus()

        elif (id == 'RIGHT'):
            #self.grid.DisableCellEditControl()
            success = self.grid.MoveCursorRight(False)
            
            if not success:
                newRow = self.grid.GetGridCursorRow() + 1
                if newRow <= 50:
                    if newRow >= self.grid.GetNumberRows():
                        self.grid.AppendRows(1,False)
                    self.grid.SetGridCursor(newRow, 0)
                    self.grid.MakeCellVisible(newRow, 0)
            
            self.grid.SetFocus()
        
        elif (id == 'DIV'):
            self.divsymbol()

        elif (id == 'LCM'):
            self.lcmsymbol()

        elif (id == 'BY'):
            self.bysymbol()

        elif (id == 'CROSS'):
            self.crosssymbol()

        elif (id == 'DOT'):
            self.grid.SetCellValue(self.currow,self.curcol,str('.'))
            self.setcellvalue('RIGHT')

        elif (id == 'DEL'):
            self.grid.SetCellValue(self.currow,self.curcol,str(''))
            self.grid.SetCellRenderer(self.currow,self.curcol, self.grid.GetDefaultRenderer())
            
            self.grid.SetFocus()
           # self.setcellvalue(23)
        elif (id == ' -- '):
            self.grid.SetCellValue(self.currow,self.curcol,str('-'))
            self.setcellvalue('RIGHT')

        elif id in string.letters:
            self.grid.SetCellValue(self.currow,self.curcol,str(id.lower()))
            self.setcellvalue('RIGHT')
        
        else:
            self.grid.SetCellValue(self.currow,self.curcol,id)
            self.setcellvalue('RIGHT')

    def OnButtonClick(self,event):
        """
        Buttonclick event handler.
        when a button clicked, It performs the corresponding operation
        at current grid cursor position in grid panel or button panel.        
        """
        id = event.GetEventObject().GetLabel()
                
        self.curcol = self.grid.GetGridCursorCol()
        self.currow = self.grid.GetGridCursorRow()  
        
        self.setcellvalue(id)
            
        #print 'bclick' , id
        #wx.grid.Grid.
        """ print 'button click event',event.GetId()
        print 'col' , self.curcol
        print 'row' , self.currow"""
        
    def OnButtontoleftclick(self,event):
        """
        Buttonclick event handler. (only when Button click option is disabled and Left click option is enabled)
        It redirects button click event as left click event.
        """
        if (self.chklc.IsChecked() == True):
            self.OnLeftClick(event)    
        else:
            pass

    def OnLeftDclick(self,event):
        """
        Doubleclick event handler.
        Used to change the highlighting to Menugroup level.
        """
        self.timer.Stop()
        self.menuboxitem = False
        self.buttonid = -1
        self.butlabel = ''
        self.Refresh()
        self.OnChangeCursor(self)      

    def OnLeftClick(self,event):
        """
        Leftclick event handler.
            - if menuboxitem variable is false, highlighting changed from Menugroup level to Menuitem level when left clicked.
            - else calls setcellvalue function to perform the current button operation when left clicked. 
        """
        if self.menuboxitem == False:
            self.timer.Stop()
            self.menuboxitem = True
            #self.buttonid = event.GetId()
            self.Refresh()
            self.OnChangeCursor(self)
        
        else:
            self.curcol = self.grid.GetGridCursorCol()
            self.currow = self.grid.GetGridCursorRow()  
            
            self.setcellvalue(self.butlabel)
            
        #print 'mouse left clik event'
        #print 'bid' ,self.butlabel
       
    def OnChangeCursor(self,event):
        """
        Timer event handler.
            - If menuboxitem variable is false, highlighting coutinued to next Menugroup.
            - else highlighting continued to next Menuitem level.
        calls playsound function if playsound option is enabled.
        Starts timer for a time interval to call this function.
        """
        if self.menuboxitem == False:
            self.menubox = (self.menubox + 1) % int(self.panelnos)     
            if self.menubox==0:
                self.topx,self.topy = self.gbox1.GetPosition()
                self.width,self.height = self.gbox1.GetSize()
            elif self.menubox==1:
                self.topx,self.topy = self.gbox2.GetPosition()
                self.width,self.height = self.gbox2.GetSize()
            elif self.menubox==2:
                self.topx,self.topy = self.gbox3.GetPosition()
                self.width,self.height = self.gbox3.GetSize()
            
            self.topx,self.topy = self.topx-5 ,self.topy-5    
            self.width,self.height = self.width+10 ,self.height+10       
            self.Refresh()
            if self.soundflag == True:
                self.playsound()
            self.timer.Start(self.menuspeed)
        else:
                       
            if self.menubox == 0:
                self.buttonid = (self.buttonid + 1)%12
                self.butlabel = self.butList1[self.buttonid].GetLabel()
                self.topx,self.topy = self.butList1[self.buttonid].GetPosition()
                self.width,self.height = self.butList1[self.buttonid].GetSize()
            
            elif self.menubox==1:          
                self.buttonid = (self.buttonid + 1)%12
                self.butlabel = self.butList2[self.buttonid].GetLabel()
                self.topx,self.topy = self.butList2[self.buttonid].GetPosition()
                self.width,self.height = self.butList2[self.buttonid].GetSize()
                    
            elif self.menubox==2:
                self.buttonid = (self.buttonid + 1)%12
                self.butlabel = self.butList3[self.buttonid].GetLabel()
                self.topx,self.topy = self.butList3[self.buttonid].GetPosition()
                self.width,self.height = self.butList3[self.buttonid].GetSize()
                        
            self.topx,self.topy = self.topx-5 ,self.topy-5    
            self.width,self.height = self.width+10 ,self.height+10       
            self.Refresh()
            if self.soundflag == True:
                self.playsound()
            self.timer.Start(self.butspeed)
    
    def playsound(self):
        """
        It used to play the voice sound according to the current highlighting.
            - If menuboxitem is false, It plays the Menugroup names
            - else it plays the Menuitem names
        """
        if self.menuboxitem == False:
            if self.menubox == 0:
                sound = wx.Sound('source/voice/NUMBERS.wav')
            elif self.menubox == 1:
                sound = wx.Sound('source/voice/OPERATORS.wav')
            elif self.menubox == 2:
                sound = wx.Sound('source/voice/SYMBOLS.wav')
        else:
            if (self.butlabel == '<---'):
                sound = wx.Sound('source/voice/BACKWARD.wav')
            elif (self.butlabel == ' + '):
                sound = wx.Sound('source/voice/ADDITION.wav')
            elif (self.butlabel == ' -- '):
                sound = wx.Sound('source/voice/SUBTRACTION.wav')
            elif (self.butlabel == ' * '):
                sound = wx.Sound('source/voice/MULTIPLICATION.wav')
            elif (self.butlabel == ' / '):
                sound = wx.Sound('source/voice/DIVISION.wav')
            elif (self.butlabel == ' = '):
                sound = wx.Sound('source/voice/EQUALTO.wav')
            elif (self.butlabel == 'NEXTT'):
                sound = wx.Sound('source/voice/NEXTSTEP.wav')	
            else:
                sound = wx.Sound('source/voice/'+self.butlabel+'.wav')

        sound.Play()
        #sound.Stop()  


if __name__=='__main__':
    """
    This is the Entry point of the application.
    Starts application by creating the Math assistant object.
    """
    app=wx.App(0)
    ma=mathassist(None, -1, 'Math Assistant')
    app.SetTopWindow(ma)
    app.MainLoop()
