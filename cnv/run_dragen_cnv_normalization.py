import glob
import os
import json

# function
def changejsonfile(data, targetcountsfile, sampleid, normalfile):
    data['CNV_N.targetcountsfile'] = targetcountsfile
    data['CNV_N.output_prefix'] = 'dragen_cnv_normalization_' + sampleid
    data['CNV_N.normal_list'] = normalfile
    return data


# part 1: get bam files name and sample ids
bamlist = glob.glob('*.bam')
sampleids = [i.split('.')[0] for i in bamlist]

# part 2: read json file 
# jsonfile = '/Users/liul8/cromwell/cnv_normalization.json'
# jsonfile = "/staging/scratch/exome_cnv/cnv_normalization.json"
jsonfile = "/mnt/isilon/conlin_lab/data/clinical/v2_exome_parents/cnv_normalization.json"
f = open(jsonfile, 'r')
data = json.load(f)
f.close()


# ponfile = "/Users/liul8/cromwell/normal.txt"
# ponfile = "/staging/scratch/exome_cnv/normal.txt"
ponfile = "/mnt/isilon/conlin_lab/data/clinical/v2_exome_parents/normal.txt"
pon = open(ponfile, 'rt')
ponread = pon.readlines()
ponlist = [i.strip() for i in ponread]
# ponlist
pon.close()



# create reference PON normal.txt for each case
refnormalfile_list = []
for id in sampleids:
    refpath_list = [i for i in ponlist if id not in i]
    ref_normalfile = '/mnt/isilon/conlin_lab/data/clinical/v2_exome_parents/normalfiles/normal_' + id +'.txt'
    refnormalfile_list.append(ref_normalfile)
    normal = open(ref_normalfile, 'w')
    for line in refpath_list:
        normal.write(line + '\n')
    normal.close()


# targetcounts = "/Users/liul8/cromwell/targetcounts.txt"
# targetcounts = "/staging/scratch/exome_cnv/targetcounts_list.txt"
targetcounts = "/mnt/isilon/conlin_lab/data/clinical/v2_exome_parents/targetcounts_list.txt"
t = open(targetcounts, 'r')
targetcountsread = t.readlines()
targetcountslist = [i.strip() for i in targetcountsread]
t.close()


# part 3: edit json info for each sample and run wdl for each sample file
# cmds = "nohup java -jar /staging/scratch/lanxin/cromwell-55.jar run cnv_target_counts.wdl --inputs cnv_target_counts.json --options options.json &"
jsonpath = []
for i in range(len(bamlist)):
    sampleid = sampleids[i]
    targetcountsfile = [targetcountslist[i] for i in range(len(targetcountslist)) if sampleid in targetcountslist[i]][0]
    normalfile = refnormalfile_list[i] 
    output = changejsonfile(data, targetcountsfile, sampleid, normalfile)
    outputjson = '/mnt/isilon/conlin_lab/data/clinical/v2_exome_parents/jsonfiles/cnv_normalization_' + sampleid + '.json'
    json_object = json.dumps(output, indent = 10)
    with open(outputjson, 'w') as json_file:
        json_file.write(json_object)
    jsonpath.append(outputjson)

run_wdl = 'run_wdl_cnv_normalization.sh'    
b = open(run_wdl, 'w')
for i in jsonpath:
    cmd = "java -jar /staging/scratch/lanxin/cromwell-55.jar run cnv_normalization.wdl --inputs " + str(i) + '\n'
    b.write(cmd)
b.close()




