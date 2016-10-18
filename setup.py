import os
from setuptools import setup, find_packages

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	
	name = "cwProbe",
	#packages = ["cwProbe"],
	packages = find_packages(),
	version = "3.0",
	description = "CloudWave Monitoring Probe for Y3.",
	author = "UniMe Team - Nicola Peditto",
	author_email = "npeditto@unime.it",
	url = "http://www.cloudwave-fp7.eu/",
	download_url = "",
	keywords = ["probe", "monitoring", "cloudwave"],
	classifiers = [
	        "Programming Language :: Python",
	        "Programming Language :: Python :: 2.7",
	        "Development Status :: 4 - Beta",
	        "Environment :: Other Environment",
	        "Intended Audience :: Developers",
	        "License :: OSI Approved :: GNU General Public License (GPL)",
	        "Operating System :: OS Independent",
	        "Topic :: Software Development :: Libraries :: Python Modules",
	],
	license='GPL',
	platforms=['Any'],
	
	dependency_links = [
		'http://ing-wn-21.me.trigrid.it:8094/d/pyloglib/',
		'http://ing-wn-21.me.trigrid.it:8094/d/pyyamllib/',
		'http://ing-wn-21.me.trigrid.it:8094/d/cwconfparser/',
	],


	
	entry_points={
    	'cwprobe.plugins.monitors': [
    	    'cpu = cwProbe.plugins.cwpl_cpu:Cwpl_Cpu',
    	    'mem = cwProbe.plugins.cwpl_mem:Cwpl_Mem',
    	    #'mysql = cwProbe.plugins.cwpl_mysql:Cwpl_MySql',
    	    #'apache = cwProbe.plugins.cwpl_apache:Cwpl_Apache',
    	    #'test = cwProbe.plugins.cwpl_test:Cwpl_Test',
    	    
    	],
	},
	
    install_requires=[
		'setuptools',
		'greenlet',
		'httplib2',
		'stevedore',
		'psutil',
		'pyyamllib',
		'pyloglib',
		'cwconfparser',
    ],
	

	include_package_data = True,
	
	data_files=[
		('/etc/init.d', ['scripts/etc/init.d/cwProbe']),
		('/usr/bin', ['scripts/usr/bin/cwProbe']),
		('/opt/cloudwave/cwprobe', ['config/opt/cloudwave/cwprobe/cwprobe.conf']),
    ],
    
	
    #package_data = {
    #    '': ['scripts/etc/init.d/cwProbe', 'scripts/usr/bin/cwProbe'],
    #},
	
	
	#options = {'bdist_rpm':{'post_install' : 'scripts/post_install'},
	
	zip_safe=False,
	long_description=read('README.txt')


)

