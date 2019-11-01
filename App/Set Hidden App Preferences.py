#MenuTitle: Set Hidden App Preferences
# -*- coding: utf-8 -*-
__doc__="""
GUI for a number of hidden prefs, hard to memorize otherwise.
"""

import vanilla
from AppKit import NSFont

class SetHiddenAppPreferences( object ):
	prefs = (
		"AppleLanguages",
		"drawShadowAccents",
		"GSftxenhancerPath",
		"GSKerningIncrementHigh",
		"GSKerningIncrementLow",
		"GSShowVersionNumberInDockIcon",
		"GSShowVersionNumberInTitleBar",
		"GSSpacingIncrementHigh",
		"GSSpacingIncrementLow",
		"MacroCodeFontSize",
		"TextModeNumbersThreshold",
		"TTPreviewAlsoShowOffCurveIndexes",
		"GSFontViewDarkMode",
		"GSEditViewDarkMode",
		"com.mekkablue.ShowItalic.drawItalicsForInactiveGlyphs",
	)
	
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 350
		windowHeight = 110
		windowWidthResize  = 500 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Set Hidden App Preferences", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.mekkablue.SetHiddenAppPreferences.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		linePos, inset, lineHeight = 8, 12, 22
		self.w.descriptionText = vanilla.TextBox( (inset, linePos+2, -inset, 14), "Choose and apply the app defaults:", sizeStyle='small', selectable=True )
		linePos += lineHeight
		
		self.w.pref = vanilla.ComboBox( (inset, linePos-2, -inset-100, 25), self.prefs, callback=self.SavePreferences, sizeStyle='regular' )
		self.w.pref.getNSComboBox().setFont_(NSFont.userFixedPitchFontOfSize_(11))
		self.w.pref.getNSComboBox().setToolTip_("Pick an app default from the list, or type in an identifier.")
		
		self.w.prefValue = vanilla.EditText( (-inset-90, linePos, -inset, 21), "", sizeStyle='regular' )
		self.w.prefValue.getNSTextField().setToolTip_("Enter a value for the chosen app default.")
		linePos += lineHeight
		
		# Run Button:
		self.w.delButton = vanilla.Button( (-170-inset, -20-inset, -90-inset, -inset), "Reset", sizeStyle='regular', callback=self.SetHiddenAppPreferencesMain )
		self.w.delButton.getNSButton().setToolTip_("Will delete the setting, effectively resetting it to its default.")
		
		self.w.runButton = vanilla.Button( (-80-inset, -20-inset, -inset, -inset), "Apply", sizeStyle='regular', callback=self.SetHiddenAppPreferencesMain )
		self.w.runButton.getNSButton().setToolTip_("Sets the entered value for the chosen app default.")
		self.w.setDefaultButton( self.w.runButton )
		
		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Set Hidden App Preferences' could not load preferences. Will resort to defaults"
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def updatePrefValue( self, sender ):
		self.w.prefValue.set( Glyphs.defaults[self.w.pref.get()] )
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.mekkablue.SetHiddenAppPreferences.pref"] = self.w.pref.get()
			
			if sender == self.w.pref:
				self.updatePrefValue(None)
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			Glyphs.registerDefault("com.mekkablue.SetHiddenAppPreferences.pref", "")
			self.w.pref.set( Glyphs.defaults["com.mekkablue.SetHiddenAppPreferences.pref"] )
			self.updatePrefValue(None)
		except:
			return False
			
		return True

	def SetHiddenAppPreferencesMain( self, sender ):
		try:
			if not self.SavePreferences( self ):
				print "Note: 'Set Hidden App Preferences' could not write preferences."
			
			if sender == self.w.delButton:
				del Glyphs.defaults[ self.w.pref.get() ]
				self.w.prefValue.set( None )
				print "Deleted pref: %s" % self.w.pref.get()
				
			elif sender == self.w.runButton:
				Glyphs.defaults[ self.w.pref.get() ] = self.w.prefValue.get()
				print "Set pref: %s --> %s" % (self.w.pref.get(), self.w.prefValue.get())
				
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Set Hidden App Preferences Error: %s" % e
			import traceback
			print traceback.format_exc()

SetHiddenAppPreferences()