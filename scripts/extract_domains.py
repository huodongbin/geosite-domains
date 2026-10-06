import json
from pathlib import Path

SOURCE_DIR = Path("source/geo/geosite")
OUTPUT_DIR = Path("domains")


def extract_domains(json_file: Path):
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    domains = []
    for rule in data.get("rules", []):
        for key in ("domain", "domain_suffix"):
            value = rule.get(key, [])
            if isinstance(value, str):
                domains.append(value)
            elif isinstance(value, list):
                domains.extend(value)

    return list(dict.fromkeys(
        item.strip()
        for item in domains
        if isinstance(item, str) and item.strip()
    ))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old generated files so deleted upstream JSON files don't linger.
    for old_file in OUTPUT_DIR.glob("*.txt"):
        old_file.unlink()

    json_files = sorted(SOURCE_DIR.glob("*.json"))
    print(f"Found {len(json_files)} JSON files")

    total_domains = 0
    for json_file in json_files:
        domains = extract_domains(json_file)
        output_file = OUTPUT_DIR / f"{json_file.stem}.txt"
        output_file.write_text(
            "\n".join(domains) + ("\n" if domains else ""),
            encoding="utf-8",
        )
        total_domains += len(domains)
        print(f"{json_file.name} -> {output_file.name}: {len(domains)} domains")

    print(f"Done: {len(json_files)} files, {total_domains} total domain entries")


if __name__ == "__main__":
    main()
