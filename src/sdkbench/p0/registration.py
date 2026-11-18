"""Content-addressed component/configuration/environment registration."""
from dataclasses import dataclass
from .models import digest, integer, keys, require


@dataclass(frozen=True)
class Registration:
    stack_id: str
    components: list
    configuration: dict
    environment: dict
    schema_version: int = 1

    def __post_init__(self):
        require(type(self.schema_version) is int and self.schema_version == 1, 'Unknown registration schema')
        require(isinstance(self.stack_id, str) and self.stack_id.strip(), 'Missing stack identity')
        require(isinstance(self.components, list) and self.components, 'Missing component attribution')
        for component in self.components:
            keys(component, ('name', 'version', 'role', 'artifact_sha256'))
            for value in component.values():require(isinstance(value, str) and value.strip(), 'Missing component identity')
            require(len(component['artifact_sha256']) == 64 and all(c in '0123456789abcdef' for c in component['artifact_sha256']), 'Invalid component hash')
        keys(self.configuration, ('profile', 'precision', 'threads', 'options'))
        require(self.configuration['profile'] == 'CPU1-FP64' and self.configuration['precision'] == 'float64/complex128', 'Wrong registered resource/precision profile')
        integer(self.configuration['threads'], 1); require(self.configuration['threads'] == 1, 'Wrong thread profile')
        require(isinstance(self.configuration['options'], dict), 'Options must be explicit')
        keys(self.environment, ('python', 'os', 'image_sha256', 'dependency_lock_sha256', 'host'))
        for name in ('python', 'os'):require(isinstance(self.environment[name], str) and self.environment[name], 'Missing environment fact')
        for name in ('image_sha256', 'dependency_lock_sha256'):
            value = self.environment[name]; require(isinstance(value, str) and len(value) == 64 and all(c in '0123456789abcdef' for c in value), 'Invalid environment hash')
        require(isinstance(self.environment['host'], dict) and self.environment['host'], 'Missing host manifest')
        digest(self.to_dict())

    def to_dict(self):
        from dataclasses import asdict
        return asdict(self)

    @property
    def configuration_sha256(self):return digest({'components': self.components, 'configuration': self.configuration})

    @property
    def environment_sha256(self):return digest(self.environment)

    def identity(self, bundle, instance):
        return bundle.identity(instance, self.stack_id, self.configuration_sha256, self.environment_sha256)
