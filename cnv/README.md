## Copy number variant calling (CNV) for WES

Workflows for target counts and normalization

### Target counts

Requirements:

+ Bam file
+ target bed file

Output:

+ Target counts
+ gc corrected files
+ ...

Command:

```bash
java -jar cromwell-55.jar run cnv_target_counts.wdl --inputs cnv_target_counts.json
```

### Normalization - panel of normal

Requirements:

+ PON file
+ case target counts file

Output:

+ CNV VCF
+ ...

Command:

```bash
java -jar cromwell-55.jar run cnv_normalization.wdl --inputs cnv_normalization.json
```

### Using

+ create each sample json files and generate a bash shell to run each command by using python script 'run_dragen_cnv_targetcounts.py'

  ```bash
  python run_dragen_cnv_targetcounts.py
  ```
+ Target counts for each samples by running the bash shell called 'run_wdl_cnv_targetcounts.sh' created by python script
  ```bash
  ./run_wdl_cnv_targetcounts.sh
  ```

+ create PON file

  ```bash
  find PATH -name "*.target.counts.gc-corrected" -exec cat {} \; > normal.txt
  ```

  

+ run panel of normal workflow

  ```bash
  java -jar cromwell-55.jar run cnv_panelofnormal.wdl --inputs cnv_panelofnormal.json
  ```
