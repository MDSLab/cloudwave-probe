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


class Cwpl_Mem(CwPluginBase.CwPluginBase):


    def __init__(self,probe):
        print 'INIT plugin: CW Mem.'
        
        super(Cwpl_Mem, self).__init__()
        
        self.name="Mem"
        self.loop_time = probe.loop_time
        
        self.start()
        

    def run(self):
        print "\t"+self.name+" plugin started"   
        self.main()
                
                
                
                
    def main(self):
        """Main plugin method."""
        
        print "Sending RAM measure..."
        bashCommand = "free -m"
        
        while(1):
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            process.wait()
            output = process.communicate()[0]
            values = output.split('\n')[1]
            
            per_cent = int((float(values.split()[2])*100.0)/float(values.split()[1]))
            data=Metric('mem_per_cent',per_cent,'%')
            self.send_metric(data)
            
            m_val=int(values.split()[2])
            self.send_metric(Metric('mem_used',m_val,'MB'))
            time.sleep(float(self.loop_time))
            

        
                


