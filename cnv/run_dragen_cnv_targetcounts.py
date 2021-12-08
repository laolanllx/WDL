# Task Summary: create json files for each samples and generate a bash shell including each samples wdl running commands 
# Tool Name: python
# Input: cnv target counts json file
# Outputs: each sample json file and a bash script with workflow running commands

import glob
import os
import json

# function
# change json file based on the different sample information
def changejsonfile(data, bampath, sampleid):
    data['CNV_TC.inputBam'] = bampath
    data['CNV_TC.output_prefix'] = sampleid
    return data

jsonfile = "/mnt/isilon/conlin_lab/data/clinical/v2_exome_parents/cnv_target_counts.json"

# part 1: get bam files name and sample ids
bamlist = glob.glob('*.bam')
sampleids = [i.split('.')[0] for i in bamlist]

# part 2: read json file 
# jsonfile = "/staging/scratch/exome_cnv/cnv_target_counts.json"
f = open(jsonfile,'r')
data = json.load(f)
f.close()


# part 3: edit json info for each sample and run wdl for each sample file
# cmds = "nohup java -jar /staging/scratch/lanxin/cromwell-55.jar run cnv_target_counts.wdl --inputs cnv_target_counts.json --options options.json &"

jsonpath = []

for i in range(len(bamlist)):
    sampleid = sampleids[i]
    bampath = os.path.abspath(bamlist[i])
    data = changejsonfile(data, bampath, sampleid)
    jsontitle = '/mnt/isilon/conlin_lab/data/clinical/v2_exome_parents/jsonfiles/cnv_target_counts_'
    outputjson = jsontitle + sampleid + '.json'
    json_object = json.dumps(data, indent = 7)
    with open(outputjson, 'w') as json_file:
        json_file.write(json_object)
    jsonpath.append(outputjson)

run_wdl = 'run_wdl_cnv_targetcounts.sh'    
b = open(run_wdl, 'w')
for i in jsonpath:
    cmd = "java -jar /staging/scratch/lanxin/cromwell-55.jar run cnv_target_counts.wdl --inputs " + str(i) + '\n'
    b.write(cmd)
b.close()


