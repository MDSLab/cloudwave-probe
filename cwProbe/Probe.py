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

@author: UniMe Team - Nicola Peditto <npeditto@unime.it>
'''


__author__="UniMe Team: Nicola Peditto"



import httplib2 
import json
import os,signal,sys
from qpid.messaging import *
from qpid.log import enable, DEBUG, INFO
from stevedore import extension, named
import pkg_resources
from ctypes import *

#CloudWave libraries:
from pyyamllib import PyYamlLib
from pyloglib import PyLogLib
from cwconfparser import cwconfparser  

#GLOBAL variables:
ACTIVE_LOG=False

class Metric (object):
    """
    Metric class
    """ 
    def __init__(self, volume, timestamp, name, unit, type, additional_metadata):
        '''
        Constructor
        @param    volume    value of the metric (Numeric: no string!!!)
        @param    timestamp    timestamp of the metric (String: application's format)
        @param    name    name of the metric (String)
        @param    unit    unit of the metric (String)
        @param    type    Openstack's metric type (gauge, cumulative, delta) (String)
        @param    additional_metadata    JSON user metadata (JSON object)
        ''' 

        self.volume = volume
        self.timestamp=timestamp
        self.name=name
        self.unit=unit
        self.ev_type = "measure"
        self.source_type = "vm"
        self.type = type
        self.additional_metadata = additional_metadata
          



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
        
        self.conf_file="/opt/cloudwave/cwprobe/cwprobe.conf" #"cwprobe.confg"  
        
        self.logfile="/var/log/cloudwave/cwprobe.log"
        self.logpath="/var/log/cloudwave/"
        self.logtag="cwProbe"
        self.logger=None
        
        #LOAD PROBE'S CONFIGURATIONS
        self.loadConfig()

        #LOAD PROBE'S PLUGINS
        self.pluginsLoader()
    
        
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


            self.logconfig=cwconfparser.getOptions(self.conf_file,"logging")
            self.logfile=self.logconfig["logfile"] 
            print "Logfile: "+self.logfile

            self.logger=PyLogLib.PyLogLib(self.logtag, filename=self.logfile)
            self.logger.info("Logfile: "+self.logfile)
            self.logger.info("cwProbe logging configured!")
        
            #Get injected parameters from Openstack script          
            self.config=cwconfparser.getOptions(self.conf_file,"openstack_info")
            self.logger.info("Parsing configuration file completed!")
            
            #Get compute hostname
            self.compute=self.config["compute"] #"ing-res-04"   
            print "Compute: "+self.compute
            self.logger.debug("Compute: "+self.compute)
            
            #Get compute qpid server IP
            self.qpid_server_ip=self.config["qpid_server_ip"]
            
            #Set Qpid logging level
            enable("qpid.messaging.io", INFO)
            
            """
            http = httplib2.Http()
            response, content=http.request('http://169.254.169.254/openstack/latest/meta_data.json',"GET")
            #print "Server response:", json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
            #print "CONTENT: " + content
            data = json.loads(content)
            self.instance_name = data['uuid']
            """
            self.instance_name = self.getInstanceUUID()
            
            print "Instance: "+self.instance_name
            self.logger.info("Instance: "+self.instance_name)
            
            """  
            #.SO LIBRARY MANAGEMENT
            print "CW .so loading..."
            self.lib=cdll.LoadLibrary("libcloudwave.so")
            self.lib.CloudWave_SO_Init()
            self.logger.info("CW .so loaded!")
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
            #.SO LIBRARY MANAGEMENT            
            print "CW .so loading..."
            self.lib=cdll.LoadLibrary("libcloudwave.so")
            self.lib.CloudWave_SO_Init()
            self.logger.info("CW .so loaded!")

            extension.ExtensionManager(
                    namespace='cwprobe.plugins.monitors',
                    invoke_on_load=True,
                    invoke_args=(self,),
            )

        """
        #Selective plugin loader through yaml file
        
        active_plugins=PyYamlLib.PyYamlLib("configProbe.yaml").getYamlList("probe_plugins","plugin")
        print "cwProbe PLUGINs loaded:\n\t"+str(active_plugins)

        named.NamedExtensionManager(
            namespace='cwprobe.plugins.monitors',
            names=active_plugins,
            invoke_on_load=True,
            invoke_args=(self,),
        )
      
        extension.ExtensionManager(
            namespace='cwprobe.plugins.monitors',
            invoke_on_load=True,
            invoke_args=(self,),
        )


       """ 
        
    """  
    #DON'T USE IT      
    def sendMeasureQpid(self, broker, amq_topic, data="No data"):
       
        connection = Connection(broker)
        
        try:
            connection.open()
            session = connection.session()
            sender = session.sender(amq_topic)
            sender.send(Message(data))
            session.acknowledge()
        
            print "DATA send to Ceilometer: "+data
            self.logger.info("DATA sent to Ceilometer: "+data)
            
        except MessagingError,m:
            print m
            
        finally:
            connection.close()
        
    """    



    def sendMeasure(self, metric):
        '''
        .SO sender measures.
        @param    data    Json message with the measure

        '''

        #additional_metadata = '{"cloudwave":{"geo_meter":{"lat":"38.269185", "long":"15.626249"}, "meter_dest":"ceiloesper"}}'
        #print str(type(metric.volume)) + " " +metric.volume
        if type(metric.volume) is float:
            #print "Float metric"
            self.lib.record_metric_longlong( 0, str(metric.name), str(metric.additional_metadata), str(metric.unit), 0, long(metric.volume))

        elif type(metric.volume) is int:
            #print "Int metric"
            self.lib.record_metric_longlong( 0, str(metric.name), str(metric.additional_metadata), str(metric.unit), 0, metric.volume)

        elif type(metric.volume) is str:
            #print "String metric"
            #self.lib.record_metric_string( 0, str(metric.name), str(metric.additional_metadata), str(metric.unit), 0, str(metric.volume))
            self.lib.record_metric_longlong( 0, str(metric.name), str(metric.additional_metadata), str(metric.unit), 0, metric.volume)

        elif type(metric.volume) is long:
            #print "Long metric"
            self.lib.record_metric_longlong( 0, str(metric.name), str(metric.additional_metadata), str(metric.unit), 0, metric.volume)

        else:
            print "SAMPLE NO SENT!"
            self.logger.info("SAMPLE NO SENT!")




        """     
        add_meta = json.loads('{"md":"ce"}')
        print add_meta
        #self.lib.record_metric_longlong( 0, str(metric.name), str(add_meta), str(metric.unit), 0, metric.volume)
        """
        print "Metric sent to Ceilometer: "+str(metric.name)+" - "+str(metric.volume)+" "+str(metric.unit)
        #self.logger.info("DATA sent to Ceilometer: "+str(metric.name)+" - "+str(metric.volume)+" "+str(metric.unit))


        


    
            
                
def startProbe():
        '''
        Start method for init.d script.
        '''     
        probe=Probe()
        
        
        
"""    """
if __name__ == "__main__":    

    probe=Probe()
