# -*- coding: utf-8 -*-
from opulence.agent.exceptions import BaseAgentException


# Root exception for collectors
class BaseCollectorException(BaseAgentException):
    def __init__(self, value=None):
        self.value = value or ""


# Collector errors
class InvalidCollectorDefinition(BaseCollectorException):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Invalid collector definition: {self.value}"


class CollectorRuntimeError(BaseCollectorException):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Collector runtime error: {self.value}"


# Collector's dependencies exceptions
# class DependencyMissing(BaseCollectorException):
#     def __init__(self, value=None, dependency=None):
#         super(DependencyMissing, self).__init__(value)
#         self.dependency = dependency

#     def __str__(self):
#         return "Missing dependency (default): {}".format(self.dependency)


# class ModuleDependencyMissing(DependencyMissing):
#     def __str__(self):
#         return "Could not find module: {}".format(self.dependency)


# class PasswordDependencyMissing(DependencyMissing):
#     def __str__(self):
#         return "Could not find password: {}".format(self.dependency)


# class BinaryDependencyMissing(DependencyMissing):
#     def __str__(self):
#         return "Could not binary file: {}".format(self.dependency)


# class FileDependencyMissing(DependencyMissing):
#     def __str__(self):
#         return "Could not find file: {}".format(self.dependency)
