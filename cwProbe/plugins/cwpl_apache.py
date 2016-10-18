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
import shutil


class Cwpl_Apache(CwPluginBase.CwPluginBase):


    def __init__(self,probe):
        print 'INIT plugin: CW Apache.'
        
        super(Cwpl_Apache, self).__init__()
        
        self.name="Apache"
        self.loop_time = probe.loop_time
        
        self.start()
        

    def run(self):
        print "\t"+self.name+" plugin started"   
        self.main()
                


    def get_apache_metrics(self,faccess,tmpaccess,t):
        t=float(t)

        bashCommand = "diff "+faccess+" "+tmpaccess+" | grep -v ' dummy ' > /tmp/diff"
        process = subprocess.Popen(['sh','-c', bashCommand], stdout=subprocess.PIPE)
        process.wait()
        
        vector=[]
        f=open('/tmp/diff')
        lines=f.readlines()[1:]
        
        for l in lines:
            try:
                vector.append(float(l.split('**')[-2:-1][0]))
            except:
                print "fail for line", l
        f.close()

        if vector:
            mean_elab_time=(reduce(lambda x, y: x + y, vector) / len(vector))/1000
            self.send_metric(Metric('elab_time',("%.3f" % mean_elab_time),'milliseconds'))
        else:
            self.send_metric(Metric('elab_time',("%.3f" % 0),'milliseconds'))
            print 'no requests, skip elab_time meter'

        tot_req = float(len(vector))

        bashCommand = "cat /tmp/diff | grep ' 500 ' |wc -l"
        process = subprocess.Popen(['sh','-c', bashCommand], stdout=subprocess.PIPE)
        process.wait()
        n_errors = float(process.communicate()[0])

        self.send_metric(Metric('requests_rate',tot_req/t,'requests/s'))
        self.send_metric(Metric('requests',tot_req,'request'))
        self.send_metric(Metric('errors_rate',n_errors/t,'errors/s'))
        self.send_metric(Metric('errors',n_errors,'errors'))
        self.send_metric(Metric('accesses_rate',(tot_req - n_errors)/t,'accesses/s'))
        self.send_metric(Metric('accesses',(tot_req - n_errors),'accesses'))
        error_percent=0
        if tot_req != 0: error_percent=100.0*(n_errors/tot_req)
        self.send_metric(Metric('errors_percent',error_percent,'%'))                

                
    def main(self):
        """Main plugin method."""
        
        print "Sending Apache measure..."
        
        
        path='/var/log/apache2/'
        delta_path='/tmp/delta_'
        faccess='access.log'
            
        while(1):
            try:
                shutil.copy(path+faccess,delta_path+faccess)
            except e:
                print e
            pass
            
            time.sleep(float(self.loop_time))
            self.get_apache_metrics(path+faccess,delta_path+faccess,self.loop_time)
            
            
            

        
                


