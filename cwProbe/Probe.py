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
Created on 16/giu/2014

@author: Nicola Peditto <npeditto@unime.it>
'''


__author__="UniMe Team: Nicola Peditto"



import httplib2 
import json
import os,signal,sys
from stevedore import extension, named
import pkg_resources
from ctypes import *

#CloudWave libraries:
#from pyyamllib import PyYamlLib
from pyloglib import PyLogLib
from cwconfparser import cwconfparser  


#GLOBAL variables:
ACTIVE_LOG=False

class Metric (object):
    """
    Metric class
    """ 
    #def __init__(self, volume, timestamp, name, unit, type, source_type, additional_metadata):
    def __init__(self,name,value,unit,type='m',ceilometer_type='g',refered_to='a',metadata='{\"meta\":\"data\"}'):
        '''
        Constructor
        @param    volume:    value of the metric (Numeric: no string!!!)
        @param    name:    name of the metric (String)
        @param    unit:    unit of the metric (String)
        
        @param    type:    Openstack's metric type (0:gauge, 1:delta or 2:cumulative) (int)
        @param    source_type: metric's source type (0:application or 1:VM) (int)
        @param    additional_metadata:    JSON user metadata (JSON object)
        ''' 
        self.name = name
        self.value = value
        self.unit = unit
        
        self.type= type
        self.ceilometer_type = ceilometer_type
        self.refered_to = refered_to
        self.metadata = metadata
        
          



class Probe(object):
    """
    Probe class
    """      

 
    def __init__(self):
        '''
        Constructor
        '''   
        print "INIT cwProbe!"
        
        self.config=None
        self.logconfig=None
        
        self.conf_file= "/opt/cloudwave/cwprobe/cwprobe.conf" 
        
        self.logfile="cwprobe.log"
        self.logpath="/var/log/cloudwave/"
        self.logtag="cwProbe"
        self.logger=None
        
        #LOAD PROBE'S CONFIGURATIONS
        self.loadConfig()

        #LOAD PROBE'S PLUGINS
        self.pluginsLoader()
        
        self.loop_time=10 #default value
    
        
    def loadConfig(self):
        '''
        Probe configuration file parser method.
        '''       
        
        if self.checkConfig():
            
            print "Loading probe configuration!"
            
            if not os.path.exists(self.logpath):
                #os.chmod("/var/log/", 0777)
                os.makedirs(self.logpath)
                #os.chmod(self.logpath, 0777)

            if not os.path.isfile(self.logfile):
                open(self.logfile, "a")

            self.loop_time=cwconfparser.getOptions(self.conf_file,"probe")['loop_time']
            print "Loop time: "+self.loop_time
            
            self.logconfig=cwconfparser.getOptions(self.conf_file,"logging")
            self.logfile=self.logconfig["logfile"] 
            print "Logfile: "+self.logfile
            
            self.logger=PyLogLib.PyLogLib(self.logtag, filename=self.logfile)
            self.logger.info("Logfile: "+self.logfile)
            self.logger.info("cwProbe logging configured!")
            
            """
            self.instance_name = self.getInstanceUUID()
            print "Instance: "+self.instance_name
            self.logger.info("Instance: "+self.instance_name)
            """
            
            
            self.logger.info("END cwProbe configuration!")

        else:
            print "No configuration file...EXIT!"
            sys.exit()
            


    def checkConfig(self):
        '''
        Method to check the presence of probe configuration file
        '''           
        return os.path.isfile(self.conf_file)


    def getInstanceUUID(self):
        '''
        Method to get instance UUID through Openstack REST API
        '''   
        http = httplib2.Http()
        response, content=http.request('http://169.254.169.254/openstack/latest/meta_data.json',"GET")
        #print "Server response:", json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
        #print "CONTENT: " + content
        data = json.loads(content)
        return data['uuid']


    def pluginsLoader(self):
        '''
        Plugin loader method thorugh stevedore libraries.
        '''          
        print "Available plugins: "
       
        ep=[] 
        #named_objects = []
        for ep in pkg_resources.iter_entry_points(group='cwprobe.plugins.monitors'):
            print "\t "+str(ep)
            #named_objects.append(ep.load())
    
        if not ep:
            print "No plugins available!"
            self.logger.info("No plugins available!")
            sys.exit()
    
        else:
            extension.ExtensionManager(
                    namespace='cwprobe.plugins.monitors',
                    invoke_on_load=True,
                    invoke_args=(self,),
            )

            
                
def startProbe():
        '''
        Start method for init.d script.
        '''     
        probe=Probe()
        
        
        

if __name__ == "__main__":    
    probe=Probe()
