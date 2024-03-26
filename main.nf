process BUILD_DB {
    input:
    path phibase

    output:
    path "${phibase}*"

    """
    makeblastdb -in ${phibase} -dbtype prot
    """

    }

process BLASTP {
    input:
    path protiens
    path db
    path phibase
    

    output:
    path "${protiens}.out"

    """
    blastp -db ${phibase.Name} -query ${protiens}/*proteins* -out ${protiens.baseName}.out -num_threads 8 -outfmt "6 qseqid sseqid evalue pident"
    """

    }

process GET_EFFECTORS {
    input:
    path protiens
    path blastp
    val species

    output:
    path "${protiens.baseName}.tsv"


    """
    python $projectDir/bin/getEffectors.py ${protiens}.out ${species} ${protiens.baseName}
    """
    }

process CUSP {
    input:
    path protiens

    output:
    path "cds.cusp"

    """
    cusp -sequence ${protiens}/*CDS* -outfile cds.cusp
    """
    }

process CAI {
    input:
    path genes
    path proteome_cusp

    output:
    path "${genes.Name}.cai"

    """
    cai -seqall ${genes}/*CDS* -cfile ${proteome_cusp} -outfile ${genes.Name}.cai
    """
    }

process GET_FULL_TABLE {
    publishDir("CAI")
    input:
    path cai
    path effectors

    output:
    path "${cai}.tsv"

    """
    python3 $projectDir/bin/getFullTable.py ${cai} ${effectors}
    """
}

process PLOT_CAI {
    publishDir("CAI")
    input:
    path full_table

    output:
    path "${full_table}.png"

    """
    python3 $projectDir/bin/plotCAI.py ${full_table}
    """
}



workflow {
    phibase = file(params.in_phibase)
    db = BUILD_DB(file(params.in_phibase))
    blast = BLASTP(file(params.in_genome), db, phibase)
    effectors = GET_EFFECTORS(file(params.in_genome), blast, params.species)
    proteome_cusp = CUSP(file(params.in_genome))
    cai = CAI(file(params.in_genome), proteome_cusp)
    full = GET_FULL_TABLE(cai, effectors)
    plot = PLOT_CAI(full)
    }

