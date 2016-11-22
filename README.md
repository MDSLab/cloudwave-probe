# CloudWave Probe
CloudWave Probe to monitor resources and applications of the virtual machines.

This component is injected into each CloudWave virtual machine and it allows loading one or more plugins written by the CloudWave developer to collect measurements and event at the platform and virtual machine layers. The CloudWave Probe uses the CloudWave .so library (cw-so) to send measurements and event to the CloudWave Ceilometer Agent (cw-agent). 

