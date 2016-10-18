# cloudwave-probe
CloudWave probe to monitor resources and applications of the virtual machines.

This component is injected into each CW virtual machine and it allows loading one or more plugins written by the CW developer to collect measurements and event at the platform and virtual machine layers. The CW Probe uses the CW .so library to send measurements and event to the CW Ceilometer Agent (cw-agent). 
