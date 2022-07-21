#!/usr/bin/python3
import sys
from cortx.utils.process import SimpleProcess
import json
import time

endpoint='__ENDPOINT__'
cmd= f'aws s3api list-object-versions --bucket bucket1 --max-keys 1011  --endpoint={endpoint} --no-paginate'
res, err, rc = SimpleProcess(cmd).run()

if rc !=0:
    print(err)
    sys.exit()
    
res = res.decode()
res = json.loads(res)
versions = res['Versions']

print("no of versions in lists  - ", len(versions))print("MaxKeys  -  ", res["MaxKeys"])
