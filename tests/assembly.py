#
# Copyright (C) 2011 Red Hat, Inc.
#
# Author: Angus Salkeld <asalkeld@redhat.com>
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
import time
from oz.Fedora import FedoraGuest
import oz.TDL
import libxml2

class Assembly(FedoraGuest):
    def __init__(self, name, number, config, tdl):
        self.name = name
        self.number = number

        tdl_filename = '%s/%d.tdl' % (name, number)
        kickstart_filename = '%s/%d.ks' % (name, number)
        self.libvirt_filename = '%s/%d.xml' % (name, number)

        FedoraGuest.__init__(self, tdl, config, kickstart_filename,
                "virtio", True, "virtio", True)

        self.libvirt_xml = open(self.libvirt_filename, 'r').read()
        self.libvirt_dom = None
        self.guestaddr = None

    def stop(self):
        self.shutdown_guest(self.guestaddr, self.libvirt_dom)
        self.collect_teardown(self.libvirt_xml)

    def __del__(self):
        self.stop()

    def rsh(self, command):
        if self.guestaddr is None:
            retcode = 1
            stdout = 'call start first'
        else:
            stdout, stderr, retcode = self.guest_execute_command(self.guestaddr, command)
        return (retcode, stdout)

    def fix_network(self):

        doc = libxml2.parseMemory(self.libvirt_xml, len(self.libvirt_xml))

        interface = doc.xpathEval('/domain/devices/interface')
        if len(interface) != 1:
            print "no interfaces"
            exit()
        interface[0].setProp('type', 'network')

        source = doc.xpathEval('/domain/devices/interface/source')
        if len(source) != 1:
            print "no source"
            exit()
        source[0].unsetProp('bridge')
        source[0].setProp('network', 'dhcp')

        print doc.serialize(format=1)

        doc.freeDoc()


    def start(self):

        self.fix_network()

        self.collect_setup(self.libvirt_xml)

        self.libvirt_dom = self.libvirt_conn.createXML(self.libvirt_xml, 0)

        self.guestaddr = self.wait_for_guest_boot()
