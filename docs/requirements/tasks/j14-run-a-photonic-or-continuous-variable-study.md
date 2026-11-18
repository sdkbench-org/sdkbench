<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->

# J14 - Run a photonic or continuous-variable study

[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)

Status: requirements only. No task in this file is claimed as implemented or executed.

Workflow grounding: [S05](../SOURCES.md#s05). Sources inform context; they do not establish universal requirements or user-study validation.

<a id="t066"></a>

## T066 - Prepare and transform a mode-based input state

**User need:** A photonic researcher needs mode order and quadrature conventions preserved.

**Target users:** [P13](../REQUIREMENTS_MAP.md#p13).

**Applicability tags:** cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** express, verify, execute.

**Required input and constraints:** Vacuum, coherent, squeezed and small non-Gaussian states; transformations; declared hbar/quadrature convention.

**Required output:** State moments or small-basis outputs with convention metadata.

**Required capabilities:** [C04](../CAPABILITIES.md#c04), [C17](../CAPABILITIES.md#c17), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F17.01](../CAPABILITIES.md#f17-01): Represent modes and conventions. Required for every instance of this task family.
- [F17.02](../CAPABILITIES.md#f17-02): Evolve Gaussian and non-Gaussian processes. Required for every instance of this task family.
- [F04.01](../CAPABILITIES.md#f04-01): Represent states and linear operators. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Analytic moments and independent small fixtures agree after only declared convention conversions; mode identities and physical units are preserved.

**Measurements:** moment/state error; execution time; memory.

**Required negative case:** A vacuum variance or displacement convention mismatch cannot be hidden by rescaling only the plotted output.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t067"></a>

## T067 - Compute Gaussian optical transformations and correlations

**User need:** A researcher needs scalable Gaussian observables or sampling with correct covariance semantics.

**Target users:** [P13](../REQUIREMENTS_MAP.md#p13).

**Applicability tags:** cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** An interferometer, Gaussian inputs/channels and requested first/second moments or measured distributions.

**Required output:** Moments, covariance or samples in the declared ordering.

**Required capabilities:** [C05](../CAPABILITIES.md#c05), [C12](../CAPABILITIES.md#c12), [C17](../CAPABILITIES.md#c17).

**Function traceability:**

- [F17.02](../CAPABILITIES.md#f17-02): Evolve Gaussian and non-Gaussian processes. Required for every instance of this task family.
- [F17.01](../CAPABILITIES.md#f17-01): Represent modes and conventions. Required for every instance of this task family.
- [F05.03](../CAPABILITIES.md#f05-03): Compute exact observables and reduced states. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A04](../ACCEPTANCE.md#a04), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Analytic small references, physical covariance constraints and the applicable statistical equivalence contract pass.

**Measurements:** time to requested output; memory; moment/distribution error.

**Required negative case:** An incorrect symplectic or mode permutation must fail despite preserved scalar normalization.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t068"></a>

## T068 - Compute a non-Gaussian process with controlled Fock truncation

**User need:** A researcher needs a non-Gaussian result with a justified cutoff.

**Target users:** [P13](../REQUIREMENTS_MAP.md#p13).

**Applicability tags:** cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, verify, estimate.

**Required input and constraints:** A finite-mode non-Gaussian circuit, cutoff/refinement sequence, output quantity and error budget.

**Required output:** Requested outputs, truncation diagnostics and convergence evidence.

**Required capabilities:** [C07](../CAPABILITIES.md#c07), [C17](../CAPABILITIES.md#c17), [C19](../CAPABILITIES.md#c19).

**Function traceability:**

- [F17.02](../CAPABILITIES.md#f17-02): Evolve Gaussian and non-Gaussian processes. Required for every instance of this task family.
- [F17.03](../CAPABILITIES.md#f17-03): Control Fock-space approximation. Required for every instance of this task family.
- [F07.03](../CAPABILITIES.md#f07-03): Track numerical and approximation error. Required for every instance of this task family.
- [F19.04](../CAPABILITIES.md#f19-04): Measure and enforce execution budgets. Required for every instance of this task family.

**Acceptance profiles:** [A03](../ACCEPTANCE.md#a03), [A06](../ACCEPTANCE.md#a06), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Small independent Fock references and cutoff refinement meet the output-error target; discarded probability and any renormalization remain visible.

**Measurements:** error versus cutoff; time to accuracy; memory; discarded probability.

**Required negative case:** A truncated result cannot be reported as exact merely because the retained vector has been normalized.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t069"></a>

## T069 - Analyze photon-counting or quadrature observations

**User need:** A user needs measurement records with detector, loss and postselection meaning intact.

**Target users:** [P13](../REQUIREMENTS_MAP.md#p13), [P08](../REQUIREMENTS_MAP.md#p08).

**Applicability tags:** cv. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** execute, estimate.

**Required input and constraints:** Homodyne/heterodyne or number-resolving fixtures, detector/loss assumptions, sample units and a selection rule.

**Required output:** Typed measurement outcomes and raw/conditional estimates with uncertainty.

**Required capabilities:** [C12](../CAPABILITIES.md#c12), [C17](../CAPABILITIES.md#c17).

**Function traceability:**

- [F17.04](../CAPABILITIES.md#f17-04): Sample photonic measurements. Required for every instance of this task family.
- [F12.01](../CAPABILITIES.md#f12-01): Validate and normalize result records. Required for every instance of this task family.
- [F12.02](../CAPABILITIES.md#f12-02): Estimate quantities with uncertainty. Required for every instance of this task family.
- [F12.05](../CAPABILITIES.md#f12-05): Export interpretable analysis. Required for every instance of this task family.

**Acceptance profiles:** [A04](../ACCEPTANCE.md#a04), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Analytic or independent finite-size distributions satisfy the frozen statistical contract; mode order, units and all selection denominators reconcile.

**Measurements:** sampling throughput; distribution error; selection yield.

**Required negative case:** A continuous quadrature record cannot be treated as a discrete photon count or silently binned with an undisclosed rule.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.

<a id="t070"></a>

## T070 - Transfer a mode program to another execution boundary

**User need:** A user needs an optical program to retain its transformation, measurement and feed-forward intent.

**Target users:** [P13](../REQUIREMENTS_MAP.md#p13), [P16](../REQUIREMENTS_MAP.md#p16).

**Applicability tags:** cv, adaptive. Instance selection and conditional edges must be frozen before participant evaluation.

**Workflow stages:** compile, exchange, verify.

**Required input and constraints:** A mode program, target operations/constraints, source/target conventions and supported adaptive profile.

**Required output:** A compiled or converted artifact plus a loss/rejection report.

**Required capabilities:** [C03](../CAPABILITIES.md#c03), [C17](../CAPABILITIES.md#c17), [C20](../CAPABILITIES.md#c20).

**Function traceability:**

- [F17.05](../CAPABILITIES.md#f17-05): Compile or adapt mode programs. Required when the frozen instance includes the cv applicability tag.
- [F20.01](../CAPABILITIES.md#f20-01): Import and export declared formats. Required for every instance of this task family.
- [F20.02](../CAPABILITIES.md#f20-02): Normalize conventions across boundaries. Required for every instance of this task family.
- [F20.03](../CAPABILITIES.md#f20-03): Round-trip artifacts without hidden loss. Required for every instance of this task family.
- [F03.02](../CAPABILITIES.md#f03-02): Condition on recorded outcomes. Required for every instance of this task family.

**Acceptance profiles:** [A02](../ACCEPTANCE.md#a02), [A03](../ACCEPTANCE.md#a03), [A05](../ACCEPTANCE.md#a05), [A10](../ACCEPTANCE.md#a10).

**Task-specific acceptance:** Small observables or instruments agree after declared conversions and target checks pass; unsupported non-Gaussian/adaptive features are rejected explicitly.

**Measurements:** semantic retention; conversion/compile cost; target legality.

**Required negative case:** A mode cutoff, measurement type or feed-forward rule cannot disappear during interchange.

**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.
