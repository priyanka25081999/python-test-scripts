# This script PUT the multipart upload object in versioning enabled bucket

for i in {1..2}
do
  echo -e "loop number $i"
  rm -rf /tmp/upload.log
  KEY="multipart"
  echo -e $KEY
  aws s3api create-multipart-upload --bucket versioning5 --key multipart --endpoint-url http://localhost:8000 >> /tmp/upload.log
  UPLOAD_ID=$(cat /tmp/upload.log | grep -o "UploadId[\"]:.*" | cut -c12-48)
  modified="${UPLOAD_ID:1:-1}"
  echo $modified
  aws s3api upload-part --bucket versioning5 --key multipart --part-number 1 --body 5mfile --upload-id $modified --endpoint-url http://localhost:8000 >> /tmp/part1.log
  aws s3api upload-part --bucket versioning5 --key multipart --part-number 2 --body 5mfile --upload-id $modified --endpoint-url http://localhost:8000 >> /tmp/part2.log
  
  aws s3api complete-multipart-upload --multipart-upload file://fileparts.json --bucket versioning5 --key multipart --upload-id $modified --endpoint-url http://localhost:8000
  echo -e "multipart upload $i complete"
done
