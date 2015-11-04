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
from cwProbe.Probe import Metric


#USER IMPORT
import MySQLdb
import time


class Cwpl_MyCheckPoint(CwPluginBase.CwPluginBase):


    def __init__(self, probe):
        print 'INIT plugin: CW Mycheckpoint.'
        
        super(Cwpl_MyCheckPoint, self).__init__()
        
        self.name="MyCheckPoint"
        self.probe=probe
        
        self.start()
        

    def run(self):
        print "\t"+self.name+" plugin started"   
        self.main()
                
                
                
                
    def main(self):
        """Main plugin method."""
        
        print "Sending Mycheckpoint measures..."
        
        m_name="wp:th_con" #measure name
        m_unit="conn"    #measure unit

        db = MySQLdb.connect(
                                 host="10.8.21.6",  # your host, usually localhost
                                 user="root",       # your username
                                 passwd="root",     # your password
                                 db="mycheckpoint") # name of the database
        
        while(1):
        
            try:
                # you must create a Cursor object. It will let you execute all the queries you need
                cur = db.cursor() 
                
                #db.begin()
        
                # Use all the SQL you like
                cur.execute("SELECT ts, threads_connected FROM mycheckpoint.sv_report_sample ORDER BY ts DESC LIMIT 1 ;")
                
                # print all the first cell of all the rows
                for row in cur.fetchall() :
                    
                    print "\n\nTimestamp:", row[0] , "--> MYSQL connections: " , row[1]
                    
                    #DATA GET FROM APPLICATION!!!!
                    m_volume = row[1]   #measure value
                    #Application timestamp different from Openstack timestamp!
                    m_st = row[0] 
                    #Additional application specific data. NB: "meter_dest" is necessary for Ceiloesper management
                    additional_metadata = '{"geo_meter":{"lat":"38.269185", "long":"15.626249"}, "meter_dest":"ceiloesper"}' 
                    #additional_metadata = '{cloudwave:{"geo_meter":{"lat":"38.269185", "long":"15.626249"}, "meter_dest":"ceiloesper"}}'
                    
                    '''
                    #QPID VERSION
                    data='{"probe_inst":"'+self.probe.instance_name+'","volume":'+str(m_volume)+',"timestamp":"'+str(m_st)+'","name":"'+str(m_name)+'", "unit":"'+str(m_unit)+'", "ev_type":"measure", "source_type":"vm", "type":"'+self.TYPE_GAUGE+'", "additional_metadata":'+additional_metadata+' }'
                    amq_topic="cloudwave."+self.probe.instance_name
                    broker = self.probe.qpid_server_ip  
                    self.probe.sendMeasureQpid(broker, amq_topic, data)
                    ''' 
                    
                    data=Metric(m_volume, m_st, m_name, m_unit, self.TYPE_GAUGE, additional_metadata)
                    self.probe.sendMeasure(data)
                    
                    
                
                cur.close()
                
                time.sleep(60)
            
            except MySQLdb.Error, e:
                print "ERROR: ",e  
                
        
        db.close() 
        
                


