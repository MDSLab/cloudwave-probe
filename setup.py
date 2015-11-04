import os
from setuptools import setup, find_packages

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	
	name = "cwProbe",
	#packages = ["cwProbe", "plugins"],
	packages = find_packages(),
	version = "1.6.1",
	description = "CloudWave Monitoring Probe.",
	author = "UniMe Team - Nicola Peditto",
	author_email = "npeditto@unime.it",
	url = "http://www.cloudwave-fp7.eu/",
	download_url = "",
	keywords = ["probe", "monitoring", "cloudwave"],
	classifiers = [
	        "Programming Language :: Python",
	        "Programming Language :: Python :: 2.6",
	        "Development Status :: 4 - Beta",
	        "Environment :: Other Environment",
	        "Intended Audience :: Developers",
	        "License :: OSI Approved :: GNU General Public License (GPL)",
	        "Operating System :: OS Independent",
	        "Topic :: Software Development :: Libraries :: Python Modules",
	],
	license='GPL',
	platforms=['Any'],
	#provides=['plugins',],
	

	dependency_links = [
		'http://ing-wn-21.me.trigrid.it:8094/d/pyloglib/',
		'http://ing-wn-21.me.trigrid.it:8094/d/pyyamllib/',
		'http://ing-wn-21.me.trigrid.it:8094/d/cwconfparser/',
	],


	
	entry_points={
    	'cwprobe.plugins.monitors': [
    	    #'mycheck = plugins.cwpl_mycheckpoint:Cwpl_MyCheckPoint',
    	    #'cpu = plugins.cwpl_cpu:Cwpl_Cpu',
			#'awstats = plugins.cwpl_awstats:Cwpl_Awstat',
    	    #'test = plugins.cwpl_test:Cwpl_Test',
    	    

    	],
	},
	
    install_requires=[
		'setuptools',
		'greenlet',
		'httplib2',
		'stevedore',
		'psutil',
		'qpid-python==0.20',
		'pyyamllib',
		'pyloglib',
		'cwconfparser',
		#'MySQL-python',
    ],
	

	include_package_data = True,
	
	data_files=[
		#('/etc/init.d', ['scripts/etc/init.d/cwProbe']),
		('/etc/init.d', ['scripts/etc/init.d/cwProbe', 'scripts/etc/init.d/cwProbe-sci',]),
		('/usr/bin', ['scripts/usr/bin/cwProbe']),
		#('/opt/cloudwave/cwprobe', ['config/opt/cloudwave/cwprobe/cwprobe.conf']),
    ],
    
	
    #package_data = {
    #    '': ['scripts/etc/init.d/cwProbe', 'scripts/usr/bin/cwProbe'],
    #},
	
	
	#options = {'bdist_rpm':{'post_install' : 'scripts/post_install'},
	
	zip_safe=False,
	long_description=read('README.txt')


)

