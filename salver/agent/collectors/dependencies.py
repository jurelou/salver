# -*- coding: utf-8 -*-
# import os
# import sys
# from importlib import import_module
# from shutil import which

# #from opulence.common.passwordstore import Store

# from opulence.agent.collectors import exceptions


# class Dependency:
#     exception = exceptions.DependencyMissing

#     def __init__(self, dependency):
#         self.dependency_name = dependency
#         self._satisfied = False

#     def is_satisfied(self):
#         raise NotImplementedError

#     def satisfied(self):
#         if not self._satisfied:
#             self._satisfied = self.is_satisfied()
#         return self._satisfied

#     def verify(self):
#         if not self.satisfied():
#             raise self.exception(dependency=self.dependency_name)


# class BinaryDependency(Dependency):
#     exception = exceptions.BinaryDependencyMissing

#     def is_satisfied(self):
#         return which(self.dependency_name) is not None


# #class PasswordDependency(Dependency):
# #    exception = PasswordDependencyMissing
# #
# #    def is_satisfied(self):
# #        return Store().get_decrypted_password(self.dependency_name) is not None


# class ModuleDependency(Dependency):
#     exception = exceptions.ModuleDependencyMissing

#     def is_satisfied(self):
#         if self.dependency_name in sys.modules:
#             return True
#         try:
#             import_module(self.dependency_name)
#             return True
#         except Exception:
#             return False


# class FileDependency(Dependency):
#     exception = exceptions.FileDependencyMissing

#     def is_satisfied(self):
#         return os.path.exists(self.dependency_name) and os.path.isfile(
#             self.dependency_name
#         )
