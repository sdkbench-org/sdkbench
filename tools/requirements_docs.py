#!/usr/bin/env python3
"""Render and validate the requirements catalog using only the Python standard library."""
import argparse
import csv
import io
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs' / 'requirements'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def anchor(identifier):
    return identifier.lower().replace('.', '-')


def task_path(task, journeys):
    journey = journeys[task['journey']]
    slug = re.sub(r'[^a-z0-9]+', '-', journey['title'].lower()).strip('-')
    return 'tasks/' + journey['id'].lower() + '-' + slug + '.md'


def validate(data):
    require(data['schema_version'] == 1, 'Unsupported catalog schema')
    require(not re.search(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]', json.dumps(data, ensure_ascii=False)), 'CJK text in decoded catalog')
    collections = ['personas', 'models', 'acceptance_profiles', 'sources', 'capabilities', 'functions', 'journeys', 'tasks']
    indexes = {}
    for name in collections:
        items = data[name]
        require(isinstance(items, list) and bool(items), 'Empty collection: ' + name)
        ids = [item['id'] for item in items]
        require(len(ids) == len(set(ids)), 'Duplicate IDs in ' + name)
        indexes[name] = {item['id']: item for item in items}
    require(len(data['stages']) == len(set(data['stages'])), 'Duplicate workflow stages')
    for function in data['functions']:
        require(function['capability'] in indexes['capabilities'], 'Unknown capability')
        require(re.fullmatch(r'F\d{2}\.\d{2}', function['id']) is not None, 'Invalid function ID')
        require(function['id'][1:3] == function['capability'][1:], 'Function/capability ID mismatch')
        require(bool(function['contract'].strip()), 'Empty function contract')
    seen = {name: set() for name in ['personas', 'models', 'acceptance_profiles', 'functions', 'journeys']}
    seen_stages = set()
    for task in data['tasks']:
        require(re.fullmatch(r'T\d{3}', task['id']) is not None, 'Invalid task ID')
        require(task['readiness'] == 'requirements-only' and task['evidence_status'] == 'not-executed', 'Requirements must not assert execution evidence')
        for field in ['slug', 'title', 'user_need', 'inputs', 'required_output', 'acceptance', 'negative_case']:
            require(isinstance(task[field], str) and bool(task[field].strip()), task['id'] + ': empty ' + field)
        require(task['journey'] in indexes['journeys'], 'Unknown journey')
        seen['journeys'].add(task['journey'])
        for name in ['personas', 'models', 'acceptance_profiles', 'functions']:
            values = task[name]
            require(bool(values) and len(values) == len(set(values)), task['id'] + ': empty/duplicate ' + name)
            require(set(values) <= indexes[name].keys(), task['id'] + ': dangling ' + name)
            seen[name].update(values)
        require(bool(task['stages']) and set(task['stages']) <= set(data['stages']), 'Unknown workflow stage')
        require(len(task['stages']) == len(set(task['stages'])), 'Duplicate task stages')
        seen_stages.update(task['stages'])
        require(bool(task['metrics']) and all(isinstance(v, str) and v.strip() for v in task['metrics']), 'Missing metrics')
        conditions = task['function_conditions']
        require(set(conditions) <= set(task['functions']), 'Condition refers to an unlinked function')
        require(all(isinstance(v, str) and v.strip() for v in conditions.values()), 'Empty condition')
    for name, ids in seen.items():
        require(ids == indexes[name].keys(), 'Unreferenced ' + name + ': ' + ', '.join(sorted(indexes[name].keys() - ids)))
    require(seen_stages == set(data['stages']), 'Uncovered workflow stage')
    cap_ids = {function['capability'] for function in data['functions']}
    require(cap_ids == indexes['capabilities'].keys(), 'Capability has no functions')
    for journey in data['journeys']:
        require(set(journey['personas']) <= indexes['personas'].keys(), 'Unknown journey persona')
        require(bool(journey['sources']) and set(journey['sources']) <= indexes['sources'].keys(), 'Unknown journey source')
    for source in data['sources']:
        require(source['url'].startswith('https://') and bool(source['role']), 'Invalid source')
    return indexes


def render(data, indexes):
    tasks, journeys = data['tasks'], indexes['journeys']
    generated = '<!-- Generated from catalog.json by tools/requirements_docs.py. Do not edit directly. -->\n\n'
    out = {}
    intro = ('Requirements baseline ' + data['requirements_version'] + '. These are user-task requirements, '
             'not implemented benchmarks, executed evidence, or participant support claims. '
             'Read [the requirements map](REQUIREMENTS_MAP.md) and [acceptance rules](ACCEPTANCE.md) before using them.\n\n')
    lines = [generated, '# Task catalog\n\n', intro,
             f'{len(tasks)} task families across {len(journeys)} user journeys. Each family requires a frozen executable instance specification before measurement.\n\n',
             '| Journey | User objective | Task count |\n| --- | --- | --- |\n']
    for j in data['journeys']:
        selected = [t for t in tasks if t['journey'] == j['id']]
        path = task_path(selected[0], journeys)
        lines.append(f"| {j['id']} | [{j['title']}]({path}) | {len(selected)} |\n")
    lines.append('\n## All tasks\n\n| Task | User outcome | Users | Applicability tags |\n| --- | --- | --- | --- |\n')
    for task in tasks:
        link = task_path(task, journeys) + '#' + anchor(task['id'])
        lines.append(f"| [{task['id']}]({link}) | {task['title']} | {', '.join(task['personas'])} | {', '.join(task['models'])} |\n")
    out['TASK_CATALOG.md'] = ''.join(lines)
    for journey in data['journeys']:
        selected = [t for t in tasks if t['journey'] == journey['id']]
        path = task_path(selected[0], journeys)
        lines = [generated, '# ' + journey['id'] + ' - ' + journey['title'] + '\n\n',
                 '[All tasks](../TASK_CATALOG.md) | [Acceptance rules](../ACCEPTANCE.md) | [Traceability](../TRACEABILITY.md)\n\n',
                 'Status: requirements only. No task in this file is claimed as implemented or executed.\n\n',
                 'Workflow grounding: ' + ', '.join(f"[{s}](../SOURCES.md#{anchor(s)})" for s in journey['sources']) + '. Sources inform context; they do not establish universal requirements or user-study validation.\n\n']
        for task in selected:
            caps = sorted({indexes['functions'][f]['capability'] for f in task['functions']})
            lines.extend([f'<a id="{anchor(task["id"])}"></a>\n\n', '## ' + task['id'] + ' - ' + task['title'] + '\n\n',
                          '**User need:** ' + task['user_need'] + '\n\n',
                          '**Target users:** ' + ', '.join(f"[{p}](../REQUIREMENTS_MAP.md#{anchor(p)})" for p in task['personas']) + '.\n\n',
                          '**Applicability tags:** ' + ', '.join(task['models']) + '. Instance selection and conditional edges must be frozen before participant evaluation.\n\n',
                          '**Workflow stages:** ' + ', '.join(task['stages']) + '.\n\n',
                          '**Required input and constraints:** ' + task['inputs'] + '\n\n',
                          '**Required output:** ' + task['required_output'] + '\n\n',
                          '**Required capabilities:** ' + ', '.join(f"[{c}](../CAPABILITIES.md#{anchor(c)})" for c in caps) + '.\n\n',
                          '**Function traceability:**\n\n'])
            for f in task['functions']:
                condition = task['function_conditions'].get(f, 'Required for every instance of this task family.')
                lines.append(f"- [{f}](../CAPABILITIES.md#{anchor(f)}): {indexes['functions'][f]['title']}. {condition}\n")
            lines.extend(['\n**Acceptance profiles:** ' + ', '.join(f"[{a}](../ACCEPTANCE.md#{anchor(a)})" for a in task['acceptance_profiles']) + '.\n\n',
                          '**Task-specific acceptance:** ' + task['acceptance'] + '\n\n',
                          '**Measurements:** ' + '; '.join(task['metrics']) + '.\n\n',
                          '**Required negative case:** ' + task['negative_case'] + '\n\n',
                          '**Instance readiness:** Use the [instance specification template](../TASK_SPEC_TEMPLATE.md); bind fixtures, independent references, numerical/statistical thresholds, budgets, and attribution rules before execution.\n\n'])
        out[path] = ''.join(lines)
    lines = [generated, '# Capability and function dictionary\n\n', intro,
             'Function IDs describe required behavior, not named API methods or preferred implementations. Conditional requirements are explicit on task edges.\n\n']
    for cap in data['capabilities']:
        lines.extend([f'<a id="{anchor(cap["id"])}"></a>\n\n', f"## {cap['id']} - {cap['title']}\n\n"])
        for f in [f for f in data['functions'] if f['capability'] == cap['id']]:
            users = [t for t in tasks if f['id'] in t['functions']]
            lines.extend([f'<a id="{anchor(f["id"])}"></a>\n\n', f"### {f['id']} - {f['title']}\n\n", f['contract'] + '\n\n',
                          '**Required by:** ' + ', '.join(f"[{t['id']}]({task_path(t, journeys)}#{anchor(t['id'])})" for t in users) + '.\n\n'])
    out['CAPABILITIES.md'] = ''.join(lines)
    lines = [generated, '# Task-capability-function matrix\n\n', intro,
             'Each function links to a behavioral contract. `*` marks a conditional edge; its exact condition is in the task card and machine-readable matrix. Capability lists are derived from functions rather than maintained independently.\n\n',
             '| Task | User objective | Capabilities | Functions |\n| --- | --- | --- | --- |\n']
    csv_stream = io.StringIO(newline='')
    writer = csv.DictWriter(csv_stream, fieldnames=['task_id', 'task_title', 'journey_id', 'personas', 'applicability_tags', 'capability_id', 'function_id', 'function_title', 'condition', 'acceptance_profiles', 'task_acceptance', 'evidence_status'], lineterminator='\n')
    writer.writeheader()
    for task in tasks:
        caps = sorted({indexes['functions'][f]['capability'] for f in task['functions']})
        function_links = ', '.join(f"[{f}](CAPABILITIES.md#{anchor(f)})" + ('\\*' if f in task['function_conditions'] else '') for f in task['functions'])
        cap_links = ', '.join(f'[{c}](CAPABILITIES.md#{anchor(c)})' for c in caps)
        lines.append(f"| [{task['id']}]({task_path(task, journeys)}#{anchor(task['id'])}) | {task['title']} | {cap_links} | {function_links} |\n")
        for f in task['functions']:
            writer.writerow(dict(task_id=task['id'], task_title=task['title'], journey_id=task['journey'], personas=';'.join(task['personas']), applicability_tags=';'.join(task['models']), capability_id=indexes['functions'][f]['capability'], function_id=f, function_title=indexes['functions'][f]['title'], condition=task['function_conditions'].get(f, 'Required for every instance of this task family.'), acceptance_profiles=';'.join(task['acceptance_profiles']), task_acceptance=task['acceptance'], evidence_status=task['evidence_status']))
    out['TRACEABILITY.md'] = ''.join(lines)
    out['matrix.csv'] = csv_stream.getvalue()
    lines = [generated, '# Coverage audit\n\n', intro,
             '**This is a structural traceability audit, not proof of exhaustive real-world coverage.** Every listed persona, applicability tag, stage, acceptance profile and function has a task reference. Domain experts must still review depth, missing variants and task relevance. No runnable-instance or participant coverage follows from these counts.\n\n']
    for name, field, label in [('personas', 'personas', 'Target users'), ('models', 'models', 'Applicability tags'), ('acceptance_profiles', 'acceptance_profiles', 'Acceptance profiles')]:
        lines.extend(['## ' + label + '\n\n', '| ID | Meaning | Referencing tasks |\n| --- | --- | --- |\n'])
        for item in data[name]:
            refs = [t for t in tasks if item['id'] in t[field]]
            title = item.get('title', item.get('scope'))
            lines.append(f"| {item['id']} | {title} | " + ', '.join(f"[{t['id']}]({task_path(t, journeys)}#{anchor(t['id'])})" for t in refs) + ' |\n')
        lines.append('\n')
    lines.extend(['## Workflow stages\n\n', '| Stage | Task count |\n| --- | --- |\n'])
    for stage in data['stages']:
        lines.append(f"| {stage} | {sum(stage in t['stages'] for t in tasks)} |\n")
    lines.extend(['\n## Required human review\n\n',
                  '- Review each user journey with intended users; the persona descriptions are hypotheses, not completed interviews.\n',
                  '- Review each model and control level, including non-gate and measurement-based workflows.\n',
                  '- Review every conditional edge before cohort registration; SDK omissions cannot create new exceptions.\n',
                  '- Exercise each function variant, boundary case and negative case; one linked task is not evidence that all variants are covered.\n',
                  '- Audit full user outcomes, frontend/component attribution and externally supplied functionality.\n',
                  '- Review inaccessible hardware, proprietary components, unusual platforms and large-instance oracle limitations as evidence gaps.\n',
                  '- Record any new need in the catalog, or give an explicit scope/relevance rationale; absence from current SDKs is not an exclusion reason.\n',
                  '- Record review decisions and unresolved objections before freezing executable instances.\n'])
    out['COVERAGE.md'] = ''.join(lines)
    lines = [generated, '# Workflow grounding and primary sources\n\n',
             'Reviewed on ' + data['date'] + '. These standards, primary research and official workflow descriptions are context, not a popularity-based task-selection rule. A project documenting a workflow does not make its API mandatory, establish that all SDKs support it, or prove stakeholder demand. The task requirements and acceptance rules are independently specified here.\n\n',
             'Live documentation can change. Executable studies must pin relevant specification revisions, source commits, fixtures and references in their manifests. No performance claim or vendor ranking is inferred from these sources.\n\n']
    for source in data['sources']:
        lines.extend([f'<a id="{anchor(source["id"])}"></a>\n\n', f"## {source['id']} - {source['title']}\n\n", f"[{source['title']}]({source['url']}). {source['role']}\n\n"])
    out['SOURCES.md'] = ''.join(lines)
    return out


def check_documents():
    for file in DOCS.rglob('*'):
        if not file.is_file() or file.suffix not in {'.md', '.json', '.csv'}:
            continue
        text = file.read_text(encoding='utf-8')
        require(not re.search(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]', text), 'Non-English CJK text in ' + str(file))
        if file.suffix != '.md':
            continue
        require(text.endswith('\n') and not text.endswith('\n\n'), 'Invalid final newline: ' + str(file))
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            path_part, _, fragment = target.partition('#')
            target_file = (file.parent / path_part).resolve() if path_part else file
            require(target_file.is_file(), f'Broken link from {file.name}: {target}')
            if fragment:
                target_text = target_file.read_text(encoding='utf-8')
                explicit = re.findall(r'<a id="([^"]+)"', target_text)
                implicit = [re.sub(r'[^\w -]', '', h.lower()).replace(' ', '-') for h in re.findall(r'^#+ (.+)$', target_text, flags=re.M)]
                require(fragment in explicit + implicit, f'Broken anchor from {file.name}: {target}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate and detect stale generated documentation without modifying files')
    args = parser.parse_args()
    try:
        data = json.loads((DOCS / 'catalog.json').read_text())
        indexes = validate(data)
        outputs = render(data, indexes)
        for relative, content in outputs.items():
            content = content.rstrip() + '\n'
            target = DOCS / relative
            if args.check:
                require(target.is_file() and target.read_text() == content, 'Stale generated document: ' + relative)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding='utf-8')
        for existing in DOCS.rglob('*.md'):
            if existing.read_text().startswith('<!-- Generated from catalog.json'):
                require(existing.relative_to(DOCS).as_posix() in outputs, 'Obsolete generated document: ' + str(existing))
        check_documents()
        edges = sum(len(t['functions']) for t in data['tasks'])
        print(f"Validated {len(data['tasks'])} task families, {len(data['capabilities'])} capabilities, {len(data['functions'])} functions, and {edges} task/function edges; English-only documents and local links pass.")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        print('requirements: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
