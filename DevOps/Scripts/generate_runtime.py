# create runtime values yaml file, consisting of container image tag in k8s namespace, and push it to git 
# later to be used for tracking and using the image files in running envs

import os
import sys
import yaml

tag = sys.argv[1]
namespace = sys.argv[2]
runtime_file = {"image": {"tag": tag}}
with open(f'{os.getenv("path_to_runtime")}/runtime.yaml', 'w+') as file:
  yaml.dump(runtime_file, file)
os.system(f'git add {os.getenv("path_to_runtime")}/runtime.yaml')
if os.popen("git diff master").read():
  os.system(f'git commit -m "Update {namespace} Runtime Values" {os.getenv("path_to_runtime")}/runtime.yaml')
  os.system(f'git push origin')
else:
  print("Runtime values unchanged, no changes to push to git.")