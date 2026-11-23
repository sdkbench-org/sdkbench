# Single-GPU statevector engineering pilot

This is a separate engineering cohort, not an extension of the CPU P1a records
or the website's 125 planned metric definitions. The fixed profile is
`gpu-statevector-profile.json`. Versions must pass admission before execution.
Do not alter thresholds, cases or seeds after retrieving performance values.

The two native paths are NVIDIA cuStateVec `apply_matrix` and released
FlagQuantum `Circuit.state(refresh=True)`, complex128, one real NVIDIA GPU.
They execute identical asymmetric RY/RZ rotations and alternating CX chains.
The logical first qubit is the most significant state-vector index bit. A
separate NumPy complex128 implementation supplies the reference for every case.
All warmup and measured full states are retained with hashes. Every result must
pass finite-value, maximum absolute error and normalization checks. Device type
and dtype are asserted; CPU fallback is forbidden.

Each participant/case has ten fresh-process blocks, two warmups and three measured
requests per block. Participant order alternates between blocks. The request
starts before native circuit/handle/matrix preparation, includes zero-state
initialization, all operations and full host-state delivery, and ends after
cuStateVec handle cleanup. SDK imports and NumPy evaluation are outside timing.
Report setup, synchronized initialization/evolution, device-to-host copy,
cleanup and total wall time separately. The gate list is already constructed.
The initial state is prepared on-device; there is no large host-to-device state
upload. Matrix upload belongs to setup. Phase sums are diagnostic, not substitutes
for the separately measured total. This is Python-driven backend execution,
not a GPU kernel microbenchmark or a full application SDK score.

Torch allocated/reserved peaks, CuPy retained pool bytes and cuStateVec workspace
are distinct resource observations. They do not measure the same thing and must
not be combined into a GPU memory ranking. Device process-memory profiling,
energy, multi-GPU, gradients, tuning and circuit fusion remain out of scope.
The GPU is shared infrastructure; observed idleness does not prove exclusive
reservation or sealed-host qualification. Publication eligibility remains false.

Run on an admitted NVIDIA CUDA host using an isolated environment:

```sh
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
python tools/gpu_statevector.py campaign \
  --profile docs/implementation/gpu-statevector-profile.json \
  --output /absolute/path/to/new-evidence \
  --source-commit EXACT_COMMIT --gpu-uuid PHYSICAL_GPU_UUID \
  --container-image sha256:EXACT_IMAGE
```

The command refuses to overwrite results. Every child execution retains stdout,
stderr, exit code and timing, including failures/timeouts. The final inventory
binds full-state outputs and metadata. Qualification smoke runs use a different
output directory and are never pooled into the measured cohort.

NVIDIA binding contract checked 2026-11-23:
https://docs.nvidia.com/cuda/cuquantum/26.11.0/python/bindings/generated/cuquantum.bindings.custatevec.apply_matrix.html
