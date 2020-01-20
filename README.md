
# Validate variables in Ansible

This repository contains the solution for validating the complex variables in Ansible.

We have possibilities to validate variables in Ansible but if you want to validate a more complicated dictionary, your playbook/role is a bit too tedious.

Imagine you have this dict:

```yaml
server_new:
  os_version: 8
  boot_mode: bios
  domain: <Domain name>
  ip: 172.17.0.1/24
  vm:
    hardware:
      memory_mb: 4096
      num_cpus: 2
    cluster: <VMware cluster name>
    datacenter: <VMware DC name>
    folder: <VMware folder>
    annotation: <VM description>
    network: <VMware network name>
    disks:
      - size_gb: 40
        type: thin
        datastore: <VMware Datastore name>
      - size_gb: 30
        type: thin
        datastore: <VMware Datastore name>
  swap_size_mb: 1024
  filesystems:
    - path: <FS mount point>
      label: <FS label>
      size_mb: 1024
      fstype: ext4
      fsoptions: nosuid,nodev
```

and want to check if the required keys are present (os_version, ip, ..) and if you specify vm you want to check if the next required variables are present and have meaningful values.
Yes, it is doable but it could be simpler.

For this reason I have prepared an Action Plugin to simplify validation of variables.
I decided to use JSON schema for validation (https://json-schema.org/).


## How to install it in Ansible

Required python modules:
- jsonschema

Place `validate_var.py` in your Ansible directory structure according to your preferences and insert action_plugins configuration directive into ansible.cfg
https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-action-plugin-path

The usage in playbook/role is very easy:

```yaml
  - validate_var:
      var: "{{ server_new }}"
      schema: server.json
```

You can place the schema file somewhere in Ansible search path. If you follow best practice directory structure, you can place the schema file in files directory in your role where validate_var task is used.
