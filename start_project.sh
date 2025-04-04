#!/bin/bash
echo "PostgreSQL wird gestartet..."
sudo service postgresql start
echo "PostgreSQL läuft!"

# chmod +x start_project.sh  // einmalig in wsl Berechtigungen vergeben. 