# a = ['F000071089_DGD-20-3637_WESTRIO_F.markdups.bam','F000071386_DGD-20-3468_WESTRIO_M.markdups.bam','F000073921_DGD-20-7133_WESTRIO_F.markdups.bam','F000062875_DGD-20-7146_WESTRIO_M.markdups.bam','F000071098_DGD-20-3332_WESTRIO_M.markdups.bam','F000078131_DGD-20-7334_WESTRIO_M.markdups.bam', 'F000062875_DGD-20-7120_WESTRIO_F.markdups.bam', 'F000024283_DGD-20-7172_WESTRIO_M.markdups.bam','F000071023_DGD-20-3274_WESTRIO_F.markdups.bam','F000078708_DGD-20-7168_WESTRIO_M.markdups.bam','F000070786_DGD-20-3097_WESTRIO_F.markdups.bam','F000066050_DGD-20-3326_WESTRIO_F.markdups.bam','F000049712_DGD-20-3323_WESTRIO_F.markdups.bam','F000078670_DGD-20-7147_WESTRIO_F.markdups.bam','F000070786_DGD-20-3101_WESTRIO_M.markdups.bam','F000029781_DGD-18-2260_WESTRIO_M.markdups.bam','F000075863_DGD-20-7281_WESTRIO_F.markdups.bam','F000071386_DGD-20-3467_WESTRIO_F.markdups.bam', 'F000029781_DGD-18-2262_WESTRIO_F.markdups.bam', 'F000078108_DGD-20-7228_WESTRIO_F.markdups.bam','F000004302_DGD-16-119_WESTRIO_M.markdups.bam','F000071811_DGD-20-3788_WESTRIO_F.markdups.bam','F000066791_DGD-20-3390_WESTRIO_M.markdups.bam','F000073921_DGD-20-7134_WESTRIO_M.markdups.bam','F000071089_DGD-20-3328_WESTRIO_M.markdups.bam', 'F000078405_DGD-20-7423_WESTRIO_F.markdups.bam', 'F000077569_DGD-20-6550_WESTRIO_M.markdups.bam', 'F000078708_DGD-20-7169_WESTRIO_F.markdups.bam','F000005363_DGD-16-2559_WESTRIO_F.markdups.bam', 'F000071273_DGD-20-3434_WESTRIO_F.markdups.bam', 'F000071023_DGD-20-3275_WESTRIO_M.markdups.bam','F000078131_DGD-20-6912_WESTRIO_F.markdups.bam','F000078108_DGD-20-7190_WESTRIO_M.markdups.bam','F000024283_DGD-20-7173_WESTRIO_F.markdups.bam', 'F000067986_DGD-20-3400_WESTRIO_M.markdups.bam', 'F000005363_DGD-16-2558_WESTRIO_M.markdups.bam', 'F000078863_DGD-20-7250_WESTRIO_M.markdups.bam','F000075863_DGD-20-7280_WESTRIO_M.markdups.bam', 'F000066791_DGD-20-3389_WESTRIO_F.markdups.bam', 'F000071069_DGD-20-3282_WESTRIO_F.markdups.bam', 'F000079075_DGD-20-7338_WESTRIO_F.markdups.bam','F000067986_DGD-20-3399_WESTRIO_F.markdups.bam', 'F000078657_DGD-20-7138_WESTRIO_F.markdups.bam', 'F000069056_DGD-20-3196_WESTRIO_F.markdups.bam', 'F000078610_DGD-20-7157_WESTRIO_F.markdups.bam','F000071101_DGD-20-7335_WESTRIO_M.markdups.bam', 'F000071069_DGD-20-3280_WESTRIO_M.markdups.bam','F000069056_DGD-20-3197_WESTRIO_M.markdups.bam', 'F000078863_DGD-20-7251_WESTRIO_F.markdups.bam', 'F000070655_DGD-20-7237_WESTRIO_M.markdups.bam','F000071088_DGD-20-3316_WESTRIO_M.markdups.bam', 'F000071223_DGD-20-3403_WESTRIO_M.markdups.bam','F000079075_DGD-20-7340_WESTRIO_M.markdups.bam', 'F000004302_DGD-16-120_WESTRIO_F.markdups.bam', 'F000071273_DGD-20-3439_WESTRIO_M.markdups.bam','F000071098_DGD-20-3333_WESTRIO_F.markdups.bam','F000078610_DGD-20-7156_WESTRIO_M.markdups.bam', 'F000077569_DGD-20-7165_WESTRIO_F.markdups.bam', 'F000049712_DGD-20-3322_WESTRIO_M.markdups.bam', 'F000066050_DGD-20-3324_WESTRIO_M.markdups.bam']
# len(a)
# tmp = [targetcountslist[i] for i in range(len(targetcountslist)) if sampleids[0] in targetcountslist[i]]
# tmp[0]
# sampleids = [i.split('.')[0] for i in a]
# sampleids[0]
# targetcountslist