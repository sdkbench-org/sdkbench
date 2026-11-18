"""Load a content-verified, explicitly selected protocol bundle."""
import hashlib
from pathlib import Path
from .models import Identity, read_json, require


class Bundle:
    def __init__(self, directory):
        self.directory = Path(directory).resolve()
        self.manifest = read_json(self.directory / 'artifacts.json')
        self.sha256 = hashlib.sha256((self.directory / 'artifacts.json').read_bytes()).hexdigest()
        self.plan = read_json(self.directory / 'roadmap.json')
        require(self.plan['schema_version'] == 1, 'Unsupported protocol schema')
        self.cases = {c['id']: c for c in self.plan['instances']}
        require(len(self.cases) == len(self.plan['instances']), 'Duplicate case ID')
        expected = {'roadmap.json', 'candidate-packages.json'} | {
            c[k] for c in self.cases.values() for k in ('fixture', 'reference_artifact')}
        require(set(self.manifest['files']) == expected, 'Incomplete bundle hash manifest')
        require(self.manifest['protocol_revision'] == self.plan['protocol_revision'], 'Manifest revision mismatch')
        for relative, digest in self.manifest['files'].items():
            path = (self.directory / relative).resolve()
            require(path.is_relative_to(self.directory), 'Artifact path leaves the bundle')
            require(hashlib.sha256(path.read_bytes()).hexdigest() == digest, 'Artifact hash mismatch: ' + relative)
        self.fixtures = {k: read_json(self.directory / c['fixture']) for k, c in self.cases.items()}
        self.references = {k: read_json(self.directory / c['reference_artifact']) for k, c in self.cases.items()}

    def identity(self, instance, stack_id, configuration_sha256, environment_sha256):
        require(instance in self.cases, 'Unknown instance')
        return Identity(protocol_revision=self.plan['protocol_revision'], instance_id=instance,
                        fixture_sha256=self.manifest['files'][self.cases[instance]['fixture']],
                        reference_sha256=self.manifest['files'][self.cases[instance]['reference_artifact']],
                        bundle_sha256=self.sha256, stack_id=stack_id,
                        configuration_sha256=configuration_sha256, environment_sha256=environment_sha256)

    def request(self, identity, block=0, repetition=0):
        """No reference output is passed to an adapter. Deep copy prevents mutation."""
        from dataclasses import asdict
        from copy import deepcopy
        from .models import integer
        self.verify_identity(identity)
        integer(block); integer(repetition)
        require(block < 10, 'Invalid block')
        instance = identity.instance_id
        seed_prefix = f"sdkbench-first-wave:{identity.protocol_revision}:{instance}:{block}:"
        contexts = len(self.fixtures[instance].get('contexts', [0]))
        seeds = [int.from_bytes(hashlib.sha256((seed_prefix + str(c)).encode()).digest()[:8], 'big') % 2**32
                 for c in range(contexts)]
        return {'schema_version': 1, 'identity': asdict(identity), 'block': block, 'repetition': repetition,
                'fixture': deepcopy(self.fixtures[instance]), 'sampling_seeds': seeds,
                'compiler_seed': self.plan['execution_profile']['compiler_seeds'][block],
                'training_initialization_index': block % 5}

    def verify_identity(self, identity):
        require(identity.instance_id in self.cases, 'Unknown instance')
        require(identity.protocol_revision == self.plan['protocol_revision'], 'Protocol revision mismatch')
        require(identity.fixture_sha256 == self.manifest['files'][self.cases[identity.instance_id]['fixture']],
                'Fixture identity mismatch')

        require(identity.reference_sha256 == self.manifest['files'][self.cases[identity.instance_id]['reference_artifact']], 'Reference identity mismatch')
        require(identity.bundle_sha256 == self.sha256, 'Protocol bundle identity mismatch')
