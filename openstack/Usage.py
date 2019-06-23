from ansible_api import ansible_run
from ansible_api import inventory_host
import json

# print inventory_host('compute')
def Usage(host):
    result_raw = ansible_run()
    # print '1111111111'
    # print json.dumps(result_raw)
    vmCount = 1
    cpuPhysical = 2
    result = dict(vmCount= vmCount,
                  cpuPhysical = cpuPhysical,
                  datacenter = 'she_o1',
                  )

    node_count = 0
    cpu_virtual = 0
    ramPhycsical = 0

    result_list = list()
    for i in inventory_host(host):
         result_dict = dict()

         if 'unreachable' not in result_raw[i]:



         # result_dict = dict()
         #print result_raw[i]
         #print  result_raw[i]['ansible_facts']['ansible_hostname']
         #print result_raw[i]['ansible_facts']['ansible_date_time']['date']
             result_dict['node'] = result_raw[i]['ansible_facts']['ansible_hostname']
             result_dict['collectDate'] = result_raw[i]['ansible_facts']['ansible_date_time']['date'] + ' ' + result_raw[i]['ansible_facts']['ansible_date_time']['time']

             result_dict['cores'] = result_raw[i]['ansible_facts']['ansible_processor_vcpus']
             result_dict['ramUsage'] = result_raw[i]['ansible_facts']['ansible_memfree_mb']
             result_dict['ramTotal'] = result_raw[i]['ansible_facts']['ansible_memtotal_mb']
             result_dict['swapUsage'] = result_raw[i]['ansible_facts']['ansible_swapfree_mb']
             result_dict['IP'] = result_raw[i]['ansible_facts']['ansible_default_ipv4']['address']

             node_count = node_count + 1
             cpu_virtual = cpu_virtual + int(result_dict['cores'])
             ramPhycsical = ramPhycsical + int(result_dict['ramTotal'])

         else:
             result_dict[i] = 'unreachable'


         result_list.append(result_dict)
    #
    #
         # node_count = node_count + 1
         # cpu_virtual = cpu_virtual + int(result_dict['cores'])
         # ramPhycsical = ramPhycsical + int(result_dict['ramTotal'])
    # #      print result_raw[i]['ansible_facts']['ansible_date_time']['time']
    # # print result_list
    #
    result["collectionData"] = result_list
    result['nodeCount'] = node_count   # compute count
    result['cpuVirtual'] = cpu_virtual
    result['ramPhycsical'] = ramPhycsical

    return json.dumps(result)

# {'cpuVirtual': '33537', 'collectionData':[{'node': 'node-44', 'collectionDatalectDate': '2019-06-12 16:32:21', 'cpuUsageAvg': '0.062', 'cores': '72'}],
#  'vmCount': '3990', 'cpuPhysical': '5472', 'datacenter':datacenter 'she_o1', 'nodeCount': '77'}


if __name__ == '__main__':
    result = Usage('compute')
    print result




