from abc import ABCMeta, abstractclassmethod

class Command:
	__metaclass__ = ABCMeta

	def __init__(self, name):
		self.name = name

	def getName(self):
		return self.name
	
	@abstractclassmethod
	def start(self):
		pass

	@abstractclassmethod
	def end(self):
		pass

class Sync(Command):
    def __init__(self, name):
        super(Sync, self).__init__(name)
        print('init ' + name + ' command')
    
    def start(self):
        pass

    def end(self):
        pass
