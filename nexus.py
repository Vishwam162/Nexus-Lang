import os, sys, urllib.request
from lexer import lexer
from parser import parser
from compiler import NexusInterpreter

VERSION = "8.1.1"
GITHUB_USER = "Vishwam162"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/Nexus-Lang/main/"

def auto_update():
    try:
        with urllib.request.urlopen(BASE_URL + "version.txt", timeout=2) as r:
            remote_version = r.read().decode().strip()
            if remote_version != VERSION:
                print(f"[*] Update Found: {remote_version}. Syncing...")
                target_dir = os.path.dirname(__file__)
                for f in ["nexus.py", "lexer.py", "parser.py", "compiler.py", "version.txt"]:
                    urllib.request.urlretrieve(BASE_URL + f, os.path.join(target_dir, f))
                print("[+] Auto-Update Complete. Restarting...")
                os.execv(sys.executable, ['python'] + sys.argv)
    except: pass

def main():
    auto_update()
    if len(sys.argv) < 2:
        print(f"Nexus v{VERSION} | Usage: nexus <file.nxs>")
        return

    script_path = sys.argv[-1] 
    if script_path.endswith(".nxs"):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            ast = parser.parse(code)
            if ast:
                interp = NexusInterpreter()
                for node in ast: interp.walk(node)
        except Exception as e: print(f"Nexus Error: {e}")

if __name__ == "__main__":
    main()
