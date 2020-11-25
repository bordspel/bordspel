import os
import threading

class DependencyManager:

    def __init__(self):
        self.dependencies = []
        self.installed = 0

    def isAllDependenciesInstalled(self):
        return self.installed == len(self.dependencies)

    def addDependency(self, dependency):
        self.dependencies.append(dependency)

    def installDependencies(self):
        for dependency in self.dependencies:
            thread = threading.Thread(target=self.installDependency, args=(dependency, ))
            thread.start()

    def installDependency(self, dependency):
        # response = 1 -> There was an error while installing the dependency.
        # response = 0 -> The dependency has been correctly installed.
        response = os.system("pip3 install " + str(dependency) + " > nul 2>&1")

        if response != 0:
            print("There was an error while trying to install the dependency" + dependency)
        else:
            self.installed += 1