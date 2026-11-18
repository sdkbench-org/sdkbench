"""SDKBench command-line entry point."""
import argparse
import json
import sys
from pathlib import Path
from . import __version__
from .backends import BACKENDS, available_backends
from .circuits import WORKLOADS
from .runner import OPERATIONS, run_benchmarks
from .reporting import compare_reports, write_csv, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description="Measure quantum SDK performance and correctness")
    parser.add_argument("--version",action="version",version=__version__)
    commands = parser.add_subparsers(dest="command",required=True)
    commands.add_parser("list",help="List workloads, operations and optional SDK availability")
    run = commands.add_parser("run",help="Execute serial, correctness-checked benchmarks")
    run.add_argument("--sdk",action="append",choices=BACKENDS)
    run.add_argument("--workload",action="append",choices=WORKLOADS)
    run.add_argument("--operation",action="append",choices=OPERATIONS)
    run.add_argument("--qubits",type=int,default=8)
    run.add_argument("--depth",type=int,default=4)
    run.add_argument("--seed",type=int,default=0)
    run.add_argument("--repeats",type=int,default=5)
    run.add_argument("--warmups",type=int,default=1)
    run.add_argument("--output",type=Path,help="Write full JSON report")
    run.add_argument("--csv",type=Path,help="Also write a flat CSV report")
    compare = commands.add_parser("compare",help="Compare matching JSON reports")
    compare.add_argument("baseline",type=Path)
    compare.add_argument("candidate",type=Path)
    compare.add_argument("--output",type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            print(json.dumps({"sdks":available_backends(),"workloads":WORKLOADS,"operations":OPERATIONS},indent=2))
            return 0
        if args.command == "compare":
            report = compare_reports(json.loads(args.baseline.read_text()),json.loads(args.candidate.read_text()))
            if args.output: write_json(report,args.output)
            else: print(json.dumps(report,indent=2,allow_nan=False))
            return 0
        report = run_benchmarks(sdks=args.sdk or ["reference"],workloads=args.workload or WORKLOADS,
                                operations=args.operation or OPERATIONS,n_qubits=args.qubits,
                                depth=args.depth,seed=args.seed,repeats=args.repeats,warmups=args.warmups)
        if args.csv: write_csv(report,args.csv)
        if args.output:
            write_json(report,args.output)
            print(json.dumps(report["summary"]))
        else: print(json.dumps(report,indent=2,allow_nan=False))
        return int(report["summary"]["failed"]>0 or report["summary"]["error"]>0 or report["summary"]["passed"]==0)
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print("sdkbench: "+str(exc),file=sys.stderr)
        return 2
