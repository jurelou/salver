class PluginError(Exception):
    def __init__(self, value=None):
        self.value = value or ""


class PluginFormatError(PluginError):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "Plugin format error: ({})".format(self.value)


class PluginRuntimeError(PluginError):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "Plugin runtime error: ({})".format(self.value)


class PluginVerifyError(PluginError):
    def __init__(self, value=None):
        super().__init__(value)

    def __str__(self):
        return "Plugin additional verification failed: ({})".format(self.value)


class DependencyMissing(PluginError):
    def __init__(self, value=None, dependency=None):
        super(DependencyMissing, self).__init__(value)
        self.dependency = dependency

    def __str__(self):
        return "Missing dependency (default): {}".format(self.dependency)


class RateLimitException(PluginError):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "Plugin Rate limit error: ({})".format(self.value)


class ModuleDependencyMissing(DependencyMissing):
    def __str__(self):
        return "Could not find module: {}".format(self.dependency)


class PasswordDependencyMissing(DependencyMissing):
    def __str__(self):
        return "Could not find password: {}".format(self.dependency)


class BinaryDependencyMissing(DependencyMissing):
    def __str__(self):
        return "Could not binary file: {}".format(self.dependency)


class FileDependencyMissing(DependencyMissing):
    def __str__(self):
        return "Could not find file: {}".format(self.dependency)
