from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import  VariableManager
from collections import namedtuple
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import json



# InventoryManager
loader = DataLoader()
inventory = InventoryManager(loader=loader,sources=["/etc/ansible/hosts"])
# print inventory.get_groups_dict()
variable_manager = VariableManager(loader=loader,inventory=inventory)
Options = namedtuple('Options',[
                                'connection',
                                'module_path',
                                'forks',
                                'timeout',
                                'remote_user',
                                'ask_pass',
                                'private_key_file',
                                'ssh_common_args',
                                'ssh_extra_args',
                                'sftp_extra_args',
                                'scp_extra_args',
                                'become',
                                'become_method',
                                'become_user',
                                'ask_value_pass',
                                'verbosity',
                                'check',
                                'listhosts',
                                'listtasks',
                                'listtags',
                                'syntax',
                                'diff'
])

options = Options(connection='smart',
                  module_path=None,
                  forks=100,
                  timeout=10,
                  remote_user='root',
                  ask_pass=False,
                  private_key_file=None,
                  ssh_common_args=None,
                  ssh_extra_args=None,
                  sftp_extra_args=None,
                  scp_extra_args=None,
                  become=None,
                  become_method=None,
                  become_user='root',
                  ask_value_pass=False,
                  verbosity=None,
                  check=False,
                  listhosts=False,
                  listtasks=False,
                  listtags=False,
                  syntax=False,
                  diff=True,
                  )
play_source = dict(
    name = "ansible play ad-hoc test",
    hosts = 'compute',

    gather_facts = 'yes',
    tasks = [
        # dict(action=dict(module='shell',args='date "+%Y-%m-%d %H:%M:%S"')),
        dict(action=dict(module='setup'))

    ]
)
play = Play().load(play_source,variable_manager=variable_manager,loader=loader)


class ModelResultsCollector(CallbackBase):
    def __init__(self,*args,**kwargs):
        super(ModelResultsCollector,self).__init__(*args,**kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
    def v2_runner_on_unreachable(self,result):
        self.host_unreachable[result._host.get_name()] = result
    def v2_runner_on_ok(self,result,*args,**kwargs):
        self.host_ok[result._host.get_name] = result
    def v2_runner_on_failed(self, result, *args,**kwargs):
        self.host_failed[result._host.get_name] = result
class MyCallback(CallbackBase):

    def __init__(self,*args):
        super(MyCallback,self).__init__(display=None)
        self.status_ok=json.dumps({})
        self.status_fail=json.dumps({})
        self.status_unreachable=json.dumps({})
        self.status_playbook=''
        self.status_no_hosts=False
        self.host_ok = {}
        self.host_failed={}
        self.host_unreachable={}
    def v2_runner_on_ok(self,result):
        host=result._host.get_name()
        self.runner_on_ok(host, result._result)
        #self.status_ok=json.dumps({host:result._result},indent=4)
        self.host_ok[host] = result
    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        self.runner_on_failed(host, result._result, ignore_errors)
        #self.status_fail=json.dumps({host:result._result},indent=4)
        self.host_failed[host] = result
    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        self.runner_on_unreachable(host, result._result)
        #self.status_unreachable=json.dumps({host:result._result},indent=4)
        self.host_unreachable[host] = result
    def v2_playbook_on_no_hosts_matched(self):
        self.playbook_on_no_hosts_matched()
        self.status_no_hosts=True
    def v2_playbook_on_play_start(self, play):
        self.playbook_on_play_start(play.name)
        self.playbook_path=play.name
# callback = ModelResultsCollector()
callback = MyCallback()
passwords = dict()
tqm = TaskQueueManager(
    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader,
    #options=options,
    passwords=passwords,
    stdout_callback= callback,
)

def ansble_run():
    result = tqm.run(play)
    # print result
    result_raw = {'success':{},'failed':{},'unreachable':{}}
    for host,result in callback.host_ok.items():
        result_raw['success'][host] = result._result
    result_raw = result_raw['success']
    # print result_raw
    # print type(result_raw)
    return result_raw

def inventory_host(group):
    return inventory.get_groups_dict()[group]
if __name__ == '__main__':
    result_raw = ansble_run()
    print json.dumps(result_raw)

    # print inventory_host()


    # print inventory.get_groups_dict()['compute']
     # for i in inventory.get_groups_dict()['compute']:
     #     print result_raw[i]['ansible_facts']['ansible_processor_vcpus']







