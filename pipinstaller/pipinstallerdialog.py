# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PipinstallerDialog
                                 A QGIS plugin
 A sperimental plugin to install python modules through pip module
                             -------------------
        begin                : 2014-03-03
        copyright            : (C) 2014 by Luca Mandolesi
        email                : pyarchinit@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os, sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_pipinstaller import Ui_Pipinstaller

# create the dialog for zoom to point



class PipinstallerDialog(QtGui.QDialog, Ui_Pipinstaller):
	plugin_dir = ""
	OSGEOENVIRON = os.environ['OSGEO4W_ROOT']
	PIPINSTALLED_first = 0
	def __init__(self):
		QtGui.QDialog.__init__(self)
		# Set up the user interface from Designer.
		# After setupUI you can access any designer object by doing
		# self.<objectname>, and you can use autoconnect slots - see
		# http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
		# #widgets-and-dialogs-with-auto-connect
##		self.installationpip()

		self.setupUi(self)
		self.pushButton_try_to_install.clicked.connect(self.onClick)
		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		plugin_dir_rel_path = os.path.join(os.sep,'.qgis2', 'python', 'plugins','pipinstaller')
		self.plugin_dir = ('%s%s') % (home,plugin_dir_rel_path)
		result_installation = self.try_install_setuptools()
		if result_installation == 1:
			QMessageBox.warning(self, "Alert!","Please restart Qgis to run pipinstaller." , QMessageBox.Ok)


	def try_install_setuptools(self):
		try:
			import easy_install
		except:
			cmd = ('%s\Osgeo4W.bat python %s/ez_setup.py') % (self.OSGEOENVIRON, self.plugin_dir) #installa easy_install ma richiede un riavvio di Qgis
			self.proc = QProcess()
			self.proc.start(cmd)
			self.proc.setProcessChannelMode(QProcess.MergedChannels);
			QObject.connect(self.proc, SIGNAL("readyReadStandardOutput()"), self, SLOT("readStdOutput()"));
			self.textEdit_output.append(str("Please retart Qgis and run easy_install pip"))
			return 1

	@pyqtSlot()
	def readStdOutput(self):
		self.textEdit_output.append(str(self.proc.readAllStandardOutput()))


	def onClick(self):
		try:
			import pip
			#after installing easy_install run in command line easy_install pip
			command_line = self.lineEdit_package_name.text()
			cmd = ('%s\OSGeo4W.bat %s') % (self.OSGEOENVIRON,command_line)
			#cmd =  "C:\\PROGRA~2\\QGISDU~1\\OSGeo4W.bat pip install %s" % package_name
			self.proc = QProcess()
			self.proc.start(cmd)
			self.proc.setProcessChannelMode(QProcess.MergedChannels);
			QObject.connect(self.proc, SIGNAL("readyReadStandardOutput()"), self, SLOT("readStdOutput()"));
		except:
			QMessageBox.warning(self, "Alert!","""Module pip will be installed. Please restart Qgis.""" , QMessageBox.Ok)
			cmd = ('%s\Osgeo4W.bat easy_install pip') % (self.OSGEOENVIRON) #installa easy_install ma richiede un riavvio di Qgis
			self.proc = QProcess()
			self.proc.start(cmd)
			self.proc.setProcessChannelMode(QProcess.MergedChannels);
			QObject.connect(self.proc, SIGNAL("readyReadStandardOutput()"), self, SLOT("readStdOutput()"));
			self.PIPINSTALLED_first = 1
