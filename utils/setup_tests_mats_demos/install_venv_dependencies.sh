# first need to   `chmod +x install_venv_dependencies.sh`
python3 -m venv .venv

source venv/bin/activate

if [ ! -f requirements.txt ]; then
    echo "Generating requirements.txt from imports..."
    pip install pipreqs
    pipreqs . --force
fi

pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment set up and dependencies installed."
