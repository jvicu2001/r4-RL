if [[ ! -e "./python/.venv" ]]; then
	echo "Creating virtual environment"
	python -m venv ./python/.venv
	echo "Installing python packages in virtual environment"
	python/.venv/bin/pip install -r python/requirements.txt
fi

cd python
.venv/bin/python r4_neat.py