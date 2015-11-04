from ctypes import *
import json

print "LOAD LIBSTART!"
lib=cdll.LoadLibrary("libcloudwave.so")

print "LOAD LIB END!"

print "INIT LIB START!"
lib.CloudWave_SO_Init()
print "INIT LIB END!"

add_meta = json.loads('{"md":"ce"}')
add_meta = '{"md":"ce"}'
#lib.record_metric_longlong( lib.SOURCE_APPLICATION, "so:test","{ \"hi\" : \"world\" }","%", lib.METRICEVENTTYPE_GAUGE, 777.0);
#lib.record_metric_longlong( 0, "so4:test4","{'md':'ce'}", "%", 0, 777)
lib.record_metric_longlong( 0, "so4:test4", str(add_meta), "%", 0, 888)



print "METRIC SENT!"

lib.CloudWave_SO_Cleanup()

print "END!!!!"

