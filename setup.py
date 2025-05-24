import subprocess
import sys
import os
import importlib.util

# Required packages for the VirtualDoctor application
required_packages = [
    'kivy',
    'flask',
    'matplotlib',
    'numpy',
    'psycopg2-binary',
    'sqlalchemy',
    'scipy',
]

def is_package_installed(package_name):
    """Check if a package is installed."""
    try:
        spec = importlib.util.find_spec(package_name)
        return spec is not None
    except (ImportError, AttributeError):
        return False

def check_and_install_dependencies():
    """Check for required Python packages and install missing ones."""
    missing = []
    
    print("Checking for required Python packages...")
    
    for package in required_packages:
        package_name = package.split('>=')[0].lower()
        if not is_package_installed(package_name):
            missing.append(package)
    
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print("Installing missing packages...")
        
        try:
            for package in missing:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print("All required packages installed successfully!")
        except subprocess.CalledProcessError:
            print("Failed to install some packages. Please install them manually.")
            print("Required packages:")
            for package in missing:
                print(f"  - {package}")
            return False
    else:
        print("All required packages are already installed!")
    
    return True

def check_database_config():
    """Check if database configuration exists."""
    if not os.environ.get('DATABASE_URL'):
        print("\nWARNING: DATABASE_URL environment variable not found!")
        print("You can set it up by:")
        print("1. Creating a .env file with DATABASE_URL=postgresql://username:password@host:port/dbname")
        print("2. Or by exporting it directly in your terminal")
        print("3. Or by modifying utils/db_manager.py to use SQLite instead (see SETUP_INSTRUCTIONS.md)")
        return False
    
    print("\nDatabase URL found in environment variables.")
    return True

def main():
    """Main setup function."""
    print("=== VirtualDoctor Setup ===")
    
    deps_ok = check_and_install_dependencies()
    db_ok = check_database_config()
    
    if deps_ok and db_ok:
        print("\nSetup complete! You can now run:")
        print("- Kivy interface: python kivy_doctor.py")
        print("- Web interface: python web_doctor.py")
        print("- Console interface: python main.py")
    else:
        print("\nSetup incomplete. Please resolve the issues mentioned above.")

if __name__ == "__main__":
    main()