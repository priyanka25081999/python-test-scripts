# Script to delete all buckets (versioned/unversioned)
# ------------------------------------------------------

#!/bin/bash

bucket=$1
set -e

echo "Removing all versions from $bucket"

versions=`aws s3api list-object-versions --bucket $bucket |jq '.Versions'`
markers=`aws s3api list-object-versions --bucket $bucket |jq '.DeleteMarkers'`
let count=`echo $versions |jq 'length'`-1

if [ $count -gt -1 ]; then
        echo "removing files"
        for i in $(seq 0 $count); do
                key=`echo $versions | jq .[$i].Key |sed -e 's/\"//g'`
                versionId=`echo $versions | jq .[$i].VersionId |sed -e 's/\"//g'`
                cmd="aws s3api delete-object --bucket $bucket --key $key --version-id $versionId"
                echo $cmd
                $cmd
        done
fi

let count=`echo $markers |jq 'length'`-1

if [ $count -gt -1 ]; then
        echo "removing delete markers"

        for i in $(seq 0 $count); do
                key=`echo $markers | jq .[$i].Key |sed -e 's/\"//g'`
                versionId=`echo $markers | jq .[$i].VersionId |sed -e 's/\"//g'`
                cmd="aws s3api delete-object --bucket $bucket --key $key --version-id $versionId"
                echo $cmd
                $cmd
        done
fi
# --------------------------------------------------------

# Steps to run the above script:
# pip3 install awscli
# pip3 install awscli-plugin-endpoint
# aws configure set plugins.endpoint awscli_plugin_endpoint
# aws configure set s3.endpoint_url http://localhost:8000
# aws configure set s3api.endpoint_url http://localhost:8000
# aws s3 ls | cut -d" " -f 3 | xargs -I{} sh delete_versioned_buckets.sh {}
# aws s3 ls | cut -d" " -f 3 | xargs -I{} aws s3 rb s3://{} --force

