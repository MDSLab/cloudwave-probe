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

from cwProbe.plugins import CwPluginBase
from cwProbe.Probe import Metric


#USER IMPORT
import subprocess
import time


class Cwpl_MySql(CwPluginBase.CwPluginBase):


    def __init__(self,probe):
        print 'INIT plugin: CW MySql.'
        
        super(Cwpl_MySql, self).__init__()
        
        self.name="MySql"
        self.loop_time = probe.loop_time
        
        self.start()
        

    def run(self):
        print "\t"+self.name+" plugin started"   
        self.main()
                
                
                
                
    def main(self):
        """Main plugin method."""
        
        print "Sending mysql measure..."
        bashCommand = "mysqladmin status -u root -ppassword"
        
        while(1):
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            process.wait()
            output = process.communicate()[0]
            """
            template output:
            Uptime: 23996  Threads: 1  Questions: 12217  Slow queries: 0  Opens: 216  Flush tables: 1  Open tables: 57  Queries per second avg: 0.509
            
            Uptime: Uptime of the mysql server in seconds
            Threads: Total number of clients connected to the server.
            Questions: Total number of queries the server has executed since the startup.
            Slow queries: Total number of queries whose execution time waas more than long_query_time variable s value.
            Opens: Total number of tables opened by the server.
            Flush tables: How many times the tables were flushed.
            Open tables: Total number of open tables in the database.
            """
            data=Metric('thr_sql',int(output.split()[3]),'thr')
            
            self.send_metric(data)
            time.sleep(float(self.loop_time))
            

        
                


