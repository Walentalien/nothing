# first need to   `chmod +x install_venv_dependencies.sh`
# Step 1: Create virtual environment
python3 -m venv .venv

# Step 2: Activate virtual environment
source venv/bin/activate

# Step 3: Try generating requirements.txt if it doesn't exist
if [ ! -f requirements.txt ]; then
    echo "Generating requirements.txt from imports..."
    pip install pipreqs
    pipreqs . --force
fi

# Step 4: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Done
echo "✅ Virtual environment set up and dependencies installed."
