#!/bin/bash

# Update package lists and ensure Python and pip are installed
echo "Updating package lists and installing Python & pip..."
#sudo apt update && sudo apt install -y python3 python3-pip
chmod +x fsg.sh
# Install Python libraries
echo "Installing required Python libraries..."
pip3 install --upgrade pip
pip3 install numpy scikit-learn pandas networkx
pip3 install shap imbalanced-learn

# Standard libraries (these come with Python by default, but ensuring compatibility)
echo "Ensuring standard Python libraries are available..."







# Update package lists and ensure Python and pip are installed
echo "Updating package lists and installing Python & pip..."
sudo apt update && sudo apt install -y python3 python3-pip

# Install Python libraries
echo "Installing required Python libraries..."
pip3 install --upgrade pip
pip3 install numpy scikit-learn pandas networkx

# Standard libraries (these come with Python by default, but ensuring compatibility)
echo "Ensuring standard Python libraries are available..."
pip3 install --upgrade sys os csv collections

echo "Installation complete!"
echo "Installation complete!"
set -e  


