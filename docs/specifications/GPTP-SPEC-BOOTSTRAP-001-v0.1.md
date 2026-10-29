# GPT Partner — Bootstrap Specification and Validation Plan

- **Document ID:** GPTP-SPEC-BOOTSTRAP-001
- **Version:** 0.1
- **Date:** 2026-10-29
- **Status:** PROPOSED / EXPERIMENTAL / NOT VERIFIED / NOT ADOPTED
- **Repository:** `Badreddine1982/GPT-Partner`
- **Branch:** `experiment/bootstrap-spec-v0.1`

## 1. Purpose

Establish a small, evidence-driven starting point for GPT Partner: a governed capability and execution layer that can discover available capabilities, request authorization for consequential actions, invoke permitted tools, and report verifiable outcomes.

This document is a testable starting hypothesis, not a final architecture decision.

## 2. Core hypothesis

A single, narrow interface can coordinate capabilities without embedding every capability implementation inside GPT Partner, provided each capability exposes a declared contract and every action passes through explicit policy and evidence handling.

**Hypothesis status:** PROPOSED — no runtime implementation or end-to-end behavior has yet been verified.

## 3. Design principles

1. **One front door, modular internals.** The user should interact with one coherent partner interface; capabilities remain replaceable modules or adapters.
2. **Authorization before consequential action.** Discovering a capability is not permission to use it. Permission must be explicit, scoped, and checked at execution time.
3. **Evidence over assertion.** The system distinguishes requested, attempted, completed, read-back verified, tests passed, and accepted.
4. **Fail closed.** Missing policy, ambiguous authorization, invalid input, or unavailable verification must not silently grant access.
5. **Isolation is a real boundary.** A future execution runtime must enforce resource and access limits outside the model's own instructions.
6. **No automatic adoption.** Experiments may inform proposals; they do not silently change approved behavior.
7. **Replaceable connectivity.** MCP is a candidate transport, not a settled architectural requirement. Direct APIs or other adapters may be compared when useful.
8. **Minimize privileged surface.** The first prototype must not execute arbitrary user-supplied code or gain broad host access.

## 4. Candidate responsibility boundaries

These are conceptual boundaries to test, not a commitment to a specific deployment topology.

- **Partner interface:** receives a goal and returns plans, authorization requests, execution summaries, and evidence references.
- **Capability catalog:** records capability ID, version, input/output contract, required permissions, risk class, and verification method.
- **Policy and authorization gate:** evaluates whether a proposed action is allowed and whether fresh user approval is required.
- **Connector adapters:** communicate with approved external tools or services; MCP may be one adapter.
- **Execution boundary:** a future isolated runtime for bounded jobs, with explicit resource, filesystem, network, and time limits.
- **Evidence ledger:** records intent, authorization, action, result, verification, and failure reason with timestamps and stable identifiers.
- **Memory interface:** retrieves approved operational records and experiment results. It does not imply direct control over ChatGPT's private internal memory.
- **Learning proposal loop:** proposes changes from evidence; tests and human approval are required before adoption.

## 5. First milestone: contract and authorization dry run

Before adding a real cloud runtime or allowing arbitrary execution, prove a small vertical slice with a harmless mock capability.

### Test case A — capability discovery

Given a local/mock catalog with one read-only capability and one state-changing capability, the interface returns their IDs, versions, contracts, risk classes, and required permissions without executing either one.

**Pass criteria**
- Both capabilities are listed with complete required metadata.
- Discovery causes no side effects.
- Unknown or missing metadata is reported rather than guessed.

### Test case B — authorization gate

Submit a proposed state-changing action without approval, then with an explicit scoped approval token in the test harness.

**Pass criteria**
- Without valid approval, the action is denied and the mock side effect does not occur.
- Approval is bound to the action, capability, and scope; it cannot authorize a different action.
- A denial is recorded as a denial, not reported as a successful execution.

### Test case C — evidence semantics

Run one allowed harmless mock action and one denied action.

**Pass criteria**
- The result distinguishes `requested`, `attempted`, `completed`, `verified`, `tests_passed`, and `accepted`.
- A completed action is not automatically labelled verified.
- The ledger captures a correlation ID, capability/version, decision, result, and verification status.

### Test case D — failure classification

Simulate an unavailable connector and a verification failure.

**Pass criteria**
- The outcome is reported as failed or unknown with a reason.
- The system does not retry through a different privileged path or claim success without evidence.

## 6. Initial capability contract (draft)

Each capability should eventually declare:

- `capability_id`
- `version`
- `description`
- `input_schema`
- `output_schema`
- `risk_class`
- `required_permissions`
- `side_effects`
- `timeout_seconds`
- `resource_limits` (where execution applies)
- `verification_method`
- `failure_modes`

The exact schema format remains open pending the first test. Avoid premature standardization.

## 7. Explicit non-goals for v0.1

- No claim that GPT Partner is already connected to ChatGPT through a persistent MCP session.
- No claim that an isolated cloud runtime exists or has been provisioned.
- No arbitrary shell, filesystem, network, or code execution.
- No autonomous installation of tools or plugins without user authorization.
- No attempt to bypass platform, connector, repository, or service security controls.
- No direct mutation of ChatGPT's internal memory.
- No model-weight training or autonomous self-modification.
- No production-readiness claim.

## 8. Questions to resolve through evidence

1. What connection path is actually available from the intended ChatGPT environment, and what are its authentication and permission limits?
2. Can capability discovery be implemented independently of any one transport?
3. What is the smallest runtime boundary that can pass isolation tests in the intended deployment environment?
4. Which operational records should be persisted, for how long, and with what redaction/access policy?
5. Which failures originate in the platform, connector, remote service, runtime, or verification layer, and how can they be distinguished reliably?

## 9. Proposed implementation sequence

1. Review this specification and the repository baseline.
2. Implement a mock capability catalog and typed request/result contracts.
3. Implement a deny-by-default authorization dry run.
4. Add deterministic tests for discovery, denial, scoped approval, and evidence status.
5. Review test output and failure cases before selecting a real connector.
6. Evaluate MCP against a concrete use case; do not add a permanent connection agent unless evidence shows a real recovery need.
7. Only after the mock gate passes, prototype a tightly bounded execution adapter and test its isolation separately.

## 10. Evidence and acceptance rules

For each experiment, preserve:
- experiment ID and version;
- exact command or input;
- environment and dependency versions;
- observed output and exit status;
- test results;
- artifact or commit identifiers;
- known limitations and unresolved failures.

Use these states distinctly:

- **PROPOSED:** idea documented.
- **SPECIFIED:** behavior and acceptance criteria documented.
- **TESTED:** a test was run and its output preserved.
- **VERIFIED:** evidence supports the stated acceptance criteria.
- **CONFIRMED:** independent or repeatable evidence supports the result.
- **ADOPTED:** explicitly approved for use.

A GitHub commit proves that a change was committed; it does not prove that the implementation works.

## 11. Current baseline

- Repository exists and is public.
- Default branch: `main`.
- Initial commit: `5b30b4d59bf8760c966dabe61953742cc93556fc`.
- Initial contents observed: `README.md` and `LICENSE`.
- No implementation or tests have been verified at this point.

## 12. Decision record

**Decision:** Begin with a specification and mock authorization vertical slice rather than immediately installing services, creating a cloud runtime, or committing to MCP-only architecture.

**Reason:** This creates an early falsifiable test of the project's defining claim—unified capability access under explicit authorization and evidence—while keeping the initial privileged surface small.

**Review gate:** Do not label the architecture verified or adopted until the test evidence exists and has been reviewed.
