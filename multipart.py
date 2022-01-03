# This is multipart upload test script
# Multipart API - Create, Upload-part, Complete
 
import json
import os
import subprocess
from ast import literal_eval
from config import Config
from subprocess import PIPE

def main():
    
    # Make an object of Config class
    # Please note : source bucket should be exist
    config = Config()
    source_bucket_name = config.source_bucket_name 
    source_object_name = config.source_object_name
    target_bucket_name = "targetbucket"
    print("\nBucket Name : " + source_bucket_name + "\n" + "Object Name : " + source_object_name)
    print("----------------------------------------")

    # Create multipart upload
    # without metadata parameter
    #command1 = "aws s3api create-multipart-upload --bucket " + source_bucket_name + " --key " + source_object_name

    # with metadata parameter
    # replace __TARGET_SITE__ with the target_site 
    # For example == "target-site": "awss3" 
    command1 = "aws s3api create-multipart-upload --bucket " + source_bucket_name + " --key " + source_object_name + " --metadata '{\"target-site\": \"__TARGET_SITE__\", \"replication\" : \"true\", \"target-bucket\": \"" +target_bucket_name + "\"}'"
    print("command 1  = ", command1)
    output1 = subprocess.check_output(command1, shell=True)
    result1 = output1.decode('utf-8')
    print("Create multipart upload : {}".format(result1))

    # Convert result into dictionary to get upload-id
    final_res = literal_eval(result1)
    upload_id = final_res.get("UploadId")
    print("Upload ID : ",upload_id)
    print("----------------------------------------\n")

    # Split a file 
    command2 = "split  -d -n " + str(config.part_no) +" ~/test50M"
    output2 = subprocess.check_output(command2, shell=True)
    result2 = output2.decode('utf-8')

    # create a list
    process = subprocess.run("ls -la x*  | awk '{print $NF}'", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    object_part = (output.split("\n")[0:-1])

    # Upload part
    etag_dict = {}
    
    for part_no in range(len(object_part)):
        command3 = "aws s3api upload-part --bucket " + source_bucket_name + " --key " + source_object_name + " --upload-id '" + upload_id + "' --part-number "+str(part_no+1) + " --body " + "x0"+str(part_no)
        output3 = subprocess.check_output(command3, shell=True)
        result3 = json.loads(output3.decode('utf-8'))
        print("Upload Part {}  : {}".format(part_no+1, result3))
        etag = result3.get("ETag")
        etag_dict[part_no+1] = etag
    print("\nUpload part ETag Dict : {}".format(etag_dict))
    print("----------------------------------------")

    # Complete multipart upload
    # Create and open a new file
    file_obj = open('etag_file.json','w+')
    file_obj.write('{"Parts":[')

    length=len(etag_dict)
    i=1

    for key, etag in etag_dict.items():
      if i == length:
        file_obj.write('{"ETag" '+" : " +etag)
        file_obj.write(', "PartNumber" '+" : " + str(key) + "}")
      else:
        file_obj.write('{"ETag" '+" : " +etag)
        file_obj.write(', "PartNumber" '+" : " + str(key) + "},")
      i+=1
    
    file_obj.write(']}')
    file_obj.close()

    command4 = "aws s3api complete-multipart-upload --bucket " + source_bucket_name + " --key "+source_object_name+ " --upload-id '" + upload_id + "' --multipart-upload "+ "file://etag_file.json"

    output4 = subprocess.check_output(command4, shell=True)
    result4 = output4.decode('utf-8')
    print("\nComplete multipart upload : {}".format(result4))
    result4 = json.loads(result4)
    final_etag = result4.get("ETag")
    print("\nFinal ETag : {}".format(final_etag))

    # Remove the file
    os.system('rm -rf etag_file.json')

main()

