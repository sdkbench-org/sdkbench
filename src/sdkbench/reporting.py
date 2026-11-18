"""Report export and matched-run timing comparisons."""
import csv
import json
import math
from pathlib import Path


def write_json(report, path):
    Path(path).write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")


def write_csv(report, path):
    fields = ["sdk","workload","operation","status","n_qubits","input_gates",
              "median_ns","mean_ns","min_ns","max_ns","stdev_ns","p95_ns",
              "output_gates","output_two_qubit_gates","output_depth","reason"]
    with Path(path).open("w",newline="",encoding="utf-8") as stream:
        writer = csv.DictWriter(stream,fieldnames=fields)
        writer.writeheader()
        for row in report["results"]:
            flat = {key:row[key] for key in fields if key in row}
            flat.update(row.get("timing",{}))
            flat.update({"output_"+key:value for key,value in row.get("output_metrics",{}).items()})
            writer.writerow(flat)


def compare_reports(baseline, candidate):
    """Match identical run configurations; ratio >1 means a faster candidate."""
    if baseline.get("schema_version")!=1 or candidate.get("schema_version")!=1:
        raise ValueError("Expected report schema_version=1")
    if not baseline.get("config") or baseline["config"] != candidate.get("config"):
        raise ValueError("Run configurations must match exactly for comparison")
    def index(report):
        result = {}
        for row in report["results"]:
            key = (row["sdk"],row["workload"],row["operation"])
            if key in result: raise ValueError("Duplicate result key")
            result[key] = row
        return result
    old,new = index(baseline),index(candidate)
    if old.keys()!=new.keys():
        raise ValueError("Report result keys must match")
    comparisons = []
    for key,a in old.items():
        b = new[key]
        item = dict(zip(("sdk","workload","operation"),key))
        item.update(baseline_status=a["status"],candidate_status=b["status"])
        if a["status"]==b["status"]=="passed":
            if a.get("circuit_sha256") != b.get("circuit_sha256"):
                raise ValueError("Circuit fingerprints differ")
            first,second = a["timing"]["median_ns"],b["timing"]["median_ns"]
            if any(type(x) not in (int,float) or not math.isfinite(x) or x<=0 for x in (first,second)):
                raise ValueError("Medians must be finite and positive")
            item.update(baseline_median_ns=first,candidate_median_ns=second,speedup=first/second)
        comparisons.append(item)
    return {"schema_version":1,"ratio_definition":"baseline_median_ns / candidate_median_ns",
            "environment_matches":baseline.get("environment")==candidate.get("environment"),
            "comparisons":comparisons}
