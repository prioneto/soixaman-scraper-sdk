#!/bin/bash

# Update and install dependencies
apt-get update
apt-get install -y wget unzip chromium-browser chromium-chromedriver

# Ensure chromedriver is in PATH
export PATH=$PATH:/usr/bin/chromedriver