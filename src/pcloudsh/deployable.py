#
# Copyright (C) 2011 Red Hat, Inc.
#
# Author: Steven Dake <sdake@redhat.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
import os
import time
import re
import random
import logging
import libxml2
import exceptions

class Deployable(object):

    def __init__(self):
        try:
            self.doc = libxml2.parseFile('db_deployable.xml')
            self.doc_images = self.doc.getRootElement()
	except:
            self.doc = libxml2.newDoc ("1.0")
            self.doc.newChild(None, "deployables", None); 
            self.doc_images = self.doc.getRootElement()

    def create(self, name):
        deployable_path = self.doc_images.newChild (None, "deployable", None); 
        deployable_path.newProp("name", name); 
        self.doc.serialize(None, 1)
	self.doc.saveFile ('db_deployable.xml');

    def assembly_add(self, deployable_name, assembly_name):
        deployable_path = self.doc.xpathEval("/deployables/deployable[@name='%s']" % deployable_name)
	root_node = deployable_path[0]
        assembly_root = root_node.newChild(None, "assembly", None); 
        assembly_root.newProp("name", assembly_name); 
	self.doc.saveFile ('db_deployable.xml');

    def assembly_remove(self, deployable_name, assembly_name):
        deployable_path = self.doc.xpathEval("/deployables/deployable/assembly[@name='%s']" % assembly_name)
	root_node = deployable_path[0]
        root_node.unlinkNode();
        self.doc.saveFile ('db_deployable.xml');

    def list(self, listiter):
        deployable_list = self.doc.xpathEval("/deployables/deployable")
	for deployable_data in deployable_list:
            listiter.append("%s" % (deployable_data.prop('name')))