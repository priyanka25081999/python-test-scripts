import asyncio
import subprocess
import fileinput
import json
import os
from subprocess import PIPE
from ast import literal_eval
from config import Config

def main():
    config = Config()
    source_bucket_name = config.source_bucket_name #"sourcebucket" 
    source_object_name = config.source_object_name      #"rt-object34"
    print(source_bucket_name + " " + source_object_name)
    command = "aws s3api create-multipart-upload --bucket " + source_bucket_name + " --key " + source_object_name
    out = subprocess.check_output(command, shell=True)
    res = out.decode('utf-8')
    print(res)
    final_res = literal_eval(res)
    print("Create multipart upload : {}".format(final_res))
    upload_id = final_res.get("UploadId")
    print(upload_id)

    ### Split file and create a list ###
    cmd = "split  -d -n " + str(config.part_no) +" ~/test50M"
    print("Command : {}".format(cmd))
    out2 = subprocess.check_output(cmd, shell=True)
    res2 = out2.decode('utf-8')
    print(res2)
    process = subprocess.run("ls -la x*  | awk '{print $NF}'", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    object_part = (output.split("\n")[0:-1])
    print(object_part)


    etag_dict = {}
    ### Upload all Parts ####
    for i in range(len(object_part)):
        command2 = "aws s3api upload-part --bucket " + source_bucket_name + " --key " + source_object_name + " --upload-id '" + upload_id + "' --part-number "+str(i+1) + " --body " + "x0"+str(i)
        print("Command : {}".format(command2))
        status = os.system(command2)
        out3 = subprocess.check_output(command2, shell=True)
        res3 = json.loads(out3.decode('utf-8'))
        #print("**res  : {}".format(res3))
        etag = res3.get("ETag")
        etag_dict[i+1] = etag
    print("Upload part : {}".format(etag_dict))

    # Complete multipart upload"
    # etag_str =json.dump(etag_dict, out)
    #xml_f = open('etag_xml.json','w+') 
    #xml_f.write('{"Parts":[')
    #json.dump(etag_dict, xml_f)
    #xml_f.write(']}')


    xml_f = open('etag_xml.json','w+')
    xml_f.write('{"Parts":[')
#json.dump(e_dict, xml_f)

    l=len(etag_dict)
    print(l)
    i=1
    for key, etag in etag_dict.items():
      if i == l:
        xml_f.write('{"ETag" '+" : " +etag)
        xml_f.write(', "PartNumber" '+" : " + str(key) + "}")
      else:
        xml_f.write('{"ETag" '+" : " +etag)
        xml_f.write(', "PartNumber" '+" : " + str(key) + "},")
      i+=1
    
    xml_f.write(']}')

    command3 = "aws s3api complete-multipart-upload --bucket " + source_bucket_name + " --key "+source_object_name+ " --upload-id '" + upload_id + "' --multipart-upload "+ "file://etag_xml.json"

 #tr(etag_str)
    print("*********"+command3)
    status = os.system(command3)
    out4 = subprocess.check_output(command3, shell=True)
    os.system('rm -rf etag_xml.json')
    res4 = out4.decode('utf-8')
    print("Complete multipart upload : {}".format(res4))



main()

