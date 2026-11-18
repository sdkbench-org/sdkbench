"""Public P0 command contracts and error behavior."""
import json
from pathlib import Path
import subprocess
import sys
from sdkbench.p0 import Bundle
from sdkbench.p0.cli import main
from sdkbench.p0.models import canonical_bytes
from p0_cases import record

ROOT = Path(__file__).resolve().parents[1]


def test_inspect_and_validate_cli(tmp_path, capsys):
    path = ROOT / 'docs/implementation'; args = ['--bundle', str(path)]
    assert main(args + ['inspect']) == 0
    inspected = json.loads(capsys.readouterr().out); assert len(inspected['instances']) == 24
    bundle = Bundle(path); result = record(bundle, 'PARAM-04'); output = tmp_path / 'result.json'
    output.write_bytes(canonical_bytes(result.to_dict()))
    assert main(args + ['validate', str(output)]) == 0
    assert json.loads(capsys.readouterr().out)['status'] == 'accepted'
    result.payload['outputs'][0]['X0'] = .1; output.write_bytes(canonical_bytes(result.to_dict()))
    assert main(args + ['validate', str(output)]) == 1
    assert json.loads(capsys.readouterr().out)['status'] == 'incorrect'
    output.write_text('{bad')
    assert main(args + ['validate', str(output)]) == 2
    assert 'Invalid JSON' in capsys.readouterr().err


def test_full_case_and_workflow_cli(tmp_path, capsys):
    path = ROOT / 'docs/implementation'; bundle = Bundle(path); args = ['--bundle', str(path)]; output = tmp_path / 'records.json'
    records = [record(bundle, 'PARAM-04', b, r).to_dict() for b in range(10) for r in range(3)]
    output.write_bytes(canonical_bytes(records))
    assert main(args + ['validate', '--full-case', str(output)]) == 0
    capsys.readouterr()
    records = [record(bundle, id_, b).to_dict() for id_ in ['SAMPLE-03', 'SAMPLE-05'] for b in range(10)]
    output.write_bytes(canonical_bytes(records))
    assert main(args + ['validate', '--workflow', 'W08', str(output)]) == 0
    capsys.readouterr()
    assert main(args + ['validate', '--workflow', 'W02', str(output)]) == 1
    assert json.loads(capsys.readouterr().out)['status'] == 'incorrect'


def test_independent_core_imports_no_participant_modules():
    command = 'import sys; import sdkbench.p0.evaluators; import sdkbench.p0.supervisor; assert not any(n.split(".")[0] in {"qiskit","cirq","flagquantum","pennylane","cudaq","qibo","qulacs","mindquantum","tensorcircuit","torchquantum","pytket","braket"} for n in sys.modules)'
    subprocess.run([sys.executable, '-c', command], check=True, timeout=10)
