# 05_engine/content_loader.py
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# -----------------------------
# Errors
# -----------------------------
class ContentLoaderError(Exception):
    pass


@dataclass
class LoadIssue:
    kind: str           # e.g., "io", "json", "schema", "shape"
    category: str       # "quests" | "items" | "monsters"
    file: str           # path string
    message: str


# -----------------------------
# Result Container
# -----------------------------
@dataclass
class ContentPack:
    # Minimal: keep raw JSON dicts; runtime layer will interpret them.
    quests: List[Dict[str, Any]]
    items: List[Dict[str, Any]]
    monsters: List[Dict[str, Any]]
    issues: List[LoadIssue]

    def ok(self) -> bool:
        return len(self.issues) == 0


# -----------------------------
# Loader
# -----------------------------
class ContentLoader:
    """
    MVL content loader for Engine Phase B:
    - Scan official fixture: 03_data/{quests,items,monsters}/test_*.json
    - Read JSON
    - Schema string check only (no jsonschema validate here)
    """

    def __init__(self, project_root: Optional[Path] = None) -> None:
        # content_loader.py should live in 05_engine/
        # project_root -> repo root containing 03_data/
        self.project_root = project_root or Path(__file__).resolve().parents[1]

        self.data_root = self.project_root / "03_data"
        self.paths = {
            "quests": self.data_root / "quests",
            "items": self.data_root / "items",
            "monsters": self.data_root / "monsters",
        }

        # Heuristic keyword check (lightweight; does NOT enforce exact schema path)
        self.schema_keywords = {
            "quests": "quest",
            "items": "item",
            "monsters": "monster",
        }

    # ---------
    # Public API
    # ---------
    def load_all(self, pattern: str = "test_*.json") -> ContentPack:
        issues: List[LoadIssue] = []

        quests = self._load_category("quests", pattern, issues)
        items = self._load_category("items", pattern, issues)
        monsters = self._load_category("monsters", pattern, issues)

        return ContentPack(
            quests=quests,
            items=items,
            monsters=monsters,
            issues=issues,
        )

    # ---------
    # Internals
    # ---------
    def _load_category(
        self,
        category: str,
        pattern: str,
        issues: List[LoadIssue],
    ) -> List[Dict[str, Any]]:
        folder = self.paths[category]

        if not folder.exists() or not folder.is_dir():
            issues.append(
                LoadIssue(
                    kind="io",
                    category=category,
                    file=str(folder),
                    message="Folder missing or not a directory",
                )
            )
            return []

        files = sorted(folder.glob(pattern))
        if not files:
            issues.append(
                LoadIssue(
                    kind="io",
                    category=category,
                    file=str(folder),
                    message=f"No files matched pattern: {pattern}",
                )
            )
            return []

        out: List[Dict[str, Any]] = []
        for fp in files:
            data = self._read_json(fp, category, issues)
            if data is None:
                continue

            if not isinstance(data, dict):
                issues.append(
                    LoadIssue(
                        kind="shape",
                        category=category,
                        file=str(fp),
                        message="Top-level JSON must be an object/dict",
                    )
                )
                continue

            self._check_schema_string(data, category, fp, issues)

            out.append(data)

        return out

    def _read_json(
        self,
        fp: Path,
        category: str,
        issues: List[LoadIssue],
    ) -> Optional[Dict[str, Any]]:
        try:
            text = fp.read_text(encoding="utf-8")
        except Exception as e:
            issues.append(
                LoadIssue(
                    kind="io",
                    category=category,
                    file=str(fp),
                    message=f"Read failed: {e}",
                )
            )
            return None

        try:
            parsed = json.loads(text)
        except Exception as e:
            issues.append(
                LoadIssue(
                    kind="json",
                    category=category,
                    file=str(fp),
                    message=f"JSON parse failed: {e}",
                )
            )
            return None

        return parsed  # type: ignore[return-value]

    def _check_schema_string(
        self,
        obj: Dict[str, Any],
        category: str,
        fp: Path,
        issues: List[LoadIssue],
    ) -> None:
        """
        MVL requirement: "schema 字串檢查"
        - `$schema` must exist
        - must be a non-empty string
        - lightweight keyword match (avoid binding to exact structure paths)
        """
        if "$schema" not in obj:
            issues.append(
                LoadIssue(
                    kind="schema",
                    category=category,
                    file=str(fp),
                    message="Missing required field: $schema",
                )
            )
            return

        schema_val = obj.get("$schema")
        if not isinstance(schema_val, str) or not schema_val.strip():
            issues.append(
                LoadIssue(
                    kind="schema",
                    category=category,
                    file=str(fp),
                    message="$schema must be a non-empty string",
                )
            )
            return

        kw = self.schema_keywords.get(category, "")
        if kw and kw.lower() not in schema_val.lower():
            issues.append(
                LoadIssue(
                    kind="schema",
                    category=category,
                    file=str(fp),
                    message=f"$schema string does not contain expected keyword '{kw}' (got: {schema_val})",
                )
            )


# -----------------------------
# Quick smoke runner (optional)
# -----------------------------
def _format_issues(issues: List[LoadIssue]) -> str:
    lines = []
    for it in issues:
        lines.append(f"[{it.kind}] {it.category} :: {it.file} :: {it.message}")
    return "\n".join(lines)


if __name__ == "__main__":
    loader = ContentLoader()
    pack = loader.load_all()

    print("=== ContentLoader MVL ===")
    print(f"project_root: {loader.project_root}")
    print(f"quests:   {len(pack.quests)}")
    print(f"items:    {len(pack.items)}")
    print(f"monsters: {len(pack.monsters)}")
    print(f"issues:   {len(pack.issues)}")

# 在 content_loader.py 底部 __main__ 區塊，把原本的 if pack.issues: ... 改成：

    if pack.issues:
        print("\n--- Issues ---")
        print(_format_issues(pack.issues))

        fatal = [it for it in pack.issues if it.kind in ("io", "json", "shape")]
        if fatal:
            raise SystemExit(2)

    print("\nOK (schema issues are warnings in MVL)")