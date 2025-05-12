import json
import os
import subprocess
import threading

from concurrent.futures import ThreadPoolExecutor, as_completed

# kubectl get pods -A (gets from all namespaces) -o json | tee pods.json


def try_pod(command: str) -> str:
    # helps with printing I/O without needing thread locks
    try:
        result = subprocess.run(f"{command}", capture_output=True, shell=True, check=True, timeout=5)
        result = result.stdout.decode()
        if 'forbidden' in result.lower():
            return "Forbidden #1"
        else:
            return f"[ POTENTIAL RCE -> '{command}' ]"
    except Exception as err:
        return "Forbidden #2"


def main():
    commands = []
    pods_data = json.loads(open("pods.json", 'r').read())
    shell_types = ["/bin/bash", "/bin/sh"]
    
    for item in pods_data['items']:
        if item['kind'] == 'Pod':
            for shell_type in shell_types:
                # we have to do this because the POD might not have bash or sh as it's primary shell.
                NAME_SPACE = item['metadata']['namespace']
                POD_NAME = item['metadata']['name']
                    
                # don't want it hanging the I/O so I detach it.
                # had to remove -it because then we never get any output so it hangs if there is a successful RCE.
                command = f"kubectl exec -n {NAME_SPACE} {POD_NAME} --kubeconfig=player.kubeconfig --insecure-skip-tls-verify=true -- {shell_type} # use -it"
                commands.append(command)
    
    
    with ThreadPoolExecutor(max_workers=50) as exec:
        # now we'll run all the commands in parallel
        futures = [ exec.submit(try_pod, command) for command in commands ]        
        
        for future in as_completed(futures):
            result = future.result()
            if not "forbidden" in result.lower():
                print(result)
    # otherwise it'll prematurely exit LMAO
    input(f"[ Enter to EXIT. ]")
if __name__ == "__main__":
    main()
