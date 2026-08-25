import hashlib
import json
import os
import pwd
import socket
import stat
import subprocess
from pathlib import Path

ARTIFACT = Path("/usr/local/builds/adhoc-dep/artifacts/public/validation.json")
PASSWD = Path("/etc/passwd")
CONFIG = Path("/usr/local/builds/adhoc-dep/script_config.yaml")
MODULE = Path(
    "/usr/local/builds/adhoc-dep/scriptworker-scripts/"
    "iscript/src/iscript/script.py"
)


def command(*args):
   return subprocess.check_output(args, text=True).strip()


def main():
   passwd = PASSWD.read_bytes()
   module_stat = MODULE.stat()
   result = {
       "whoami": command("/usr/bin/whoami"),
       "id": command("/usr/bin/id"),
       "hostname": socket.gethostname(),
       "pwd": os.getcwd(),
       "passwd_first_line": passwd.splitlines()[0].decode("utf-8", "replace"),
       "passwd_sha256": hashlib.sha256(passwd).hexdigest(),
       "script_config_exists": CONFIG.is_file(),
       "script_config_readable": os.access(CONFIG, os.R_OK),
       "replaced_module_owner": pwd.getpwuid(module_stat.st_uid).pw_name,
       "replaced_module_mode": stat.filemode(module_stat.st_mode),
       }
   ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
   ARTIFACT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
   return 0
