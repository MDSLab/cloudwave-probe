# Copyright 2014 University of Messina (UniMe)
#
# Authors: 
#    - Nicola Peditto <npeditto@unime.it>
#    - Carmelo Romeo <caromeo@unime.it>
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

@author: 
    UniMe Team - Nicola Peditto <npeditto@unime.it>
    UniMe Team - Carmelo Romeo <caromeo@unime.it>
'''

from plugins import CwPluginBase



# USER IMPORT
import threading
from sys import exit
import os, subprocess
import time

import commands
from socket import gethostname


class Cwpl_Awstat(CwPluginBase.CwPluginBase):


    def __init__(self, probe):
        print 'INIT plugin: CW Awstats.'
        
        super(Cwpl_Awstat, self).__init__()
        
        self.name = "Awstats"
        self.probe = probe
        
        self.start()
        
        
        
        
    def run(self):
        print "\t" + self.name + " plugin started"   
        self.main()
                
                
                
                
    def main(self):
        """Main plugin method."""
        
        print "\tAwstats MAIN started!"
        print "Awstats Sending..."
        
        # Variables and flags
        i = 0   
        iterations = 999999999999999999
        inter_sleep = 60
        date_vect = []
        test_number = "statistics"
        flag = False

        hostname = gethostname()  # useful for launching awstats.pl perl script
        month_year = subprocess.Popen(['date', '+%m%Y'], stdout=subprocess.PIPE).communicate()[0][:-1]
        awstats_pathname = os.path.dirname(subprocess.Popen(['find', '/', '-name', 'awstats.pl'], stdout=subprocess.PIPE).communicate()[0][:-1])
        stats_pathname = os.path.dirname(subprocess.Popen(['find', '/', '-name', 'awstats' + str(month_year) + '.txt'], stdout=subprocess.PIPE).communicate()[0][:-1])


        # Check which one between httpd or apache2 is running. If none of them is running the plugin will exit
        output = commands.getoutput('ps -A | grep httpd')
        if 'httpd' in output:
            web_server = "httpd"
            flag = True
   
        if flag == False:
            output = commands.getoutput('ps -A | grep apache2')
        if 'apache2' in output:
            web_server = "apache2"
        else: 
            print "Neither httpd nor apache2 is running..."
            exit()	
        
        # REMOVE OLD TESTS RESULTS
        os.system("rm -rf /tmp/tests")
        # log folders
        os.system("mkdir -p /tmp/tests/accesslog_bak/" + str(test_number))
        # awstats folders
        os.system("mkdir -p /tmp/tests/awstats_stats/" + str(test_number))


        # Change web server log file to clean and service to restart
        if web_server == "httpd":
            #os.system("/etc/init.d/httpd stop && echo > /var/log/httpd/access_log && /etc/init.d/httpd start")
	    os.system("echo > /var/log/httpd/access_log")
        elif web_server == "apache2":
            os.system("echo > /var/log/apache2/access.log")
            
        time.sleep(5)




        # Main loop 
        while i < iterations:
            date = subprocess.Popen(['date', '+%Y%m%d%H%M%S'], stdout=subprocess.PIPE).communicate()[0][:-1]
            #print "\n" + str(i) + " of " + str(iterations) + ": access_log_" + str(date)
            date_vect.append(date)
    
    
            # Decide which log file to parse in function of the web server running...
            if web_server == "httpd":
                os.system("cp /var/log/httpd/access_log /tmp/tests/accesslog_bak/" + str(test_number) + "/access_log_" + str(date))
            elif web_server == "apache2":
                os.system("cp /var/log/apache2/access.log /tmp/tests/accesslog_bak/" + str(test_number) + "/access_log_" + str(date))
    
            t = AwstatsThread(self.probe, i, hostname, awstats_pathname, stats_pathname, test_number, date_vect, month_year, inter_sleep)
            t.start()
            time.sleep(inter_sleep)
            i += 1

        # remove temporary and first sample log file
        os.system("rm -f /tmp/tests/awstats_stats/temp_log")
        os.system("rm -f /tmp/tests/accesslog_bak/$test_number/access_log_*")
    
        print "THE END"





# THREAD TO RETRIEVE DATA FROM APACHE/HTTPD LOG FILES
class AwstatsThread(threading.Thread):

        def __init__ (self, probe, iteration, hostname, awstats_pathname, stats_pathname, test_number, date_vect, month_year, inter_sleep):
            threading.Thread.__init__(self)

            self.probe = probe
            self.iteration = iteration
            self.hostname = hostname
            self.awstats_pathname = awstats_pathname
            self.stats_pathname = stats_pathname
            self.test_number = test_number
            self.date_vect = date_vect
            self.month_year = month_year
            self.inter_sleep = inter_sleep
                
                
        def run(self):
                #print "Thread " + str(self.iteration) + " running..."

                if (self.iteration == 1):
                        os.system("cp /tmp/tests/accesslog_bak/" + str(self.test_number) + "/access_log_" + str(self.date_vect[self.iteration]) + " /tmp/tests/awstats_stats/temp_log")


                else:
                        os.system("diff /tmp/tests/accesslog_bak/" + str(self.test_number) + "/access_log_" + str(self.date_vect[self.iteration]) + " /tmp/tests/accesslog_bak/" + str(self.test_number) + "/access_log_" + str(self.date_vect[self.iteration - 1]) + " | sed '1d' | sed 's/> //g' > /tmp/tests/awstats_stats/temp_log")

                # Delete useless access_log files
                os.system("rm -f /tmp/tests/accesslog_bak/" + str(self.test_number) + "/access_log_" + str(self.date_vect[self.iteration - 1]))

                # os.system("/usr/local/awstats/wwwroot/cgi-bin/awstats.pl -config=nagiosvm -update")
                os.system(str(self.awstats_pathname) + "/awstats.pl -config=" + str(self.hostname) + " -update")
                
                # exists= os.path.exists("/usr/local/awstats/wwwroot/awstats"+str(month_year)+".txt")
                exists = os.path.exists(str(self.stats_pathname) + "/awstats" + str(self.month_year) + ".txt")


                if(exists == False):
                    print "\tAwstats summary file not found or empty!"
                    os.system("touch /tmp/tests/awstats_stats/" + str(self.test_number) + "/test_" + str(self.date_vect[self.iteration]) + ".txt")
                else:
                    # os.system("cp /usr/local/awstats/wwwroot/awstats"+str(month_year)+".txt /tmp/tests/awstats_stats/"+str(test_number)+"/test_"+str(date_vect[self.iteration])+".txt")
                    # os.system("rm -f /usr/local/awstats/wwwroot/awstats"+str(month_year)+".txt")
                    os.system("cp " + str(self.stats_pathname) + "/awstats" + str(self.month_year) + ".txt /tmp/tests/awstats_stats/" + str(self.test_number) + "/test_" + str(self.date_vect[self.iteration]) + ".txt")
                    os.system("echo > " + str(self.stats_pathname) + "/awstats" + str(self.month_year) + ".txt")
                    
                    # Start parsing of the awstats output diff file and send measure to the ceilometer server
                    # os.system("python parser_LIVE.py "+str(test_number)+" "+str(date_vect[self.iteration]))
                    parser(self.probe, self.test_number, self.date_vect[self.iteration], self.inter_sleep)
                    
                    # print "End of awstats metrics and Thread " + str(self.iteration) + " exiting..."


        
        
        
# PARSING CLASS
class parser:
    
    def __init__(self, probe, test_number, sample_date, inter_sleep):
        
        self.probe = probe
        self.test_number = test_number
        self.sample_date = sample_date
        self.inter_sleep = inter_sleep

        # Measurement vectors
        hits = []
        #bandwidth = []

	allwordpress = []

        wordpress_pages = []
        #wordpress_bandwidth = []
        #wordpress_entry = []
        #wordpress_exit = []




        #ALL THE METRICS
        #measurement_names = ["hits-1", "bandwidth-1", "wordpress_pages-1", "wordpress_bandwidth-1", "wordpress_entry-1", "wordpress_exit-1"]
        #measurement_units = ["NUMOF_hits", "VALUEOF_bandwidth", "NUMOF_wordpress_pages", "VALUEOF_wordpress_bandwidth", "NUMOF_wordpress_entry", "NUMOF_wordpress_exit"]
        #measurement_data = [hits, bandwidth, wordpress_pages, wordpress_bandwidth, wordpress_entry, wordpress_exit]

        #A selection of metrics
        measurement_names = ["hits-2", "wordpress_pages-2"]
        measurement_units = ["NUMOF_hits", "NUMOF_wordpress_pages"]
        measurement_data = [hits, wordpress_pages]        
    
        # print test_number
        if not os.path.exists("/tmp/tests/awstats_stats/" + str(self.test_number)):
                os.makedirs("/tmp/tests/awstats_stats/" + str(self.test_number))
        
        if not os.path.exists("/tmp/tests/results/" + str(self.test_number)):
                os.makedirs("/tmp/tests/results/" + str(self.test_number))

        f = open("/tmp/tests/awstats_stats/" + str(self.test_number) + "/test_" + str(self.sample_date) + ".txt")
        lines = f.readlines()
        f.close()
        insert = False
        insert1 = False

	insertall = False
	gl_pages = 0
        
        # Parsing entire file searching for error code 500 and worpress statistics (NEW MEASUREMENTS CAN BE PARSED IN FUTURE RELEASES)
        for line in lines:
                columns = line.split(' ')
                if columns[0] == '500':
                        # error_500.append(columns)
                        error_500 = columns
                        # print error_500[0]
                        insert = True

       		"""
                if columns[0] == '/wordpress/':
                        # wordpress.append(columns)
                        wordpress = columns
                        # print wordpress[0]
                        insert1 = True
		"""

		#if '/wordpress/' in columns[0]:
		if columns[0].startswith("/wordpress/"):
			allwordpress.append(columns)
			insertall = True


        if insert == False:
                # error_500.append(['0','0','0'])
                error_500 = ['0', '0', '0']
        """
        if insert1 == False:
                # wordpress.append(['0','0','0','0','0'])
                wordpress = ['0', '0', '0', '0', '0']
        """
	if insertall == True:
		gl_pages = 0
		for count in range(0, len(allwordpress)):
			gl_pages += int(allwordpress[count][1])
        
        # Mean on inter_sleep interval
        """
        hits.append("%.2f" % round(float(float(error_500[1]) / float(self.inter_sleep)), 2))
        bandwidth.append("%.2f" % round(float(float(error_500[2]) / float(self.inter_sleep)), 2))
        
        wordpress_pages.append("%.2f" % round(float(float(wordpress[1]) / float(self.inter_sleep)), 2))
        wordpress_bandwidth.append("%.2f" % round(float(float(wordpress[2]) / float(self.inter_sleep)), 2))
        wordpress_entry.append("%.2f" % round(float(float(wordpress[3]) / float(self.inter_sleep)), 2))
        wordpress_exit.append("%.2f" % round(float(float(wordpress[4]) / float(self.inter_sleep)), 2))
        """


        #A selection of metrics
        hits.append("%.2f" % round(float(float(error_500[1]) / float(self.inter_sleep)), 2))
#       wordpress_pages.append("%.2f" % round(float(float(wordpress[1]) / float(self.inter_sleep)), 2))
	wordpress_pages.append("%.2f" % round(float(float(gl_pages) / float(self.inter_sleep)), 2))


        ################################################################################################################################################

	for count in range(0, len(measurement_names)):
		"""
		m_name = "cw_wordpress_pages"  # measure name
		m_unit = "entry"  # measure unit
		m_volume = wordpress_pages[0]  # measure value
		m_st = self.sample_date 
		additional_metadata = '{meter_dest":"ceiloesper"}' 
		"""

		m_name = measurement_names[count]  # measure name
		m_unit = measurement_units[count]  # measure unit
		m_volume = measurement_data[count][0]  # measure value
		m_st = self.sample_date 
		#additional_metadata = '{meter_dest":"ceiloesper"}'
		additional_metadata = '{"geo_meter":{"lat":"38.269185", "long":"15.626249"}, "meter_dest":"ceiloesper"}'

		data = '{"probe_inst":"' + self.probe.instance_name + '","volume":' + str(m_volume) + ',"timestamp":"' + m_st + '","name":"' + m_name + '", "unit":"' + m_unit + '", "ev_type":"measure", "source_type":"vm", "type":"gauge", "additional_metadata":' + additional_metadata + ' }'
    
		amq_topic = "cloudwave." + self.probe.compute + "." + self.probe.instance_name
		broker = self.probe.qpid_server_ip + ":5672"
		self.probe.sendMeasureQpid(broker, amq_topic, data)            

		#print "\n\n Send Awstats measure: " + data

		#Save data to files
		exists = os.path.exists("/tmp/tests/results/" + str(self.test_number) + "/" + str(measurement_names[count]) + ".txt")
		if(exists == False):
			f = open("/tmp/tests/results/" + str(self.test_number) + "/" + str(measurement_names[count]) + ".txt", "w")
		else:
			f = open("/tmp/tests/results/" + str(self.test_number) + "/" + str(measurement_names[count]) + ".txt", "a")

		f.write(str(self.sample_date) + "\t" + str(measurement_data[count][0]) + "\n")
		print "Measure "+str(measurement_names[count])+ "\t" +str(self.sample_date) + "\t" + str(measurement_data[count][0]) + "\n"
		f.close()
        ################################################################################################################################################


