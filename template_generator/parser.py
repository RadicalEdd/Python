import json
import os


# with open('wlsa01.json') as json_file:
#     data = json.load(json_file)
#     print(data)

# f = open('wlsa01.json', "r")
# data = json.loads(f.read())
#
# for i in data:
#     print(i)
# f.close()

# From each generated file parse only information about disks and create a file containing it
for file in os.listdir("./gathered_facts"):
    with open("./gathered_facts/" + file, 'r') as f:
        distros_dict = json.load(f)
        print(distros_dict)

    with open("./parsed_facts/" + file, 'w') as new_file:
        #new_file.write(json.dumps(distros_dict['ansible_facts']['ansible_fqdn']))
        new_file.write(json.dumps(distros_dict['ansible_facts']['ansible_lvm']))


# # Take each file and create another one containing newly constructed format - template ready
for parsed_file in os.listdir("./parsed_facts"):
    with open("./parsed_facts/" + parsed_file, 'r') as f:
        parsed_dict = json.load(f)

    with open("./template_ready_facts/" + parsed_file, 'w') as new_template:
        # Creating basic structure for disks part
        td = {}
        td['lvm'] = {}
        td['disks'] = {}

        # Creating basic structure for lvm part
        for y in parsed_dict['vgs']:
            td['lvm'][y] = {}
            td['lvm'][y]["physicalVolume"] = []
            td['lvm'][y]["logicalVolumes"] = {}

        # Assigning disks with minSizeGB parameter
        for i in parsed_dict['pvs']:
            td['disks'][i] = {}
            td['disks'][i]["minSizeGB"] = int(round(float(parsed_dict['pvs'][i]['size_g'])))

        # Assigning correct disk to correct volumegroup
        for z in parsed_dict['pvs']:
            # print(z)
            # The z value will be used in physicalVolume block
            for v in parsed_dict['pvs'][z].items():
                if "vg" in v:
                    # print(v[1])
                    for x in td['lvm']:
                        if x in json.dumps(v[1]):
                            td['lvm'][x]["physicalVolume"].append(z)

        # Create structure and fill it up with disk sizes
        for o in parsed_dict['lvs']:
            for p in parsed_dict['lvs'][o].items():
                # print(p[1])
                if p[0] == "size_g":
                    size = p[1]
                if p[0] == "vg":
                    if o == "root":
                        td['lvm'][p[1]]["logicalVolumes"]["/"] = {}
                        td['lvm'][p[1]]["logicalVolumes"]["/"]["minSizeGB"] = {}
                        td['lvm'][p[1]]["logicalVolumes"]["/"]["minSizeGB"] = int(round(float(size)))
                    elif o == "swap":
                        pass
                    else:
                        td['lvm'][p[1]]["logicalVolumes"]["/" + o] = {}
                        td['lvm'][p[1]]["logicalVolumes"]["/" + o]["minSizeGB"] = {}
                        td['lvm'][p[1]]["logicalVolumes"]["/" + o]["minSizeGB"] = int(round(float(size)))

        new_template.write(json.dumps(td))
       
