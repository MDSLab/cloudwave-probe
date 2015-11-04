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

from plugins import CwPluginBase


#USER IMPORT
import time
import datetime


class Cwpl_Test(CwPluginBase.CwPluginBase):
    
    
    def __init__(self, probe):
        print 'INIT plugin: CW TEST.'
        
        super(Cwpl_Test, self).__init__()
        
        self.name="TestPlugin"
        self.probe=probe
        
        self.start()    


    def run(self):
        
        print "\t"+self.name+" plugin started"   
        
        self.main()

    
    def main(self): 
             
        print "\tTest sender plugin..."
        
        print "INSTANCE NAME: "+self.probe.instance_name
        

                
        while(1):
            
            #DATA GET FROM YOUR APPLICATION!!!!
            ################################################################################################################################################
            #Additional application specific data. NB: "meter_dest" is necessary for Ceiloesper management
            additional_metadata = '{"geo_meter":{"lat":"38.269185", "long":"15.626249"}, "meter_dest":"ceiloesper"}' 

            m_name="fake_measure" #measure name
            m_unit="num"    #measure unit
            m_volume = "4000"   #measure value
            
            #Application timestamp different from Openstack timestamp!
            m_st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') 
            ################################################################################################################################################

            #JSON Message sent to Cloudwave Pollster on Ceilometer compute agent
            data='{"probe_inst":"'+self.probe.instance_name+'","volume":'+str(m_volume)+',"timestamp":"'+m_st+'","name":"'+m_name+'", "unit":"'+m_unit+'", "ev_type":"measure", "source_type":"vm", "type":"'+self.TYPE_GAUGE+'", "additional_metadata":'+additional_metadata+' }'

            #AMQP queue namespace
            amq_topic = "cloudwave."+self.probe.compute+"."+self.probe.instance_name
            
            #AMQP server address
            broker = self.probe.qpid_server_ip + ":5672"
            
            #Probe method to send qpid messagge with the application measure
            self.probe.sendMeasureQpid(broker, amq_topic, data)            
            
            print "\n\n Send measure: " + data
            
            #Measure sent each 10 seconds for example!
            time.sleep(10)
            
          
            
            
