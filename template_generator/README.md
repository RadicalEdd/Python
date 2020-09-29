# Template generator

Generate json format template based on information gathered through ansible in format suitable with automation tool


Ansible ad hoc command to generate facts from each server in host file, creating single file per host </br>
<code> ansible all -u root -m gather_facts --tree ./gathered_facts -i hosts2 </code>

Script first takes files in folder gathered_facts and filter them to folder parsed_facts -> from these are new files prepared in template_ready_facts folder => ready to be used in original templates.
