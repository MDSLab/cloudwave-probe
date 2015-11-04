# Copyright 2014 University of Messina (UniMe)
#
# Author: Nicola Peditto <npeditto@unime.it>
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

@author: UniMe Team - Nicola Peditto <npeditto@unime.it>
'''

__author__="UniMe Team: Nicola Peditto"

import abc
import threading


class CwPluginBase(threading.Thread):
    """
    Base class for each cwProbe plugin.
    """
    
    __metaclass__ = abc.ABCMeta
    
 
    #def __init__(self, probe):
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
        
        self.TYPE_GAUGE = 'gauge'
        self.TYPE_DELTA = 'delta'
        self.TYPE_CUMULATIVE = 'cumulative'
        self.TYPES = (self.TYPE_GAUGE, self.TYPE_DELTA, self.TYPE_CUMULATIVE)
        
        
        
    
    @abc.abstractmethod
    def run(self):
        """ run thread """
       

    @abc.abstractmethod
    def main(self):
        """Main plugin method."""




