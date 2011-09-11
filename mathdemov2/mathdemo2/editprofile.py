"""
System configuration is one of the most important issues for making this tool more convenient for users.
By handling multiple profiles, we can edit, manage and load the profiles for our system.
By giving more choices for configuration, this makes our tool dynamic and easy to use.
Also configurations can be saved and reused on other systems by means of the profile handling mechanism.

Manage profile is used to perform profile creation and removal operations.
Edit profile is used to edit the default or predefined settings and saves these settings in the configuration files.
Load profile loads the specified configuration file, and assigns the saved settings to the current math assistant object.
All these operations are based on the configuration files in current directory.

Following user settings are added to this configuration module.

    - Positioning button controls in button menu panels by user choice.
    - Color Settings (Panel / Highlighting)
    - Zoom level 
    - Highlighting Speed Settings (Menu / Menu item)
    - Input settings  (Mouse left click / button click / both)
    - Sound settings.
    - Speech settings.
    - Button Panel Settings (Horizontal / Vertical)

After editing these settings the system saves that data in a configuration file for later use.
When loading any one of this configuration file, saved settings are applied to the math assistant object.


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

class editconf(wx.Panel):
    """
    This class is used to edit the configuration settings stored in a profile.
    """
    def __init__(self, parent,profiles,frame):
        """
        Constructor method for this class.        
        Used to construct this editconf notebook dialog window

        @param parent    : Parent class of the object
        @param profiles  : profiles list in current directory
        @param frame     : MainFrame class object
        
        """


        wx.Panel.__init__(self, parent)
        #t = wx.StaticText(self, -1, "This is a PageThree object", (60,60))
        # config variables
        self.frame = frame                              #: MainFrame class instance
        self.config = ConfigParser.RawConfigParser()    #: ConfigParser instance variable
        self.changed = False                            #: To determine whether an edit is performed or not
        self.paneltype = 'VERTICAL'                     #: paneltype variable
        self.panelnos = '3'                             #: No of panels variable
        
        self.line = wx.StaticLine(self)
        self.line1 = wx.StaticLine(self)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        # panel0
        self.panel0 = wx.Panel(self, -1)
        hbox01 = wx.BoxSizer(wx.HORIZONTAL)
        hbox02 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0  = wx.BoxSizer(wx.HORIZONTAL)
        self.cbtext = wx.StaticText(self.panel0, -1 , " Select a profile to Edit ")
        self.cb0 = wx.ComboBox(self.panel0, -1 , size =(150, -1) , choices = profiles , style = wx.CB_READONLY)
        #self.edit = wx.Button(self.panel0 , 1 , ' EDIT ')
        self.apply = wx.Button(self.panel0 , 1 , ' APPLY ')
        self.ok = wx.Button(self.panel0 , 2 , ' OK ')
        self.cancel = wx.Button(self.panel0 , 3 , ' CANCEL ')
        hbox01.Add(self.cbtext ,0,wx.LEFT|wx.RIGHT, 10)
        hbox01.Add(self.cb0 ,0,wx.RIGHT,50)
        #hbox0.Add(self.edit ,0,wx.ALIGN_CENTER,10) 
        hbox02.Add(self.apply ,0,wx.LEFT,50) 
        hbox02.Add(self.ok , 0 , wx.LEFT|wx.RIGHT,20)
        hbox02.Add(self.cancel ,0,wx.RIGHT,20) 
        hbox0.Add(hbox01 , 0 ,wx.TOP , 15)
        hbox0.Add(hbox02 , 0,wx.TOP|wx.ALIGN_RIGHT,15)
        self.panel0.SetSizer(hbox0)
        self.vbox.Add(self.panel0, 0,wx.EXPAND|wx.ALIGN_CENTER)
        
        self.apply.Enable(False)
        self.ok.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.Onapply, id=1)
        self.Bind(wx.EVT_BUTTON, self.Onok, id=2)
        self.Bind(wx.EVT_BUTTON, self.Oncancel, id=3)
        self.Bind(wx.EVT_COMBOBOX, self.Onselect ,self.cb0 )

        self.vbox.Add(self.line, 0, wx.ALL|wx.EXPAND, 10)
        # panel1
        self.panel1 = wx.Panel(self, -1)
        sbox1 = wx.StaticBoxSizer(wx.StaticBox(self.panel1, -1, 'Options'), orient=wx.VERTICAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        grid1 = wx.GridSizer(1, 5, 15, 15)
        self.os = wx.CheckBox(self.panel1, 11, ' Sound ')
        self.obc = wx.CheckBox(self.panel1, 12, 'Button Click') 
        self.olc = wx.CheckBox(self.panel1, 13, 'Left Click') 
        self.osg = wx.CheckBox(self.panel1, 14, 'Show Gridlines') 
        self.osb = wx.CheckBox(self.panel1, 15, 'Status Bar') 
        grid1.Add(self.os)
        grid1.Add(self.obc)
        grid1.Add(self.olc)
        grid1.Add(self.osg)
        grid1.Add(self.osb)
        vbox1.Add(grid1)
        sbox1.Add(vbox1, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        self.panel1.SetSizer(sbox1)
        self.vbox.Add(self.panel1, 0, wx.ALL|wx.EXPAND, 10)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck, id=11)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck, id=12)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck, id=13)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck, id=14)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck, id=15)
        
        # panel2
        self.mblist = ['4','5','6','7','8','9','10']
        self.milist = ['2','3','4','5','6','7','8','9','10']
        self.zlist  = ['1','2','3','4','5','6','7','8','9','10']
        self.panel2 = wx.Panel(self, -1)
        sbox2 = wx.StaticBoxSizer(wx.StaticBox(self.panel2, -1, 'Settings'), orient=wx.VERTICAL)
        grid2 = wx.GridSizer(1, 6, 0, 5)
        grid2.Add(wx.StaticText(self.panel2, -1, 'MenuBox speed(sec): ', (5, 5)))
        self.ch21 = wx.Choice(self.panel2, 21, (100, 50), choices = self.mblist)
        grid2.Add(self.ch21)
        grid2.Add(wx.StaticText(self.panel2, -1, 'MenuItem speed(sec): ', (5, 5)))
        self.ch22 = wx.Choice(self.panel2, 22, (100, 50), choices = self.milist)
        grid2.Add(self.ch22)
        grid2.Add(wx.StaticText(self.panel2, -1, 'Zoom Level: ', (5, 5)))
        self.ch23 = wx.Choice(self.panel2, 23, (100, 50), choices = self.zlist)
        grid2.Add(self.ch23)
        sbox2.Add(grid2, 0, wx.TOP|wx.LEFT|wx.BOTTOM, 10)
        self.panel2.SetSizer(sbox2)
        self.vbox.Add(self.panel2, 0, wx.ALL|wx.EXPAND, 10)

        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch21)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch22)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch23)

        # panel3
        self.panel3 = wx.Panel(self, -1)
        sbox3 = wx.StaticBoxSizer(wx.StaticBox(self.panel3, -1, 'Color Options'), orient=wx.VERTICAL)
        grid3 = wx.GridSizer(1, 4,10,10)
        #self.color = (255, 255, 0)          
        self.bptext = wx.StaticText(self.panel3, -1 , " Select ButtonPanel BG color : ")
        self.hltext = wx.StaticText(self.panel3, -1 , " Select Highlight color      : ")
        self.bpcolor = csel.ColourSelect(self.panel3, 31,size = wx.DefaultSize)
        self.hlcolor = csel.ColourSelect(self.panel3, 32,size = wx.DefaultSize)
        grid3.Add(self.bptext)
        grid3.Add(self.bpcolor,0)
        grid3.Add(self.hltext)
        grid3.Add(self.hlcolor,0)
        sbox3.Add(grid3, 0, wx.TOP|wx.LEFT|wx.BOTTOM, 10)
        self.panel3.SetSizer(sbox3)
        self.vbox.Add(self.panel3, 0, wx.ALL|wx.EXPAND, 10)

        self.bpcolor.Bind(csel.EVT_COLOURSELECT, self.OnSelectColour)
        self.hlcolor.Bind(csel.EVT_COLOURSELECT, self.OnSelectColour)
        
        #panel4 
        self.vbox.Add(self.line1, 0, wx.ALL|wx.EXPAND, 10)

        #panel5
        self.nlist = [ '0','1','2','3','4','5','6','7','8','9' ]
        self.alist = [ 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z' ]
        self.olist = [ ' + ',' -- ',' * ',' / ',' = ',' ( ',' ) ',' | ',' % ',' , ','NEXT','UP','DOWN','LEFT','RIGHT' ]
        self.slist = [ 'DIV','LCM','BY','DOT','CROSS','DEL','PREV','NEXTT','<---' ]
        self.smblist = ['one' , 'two' ,'three']
        self.smilist = ['1','2','3','4','5','6','7','8','9','10','11','12']
        self.ptypelist = ['VERTICAL' , 'HORIZONTAL']
        self.pnolist = ['3','2','1']

        self.panel5 = wx.Panel(self, -1)
        
        grid4 = wx.GridSizer(1, 8)
        grid4.Add(wx.StaticText(self.panel5, -1, ' Select a MenuBox : ', (5, 5)), 0 )
        self.ch41 = wx.Choice(self.panel5, 41, (100, 50), choices = self.smblist)
        grid4.Add(self.ch41)
        grid4.Add(wx.StaticText(self.panel5, -1, 'Select Menuitem Position : ', (5, 5)), 0)
        self.ch42 = wx.Choice(self.panel5, 42, (100, 50), choices = self.smilist)
        grid4.Add(self.ch42)
        grid4.Add(wx.StaticText(self.panel5, -1, 'Select Paneltype : ', (5, 5)), 0)
        self.ch43 = wx.Choice(self.panel5, 43, (100, 50), choices = self.ptypelist)
        grid4.Add(self.ch43)
        grid4.Add(wx.StaticText(self.panel5, -1, 'Select NoofPanel : ', (5, 5)), 0)
        self.ch44 = wx.Choice(self.panel5, 44, (100, 50), choices = self.pnolist)
        grid4.Add(self.ch44)
        
        grid5 = wx.GridSizer(1, 8 , 10,10)
        sbox5 = wx.StaticBoxSizer(wx.StaticBox(self.panel5, -1, 'Select a Menuitem'), orient=wx.VERTICAL)
        self.rb1 = wx.RadioButton(self.panel5, 51, 'NUMBERS', (10, 10), style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self.panel5, 52, 'ALPHABETS', (10, 30))
        self.rb3 = wx.RadioButton(self.panel5, 53, 'OPERATORS', (10, 50))
        self.rb4 = wx.RadioButton(self.panel5, 54, 'SYMBOLS', (10, 50))
        self.ch51= wx.Choice(self.panel5, 55, (100, 50), choices = self.nlist)
        self.ch52= wx.Choice(self.panel5, 56, (100, 50), choices = self.alist)
        self.ch53= wx.Choice(self.panel5, 57, (100, 50), choices = self.olist)
        self.ch54= wx.Choice(self.panel5, 58, (100, 50), choices = self.slist)                
        grid5.Add(self.rb1)
        grid5.Add(self.ch51)
        grid5.Add(self.rb2)
        grid5.Add(self.ch52)
        grid5.Add(self.rb3)
        grid5.Add(self.ch53)
        grid5.Add(self.rb4)
        grid5.Add(self.ch54)

        sbox5.Add(grid5, 0, wx.TOP|wx.LEFT|wx.BOTTOM, 10)
        sbox5.Add(grid4, 0, wx.TOP|wx.LEFT|wx.BOTTOM, 10)
        self.panel5.SetSizer(sbox5)
        self.vbox.Add(self.panel5, 0, wx.ALL|wx.EXPAND, 10)

        self.ch51.Enable(True)
        self.ch52.Enable(False)
        self.ch53.Enable(False)
        self.ch54.Enable(False)
        self.ch43.Enable(False)
        self.ch44.Enable(False)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch41)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch42)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch43)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch44)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch51)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch52)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch53)
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.ch54)
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, self.rb1)
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, self.rb2)
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, self.rb3)
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, self.rb4)

        
        self.font=wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.font.SetPointSize(15)
        self.font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.font.SetFamily(wx.FONTFAMILY_DEFAULT)

        #panel 6
        self.makedefaultpanel6()
        
        #panel7
        """self.panel7 = wx.Panel(self, -1)
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        vbox7 = wx.BoxSizer(wx.VERTICAL)
        self.apply = wx.Button(self.panel7 , 1 , ' APPLY ')
        self.ok = wx.Button(self.panel7 , 1 , ' OK ')
        self.cancel = wx.Button(self.panel7 , 1 , ' CANCEL ')
        hbox7.Add(self.apply ,0,wx.RIGHT,10) 
        hbox7.Add(self.ok , 0 , wx.RIGHT,10)
        hbox7.Add(self.cancel ,0) 
        vbox7.Add(hbox7,0,wx.ALIGN_RIGHT)
        self.panel7.SetSizer(vbox7)  
        vbox.Add(self.panel7, 0, wx.ALL|wx.EXPAND, 10)"""

        # disables the panels to select a profile to edit
        self.panel1.Enable(False)
        self.panel2.Enable(False)
        self.panel3.Enable(False)
        self.panel5.Enable(False)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.vbox)
        self.Centre()
        self.Show(True)


#--------------------------------------------------------------------------------------
    def makedefaultpanel6(self):
        """
        This is used to make the default preview panel
        """
        #   panel6
        self.panel6 = wx.Panel(self,-1)
        
        self.grsize = 4         #: No of rows in gridsizer
        self.gcsize = 3         #: No of cols in gridsizer
        self.bwsize = 100       #: Button width in gridsizer
        self.bhsize = 40        #: Button height in gridsizer
        
        self.butList1=range(12) 
        self.butList2=range(12)
        self.butList3=range(12)
        self.blist1=range(12) 
        self.blist2=range(12)
        self.blist3=range(12)
        
                    
        self.gbox61 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        
        for i in range(12):
            self.butList1[i]=wx.Button(self.panel6,i,'',size=(self.bwsize,self.bhsize))
            self.butList1[i].SetFont(self.font)
            #self.butList1[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)
            self.gbox61.Add(self.butList1[i],0,wx.ALL|wx.EXPAND)
        
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

        self.gbox62 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        
        for i in range(12):
            self.butList2[i]=wx.Button(self.panel6,i+12,'',size=(self.bwsize,self.bhsize))
            self.butList2[i].SetFont(self.font)
        #    self.butList2[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)                  
            self.gbox62.Add(self.butList2[i],0,wx.ALL|wx.EXPAND)
            
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
                
        self.gbox63 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)

        for i in range(12):
            self.butList3[i]=wx.Button(self.panel6,i+24,'',size=(self.bwsize,self.bhsize))
            self.butList3[i].SetFont(self.font)
            #self.butList3[i].Bind(wx.EVT_BUTTON,self.OnButtonClick)
            self.gbox63.Add(self.butList3[i],0,wx.ALL|wx.EXPAND)
            
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

        self.hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox6.Add(self.gbox61, 1, wx.ALL|wx.EXPAND,10)
        self.hbox6.Add(self.gbox62, 1, wx.ALL|wx.EXPAND,10)
        self.hbox6.Add(self.gbox63, 1, wx.ALL|wx.EXPAND,10)
        
        self.panel6.SetSizer(self.hbox6)  
        self.vbox.Add(self.panel6, 0, wx.ALL|wx.EXPAND, 10)

    def makechoicepanel6(self):
        """
        This method used to layout the preview panel using two variables
            1. paneltype
            2. panelnos
        """
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

        self.gbox61 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        self.gbox62 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        self.gbox63 = wx.GridSizer(self.grsize, self.gcsize, 3, 3)
        self.hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox6 = wx.BoxSizer(wx.VERTICAL)

        print 'height',self.bhsize
        print 'width' ,self.bwsize

        if(self.panelnos == '3'):
            print 'panelno3'
            for i in range(12):
                self.butList1[i].SetSize(wx.Size(self.bwsize,self.bhsize))
                self.butList2[i].SetSize(wx.Size(self.bwsize,self.bhsize))
                self.butList3[i].SetSize(wx.Size(self.bwsize,self.bhsize))

                self.gbox61.Add(self.butList1[i],0,wx.ALL|wx.EXPAND)
                self.gbox62.Add(self.butList2[i],0,wx.ALL|wx.EXPAND)
                self.gbox63.Add(self.butList3[i],0,wx.ALL|wx.EXPAND)
            if(self.paneltype == 'VERTICAL'):
                self.hbox6.Add(self.gbox61, 1, wx.ALL|wx.EXPAND,10)
                self.hbox6.Add(self.gbox62, 1, wx.ALL|wx.EXPAND,10)
                self.hbox6.Add(self.gbox63, 1, wx.ALL|wx.EXPAND,10)
            elif(self.paneltype == 'HORIZONTAL'):
                self.vbox6.Add(self.gbox61, 1, wx.ALL|wx.EXPAND,10)
                self.vbox6.Add(self.gbox62, 1, wx.ALL|wx.EXPAND,10)
                self.vbox6.Add(self.gbox63, 1, wx.ALL|wx.EXPAND,10)
            else:
                pass

        elif(self.panelnos == '2'):
            print 'panelno2'
            for i in range(12):
                self.butList1[i].SetSize(wx.Size(self.bwsize,self.bhsize))
                self.butList2[i].SetSize(wx.Size(self.bwsize,self.bhsize))

                self.gbox61.Add(self.butList1[i],0,wx.ALL|wx.EXPAND)
                self.gbox62.Add(self.butList2[i],0,wx.ALL|wx.EXPAND)
            if(self.paneltype == 'VERTICAL'):
                self.hbox6.Add(self.gbox61, 1, wx.ALL|wx.EXPAND,10)
                self.hbox6.Add(self.gbox62, 1, wx.ALL|wx.EXPAND,10)
            elif(self.paneltype == 'HORIZONTAL'):
                self.vbox6.Add(self.gbox61, 1, wx.ALL|wx.EXPAND,10)
                self.vbox6.Add(self.gbox62, 1, wx.ALL|wx.EXPAND,10)
            else:
                pass
        
        elif(self.panelnos == '1'):
            print 'panelno1'
            for i in range(12):
                self.butList1[i].SetSize(wx.Size(self.bwsize,self.bhsize))
                self.gbox61.Add(self.butList1[i],0,wx.ALL|wx.EXPAND)
            if(self.paneltype == 'VERTICAL'):
                self.hbox6.Add(self.gbox61, 1, wx.ALL|wx.EXPAND,10)
            elif(self.paneltype == 'HORIZONTAL'):
                self.vbox6.Add(self.gbox61, 1, wx.ALL|wx.EXPAND,10)
            pass
        
        if(self.paneltype == 'VERTICAL'):
            self.panel6.SetSizerAndFit(self.hbox6,True)  
        elif(self.paneltype == 'HORIZONTAL'):
            self.panel6.SetSizerAndFit(self.vbox6,True)  
        else:
            pass
        
        self.panel6.Layout()
        self.Layout()
        self.panel6.Refresh()
        self.Refresh()
#-------------------------------------------------------------------------------------

    def OnSelectColour(self, event):
        """
        Event handler function for colourselect control
        It stores the selected color values.
        """
        
        ob = event.GetEventObject()
        id = ob.GetId()
        if(self.changed == False):
            self.changed = True
            self.apply.Enable(True)
            self.ok.Enable(True)
        
        if (id == 31):
            self.Bpcolor = event.GetValue()
        elif (id == 32):
            self.Hlcolor = event.GetValue()
       
    
    def SetVal(self, event):
        """
        Event handler function for RadioButton controls
        It used to enable the corresponding choice control.
        also disables all other choice controls.
        """
        ob = event.GetEventObject()
        id = ob.GetId()
        
        if (id == 51):
            self.ch51.Enable(True)
            self.ch52.Enable(False)
            self.ch53.Enable(False)
            self.ch54.Enable(False)
        elif (id == 52):
            self.ch51.Enable(False)
            self.ch52.Enable(True)
            self.ch53.Enable(False)
            self.ch54.Enable(False)
        elif (id == 53):
            self.ch51.Enable(False)
            self.ch52.Enable(False)
            self.ch53.Enable(True)
            self.ch54.Enable(False)
        elif (id == 54):
            self.ch51.Enable(False)
            self.ch52.Enable(False)
            self.ch53.Enable(False)
            self.ch54.Enable(True)

    def Onapply(self, event):
        """
        Event handler function for APPLY button control
        It is used to write the edited configuration settings.
        """
        if(self.changed == True):
            self.writeconfig()
        self.changed = False
        self.apply.Enable(False)
        #self.ok.Enable(False)

    def Onok(self, event):
        """
        Event handler function for OK button control
        It is used to write the edited configuration settings.
        """
        if(self.changed == True):
            self.writeconfig()
        self.changed = False
        self.apply.Enable(False)
        self.ok.Enable(False)
        self.frame.Close()

    def Oncancel(self, event):
        """
        This method closes the EditProfile notebook dialog
        """
        self.frame.Close()
        

    def Onselect(self, event):
        """
        Event handler function for the ComboBox control.
        This method reads and displays the configuration settings in selected profile.
        """
        
        cb = event.GetEventObject()
        cb.Enable(False)
        if(self.changed == True):
            self.changed = False
        
        self.apply.Enable(False)
        self.ok.Enable(False)

        self.ch43.Enable(True)
        self.ch44.Enable(True)

        self.profile = event.GetString()
        self.config.read(self.profile)

        self.blist1 = self.config.get('dict' , 'butlist1')
        self.blist1 = eval(self.blist1)
        self.blist2 = self.config.get('dict' , 'butlist2')
        self.blist2 = eval(self.blist2)
        self.blist3 = self.config.get('dict' , 'butlist3')
        self.blist3 = eval(self.blist3)
        
        
        self.Sound      = self.config.getboolean('options' ,'sound')
        self.Bclick     = self.config.getboolean('options' ,'bclick')
        self.Lclick     = self.config.getboolean('options' ,'lclick')
        self.Showgrid   = self.config.getboolean('options' ,'showgrid')
        self.Sbar       = self.config.getboolean('options' ,'sbar')
        self.Mbspeed    = self.config.get('settings' ,'mbspeed')
        self.Mispeed    = self.config.get('settings' ,'mipeed')
        self.Zoomlevel  = self.config.get('settings' ,'zoomlevel')
        self.paneltype  = self.config.get('settings' ,'Paneltype')
        self.panelnos   = self.config.get('settings' ,'Panelnos')
        self.Bpcolor    = eval(self.config.get('color' ,'bpcolor'))
        self.Hlcolor    = eval(self.config.get('color' ,'hlcolor'))
        
        for i in range(12):
            self.butList1[i].SetLabel(self.blist1[i])
            self.butList2[i].SetLabel(self.blist2[i])
            self.butList3[i].SetLabel(self.blist3[i])
        
        #wx.lib.colourselect.ColourSelect
        self.os.SetValue(self.Sound) 
        self.obc.SetValue(self.Bclick)
        self.olc.SetValue(self.Lclick)
        self.osg.SetValue(self.Showgrid)
        self.osb.SetValue(self.Sbar)
        self.ch21.SetStringSelection(self.Mbspeed) 
        self.ch22.SetStringSelection(self.Mispeed)  
        self.ch23.SetStringSelection(self.Zoomlevel)  
        self.ch43.SetStringSelection(self.paneltype)
        self.ch44.SetStringSelection(self.panelnos)  
        self.bpcolor.SetColour(self.Bpcolor)
        self.hlcolor.SetColour(self.Hlcolor)
        
        self.makechoicepanel6()

        self.panel1.Enable(True)
        self.panel2.Enable(True)
        self.panel3.Enable(True)
        self.panel5.Enable(True)
        
        cb.Enable(True)
        print 'profile' , self.profile
    
    def OnCheck(self, event):
        """
        Event handler function for CheckBox controls
        following options are given
            - playsound
            - Buttonclick
            - Leftclick
            - Showgrid
            - Statusbar
        """

        ob = event.GetEventObject()
        id = ob.GetId()
        if(self.changed == False):
            self.changed = True
            self.apply.Enable(True)
            self.ok.Enable(True)

        if ob.IsChecked():
            if (id == 11):
                self.Sound = True
            elif (id == 12):
                self.Bclick = True
            elif (id == 13):
                self.Lclick = True
            elif (id == 14):
                self.Showgrid = True
            elif (id == 15):
                self.Sbar = True
        else:
            if (id == 11):
                self.Sound = False
            elif (id == 12):
                self.Bclick = False
            elif (id == 13):
                self.Lclick = False
            elif (id == 14):
                self.Showgrid = False
            elif (id == 15):
                self.Sbar = False


    def OnChoice(self, event):
        """
        Event handler function for Choice controls

        It used to select following settings
            - MenuBox speed
            - Menuitem speed
            - Zoom level

        It used for menu item positioning using following two choice controls
            1. Select a menubox (1-3)
            2. select menuitem position (1-12)
        after selecting these two choices, when we select any (NUMBERS, ALPHABETS, SYMBOLS, OPERATORS) 
        choice, it reflects in preview panel.

        It used to layout the button panel using following two choice controls
            1. select paneltype (HORIZONTAL/VERTICAL)
            2. No. of panels (1-3)
        after selecting No.of panels, when we select paneltype it reflects in the preview panel. 

        These settings are saved in selected profile when we press APPLY button.
        
        """

        ob = event.GetEventObject()
        id = ob.GetId()
        if(self.changed == False):
            self.changed = True
            self.apply.Enable(True)
            self.ok.Enable(True)
        
        if (id == 21):
            self.Mbspeed = event.GetString()
        elif (id == 22):
            self.Mispeed = event.GetString()
        elif (id == 23):
            self.Zoomlevel = event.GetString()
        elif (id == 43):
            self.paneltype = event.GetString()
            self.makechoicepanel6()
        elif (id == 44):
            self.panelnos = event.GetString()

        elif (id == 55 or id == 56 or id == 57 or id == 58 ):
            t = self.ch41.GetStringSelection()
            t1 = self.ch42.GetStringSelection()
            
            if(t == '' or t1 == ''):
                return
            
            i  = int(t1) - 1

            if(t == 'one'):
                self.butList1[i].SetLabel(event.GetString())
                self.blist1[i] = event.GetString()
            elif(t == 'two'):
                self.butList2[i].SetLabel(event.GetString())
                self.blist2[i] = event.GetString()
            elif(t == 'three'):
                self.butList3[i].SetLabel(event.GetString())
                self.blist3[i] = event.GetString()
            else: 
                pass
            
    def writeconfig(self):
        """
        This method used to save the edited configuration settings in selected profile
        """
        #self.config.add_section('dict')
        #self.config.add_section('options')
        #self.config.add_section('settings')
        #self.config.add_section('color')
        self.config.set('dict' ,'butlist1',repr(self.blist1))
        self.config.set('dict' ,'butlist2',repr(self.blist2))
        self.config.set('dict' ,'butlist3',repr(self.blist3))

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

        with open(self.profile, 'wb') as self.configfile:
            self.config.write(self.configfile)
    
    
class MainFrame(wx.Frame):
    """
    This class used to show the notebook dialog for EditProfile  
    """

    def __init__(self):
        """
        Constructor method for this class.
        Finds configuration files in current directory and invokes editconf class
        """

        wx.Frame.__init__(self, None, title="Profile Settings")

        p = wx.Panel(self, -1)
        nb = wx.Notebook(p,-1, style=wx.BK_DEFAULT)

        self.profiles = []              #: profiles list in current directory
        ext = '.cfg'
        for root, dirs, files in os.walk('./'):
            for name in files:       
                filename = os.path.join(root, name)
                if os.path.splitext(filename)[1] == ext:
                    self.profiles.append(name)
                    #print name
        
        self.edit = editconf(nb ,self.profiles,self)
        nb.AddPage(self.edit, "Edit Profile")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
        self.Center()
        self.Show()