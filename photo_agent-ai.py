import os, json, shutil, csv, time, argparse
from pathlib import Path
from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ValidationError
from rich import print
from rich.console import Console
from rich.table import Table

# ---------- AI backends ----------
def call_llm(prompt: str, backend: str, model: str):
    """
    Returns plain text from the model. Supports:
      backend = "ollama"  -> uses local Ollama http API
      backend = "openai"  -> uses OpenAI Chat Completions (needs OPENAI_API_KEY)
    The prompt asks the model to return strict JSON.
    """
    if backend == "ollama":
        import requests
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=300,
        )
        r.raise_for_status()
        return r.json()["response"]

    elif backend == "openai":
        from openai import OpenAI
        client = OpenAI()  # reads OPENAI_API_KEY
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role":"system","content":"You are a helpful JSON planner."},
                      {"role":"user","content":prompt}],
            temperature=0.2
        )
        return resp.choices[0].message.content

    else:
        raise SystemExit("Unsupported backend. Use 'ollama' or 'openai'.")


# ---------- Data models for plans ----------
class MoveOp(BaseModel):
    src: str
    dst: str
    action: Literal["move","copy"] = "move"

class Plan(BaseModel):
    target_root: str
    rationale: str = ""
    operations: List[MoveOp] = Field(default_factory=list)


# ---------- Helpers ----------
def list_candidate_files(source_dir: Path, exts: List[str]) -> List[Path]:
    out = []
    extset = {e.lower() for e in exts}
    for root, _, files in os.walk(source_dir):
        for fn in files:
            p = Path(root) / fn
            if p.suffix.lower() in extset:
                out.append(p)
    return out

def guess_file_date(p: Path) -> str:
    # use modified time (simple; EXIF can be added later)
    ts = p.stat().st_mtime
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

def make_prompt(user_instruction: str, source_dir: Path, target_root: Path, files: List[Path]) -> str:
    # Trim to first 40 files to keep prompt small
    sample = files[:40]
    file_lines = []
    for f in sample:
        file_lines.append(f"{f.name} | modified={guess_file_date(f)} | ext={f.suffix.lower()}")

    schema = {
        "target_root": "ABSOLUTE target folder root where you will organise into",
        "rationale": "Short explanation of your folder naming and placement choices.",
        "operations": [
            {"src": "absolute source path", "dst": "absolute destination path (under target_root)", "action": "move|copy"}
        ]
    }

    return f"""
You are an organisation planner for photos. The user will describe context like trips, years, people.
You must return STRICT JSON (no markdown, no commentary) matching this schema:

{json.dumps(schema, indent=2)}

Rules:
- Respect the user's intent (e.g., "holiday to New Zealand in 2008").
- Propose a clean, human-friendly hierarchy, e.g.: Trips/2008/New Zealand/ or Photos/2008/2008-12 NZ/.
- Use only the files we list from the source folder.
- Do NOT invent files. Only plan moves for listed paths.
- Every "dst" must be under target_root.
- Keep folder names brief, Title Case where sensible.
- Prefer "move" for large reorganisations (the user can change later).
- IMPORTANT: Return ONLY JSON.

User instruction:
"{user_instruction}"

Source folder: "{source_dir}"
Target root: "{target_root}"

Sample of files to consider (name | modified | ext):
{chr(10).join(file_lines)}

Return the final plan now as JSON only.
"""

def pretty_preview(plan: Plan, limit=60):
    table = Table(title="Planned Operations (preview)")
    table.add_column("Action", style="cyan", no_wrap=True)
    table.add_column("From")
    table.add_column("To")
    for op in plan.operations[:limit]:
        table.add_row(op.action.upper(), op.src, op.dst)
    if len(plan.operations) > limit:
        table.add_row("...", f"... and {len(plan.operations)-limit} more", "")
    print(table)
    print(f"[bold]Target root:[/bold] {plan.target_root}")
    if plan.rationale:
        print(f"[bold]Rationale:[/bold] {plan.rationale}")

def write_audit(moves: List[MoveOp]) -> str:
    name = f"photo_agent_audit_{int(time.time())}.csv"
    with open(name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp","action","src","dst"])
        ts = datetime.now().isoformat(timespec="seconds")
        for m in moves:
            w.writerow([ts, m.action, m.src, m.dst])
    return name

def apply_plan(plan: Plan):
    for m in plan.operations:
        src, dst = Path(m.src), Path(m.dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if m.action == "copy":
            shutil.copy2(src, dst)
        else:
            shutil.move(src, dst)

def undo_from_audit(audit_csv: str):
    rows = []
    with open(audit_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in reversed(rows):
        action, src, dst = row["action"], Path(row["src"]), Path(row["dst"])
        if action == "move" and dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(dst, src)
        elif action == "copy" and dst.exists():
            try: os.remove(dst)
            except OSError: pass


# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="AI-first Photo Organiser Agent")
    ap.add_argument("--source", required=True, help="Folder of photos to organise (e.g., D:\\Photos\\Inbox)")
    ap.add_argument("--target", required=True, help="Target root (e.g., D:\\Photos\\Organised)")
    ap.add_argument("--say", required=True, help='Your instruction, e.g. "New Zealand holiday 2008"')
    ap.add_argument("--backend", choices=["ollama","openai"], default="ollama")
    ap.add_argument("--model", default="llama3.1", help="Ollama: llama3.1, mistral, etc. OpenAI: gpt-4o-mini, gpt-4.1, etc.")
    ap.add_argument("--apply", action="store_true", help="Actually perform moves (default: dry run)")
    ap.add_argument("--undo", help="Undo from an audit CSV")
    ap.add_argument("--exts", default=".jpg,.jpeg,.png,.gif,.mp4,.mov", help="Comma-separated extensions to include")
    args = ap.parse_args()

    if args.undo:
        undo_from_audit(args.undo)
        print(f"[green]Undo complete from {args.undo}[/green]")
        return

    source = Path(args.source)
    target = Path(args.target)
    if not source.exists():
        raise SystemExit(f"Source not found: {source}")
    target.mkdir(parents=True, exist_ok=True)

    exts = [e.strip() for e in args.exts.split(",") if e.strip()]
    files = list_candidate_files(source, exts)
    if not files:
        print("[yellow]No matching files found. Check --exts or source path.[/yellow]")
        return

    prompt = make_prompt(args.say, source, target, files)
    raw = call_llm(prompt, backend=args.backend, model=args.model).strip()

    # The model must return strict JSON. If it returns Markdown, try to salvage braces.
    start, end = raw.find("{"), raw.rfind("}")
    raw_json = raw[start:end+1] if start != -1 and end != -1 else raw

    try:
        data = json.loads(raw_json)
        plan = Plan(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        print("[red]The model did not return valid JSON. Try simplifying the instruction or a different model.[/red]")
        print(raw[:600])
        raise SystemExit(e)

    # Preview
    pretty_preview(plan)

    # Always write audit (so you can undo even if apply is false)
    audit = write_audit(plan.operations)
    print(f"[bold]Audit written:[/bold] {audit}")

    if not args.apply:
        print("[cyan]Dry-run complete. Re-run with --apply to perform changes.[/cyan]")
        return

    apply_plan(plan)
    print("[green]Done![/green]")
    print(f"You can undo with:  python photo_agent_ai.py --undo {audit}")

if __name__ == "__main__":
    main()
