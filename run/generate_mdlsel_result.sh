cd $(dirname $0)
cd ../src
python main.py -n BioGRID STRING-EXP GIANT-TN STRING \
	-c GOBPtmp GOBP DisGeNet BeFree GWAS MGI -s Holdout 5FCV \
	-m LR-L1 LR-L2 SVM RF LP-I55 LP-I65 LP-I75 LP-I85 LP-I95 \
	-o ../results/mdlsel_result_new.tsv
