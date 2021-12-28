# multipart api
import asyncio
import subprocess
import fileinput
import os
from subprocess import PIPE
from ast import literal_eval

def main():
    source_bucket_name = "sourcebucket"
    source_object_name = "object14"
    print(source_bucket_name + " " + source_object_name)
    command = "aws s3api create-multipart-upload --bucket " + source_bucket_name + " --key " + source_object_name
    out = subprocess.check_output(command, shell=True)
    res = out.decode('utf-8')
    #print(type(res))
    final_res = literal_eval(res)
    print("Create multipart upload : {}".format(final_res))
    upload_id = final_res.get("UploadId")
    print(upload_id)


    # Upload part
    part_no = 5
    etag_dict = {}
    files = subprocess.check_output("cat etag.json", shell=True)

    #file = os.open('demo_object.txt',os.O_RDONLY)
    #tagset = os.read(file, os.path.getsize(file))
    #files = files.decode('utf-8')
    #print(files)
    for i in range(1, part_no+1):
     with open("demo_object.txt","r") as f1:
      ff2 = f1.read()
      print("****file : ",ff2)
      command2 = "aws s3api upload-part --bucket " + source_bucket_name + " --key " + source_object_name + " --upload-id '" + upload_id + "' --part-number "+str(i) + " --body file://demo_object.txt"
      print("Command : {}".format(command2))
      status = os.system(command2)
      print("**status : {}",status)
      out2 = subprocess.check_output(command2, shell=True)
      res2 = out2.decode('utf-8')
      etag = res2.get("ETag")
      etag_dict[i] = etag
    print("Upload part : {}".format(etag_dict))

   
    # complete multipart
    etag_str = "<CompleteMultipartUpload>"
    for part, etag in etag_dict.items():
        etag_str += "<Part><ETag>" + \
                str(etag) + "</ETag><PartNumber>" + str(part) + "</PartNumber></Part>"
    etag_str += "</CompleteMultipartUpload>"
    command3 = "aws s3api complete-multipart-upload --bucket " + source_bucket_name + " --key "+source_object_name+ " --upload-id '" + upload_id + "' --multipart-upload " + etag_str
    out3 = subprocess.check_output(command3, shell=True)
    #res3 = out3.decode('utf-8')
    #print("Complete multipart upload : {}".format(res3))

main()
#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())
