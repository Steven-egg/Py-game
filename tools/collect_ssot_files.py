import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = Path(__file__).resolve().parent / "ssot_list.txt"
OUTPUT_DIR = Path.home() / "Desktop" / "SSOT_EXPORT"


def parse_line(line: str) -> str | None:
    line = line.strip()
    if not line:
        return None

    line = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line)

    if line.startswith("[") and line.endswith("]"):
        return None

    if "." not in Path(line).name:
        return None

    return line.replace("\\", "/")


def resolve_source(rel_path: str):
    src = ROOT / rel_path

    # 1. 先用完整相對路徑找
    if src.exists() and src.is_file():
        return src, None

    # 2. 找不到時，改用檔名做唯一匹配
    matches = [
        p for p in ROOT.rglob(Path(rel_path).name)
        if p.is_file()
    ]

    if not matches:
        return None, "missing"

    if len(matches) > 1:
        return matches, "ambiguous"

    return matches[0], None


def main():
    if not INPUT_FILE.exists():
        print(f"[ERROR] missing input file: {INPUT_FILE}")
        return

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    copied = 0
    missing = []
    ambiguous = []
    overwritten = []

    for line in INPUT_FILE.read_text(encoding="utf-8").splitlines():
        rel_path = parse_line(line)
        if not rel_path:
            continue

        result, error = resolve_source(rel_path)

        if error == "missing":
            missing.append(rel_path)
            print(f"[MISS] {rel_path}")
            continue

        if error == "ambiguous":
            ambiguous.append((rel_path, result))
            print(f"[ERROR] ambiguous match: {rel_path}")
            for m in result:
                print(f" - {m.relative_to(ROOT)}")
            continue

        src = result
        dst = OUTPUT_DIR / src.name

        if dst.exists():
            overwritten.append(src.name)

        shutil.copy2(src, dst)
        copied += 1
        print(f"[COPY] {src.relative_to(ROOT)} -> {dst.name}")

    print()
    print(f"DONE. copied: {copied}")
    print(f"Output: {OUTPUT_DIR}")

    if overwritten:
        print()
        print("[Overwritten files]")
        for name in overwritten:
            print(f"- {name}")

    if missing:
        print()
        print("[Missing files]")
        for item in missing:
            print(f"- {item}")

    if ambiguous:
        print()
        print("[Ambiguous files]")
        for item, matches in ambiguous:
            print(f"- {item}")
            for m in matches:
                print(f"  - {m.relative_to(ROOT)}")


if __name__ == "__main__":
    main()