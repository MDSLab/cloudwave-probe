# CloudWave Probe
CloudWave Probe to monitor resources and applications of the virtual machines.

This component is injected into each CloudWave virtual machine and it allows loading one or more plugins written by the CloudWave developer to collect measurements and event at the platform and virtual machine layers. The CloudWave Probe uses the CloudWave .so library (cw-so) to send measurements and event to the CloudWave Ceilometer Agent (cw-agent). 

CloudWave Probe (cw-probe) has been tested to work on:

* Ubuntu 14.04 and 16.04

##Installation guide

0. Log in (as root) to Openstack virtual machine deployed by Openstack Heat: CloudWave scenario requires that each VM has a Openstack stack-id.
1. Requirements:
  * Install libraries:
    * apt-get update
    * apt-get install -y build-essential libncurses-dev python-dev
  * Install cw-so:
    * wget https://github.com/MDSLab/cloudwave-probe/raw/master/packages/cw-so_3.0-48_amd64.deb
    * dpkg -i cw-so_3.0-48_amd64.deb
  * Install CloudWave Python modules:
    * wget https://github.com/MDSLab/cloudwave-probe/raw/master/packages/PyLogLib-1.0.tar.gz
    * wget https://github.com/MDSLab/cloudwave-probe/raw/master/packages/cwConfParser-1.0.tar.gz
    * pip install PyLogLib-1.0.tar.gz
    * pip install cwConfParser-1.0.tar.gz
    
2. Install cw-probe:
  * wget https://github.com/MDSLab/cloudwave-probe/raw/master/packages/cwProbe-3.0.tar.gz
  * pip install cwProbe-3.0.tar.gz

##Configuration guide
Edit the cw-probe configuration file /opt/cloudwave/cwprobe/cwprobe.conf in order to edit the log file location and/or the polling time (seconds) for each running plugin.
```
[logging]
logfile=/var/log/cloudwave/cw-probe/cwprobe.log

[probe]
loop_time=10
```

##Service management
* /etc/init.d/cwProbe [start | stop | status | restart]
