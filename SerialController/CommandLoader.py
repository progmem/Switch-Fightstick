import Utility as util
import importlib, sys

class CommandLoader:
	def __init__(self, base_path, base_class):
		self.path = base_path
		self.base_type = base_class
		self.modules = []

	def load(self):
		if not self.modules: # load if empty
			self.modules = util.importAllModules(self.path)

		# return command class types
		return self.getCommandClasses()
	
	def reload(self):
		loaded_module_dic = {mod.__name__.split('.')[-1:][0]:mod for mod in self.modules}
		cur_module_names = util.getModuleNames(self.path)

		# Load only not loaded modules
		not_loaded_module_names = list(set(cur_module_names) - set(loaded_module_dic.keys()))
		if len(not_loaded_module_names) > 0:
			self.modules.extend(util.importAllModules(self.path, not_loaded_module_names))
		
		# Reload commands except deleted ones
		for mod_name in list(set(cur_module_names) & set(loaded_module_dic.keys())):
			importlib.reload(loaded_module_dic[mod_name])
		
		# Unload deleted commands
		for mod_name in list(set(loaded_module_dic.keys()) - set(cur_module_names)):
			self.modules.remove(loaded_module_dic[mod_name])
			sys.modules.pop(loaded_module_dic[mod_name].__name__) # Unimport module forcely

		# return command class types
		return self.getCommandClasses()

	def getCommandClasses(self):
		classes = []
		for mod in self.modules:
			classes.extend([c for c in util.getClassesInModule(mod)\
				if issubclass(c, self.base_type) and hasattr(c, 'NAME')])
		
		return classes
