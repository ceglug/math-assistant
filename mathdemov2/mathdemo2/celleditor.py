"""
wx.grid is one of the complex control in WxPython toolkit.
We are tuning this grid control for working math problems.
 
@license: Math Assistant is a free software;
You can redistribute it and/or modify it under
the terms of the GNU General Public License 
as published by the Free Software Foundation; 
@copyright: GNU General Public License version 3.0
@author: MURALI KUMAR. M
@contact: U{murali.au@gmail.com}

"""

import wx
import wx.grid
import string


#---------------------------------------------------------------------------
class myCellEditor(wx.grid.PyGridCellEditor):
    """
    Grid control output consist only one letter or operator or symbol inside each cell for the input.
    It displays the math problems worked out by the users. 
    for that purpose Custom editor is used to have only one value for each cell.
    This custom class used to modify the grid control and also fulfils our requirement to perform math operations.

    """
    def __init__(self):
        """
        Creates a myCellEditor object to set as a default editor for the grid control used by the application.
        """
        wx.grid.PyGridCellEditor.__init__(self)
        
    def Create(self, parent, id, evtHandler):
        """
        Creates a text control object to insert/edit/save the value in each cell of the grid control.
        also binds a event handler for the character input.
        @param parent     : Parent class of the object
        @param id         : Instance id of the object
        @param evtHandler : event handler for the object.

        """

        self._tc = wx.TextCtrl(parent, id, "")
     #  self._tc.SetInsertionPoint(0)
        self.SetControl(self._tc)
        if evtHandler:
            self._tc.PushEventHandler(evtHandler)
        self._tc.Bind(wx.EVT_CHAR, self.OnChar)                 # Event handler for the text control.
 
    def SetSize(self, rect):
        """
        set dimensions for the text control used inside each cell of the grid control. 
        this method called when editing is performed.
        @param rect: rectangle parameters for the text control.
        
        """


        self._tc.SetDimensions(rect.x, rect.y, rect.width+2, rect.height+2,wx.SIZE_ALLOW_MINUS_ONE)
       # self._tc.Alignment(wx.CENTER)
        
    """ def Show(self, show, attr):
       \""" Show or hide the edit control.  Use the attr (if not None)
            to set colors or fonts for the control.

            NOTE: There is no need to everride this if you dont need
            to do something out of the ordinary.
        \"""
        super(myCellEditor, self).Show(show, attr) """
        

    """ def PaintBackground(self, rect, attr):
        \""" Draws the part of the cell not occupied by the edit control.  The
            base class version just fills it with background colour from the
            attribute.

            NOTE: There is no need to everride this if you don't need
            to do something out of the ordinary.
        \"""
        # Call base class method.
        super(CCellEditor, self).PaintBackground(rect, attr)"""

  
    def BeginEdit(self, row, col, grid):
        """
        This method is called when editing begins in text control. 
        
        @param row : current row of the grid control
        @param col : current column of the grid control
        @param grid: grid control object
        """
        self.startValue = grid.GetTable().GetValue(row, col)
        self._tc.SetValue(self.startValue)
      #  self._tc.SetInsertionPointEnd()
      #  self._tc.SetFocus()
      #  self._tc.SetSelection(0, self._tc.GetLastPosition())
    
    def EndEdit(self, row, col, grid):
        """
        This method is called when editing ends in text control. 
        
        @param row : current row of the grid control
        @param col : current column of the grid control
        @param grid: grid control object
        """
        changed = False
        val = self._tc.GetValue()
        if val != self.startValue:
            changed = True
            grid.GetTable().SetValue(row, col, val) # update the table
        self.startValue = ''
        self._tc.SetValue('')
        return changed
    
    def Reset(self):
        """
        This method is called when editing cancelled in text control. 
        old value is restored in text contol.
        """
        self._tc.SetValue(self.startValue)
       # self._tc.SetInsertionPointEnd()
    
    def Clone(self):
        return myCellEditor()
    
    def StartingKey(self, evt):
        self.OnChar(evt)
        if evt.GetSkipped():
            self._tc.EmulateKeyPress(evt)
    
    def OnChar(self, evt):
        """
        This is the event handler for the text control inside each cell of the grid control. 
        This method allows only one value (digit/alphabet/operator) for each cell. 
        
        @param evt : event object
        """
        key = evt.GetKeyCode()              # Get the key code
        
        if key in range(256):
            char = chr(key)
        
            if char in string.letters:
                char = char.lower()
                self._tc.SetValue(char)

            elif key in range(48,58):
                self._tc.SetValue(char)

        else:
            evt.Skip()
        
        """elif   key == wx.WXK_DOWN:
            self._grid.DisableCellEditControl()     # Commit the edit
            self._grid.MoveCursorDown(False)        # Change the current cell
        elif key == wx.WXK_UP:
            self._grid.DisableCellEditControl()     # Commit the edit
            self._grid.MoveCursorUp(False)          # Change the current cell
        elif key == wx.WXK_LEFT:
            self._grid.DisableCellEditControl()     # Commit the edit
            self._grid.MoveCursorLeft(False)        # Change the current cell
        elif key == wx.WXK_RIGHT:
            self._grid.DisableCellEditControl()     # Commit the edit
            self._grid.MoveCursorRight(False)       # Change the current cell

        """
        
	        
    def Destroy(self):
        """ Final cleanup
        
            NOTE: There is no need to everride this if you don't need
            to do something out of the ordinary.
        """
        super(myCellEditor, self).Destroy()

#---------------------------------------------------------------------------
