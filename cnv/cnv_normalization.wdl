version 1.0

# Input: 
# Outputs: 

# WORKFLOW DEFINITION 
workflow CNV_N{
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
	}
	call normalization {
		input:
			RefDict=RefDict,
			output_prefix=output_prefix,
			option_ma=option_map_align,
			option_cnv=option_enable_cnv,
			targetcountsfile=targetcountsfile,
			normal_list=normal_list,
			option_gcbias_correction=option_gcbias_correction,
			cnv_counts_method=cnv_counts_method,
			cnv_min_mapq=cnv_min_mapq,
			cnv_merge_threshold=cnv_merge_threshold
	}
}

# Run normalization
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
	}
	meta {
		author: "CHOP Bioinformatics Intern Lanxin Liu"
	}
}

/* task normalization {
	output {
		File outputs = "${output_dir}"
	}
	{
	  "CNV_N.option_enable_cnv": "true",
	  "CNV_N.option_gcbias_correction": "false",
	  "CNV_N.output_prefix": "dragen_cnv_normalization_F000067723_DGD-20-990_WESTRIO_F",
	  "CNV_N.RefDict": "/staging/scratch/broad_hg38_reference/dragen",
	  "CNV_N.targetcountsfile": "/staging/scratch/exome_cnv/cromwell-executions/CNV_TC/5f2b0d54-0103-41f0-b0be-b369e2089f9f/call-target_counts/inputs/42771560/dragen_cnv1/F000067723_DGD-20-990_WESTRIO_F.target.counts",
	  "CNV_N.normal_list": "/staging/scratch/exome_cnv/normal.txt",
	  "CNV_N.option_map_align": "false"
	}
} */
