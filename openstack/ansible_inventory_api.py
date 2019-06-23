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

inventory.add_host(host='node-1',group='compute')
inventory.clear_caches()
print inventory.get_hosts()