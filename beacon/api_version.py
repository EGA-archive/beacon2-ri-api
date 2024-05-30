import subprocess
import yaml


repo_url = 'https://github.com/EGA-archive/beacon2-ri-api.git'
output_lines = subprocess.check_output(
    [
        "git",
        "ls-remote",
        "--tags",
        "--refs",
        "--sort=version:refname",
        repo_url,
    ],
    encoding="utf-8",
).splitlines()
last_line_ref = output_lines[-1].rpartition("/")[-1]

with open("beacon/api_version.yml") as api_version_file:
    api_version = yaml.safe_load(api_version_file)

api_version['api_version']=last_line_ref

with open("beacon/api_version.yml", 'w') as out:
    yaml.dump(api_version, out)