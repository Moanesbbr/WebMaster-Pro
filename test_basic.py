"""
Basic tests for NetMaster Pro application
"""
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all main modules can be imported without errors"""
    try:
        import wifitoqr
        import main_interface
        import network_manager
        import splash
        assert True, "All modules imported successfully"
    except ImportError as e:
        assert False, f"Failed to import module: {e}"

def test_requirements_file():
    """Test that requirements.txt exists and is readable"""
    assert os.path.exists("requirements.txt"), "requirements.txt should exist"
    
    with open("requirements.txt", "r") as f:
        content = f.read()
        assert len(content.strip()) > 0, "requirements.txt should not be empty"

def test_assets_directory():
    """Test that assets directory exists and contains expected files"""
    assert os.path.exists("assets"), "assets directory should exist"
    assert os.path.isdir("assets"), "assets should be a directory"

def test_main_files_exist():
    """Test that main application files exist"""
    main_files = ["wifitoqr.py", "main_interface.py", "network_manager.py", "splash.py"]
    for file in main_files:
        assert os.path.exists(file), f"{file} should exist"
        assert os.path.isfile(file), f"{file} should be a file"

if __name__ == "__main__":
    # Run basic tests
    test_imports()
    test_requirements_file()
    test_assets_directory()
    test_main_files_exist()
    print("All basic tests passed!") 