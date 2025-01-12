import toml

def bump_patch(file_path="pyproject.toml"):
    with open(file_path, "r") as file:
        data = toml.load(file)

    version = data.get("project", {}).get("version")
    if not version:
        raise ValueError("`project.version` is not set in `pyproject.toml`.")

    major, minor, patch = map(int, version.split("."))
    new_version = f"{major}.{minor}.{patch + 1}"
    data["project"]["version"] = new_version

    with open(file_path, "w") as file:
        toml.dump(data, file)

    print(f"Bumped version to {new_version}")

def get_version(file_path="pyproject.toml"):
    with open(file_path, "r") as file:
        data = toml.load(file)

    output = data.get("project", {}).get("version")

    # send to stdout
    print(output)
