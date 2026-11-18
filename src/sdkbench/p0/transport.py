"""Offline provider events only: this transport never reconciles on a client's behalf."""
from copy import deepcopy
from .models import require


def expected_trace(fixture):
    if 'operations' in fixture:
        return [
            {'operation': 'submit', 'request_key': 'request-001', 'job_id': 'job-001', 'response': 'ack-lost'},
            {'operation': 'reconcile', 'request_key': 'request-001', 'job_id': 'job-001'},
            {'operation': 'poll', 'job_id': 'job-001', 'state': 'completed'},
        ]
    return [{'operation': 'read-event', 'event': deepcopy(e)} for e in fixture['events']]


class OfflineTransport:
    def __init__(self, fixture):
        self.fixture = deepcopy(fixture)
        self.trace = []
        self._events = iter(deepcopy(fixture.get('events', [])))
        self._submissions = 0

    def submit(self, request_key):
        require('operations' in self.fixture and request_key == 'request-001', 'Unexpected offline submission')
        self._submissions += 1
        job = 'job-' + f'{self._submissions:03d}'
        self.trace.append({'operation': 'submit', 'request_key': request_key, 'job_id': job, 'response': 'ack-lost'})
        raise TimeoutError('Provider accepted the request; acknowledgment was lost')

    def reconcile(self, request_key):
        require(request_key == 'request-001' and self._submissions > 0, 'No matching accepted request')
        self.trace.append({'operation': 'reconcile', 'request_key': request_key, 'job_id': 'job-001'})
        return 'job-001'

    def poll(self, job_id):
        require(job_id == 'job-001', 'Unknown job')
        self.trace.append({'operation': 'poll', 'job_id': job_id, 'state': 'completed'})
        return 'completed'

    def next_event(self):
        event = next(self._events)
        self.trace.append({'operation': 'read-event', 'event': deepcopy(event)})
        return event
