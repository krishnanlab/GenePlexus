cd $(dirname $0)
cd ../src
python main.py -n BioGRID STRING-EXP GIANT-TN STRING \
	-c GOBPtmp GOBP DisGeNet BeFree GWAS MGI -s Holdout 5FCV \
	-m SL-A SL-I SL-E LP-A LP-I -o ../results/main_result_new.tsv
