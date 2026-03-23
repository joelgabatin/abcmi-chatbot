#!/usr/bin/env python3
"""
Auto Documentation Agent — Grace Church Chatbot
================================================
Runs automatically via Claude Code Stop hook after each session.
Detects new/modified feature files via git and generates structured
markdown documentation in .claude/docs/features/.
"""

import ast
import json
import os
import re
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR     = PROJECT_ROOT / ".claude" / "docs" / "features"

# ── What counts as a "feature file" ───────────────────────────────────────────
FEATURE_FILES = {
    "grace_api.py",
    "database.py",
    "admin.py",
    "seed.py",
    "migrate.py",
    "run_grace_chatbot.py",
}
FEATURE_DIRS  = {"actions", "data"}          # watch all files inside these dirs
FEATURE_EXTS  = {".py", ".yml", ".yaml"}


# ── Git helpers ────────────────────────────────────────────────────────────────

def git(*args):
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=PROJECT_ROOT
    )
    return result.stdout.strip()


def changed_files():
    """Return (new_files, modified_files) relative to project root."""
    porcelain = git("status", "--porcelain")
    new, modified = [], []

    for line in porcelain.splitlines():
        if len(line) < 4:
            continue
        xy       = line[:2]
        filepath = line[3:].strip().strip('"')

        p = Path(filepath)
        if p.suffix not in FEATURE_EXTS:
            continue
        if p.name not in FEATURE_FILES and p.parts[0] not in FEATURE_DIRS:
            continue

        if "?" in xy or "A" in xy:   # untracked or staged-new
            new.append(filepath)
        elif "M" in xy or "R" in xy:  # modified or renamed
            modified.append(filepath)

    return new, modified


# ── Python file analysis (AST) ─────────────────────────────────────────────────

def parse_python(filepath: Path):
    """Extract functions, classes, and their docstrings from a .py file."""
    try:
        source = filepath.read_text(encoding="utf-8", errors="ignore")
        tree   = ast.parse(source)
    except Exception:
        return [], []

    functions, classes = [], []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # skip private helpers
            if node.name.startswith("__") and node.name.endswith("__"):
                continue
            args    = [a.arg for a in node.args.args]
            doc     = ast.get_docstring(node) or ""
            functions.append({
                "name":    node.name,
                "args":    args,
                "doc":     doc,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
                "line":    node.lineno,
            })
        elif isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or ""
            classes.append({"name": node.name, "doc": doc, "line": node.lineno})

    return functions, classes


def extract_flask_routes(filepath: Path):
    """Pull @app.route decorators from a Python file."""
    source = filepath.read_text(encoding="utf-8", errors="ignore")
    routes = re.findall(
        r'@app\.route\([\'"]([^\'"]+)[\'"](?:.*?methods=\[([^\]]+)\])?',
        source
    )
    return [(path, methods.replace("'", "").replace('"', "").strip() if methods else "GET")
            for path, methods in routes]


# ── YAML file analysis ─────────────────────────────────────────────────────────

def parse_yaml_intents(filepath: Path):
    """Extract intent names from an NLU YAML file."""
    source = filepath.read_text(encoding="utf-8", errors="ignore")
    return re.findall(r"^- intent:\s+(\S+)", source, re.MULTILINE)


def parse_yaml_responses(filepath: Path):
    """Extract response names from a domain YAML file."""
    source = filepath.read_text(encoding="utf-8", errors="ignore")
    return re.findall(r"^\s{2}(utter_\S+):", source, re.MULTILINE)


def parse_yaml_actions(filepath: Path):
    """Extract custom action names from a domain YAML file."""
    source = filepath.read_text(encoding="utf-8", errors="ignore")
    return re.findall(r"^- (action_\S+)", source, re.MULTILINE)


# ── Documentation renderer ─────────────────────────────────────────────────────

def render_doc(filepath: str, is_new: bool) -> str:
    p        = PROJECT_ROOT / filepath
    label    = "New Feature" if is_new else "Updated Feature"
    now      = datetime.now().strftime("%Y-%m-%d %H:%M")
    ext      = p.suffix.lower()
    filename = p.name

    lines = [
        f"---",
        f"feature: {filename}",
        f"type: {label}",
        f"date: {now}",
        f"file: {filepath}",
        f"---",
        f"",
        f"# {label}: `{filename}`",
        f"",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| File  | `{filepath}` |",
        f"| Type  | {label} |",
        f"| Date  | {now} |",
        f"",
    ]

    # ── Python analysis ──
    if ext == ".py":
        functions, classes = parse_python(p)
        routes             = extract_flask_routes(p)

        if classes:
            lines += ["## Classes", ""]
            for c in classes:
                lines.append(f"### `{c['name']}` *(line {c['line']})*")
                if c["doc"]:
                    lines += ["", f"> {c['doc']}", ""]
                else:
                    lines.append("")

        if functions:
            lines += ["## Functions", ""]
            for f in functions:
                prefix = "async " if f["is_async"] else ""
                sig    = f"{prefix}{f['name']}({', '.join(f['args'])})"
                lines.append(f"### `{sig}` *(line {f['line']})*")
                if f["doc"]:
                    lines += ["", f"> {f['doc']}", ""]
                else:
                    lines.append("")

        if routes:
            lines += ["## API Endpoints", ""]
            lines.append("| Route | Methods |")
            lines.append("|-------|---------|")
            for route, methods in routes:
                lines.append(f"| `{route}` | {methods} |")
            lines.append("")

    # ── YAML analysis ──
    elif ext in (".yml", ".yaml"):
        fname_lower = filename.lower()

        if "nlu" in fname_lower:
            intents = parse_yaml_intents(p)
            if intents:
                lines += ["## Intents", ""]
                for intent in intents:
                    lines.append(f"- `{intent}`")
                lines.append("")

        elif "domain" in fname_lower:
            responses = parse_yaml_responses(p)
            actions   = parse_yaml_actions(p)
            if responses:
                lines += ["## Responses", ""]
                for r in responses:
                    lines.append(f"- `{r}`")
                lines.append("")
            if actions:
                lines += ["## Custom Actions", ""]
                for a in actions:
                    lines.append(f"- `{a}`")
                lines.append("")

    lines += [
        "## Notes",
        "",
        f"- Auto-generated by `auto_doc_agent.py` on {datetime.now().strftime('%Y-%m-%d')}",
        "- Review and expand with business context as needed.",
        "",
    ]

    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    # Consume stdin (Claude Code passes hook payload here)
    if not sys.stdin.isatty():
        try:
            json.loads(sys.stdin.read())
        except Exception:
            pass

    new_files, modified_files = changed_files()
    targets = [(f, True) for f in new_files] + [(f, False) for f in modified_files]

    if not targets:
        sys.exit(0)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    generated = []

    for filepath, is_new in targets:
        label    = "new" if is_new else "updated"
        stem     = Path(filepath).stem.replace("/", "_").replace("\\", "_")
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        doc_name = f"{stem}_{ts}.md"
        doc_path = DOCS_DIR / doc_name

        content = render_doc(filepath, is_new)
        doc_path.write_text(content, encoding="utf-8")
        generated.append(doc_path.name)
        print(f"[AutoDoc] {label.upper()}: {filepath} → .claude/docs/features/{doc_name}", file=sys.stderr)

    if generated:
        print(
            f"[AutoDoc] Generated {len(generated)} doc(s). "
            f"See .claude/docs/features/",
            file=sys.stderr
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
