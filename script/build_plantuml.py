#!/usr/bin/env python

# README
# Installer grapviz (mac: brew install graphviz)
# Installér PlantUML plugin i IntelliJ
# Trenger Python
# Kjøres fra rotkatalogen til prosjektet

import os
import xml.etree.ElementTree as ET

rootdir = '.'

modules = {}
artifacts = {}

rootPom = None
groupId = None

NSMAP={"pom": "http://maven.apache.org/POM/4.0.0"}

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == "pom.xml":
            filewpath = os.path.join(subdir, file)
            tree = ET.parse(filewpath)

            artifactId = tree.find('./pom:artifactId', namespaces=NSMAP).text
            if not rootPom:
                rootPom = subdir
                groupId = tree.find('./pom:groupId', namespaces=NSMAP).text
            submodules = [subdir + "/" + elem.text for elem in
                          tree.findall('./pom:modules/pom:module', namespaces=NSMAP)]
            module = {
                "subdir": subdir,
                "artifactId": artifactId,
                "submodules": submodules
            }
            modules[subdir] = module
            dependencies = [elem.text for elem in
                            tree.findall("./pom:dependencies/pom:dependency[pom:groupId='" + groupId + "']/pom:artifactId", namespaces=NSMAP)]
            artifacts[artifactId] = {
                "artifactId": artifactId,
                "dependsOn": dependencies
            }
        else:
            continue


# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(modules)
# pp.pprint(artifacts)


# write modulelist
def write_modules(subdir, modules, f):
    if subdir != rootPom:
        if len(modules[subdir]["submodules"]) == 0:  # skip modules that only contain modules
            f.write("[" + modules[subdir]["artifactId"] + "]\n")

    for submodule in modules[subdir]["submodules"]:
        write_modules(submodule, modules, f)


# traverse structure
def write_structure(subdir, modules, f):
    if subdir != rootPom:
        if len(modules[subdir]["submodules"]) > 0:
            f.write("package " + modules[subdir]["artifactId"] + "{\n")
        else:
            f.write("[" + modules[subdir]["artifactId"] + "]\n")

    for submodule in modules[subdir]["submodules"]:
        write_structure(submodule, modules, f)

    if subdir != rootPom:
        if len(modules[subdir]["submodules"]) > 0:
            f.write("}\n\n")


def write_dependencies(artifacts, f):
    for artifact in artifacts.values():
        for dependency in artifact["dependsOn"]:
            f.write("[" + artifact["artifactId"] + "] --> [" + dependency + "]\n")


with open('module_dependencies.puml', 'w') as f:
    f.write("@startuml\n")
    write_modules(rootPom, modules, f)
    write_dependencies(artifacts, f)
    f.write("@enduml\n")


with open('with_multi_module.puml', 'w') as f:
    f.write("@startuml\n")
    write_structure(rootPom, modules, f)
    write_dependencies(artifacts, f)
    f.write("@enduml\n")

