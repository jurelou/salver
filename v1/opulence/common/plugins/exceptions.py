class PluginError(Exception):
    def __init__(self, value=None):
        self.value = value or ""


class PluginFormatError(PluginError):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Plugin format error: ({self.value})"


class PluginRuntimeError(PluginError):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Plugin runtime error: ({self.value})"


class PluginVerifyError(PluginError):
    def __init__(self, value=None):
        super().__init__(value)

    def __str__(self):
        return f"Plugin additional verification failed: ({self.value})"


class DependencyMissing(PluginError):
    def __init__(self, value=None, dependency=None):
        super().__init__(value)
        self.dependency = dependency

    def __str__(self):
        return f"Missing dependency (default): {self.dependency}"


class RateLimitException(PluginError):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"Plugin Rate limit error: ({self.value})"


class ModuleDependencyMissing(DependencyMissing):
    def __str__(self):
        return f"Could not find module: {self.dependency}"


class PasswordDependencyMissing(DependencyMissing):
    def __str__(self):
        return f"Could not find password: {self.dependency}"


class BinaryDependencyMissing(DependencyMissing):
    def __str__(self):
        return f"Could not binary file: {self.dependency}"


class FileDependencyMissing(DependencyMissing):
    def __str__(self):
        return f"Could not find file: {self.dependency}"
