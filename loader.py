
'''
Created on 18/lug/2014

@author: UniMe Team - Nicola Peditto <npeditto@unime.it>
'''
from __future__ import print_function

import plugins 

from stevedore import driver
from stevedore import extension
import argparse
import mock
import pkg_resources
from plugins import PluginBase






def test_detect_plugins():
    
    em = driver.DriverManager('plugins.monitors', 'plugA')
    names = sorted(em.names())
    assert names == ['plugA']

def test_driver_property_invoked_on_load():
    em = driver.DriverManager('plugins.monitors', 'plugA', invoke_on_load=False)
    d = em.driver
    assert isinstance(d, PluginBase.PluginBase)







if __name__ == '__main__':
    
    
    print ('Loader plugin system')
    ''' 
    named_objects = []
    for ep in pkg_resources.iter_entry_points(group='plugins.monitors'):
        named_objects.append(ep.load())
    
    print named_objects
    '''
   
    #test_detect_plugins()
    #test_driver_property_invoked_on_load()
    
    
    
    
    #DRIVER MODE
    '''
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        'load_plugin',
        nargs='?',
        default='plugB',
        help='the A plugin',
    )
    
    parser.add_argument(
        '--name',
        default='AAAAA',
        type=str,
        help='name of the plugin',
    )
    
    parsed_args = parser.parse_args()
    '''
    
    
    
    
    
    '''
    mgr = driver.DriverManager(
        namespace='plugins.monitors',
        #name=parsed_args.load_plugin,
        name='plugA',
        invoke_on_load=True,
        #invoke_args=(parsed_args.name,),
    )
    
    print mgr
    ''' 
    
    
    
    
    #EXTENTIONS MODE
    
    ''' 
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--name',
        default='AAAAA',
        type=str,
        help='name of the plugin',
    )
    
    parsed_args = parser.parse_args()
    '''
    
    mgr = extension.ExtensionManager(
        namespace='plugins.monitors',
        invoke_on_load=True,
        #invoke_args=(parsed_args.name,),
    )


    data = {
        'name': 'prova',
        'version': '1.0',
    }
    
    def exec_func(ext, data):
        #print (ext.name)
        return (ext.name, ext.obj.load_plugin(data))
    
    
    results = mgr.map(exec_func, data)

    print (results)

    """ """
    for name, result in results:
        print('From plugin: {0}'.format(name))
        for chunk in result:
            print(chunk, end='')
            
        print('')
        





