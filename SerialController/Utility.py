import os
from os.path import join, relpath
from glob import glob
import inspect, importlib

# Show all file names right under the directory
def browseFileNames(path='.', ext=''):
	return [relpath(f, path) for f in glob(join(path, '*' + ext))]

def getClassesInModule(module):
	classes = []
	for members in inspect.getmembers(module, inspect.isclass):
		classes.append(members[1])
	return classes

def getModuleNames(base_path):
	return [os.path.splitext(n)[0] for n in browseFileNames(path=base_path, ext='.py')]

def importAllModules(base_path, mod_names=None):
	modules = []
	for name in getModuleNames(base_path) if mod_names is None else mod_names:
		modules.append(importlib.import_module(base_path.replace('\\', '.') + '.' + name))
	
	return modules
