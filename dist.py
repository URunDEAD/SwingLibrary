#!/usr/bin/env python

""" Create a distribution of the SwingLibrary.

Usage: jython dist.py [task]

Optional task argument can have the following value:

 - doc  Creates the documentation for the library

If no task is specified, the whole dist build will be run, which means:

 - building of all the subprojects with maven
   (Subprojects: core, test-application, test-keywords, demo-application)
 - packaging them with and without 3rd party classes
 - installing them into local maven repository
 - running the acceptance tests
 - generating the keyword documentation
 - packaging the demo application into distribution zip file

The swinglibrary.jar with and without depencencies and the demo application
zip are copied into the target directory and documentation html will be 
generated to the doc directory.
"""

import os
import re
import sys
import subprocess
import zipfile
from classversioncheck import ClassVersionCheck

VERSION = '1.1.2-SNAPSHOT'
base = os.path.abspath(os.path.normpath(os.path.dirname(__file__)))

def call(cmd):
    print " ".join(cmd)
    return subprocess.call(cmd)

def build_projects():
    build_core()
    build_test_app()
    build_test_kws()
    build_demo_app()

def build_core():
    call(['mvn', '-Ddist.version=%s' % VERSION, '-f', os.path.join('core', 'pom.xml'), 'clean', 'install', 'assembly:assembly'])

def build_test_app():
    call(['mvn', '-Ddist.version=%s' % VERSION, '-f', os.path.join('test-application', 'pom.xml'), 'clean', 'install'])

def build_test_kws():
    call(['mvn', '-Ddist.version=%s' % VERSION, '-f', os.path.join('test-keywords', 'pom.xml'), 'clean', 'install', 'assembly:assembly'])

def build_demo_app():
    call(['mvn', '-Ddist.version=%s' % VERSION, '-f', os.path.join('demo-application', 'pom.xml'), 'clean', 'install', 'assembly:assembly']) 

def init_dirs():
    call(['rm', '-r', 'target'])
    call(['mkdir', 'target'])
    call(['rm', '-r', 'doc'])
    call(['mkdir', 'doc'])

def copy_jars_to_target():
    call(['cp', os.path.join('core', 'target', 'swinglibrary-%s.jar' % VERSION), 'target'])
    call(['cp', os.path.join('core', 'target', 'swinglibrary-%s-jar-with-dependencies.jar' % VERSION), 'target'])
    call(['cp', os.path.join('demo-application', 'target', 'demo-application-%s-jar-with-dependencies.jar' % VERSION), 'target'])

def doc():
    create_doc()
    assert_doc_ok()

def create_doc():
    add_dependencies_to_classpath()
    libdoc = os.path.join(base, 'lib', 'libdoc', 'libdoc.py')
    output = os.path.join(base, 'doc', 'SwingLibrary-%s-doc.html' % (VERSION))
    command = 'jython -Dpython.path=%s %s --output %s %s' % (os.path.join(base, 'lib', 'robotframework-2.5.2.jar', 'Lib'), libdoc, output, 'SwingLibrary')
    print command
    return os.system(command)

def add_dependencies_to_classpath():
    dependencies =  get_deps() + [os.path.join(base, 'core', 'target', 'classes')]
    for deb in dependencies:
        sys.path.append(deb)
    os.environ['CLASSPATH'] = os.pathsep.join(dependencies)

def get_deps():
    os.environ['MAVEN_OPTS'] = '-DoutputAbsoluteArtifactFilename=true'
    mvn_output = sh('mvn -f %s dependency:list' % os.path.join('core', 'pom.xml')).splitlines()
    jars = [re.sub('.*:((:?C:)?)', '\\1', file) for file in mvn_output if re.search('jar', file)]
    return jars

def sh(command):
    process = os.popen(command)
    output = process.read()
    process.close()
    return output

def assert_doc_ok():
    doc_name = 'SwingLibrary-%s-doc.html' % VERSION
    docfile = open(os.path.join(base, 'doc', doc_name), 'r')
    for line in docfile.read().splitlines():
        if '*<unknown>' in line:
            raise "Errors in documentation: " + doc_name + " contains *<unknown>-tags."

def package_demo():
    print 'Packaging Demo application...'
    demo_target = 'demo'
    lib = os.path.join(demo_target, 'lib')
    zip_file = os.path.join('target', 'SwingLibrary-%s-demo.zip' % VERSION)
    call(['rm', '-r', demo_target])
    call(['rm', zip_file])
    call(['mkdir', '-p', lib])
    call(['cp', os.path.join('core', 'target', 'swinglibrary-%s-jar-with-dependencies.jar' % VERSION), lib])
    call(['cp', os.path.join('demo-application', 'target', 'demo-application-%s-jar-with-dependencies.jar' % VERSION), lib])
    call(['cp', os.path.join('demo-application', 'run.sh'), demo_target])
    call(['cp', os.path.join('demo-application', 'example.txt'), demo_target])
    zip_demo()
    call(['rm', '-r', demo_target])
    print 'Demo application packaged to', os.path.abspath(zip_file)

def zip_demo():
    toZip('demo', os.path.join('target', 'SwingLibrary-%s-demo.zip' % VERSION))

def toZip(f, filename):
    zip_file = zipfile.ZipFile(filename, 'w')
    if os.path.isfile(f):
        zip_file.write(f)
    else:
        addFolderToZip(zip_file, f)
    zip_file.close()

def addFolderToZip(zip_file, folder): 
    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
        if os.path.isfile(full_path):
            print 'File added: ' + str(full_path)
            zip_file.write(full_path)
        elif os.path.isdir(full_path):
            print 'Entering folder: ' + str(full_path)
            addFolderToZip(zip_file, full_path)

def default():
    init_dirs()
    build_projects()
    doc()
    try:
      ClassVersionCheck(49).assert_classes_have_correct_version(os.path.abspath(os.path.join('target', 'swinglibrary-%s.jar' % VERSION)))
    except RuntimeError, err:
      print err
    copy_jars_to_target()
    package_demo()

if __name__ == '__main__':
    try:
        name = sys.argv[1] if len(sys.argv) == 2 else 'default'
        {'doc': doc, 'package_demo': package_demo, 'default': default}[name]()
    except (KeyError, IndexError):
        print __doc__


