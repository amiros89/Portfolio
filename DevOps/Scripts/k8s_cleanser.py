import os
import json
from datetime import datetime

MAX_HOURS = 2

namespaces_to_clean = ['ci', 'test']
namespaces = json.loads(os.popen("kubectl get namespaces -o json").read())['items']
for namespace in namespaces:
    namespace_name = namespace['metadata']['name']
    if namespace_name in namespaces_to_clean:
        print(f'Current namespace: {namespace_name}')
        # clean old installed helm charts
        releases = json.loads(os.popen(f"helm list -o json -n {namespace_name}").read().rstrip())
        if releases:
            for release in releases:
                updated_time = release["updated"][:24]
                formatted_updated_time = datetime.strptime(updated_time, "%Y-%m-%d %H:%M:%S.%f")
                time_passed = (datetime.now() - formatted_updated_time).total_seconds() / (3600*MAX_HOURS)
                if time_passed > MAX_HOURS:
                    os.system(f"helm uninstall {release['name']} -n {namespace_name}")
                else:
                    print(f"Skipping helm release: {release['name']}, time passed since last update is only:"
                          f" {time_passed:.2f} hours.")
        else:
            print(f"No helm releases installed in namespace: {namespace_name}")

        # other kubernetes resources
        entities_to_delete = ["deployments",
                              "services"]
        for entities in entities_to_delete:
            print(f"Looking for {entities}...")
            items = json.loads(os.popen(f"kubectl get {entities} -o json -n {namespace_name} ").read())["items"]
            for item in items:
                # print(item["metadata"]["creationTimestamp"])
                item_name = item["metadata"]["name"]
                formatted_updated_time = datetime.strptime(item["metadata"]["creationTimestamp"], "%Y-%m-%dT%H:%M:%SZ")
                time_passed = (datetime.now() - formatted_updated_time).total_seconds() / (3600*MAX_HOURS)
                if 'Helm' not in item["metadata"]["labels"].values() and time_passed > MAX_HOURS:
                    print(f"found entity of kind {entities} that needs to be deleted: {item_name},"
                          f" time passed: {round(time_passed, 2)} hours")
                    os.system(f'kubectl delete {entities}/{item_name} -n {namespace_name}')
                    continue
                else:
                    print(f"Skipping entity of kind {entities} managed by helm: {item['metadata']['name']}")
    else:
        continue

print("Done.")
