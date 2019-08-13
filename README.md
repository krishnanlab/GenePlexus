# GenePlexus
This repository contains data and code to generate the results and reproduce the figures and tables found in [_Supervised learning is an accurate method for network-based gene classification_](https://www.biorxiv.org/content/10.1101/721423v1) (submitted for review). This work focuses on comparing two classes of network-based gene classification methods: supervised learning (SL) and label propagation (LP). The comparison is performed systematically across diverse prediction tasks (functions, diseases, and traits) and molecular networks using meaningful validation schemes and evaluation metrics. Based on these extendive analyses, we find that supervised learning outperforms label propagation for gene classification, especially for function prediction.

This repo provides: 
1. The data, results, and figures presented in the manuscript.
2. Code to regenerate the results.
3. The ability to add a new method. 

## Section 1: Pre-computed Data, Results, and Figures/Tables
### Data
The data used in this study (networks, embeddings, and genesets) is available on [Zenodo](https://zenodo.org/record/3352348/). To get the data run
```
sh get_data.sh
```
We note that data for KEGG and InBioMap are not included as they do not provide a permissive enough license.

### Results
`results/`: This directory contains two files:
1. `main_result.tsv`: This file contains all the results used to compare the SL and LP methods.
2. `mdlsel_result.tsv`: This file contains all the results used for model selection for supervised learning and random walk with restart.

### Geneset Properties 
`properties/`: This directory contains the network properties of every geneset based on every network.

### Figures/Tables
`figures_tables/`: This directory contains all the pre-generated figures and tables.

## Section 2: Regenerating the Results and Figures/Tables
### Dependencies
This code was tested on an Anaconda distribution of python. The major packages used are:
```
python 3.6.5
numpy 1.14.3
scipy 1.1.0
pandas 0.23.0
scikit-learn 0.19.1
matplotlib 2.2.2
seaborn 0.8.1
statsmodels 0.9.0
```
The parallelization of the code was tested with Slurm on the high performance computing cluster at Michigan State University.

#### Testing
Run the following two lines of code to test if the code works on one set of parameters: GOBP (geneset collection), STRING (network), SL-A, and LP-I (two methods):
```
cd demo
sh test_run.sh
```
This will save a sample results files named `test.tsv` into the `results/` directory. This script takes a few minutes to run. 

### Generating Results
Results can be re-generated either in parallel or on a single machine. The files must be executed within the directory they are stored.

* To generate the results on a single-machine run:
```
cd run
sh generate_main_result.sh      # This takes approximately 9 hours to run
sh generate_mdlsel_result.sh      # This takes approximately 25 hours to run
```

* To generate the results in parallel run:
```
cd run/SLURM
sbatch generate_main_result_parallel.sb      # This takes approximately 1 hour to run
sbatch generate_mdlsel_result_parallel.sb      # This takes approximately 1 hour to run
```
Result outputs will be saved as either `results/main_result_new.tsv` or `results/mdsel_result_new.tsv`. We note that development of the scikit-learn package is very active and thus the exact results depend on the specific version of scikit-learn used to regenerate the results. 

* To generate the geneset properties run:
```
cd run
sh generate_geneset_properties.sh  # This takes approximately 5 minutes to run
```
Geneset properties will be saved in `properties_new/`.

* To generate all the figures and tables in the manuscript run:
```
cd run
sh generate_figures.sh  # This takes approximately 5 minutes to run
sh generate_tables.sh   # This takes approximately 5 minutes to run
```
The figure and table generation scirpts will only run when using the orginal results in `results/main_reuslts.tsv` or `results/mdlsel_result.tsv`, and the results will be saved in `figures_tables/`. We note that if you run `sh generate_tables.sh` this will give slightly different results from Table S1 and S2 in the manuscript as these new tables will be generated with the data included in this repository, which does not include KEGG and InBioMap. 

## Section 3: Adding a New Method
A new network-based gene classification method can be added using the following steps: 

1. Create a new class object in `src/core/models.py`. A template for how to do this is included at the bottom of the `models.py` script. 
2. The file `src/main.py` will need to be updated in two places. First, a new model dictionary will have to be added to the function _get_mdl_dict_. A template of how to do this is included in that function. Second, the model name will have to be added to the _all_methods_ variable.
3. The model name will need to be added to the _-m_ argument in the scripts that re-generate the scores. We note that `generate_figures.sh` and `generate_tables.sh` will not work when a new method is added.

## Section 4: Additional Information
### Support
For support please contact [Remy Liu](https://twitter.com/RemyLau3) at liurenmi@msu.edu or [Chris Mancuso](https://twitter.com/ChrisAMancuso) at mancus16@msu.edu.

### License
See [LICENSE.md](https://github.com/krishnanlab/GenePlexus/LICENSE.md) for license information for all geneset collections and networks used in this project.

### Citation
If you use this work, please cite:  
`To be added later`

### Authors
Renming Liu#, Christopher A Mancuso#, Anna Yannakopoulos, Kayla A Johnson, Arjun Krishnan*

\# These authors are joint first authors and are listed alphabetically.  
\* General correspondence should be addressed to AK at arjun@msu.edu.

### Funding
This work was primarily supported by US National Institutes of Health (NIH) grants R35 GM128765 to AK and in part by MSU start-up funds to AK and MSU Engineering Distinguished Fellowship to AY.

### Acknowledgements
We are grateful for the support from the members of the [Krishnan Lab](https://www.thekrishnanlab.org).

### Referecnes

#### Networks
##### GIANT (version used is 1.0)
* Greene CS, Krishnan A, Wong AK, Ricciotti E, Zelaya RA, Himmelstein DS, Zhang R, Hartmann BM, Zaslavsky E, Sealfon SC, Chasman DI, FitzGerald GA, Dolinski K, Grosser T, Troyanskaya OG. (2015) Understanding multicellular function and disease with human tissue-specific networks. _Nature Genetics_ 47:569-576.
##### STRING and STRING-EXP (version used is v.10)
* Szklarczyk D, Franceschini A, Wyder S, Forslund K, Heller D, Huerta-Cepas J, Simonovic M, Roth A, Santos A, Tsafou KP, Kuhn M, Bork P, Jensen LJ, von Mering C. (2015) STRING v10: protein-protein interaction networks, integrated over the tree of life. _Nucleic Acids Research_ 43:D447-452.
##### BioGRID (version used is 3.4.136)
* Stark C, Breitkreutz BJ, Reguly T, Boucher L, Breitkreutz A, Tyers M. (2006) BioGRID: a general repository for interaction datasets. _Nucleic Acids Research_ 34:D535-539.
##### InBioMap (version used is 2016_09_12)
* Li T, Wernersson R, Hansen RB, Horn H, Mercer J, Slodkowicz G, Workman CT, Rigina O, Rapacki K, Stærfeldt HH, Brunak S, Jensen TS, Lage K. (2017) A scored human protein-protein interaction network to catalyze genomic interpretation. _Nature Methods_ 14:61-64.

#### Geneset Collections
##### GOBPtmp and GOBP (gene annotation for GOBP are from verison 2 of MyGeneInfo)
* Ashburner M, Ball CA, Blake JA, Botstein D, Butler H, Cherry JM, Davis AP, Dolinski K, Dwight SS, Eppig JT, Harris MA, Hill DP, Issel-Tarver L, Kasarskis A, Lewis S, Matese JC, Richardson JE, Ringwald M, Rubin GM, Sherlock G. (2000) Gene ontology: tool for the unification of biology. The Gene Ontology Consortium. _Nature Genetics_ 25:25-29.
* The Gene Ontology Consortium. (2019) The Gene Ontology Resource: 20 years and still GOing strong. _Nucleic Acids Research_ 47:D330-338.
* Wu C, MacLeod I, Su AI (2013) BioGPS and MyGene.info: organizing online, gene-centric information. _Nucleic Acids Research_ 41:D561-D565. 
* Xin J, Mark A, Afrasiabi C, Tsueng G, Juchler M, Gopal N, Stupp GS, Putman TE, Ainscough BJ, Griffith OL, Torkamani A, Whetzel PL, Mungall CJ, Mooney SD, Su AI, Wu C (2016) High-performance web services for querying gene and variant annotation. _Genome Biology_ 17:1-7.
##### DisGeNet and BeFree (version used 5.0)
* Piñero J, Queralt-Rosinach N, Bravo À, Deu-Pons J, Bauer-Mehren A, Baron M, Sanz F, Furlong LI. (2015) DisGeNET: a discovery platform for the dynamical exploration of human diseases and their genes. _Database_ bav028.
* Piñero J, Bravo À, Queralt-Rosinach N, Gutiérrez-Sacristán A, Deu-Pons J, Centeno E, García-García J, Sanz F, Furlong LI. (2017) DisGeNET: a comprehensive platform integrating information on human disease-associated genes and variants. _Nucleic Acids Research_ 45:D833-839.
* Schriml LM, Mitraka E, Munro J, Tauber B, Schor M, Nickle L, Felix V, Jeng L, Bearer C, Lichenstein R, Bisordi K, Campion N, Hyman B, Kurland D, Oates CP, Kibbey S, Sreekumar P, Le C, Giglio M, Greene C. (2019) Human Disease Ontology 2018 update: classification, content and workflow expansion. _Nucleic Acids Research_ 47:D955-D962.
##### MGI (data retrieved on 2018-10-01) 
* Smith CL, Blake JA, Kadin JA, Richardson JE, Bult CJ, Mouse Genome Database Group. (2018) Mouse Genome Database (MGD)-2018: knowledgebase for the laboratory mouse. _Nucleic Acids Research_ 46:D836-842.
* Smith CL, Eppig JT. (2009) The mammalian phenotype ontology: enabling robust annotation and comparative analysis. _WIREs Systems Biology and Medicine_ 3:390-399. 
##### GWAS (data downloaded from Synapse at https://www.synapse.org/#!Synapse:syn11944948)
* Choobdar S, Ahsen ME, Crawford J, Tomasoni M, Fang T, Lamparter D, Lin J, Hescott B, Hu X, Mercer J, Natoli T, Narayan R, The DREAM Module Identification Challenge Consortium, Subramanian A, Zhang JD, Stolovitzky G, Kutalik Z, Lage K, Slonim DK, Saez-Rodriguez J, Cowen LJ, Bergmann S, Marbach D. (2019) Open Community Challenge Reveals Molecular Network Modules with Key Roles in Diseases. _bioRxiv_ doi: https://doi.org/10.1101/265553.
##### KEGGBP (version used is 6.1)
* Kanehisa M, Goto S. (2000) KEGG: kyoto encyclopedia of genes and genomes. _Nucleic Acids Research_ 28:27-30.
* Kanehisa M, Furumichi M, Tanabe M, Sato Y, Morishima K. (2017) KEGG: new perspectives on genomes, pathways, diseases and drugs. _Nucleic Acids Research_ 45:D353-361.
* Kanehisa M, Sato Y, Furumichi M, Morishima K, Tanabe M. (2019) New approach for understanding genome variations in KEGG. _Nucleic Acids Research_ 47:D590-595.
* Subramanian A, Tamayo P, Mootha VK, Mukherjee S, Ebert BL, Gillette MA, Paulovich A, Pomeroy SL, Golub TR, Lander ES, Mesirov JP. (2005) Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. _Proceedings of the National Academy of Sciences U.S.A._ 43:15545-50.
* Liberzon A, Subramanian A, Pinchback R, Thorvaldsdóttir H, Tamayo P, Mesirov JP. (2011) Molecular signatures database (MSigDB) 3.0. _Bioinformatics_ 12:1739-40. 

