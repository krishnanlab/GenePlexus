home_dir=$(dirname $0)
cd $home_dir

rm -rf "Supervised-learning is an accurate method for network-based gene classification - Data.tar.gz"*

if [ -d data ]; then
	echo cleaning up old data
	rm -rf ./data/*
else
	mkdir data
fi

wget https://zenodo.org/record/3352348/files/Supervised-learning%20is%20an%20accurate%20method%20for%20network-based%20gene%20classification%20-%20Data.tar.gz
tar -xvzf "Supervised-learning is an accurate method for network-based gene classification - Data.tar.gz" -C data --strip-components=1
rm -f "Supervised-learning is an accurate method for network-based gene classification - Data.tar.gz"
