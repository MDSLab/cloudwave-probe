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


class Cwpl_Cpu(CwPluginBase.CwPluginBase):


    def __init__(self,probe):
        print 'INIT plugin: CW Cpu.'
        
        super(Cwpl_Cpu, self).__init__()
        
        self.name="Cpu"
        self.loop_time = probe.loop_time
        
        self.start()
        

    def run(self):
        print "\t"+self.name+" plugin started"   
        self.main()
                
                
                
                
    def main(self):
        """Main plugin method."""
        
        print "Sending CPU measure..."
        bashCommand = " top -b -n 5 -d.2 | grep Cpu | awk 'NR==3{ print;}'"
        
        while(1):
            process = subprocess.Popen(['sh','-c', bashCommand], stdout=subprocess.PIPE)
            process.wait()
            output = process.communicate()[0]
            data=Metric('cpu_used',float(output[8:13]),'%')
            
            self.send_metric(data)
            time.sleep(float(self.loop_time))
            

        
                


