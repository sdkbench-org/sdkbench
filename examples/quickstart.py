"""Run after pip install sdkbench. Writes reports to the current directory."""
from sdkbench import run_benchmarks, write_json, write_csv

report = run_benchmarks(sdks=["reference"],n_qubits=4,repeats=3,warmups=1)
write_json(report,"results.json")
write_csv(report,"results.csv")
print(report["summary"])
