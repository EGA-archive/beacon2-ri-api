import subprocess
import yaml


repo_url = 'https://github.com/EGA-archive/beacon2-ri-api.git'
output_lines = subprocess.check_output(
    [
        "git",
        "ls-remote",
        repo_url,
        "rev-parse",
        "--short",
        "sort=committerdate",
        "HEAD"
    ],
    encoding="utf-8",
).splitlines()

line_ref = output_lines[0].rpartition("/")[-1]

last_line_ref=line_ref[0:7]

last_line_ref="v2.0-"+last_line_ref

print(last_line_ref)

with open("beacon/api_version.yml") as api_version_file:
    api_version = yaml.safe_load(api_version_file)

api_version['api_version']=last_line_ref

with open("beacon/api_version.yml", 'w') as out:
    yaml.dump(api_version, out)