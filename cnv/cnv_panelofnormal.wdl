version 1.0
# Task Summary: Copy Number Variant Calling (CNV) panel of normals for Whole exome sequencing (WES) data.
# Tool Name: dragen
# Input: case WES BAM File, a PON txt file with control samples '*target.counts.gc-corrected' directories, a txt file with control samples '*target.counts files' directories 
# Outputs: CNV VCF...

import "/mnt/isilon/conlin_lab/data/clinical/v2_exome_parents/cnv_target_counts.wdl" as tc

# WORKFLOW DEFINITION 
workflow CNV_PoN{
	input {
		File RefDict
		String output_prefix
		Boolean option_map_align
		Boolean option_enable_cnv
		File targetcountsfile
		File normal_list
		Boolean option_gcbias_correction
		String cnv_counts_method
		Int cnv_min_mapq
		Float cnv_merge_threshold
		
		File PATH
		String filename
		String target
		
		File inputBam
		Boolean option_map_align_tc
		Boolean option_enable_cnv_tc
		File cnv_target_bed
		Int interval_width = 500
	}
	
	# target counts stage for case sample
	call tc.target_counts {
		input:
			RefDict=RefDict,
			inputBam=inputBam,
			output_prefix=output_prefix,
			option_ma=option_map_align_tc,
			option_cnv=option_enable_cnv_tc,
			target_bed=cnv_target_bed,
			interval_width=interval_width
	}
	
	# find path of case '*target.counts' file
	call find {
		input:
			PATH=PATH,
			filename=filename,
			target=target
	}
	
	# normalization
	call normalization {
		input:
			RefDict=RefDict,
			output_prefix=output_prefix,
			option_ma=option_map_align,
			option_cnv=option_enable_cnv,
			targetcountsfile=find.output_file,
			normal_list=normal_list,
			option_gcbias_correction=option_gcbias_correction,
			cnv_counts_method=cnv_counts_method,
			cnv_min_mapq=cnv_min_mapq,
			cnv_merge_threshold=cnv_merge_threshold
	}
}

# Task Definitions
task find {
	input {
		File PATH
		String filename
		String target
		String find_object = '{}'
	}
	# find path of case '*target.counts' file and copy it to a specified folder
	command {
		find ~{PATH} \
			-name ~{filename} \
			-exec cp ~{find_object} ~{target} \;
	}
	output {
		File output_file = "~{target}"
  }
}

# Run panel of normal
task normalization {
	input {
		File RefDict
		String output_prefix
		Boolean option_ma
		Boolean option_cnv
		File targetcountsfile
		File normal_list
		Boolean option_gcbias_correction
		String cnv_counts_method
		Int cnv_min_mapq
		Float cnv_merge_threshold
	}
	command {
		dragen -f \
			-r ${RefDict} \
			--output-directory ./ \
			--output-file-prefix ${output_prefix} \
			--intermediate-results-dir ./ \
			--enable-map-align ${option_ma} \
			--enable-cnv ${option_cnv} \
			--cnv-input ${targetcountsfile} \
			--cnv-normals-list ${normal_list} \
			--cnv-enable-gcbias-correction ${option_gcbias_correction} \
			--cnv-counts-method ${cnv_counts_method} \
			--cnv-min-mapq ${cnv_min_mapq} \
			--cnv-merge-threshold ${cnv_merge_threshold}
	}
	parameter_meta {
		option_gcbias_correction: "true or false for GC bias correction"
		normal_list: "a PON file, which contains a subset of the GC corrected files paths from the target counts stage"
		targetcountsfile: "case sample target counts file"
		cnv_counts_method: "Specifies the counting method for an alignment to be counted in a target bin. Values are midpoint, start, or overlap"
		cnv_min_mapq: "Specifies the minimum MAPQ for an alignment to be counted during target counts generation. The default value is 3 for self normalization and 20 otherwise."
		cnv_merge_threshold: "Specifies the maximum segment mean difference at which two adjacent segments should be merged. The segment mean is represented as a linear copy ratio value. The default is 0.2 for WGS and 0.4 for WES. To disable merging, set the value to 0"
	}
	meta {
		author: "CHOP Bioinformatics Intern Lanxin Liu"
	}
}


