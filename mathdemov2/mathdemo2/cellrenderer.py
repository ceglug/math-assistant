"""
wx.grid is one of the complex control in WxPython toolkit.
We are tuning this grid control for working math problems
To display symbols there is a need for Painting over grid control
Custom renderer is used to retain the symbol output dynamically
This custom class used to modify the grid control and also fulfils our requirement to perform math operations.
 

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
import random

#-------------------------------------------------------------------------------

class mycrossrenderer(wx.grid.PyGridCellRenderer):
    """
    This class is used as the custom renderer class for the cross symbol.
    This class is used to draw a B{cross} symbol inside a cell in the grid control.
    """
    def __init__(self):
        """
        This is the constructor method for this class
        """
	wx.grid.PyGridCellRenderer.__init__(self)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """
        This method is used to draw the cross symbol inside current cell.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param rect      : rectangle parameters of the text control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        @param isSelected: boolean value for isSelected
        """
        text = grid.GetCellValue(row, col)
        hAlign, vAlign = attr.GetAlignment()
        dc.SetFont( attr.GetFont())
               
        x1 , y1 = rect.GetBottomLeft()
        x2 , y2 = rect.GetTopRight()
        dc.SetTextBackground(wx.WHITE)
        dc.SetTextForeground(wx.BLACK)
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)              # if enabled not working
        dc.DrawRectangleRect(rect)
        grid.DrawTextRectangle(dc, text, rect, hAlign, vAlign)
        dc.Pen = wx.Pen(wx.BLUE,2)
        
        dc.DrawLine(x1+2,y1-2,x2-2,y2+2)
        
  
    def GetBestSize(self, grid, attr, dc, row, col):
        """
        This method is used get the dimensions to place the renderer value.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        """
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)

    def Clone(self):
        """
        This method returns an object of this renderer class
        """
        return mycrossrenderer()


#-------------------------------------------------------------------------------

class mydivrenderer(wx.grid.PyGridCellRenderer):
    """
    This class is used as the custom renderer class for the division symbol.
    This class is used to draw a B{DIV} symbol inside a cell in the grid control.
    """
    
    def __init__(self):
        """
        This is the constructor method for this class
        """
	wx.grid.PyGridCellRenderer.__init__(self)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """
        This method is used to draw the division symbol inside current cell.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param rect      : rectangle parameters of the text control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        @param isSelected: boolean value for isSelected
        """
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)              # if enabled not working
        dc.DrawRectangleRect(rect)
        dc.Pen = wx.Pen(wx.RED,3)
        
        x1 , y1 = rect.GetTopLeft()
        wd , ht = rect.GetSize()
        l1 = x1 + (wd/2) 
        l2 = y1 + ht
        l3 = x1 + (wd/2) 
        l4 = y1 + (ht/2) - 1
        dc.DrawLine(l1,l2,l3,l4)

        l1 = l3
        l2 = l4
        l3 = x1 + wd
        l4 = l4
        dc.DrawLine(l1,l2,l3,l4)

  
    def GetBestSize(self, grid, attr, dc, row, col):
        """
        This method is used get the dimensions to place the renderer value.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        """
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)

    def Clone(self):
        """
        This method returns an object of this renderer class
        """
        return mydivrenderer()


#-------------------------------------------------------------------------------

class mylcmrenderer(wx.grid.PyGridCellRenderer):
    """
    This class is used as the custom renderer class for the lcm symbol.
    This class is used to draw a B{LCM} symbol inside a cell in the grid control.
    """
    def __init__(self):
        """
        This is the constructor method for this class
        """
	wx.grid.PyGridCellRenderer.__init__(self)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """
        This method is used to draw the lcm symbol inside current cell.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param rect      : rectangle parameters of the text control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        @param isSelected: boolean value for isSelected
        """
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)              # if enabled not working
        dc.DrawRectangleRect(rect)
        dc.Pen = wx.Pen(wx.RED,3)
        
        x1 , y1 = rect.GetTopLeft()
        wd , ht = rect.GetSize()
        l1 = x1 + (wd/2) 
        l2 = y1 
        l3 = x1 + (wd/2) 
        l4 = y1 + (ht/2) - 1
        dc.DrawLine(l1,l2,l3,l4)

        l1 = l3
        l2 = l4
        l3 = x1 + wd
        l4 = l4
        dc.DrawLine(l1,l2,l3,l4)
  
    def GetBestSize(self, grid, attr, dc, row, col):
        """
        This method is used get the dimensions to place the renderer value.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        """
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)

    def Clone(self):
        """
        This method returns an object of this renderer class
        """
        return mylcmrenderer()


#-------------------------------------------------------------------------------

class myVbyrenderer(wx.grid.PyGridCellRenderer):
    """
    This class is used as the custom renderer class for the vertical BY symbol.
    This class is used to draw a vertical BY symbol inside a cell in the grid control.
    """
    def __init__(self):
        """
        This is the constructor method for this class
        """	
	wx.grid.PyGridCellRenderer.__init__(self)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """
        This method is used to draw the vertical BY symbol inside current cell.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param rect      : rectangle parameters of the text control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        @param isSelected: boolean value for isSelected
        """
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)              # if enabled not working
        dc.DrawRectangleRect(rect)
        dc.Pen = wx.Pen(wx.RED,3)
        
        x1 , y1 = rect.GetBottomLeft()
        wd , ht = rect.GetSize()
        l1 = x1 + (wd/2) 
        l2 = y1 - ht
        l3 = l1 
        l4 = y1
        dc.DrawLine(l1,l2,l3,l4)
  
    def GetBestSize(self, grid, attr, dc, row, col):
        """
        This method is used get the dimensions to place the renderer value.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        """
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)

    def Clone(self):
        """
        This method returns an object of this renderer class
        """
        return myVbyrenderer()


#-------------------------------------------------------------------------------

class myHbyrenderer(wx.grid.PyGridCellRenderer):
    """
    This class is used as the custom renderer class for the horizontal BY symbol.
    This class is used to draw a horizontal B{BY} symbol inside a cell in the grid control.
    """
    def __init__(self):
        """
        This is the constructor method for this class
        """	
	wx.grid.PyGridCellRenderer.__init__(self)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """
        This method is used to draw the horizontal BY symbol inside current cell.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param rect      : rectangle parameters of the text control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        @param isSelected: boolean value for isSelected
        """
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)              # if enabled not working
        dc.DrawRectangleRect(rect)
        dc.Pen = wx.Pen(wx.RED,3)
        
        x1 , y1 = rect.GetBottomLeft()
        wd , ht = rect.GetSize()
        l1 = x1
        l2 = y1 - (ht/2)
        l3 = x1 + wd 
        l4 = l2
        dc.DrawLine(l1,l2,l3,l4)
      
  
    def GetBestSize(self, grid, attr, dc, row, col):
        """
        This method is used get the dimensions to place the renderer value.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        """
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)

    def Clone(self):
        """
        This method returns an object of this renderer class
        """
        return myHbyrenderer()


#-------------------------------------------------------------------------------
class myHtextbyrenderer(wx.grid.PyGridCellRenderer):
    """
    This class is used as the custom renderer class for the BY symbol.
    This class is used to draw a horizontal B{BY} symbol over text inside a cell in the grid control.
    """
    def __init__(self):
        """
        This is the constructor method for this class
        """	
	wx.grid.PyGridCellRenderer.__init__(self)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """
        This method is used to draw the horizontal BY symbol over text inside current cell.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param rect      : rectangle parameters of the text control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        @param isSelected: boolean value for isSelected
        """
        text = grid.GetCellValue(row, col)
        hAlign, vAlign = attr.GetAlignment()
        dc.SetFont( attr.GetFont())
               
        dc.SetTextBackground(wx.WHITE)
        dc.SetTextForeground(wx.BLACK)
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)              # if enabled not working
        dc.DrawRectangleRect(rect)
        grid.DrawTextRectangle(dc, text, rect, hAlign, vAlign)
        dc.Pen = wx.Pen(wx.RED,3)
        
        x1 , y1 = rect.GetBottomLeft()
        wd , ht = rect.GetSize()
        l1 = x1
        l2 = y1 - (ht/2)
        l3 = x1 + wd 
        l4 = l2
        dc.DrawLine(l1,l2,l3,l4)
                
  
    def GetBestSize(self, grid, attr, dc, row, col):
        """
        This method is used get the dimensions to place the renderer value.
        
        @param grid      : grid control object
        @param attr      : custom attribute object of the grid control
        @param dc        : device context to paint over grid control
        @param row       : current row of the grid cursor
        @param col       : current column of the grid cursor
        """
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)

    def Clone(self):
        """
        This method returns an object of this renderer class
        """
        return myHtextbyrenderer()


#-------------------------------------------------------------------------------