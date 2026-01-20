# scripts/bundle_pack.py
import argparse
import json
import sys
from pathlib import Path
import zipfile


def parse_args():
    p = argparse.ArgumentParser(description="Pack Evaluation Bundle into ZIP")
    p.add_argument("--bundle-dir", required=True, help="Path to evaluation bundle directory")
    p.add_argument("--out-dir", help="Output directory for ZIP")
    p.add_argument("--zip-name", help="Override zip file name")
    p.add_argument("--dry-run", action="store_true", help="Validate only, do not create ZIP")
    return p.parse_args()


def load_manifest(bundle_dir: Path) -> dict:
    manifest_path = bundle_dir / "bundle_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError("bundle_manifest.json not found")

    with manifest_path.open(encoding="utf-8") as f:
        return json.load(f)


def validate_manifest(bundle_dir: Path, manifest: dict):
    if manifest.get("schema_version") != "0.1":
        raise ValueError("Unsupported bundle_manifest schema_version")

    paths = []

    obs = manifest.get("observation", {})
    paths += [obs.get("result"), obs.get("summary")]

    auto = manifest.get("evaluation_auto", {})
    paths.append(auto.get("result"))

    for h in manifest.get("evaluation_human", []):
        paths.append(h.get("record"))

    judgment = manifest.get("evaluation_judgment", {})
    paths.append(judgment.get("record"))

    for rel in paths:
        if not rel:
            continue
        p = bundle_dir / rel
        if not p.exists():
            raise FileNotFoundError(f"Missing file referenced in manifest: {rel}")


def main():
    args = parse_args()
    bundle_dir = Path(args.bundle_dir).resolve()

    if not bundle_dir.exists():
        print("Bundle directory not found", file=sys.stderr)
        sys.exit(1)

    manifest = load_manifest(bundle_dir)
    validate_manifest(bundle_dir, manifest)

    bundle_id = manifest.get("bundle_id")
    if not bundle_id:
        print("bundle_id missing in manifest", file=sys.stderr)
        sys.exit(1)

    zip_name = args.zip_name or f"evaluation_bundle_{bundle_id}.zip"
    out_dir = Path(args.out_dir).resolve() if args.out_dir else bundle_dir.parent
    zip_path = out_dir / zip_name

    if args.dry_run:
        print("[DRY-RUN] Bundle validated successfully")
        print(f"[DRY-RUN] ZIP would be created at: {zip_path}")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in bundle_dir.rglob("*"):
            if path.is_file():
                arcname = path.relative_to(bundle_dir.parent)
                zf.write(path, arcname)

    print(f"[OK] Evaluation Bundle packed: {zip_path}")


if __name__ == "__main__":
    main()
