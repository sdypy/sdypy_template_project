import re
import argparse

package_name = "sdypy_template_project"

# pyproject.toml is edited as plain text, not parsed and re-written, so that its
# comments and formatting are kept. Only the `version = "..."` line changes.
PROJECT_TABLE = re.compile(r"^\[project\][ \t]*\r?$", re.MULTILINE)
NEXT_TABLE = re.compile(r"^\[", re.MULTILINE)
VERSION_LINE = re.compile(r"^(version\s*=\s*)([\"'])(.*?)\2", re.MULTILINE)


def find_version(text):
    project = PROJECT_TABLE.search(text)
    if project is None:
        raise ValueError("No [project] table found in pyproject.toml")
    next_table = NEXT_TABLE.search(text, project.end())
    end = next_table.start() if next_table else len(text)

    match = VERSION_LINE.search(text, project.end(), end)
    if match is None:
        raise ValueError("No version found in the [project] table of pyproject.toml")
    return match


def get_version():
    with open("pyproject.toml", "r", encoding="utf8", newline="") as f:
        return find_version(f.read()).group(3)


def synchronize_version():
    print("Synchronizing version (pyproject.toml and __init__.py)...")

    version_toml = get_version()

    with open(f"{package_name}/__init__.py", "r") as f:
        init = f.readlines()

    for i, line in enumerate(init):
        if "__version__" in line:
            init[i] = "__version__ = " + f'"{version_toml}"' + "\n"
    init = "".join(init)

    with open(f"{package_name}/__init__.py", "w") as f:
        f.write(init)

    with open("docs/source/conf.py", "r", encoding="utf8") as f:
        conf = f.readlines()

    for i, line in enumerate(conf):
        if "version = " in line and not line.strip().startswith("#"):
            conf[i] = f"version = '{version_toml.rsplit('.', 1)[0]}'\n"
        elif "release = " in line and not line.strip().startswith("#"):
            conf[i] = f"release = '{version_toml}'\n"

    with open("docs/source/conf.py", "w", encoding="utf8") as f:
        f.write("".join(conf))


def set_version(version):
    with open("pyproject.toml", "r", encoding="utf8", newline="") as f:
        text = f.read()

    match = find_version(text)
    quote = match.group(2)
    text = text[:match.start()] + f"{match.group(1)}{quote}{version}{quote}" + text[match.end():]

    with open("pyproject.toml", "w", encoding="utf8", newline="") as f:
        f.write(text)


def bump_version(bump):
    version = get_version()
    version_parts = version.split(".")
    if bump == "patch":
        version_parts[2] = str(int(version_parts[2]) + 1)
    elif bump == "minor":
        version_parts[1] = str(int(version_parts[1]) + 1)
        version_parts[2] = "0"
    elif bump == "major":
        version_parts[0] = str(int(version_parts[0]) + 1)
        version_parts[1] = "0"
        version_parts[2] = "0"
    else:
        raise ValueError(f"Invalid bump type: {bump}")

    version = ".".join(version_parts)
    set_version(version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bump", default="", choices=["patch", "minor", "major"],
                        help="Bump the version of the package.")
    parser.add_argument("--set-version", type=str, help="Set the version of the package.")
    args = parser.parse_args()

    if args.set_version:
        set_version(args.set_version)
    elif args.bump:
        bump_version(args.bump)

    synchronize_version()
