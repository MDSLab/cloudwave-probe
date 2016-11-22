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
Created on 08/nov/2016

@authors: Nicola Peditto <npeditto@unime.it>, Fabio Verboso <fverboso@unime.it>
'''

from cwProbe.plugins import CwPluginBase
from cwProbe.Probe import Metric


#USER IMPORT
import subprocess
import time
import numpy as np

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
        bashCommand = "top -b -n 2 -d.1 | grep Cpu | awk 'NR==2{ print;}' | awk '{print $2}'"# "top -b -n 1 | grep Cpu | awk '{print $2}'"
        

        while(1):

	    cpu_samples=[]
	    #print "ROUNDS: "+self.loop_time
	    for num in range(1, int(self.loop_time)+1):

		
		if num == int(self.loop_time):
			cpu_avg=np.mean(cpu_samples)
			#print "CPU AVG SENT: " + str(cpu_avg)
			data=Metric('cpu_used',float(cpu_avg),'%')
			self.send_metric(data)
		else:
		
            		process = subprocess.Popen(['sh','-c', bashCommand], stdout=subprocess.PIPE)
            		process.wait()
            		output = process.communicate()[0]

  	    		#print "- cpu sample " +str(num) +  ": " + str(output)
			if "us" in output: 
				output="100.0"
	    			cpu_samples.append(float(output))
			else:
				cpu_samples.append(float(output))
		
		time.sleep(1)
