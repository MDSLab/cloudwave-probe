# Copyright 2014 University of Messina (UniMe)
#
# Authors: Nicola Peditto <npeditto@unime.it>, Fabio Verboso <fverboso@unime.it>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
Created on 18/lug/2014

@authors: Nicola Peditto <npeditto@unime.it>, Fabio Verboso <fverboso@unime.it>
'''

__author__="UniMe Team: Nicola Peditto"

import abc
import threading
import subprocess

path_sender='/opt/cloudwave/cw-so/staging/test/send'


class CwPluginBase(threading.Thread):
    """
    Base class for each cwProbe plugin.
    """
    
    __metaclass__ = abc.ABCMeta
    
 
    def __init__(self):
        '''
        Costructor
        @param    probe    probe object 
        '''        
        
        #print "\tINIT plugin base class."
        
        threading.Thread.__init__(self) 
        #self.setDaemon(1)
        self.name=""
        #self.probe=probe
        
        
        
    
    @abc.abstractmethod
    def run(self):
        """ run thread """
       

    @abc.abstractmethod
    def main(self):
        """Main plugin method."""
        
    #def send_metric(self,name,value,unit,type='m',ceilometer_type='g',refered_to='a',metadata='{\"meta\":\"data\"}'):
    def send_metric(self,metric):
        metric.type_value='c'
        if isinstance(metric.value,int):
                metric.type_value='i'
        elif isinstance(metric.value,long) or isinstance(metric.value,float):
                metric.type_value='d'
        bashCommand = "%s %s %s %s %s %s %s %s " % (path_sender,metric.type,metric.type_value,str(metric.value),metric.refered_to,metric.name,metric.unit,metric.ceilometer_type)
        bashCommand = bashCommand+metric.metadata
        print metric.name,metric.value,metric.unit
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        process.wait()
        output = process.communicate()[0]




