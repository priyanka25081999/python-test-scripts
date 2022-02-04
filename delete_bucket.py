# This script removes all existing buckets with objects

#!/usr/bin/python3
import subprocess

# run() returns a CompletedProcess object if it was successful
# errors in the created process are raised here too
process = subprocess.run("aws s3 ls | awk '{print $NF}'", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout

# List bucket names
bucket=(output.split("\n")[0:-1])
print(bucket)

# Delete all buckets
for i in bucket:
   subprocess.run("aws s3 rb s3://%s --force" % str(i), shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
   print("Deleting bucket %s" %str(i))
   output = process.stdout

