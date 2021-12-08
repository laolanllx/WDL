version 1.0
# Task Summary: Copy Number Variant Calling (CNV) target counts for WES data.
# Tool Name: dragen
# Input: WES BAM Files
# Outputs: target counts files and target counts gc-corrected files...

# WORKFLOW DEFINITION 
workflow CNV_TC{
	input {
		File RefDict
		File inputBam
		String output_prefix
		Boolean option_map_align
		Boolean option_enable_cnv
		File cnv_target_bed
		Int interval_width = 500
	}
	call target_counts {
		input:
			RefDict=RefDict,
			inputBam=inputBam,
			output_prefix=output_prefix,
			option_ma=option_map_align,
			option_cnv=option_enable_cnv,
			target_bed=cnv_target_bed,
			interval_width=interval_width
	}
}

# CNV Target Counts 
task target_counts {
	input {
		File RefDict
		File inputBam
		String output_prefix
		Boolean option_ma
		Boolean option_cnv
		File target_bed
		Int interval_width = 500
	}
	command {
		dragen -f \
			-r ${RefDict} \
			-b ${inputBam} \
			--output-directory ./ \
			--output-file-prefix ${output_prefix} \
			--intermediate-results-dir ./ \
			--enable-map-align ${option_ma} \
			--enable-cnv ${option_cnv} \
			--cnv-target-bed ${target_bed} \
			--cnv-interval-width ${interval_width}
	}
	parameter_meta {
		option_ma: "true or false for enable map and align"
		interval_width: "Specifies the width of the sampling interval for CNV processing. This option controls the effective window size. The default is 1000 for WGS analysis and 500 for WES analysis"
	}
	meta {
		author: "CHOP Bioinformatics Intern Lanxin Liu"
	}
}

