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


#USER IMPORT
import time


class Cwpl_Test(CwPluginBase.CwPluginBase):
    
    
    def __init__(self, probe):
        print 'INIT plugin: CW TEST.'
        
        super(Cwpl_Test, self).__init__()
        
        self.name="TestPlugin"
        self.loop_time=probe.loop_time
        
        self.start()    


    def run(self):
        
        print "\t"+self.name+" plugin started"   
        
        self.main()

    
    def main(self): 
        """Main plugin method."""
        
        print "Sending a measure..."
        
        while(1):
            print 'test plugin alive'
            time.sleep(float(self.loop_time))
            
            
          
            
            