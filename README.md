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
    * apt-get install -y --force-yes cw-so
2. Install cw-probe:
  * wget https://github.com/MDSLab/cloudwave-probe/raw/master/packages/cw-probe_3.0-19_amd64.deb
  * sudo dpkg -i cw-probe_3.0-19_amd64.deb

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
