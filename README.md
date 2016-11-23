# CloudWave Probe
CloudWave Probe to monitor resources and applications of the virtual machines.

This component is injected into each CloudWave virtual machine and it allows loading one or more plugins written by the CloudWave developer to collect measurements and event at the platform and virtual machine layers. The CloudWave Probe uses the CloudWave .so library (cw-so) to send measurements and event to the CloudWave Ceilometer Agent (cw-agent). 

CloudWave Probe (cw-probe) has been tested to work on:

* Ubuntu 14.04 and 16.04

##Installation guide

1. Install requirements:
  * Log in (as root) to Openstack virtual machine deployed by Openstack Heat: CloudWave scenario requires that each VM has a Openstack stack-id.
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
  * Log in to Openstack Compute Node (where the Openstack Nova compute is installed) and install the Intel cwdcontroller service:
    * wget https://github.com/MDSLab/cloudwave-probe/raw/master/packages/cw-cpt-so-2.0.0-33.x86_64.rpm
    * rpm -Uvh cw-cpt-so-2.0.0-33.x86_64.rpm
    * systemctl start cwdcontroller.service
    
2. Install cw-probe i the virtual machine:
  * wget https://github.com/MDSLab/cloudwave-probe/raw/master/packages/cwProbe-3.0.tar.gz
  * pip install cwProbe-3.0.tar.gz

##Configuration guide

* Edit the cw-probe configuration file /opt/cloudwave/cwprobe/cwprobe.conf in order to edit the log file location and/or the polling time (seconds) for each running plugin.

```
[logging]
logfile=/var/log/cloudwave/cw-probe/cwprobe.log

[probe]
loop_time=10
```
* From inside the VM enable at boot the provisioning of the CloudWave data needed by cw-so to provide that information to the cw-probe; in particular put inside the /etc/rc.local file the following command:
 * /opt/cloudwave/cw-so/staging/daemon/cwdaemon -conAi -mesAVo  -meso "CloudWave"

* In order to modify the plugins list loaded at boot of the cw-probe it is needed edit the following file in order to comment the plugin that you need to disable and vice versa:
  * /usr/local/lib/python2.7/dist-packages/cwProbe-3.0-py2.7.egg-info/entry_points.txt
  ```
  [cwprobe.plugins.monitors]
  cpu = cwProbe.plugins.cwpl_cpu:Cwpl_Cpu
  mem = cwProbe.plugins.cwpl_mem:Cwpl_Mem
  ```

##Service management
* /etc/init.d/cwProbe [start | stop | status | restart]
