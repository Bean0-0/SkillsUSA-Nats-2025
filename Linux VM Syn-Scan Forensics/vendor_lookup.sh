#!/bin/bash

# Script to lookup MAC address vendors
# First, let's extract and clean the MAC addresses

echo "=== MAC Address Vendor Lookup ==="
echo

# Clean MAC addresses extracted from the data
macs=(
    "00:21:cc:be:ca:77"
    "08:00:27:e8:99:4d"
    "08:00:27:fc:0e:f3"
    "30:23:03:fb:af:e5"
    "08:00:27:15:8f:43"
    "ff:ff:ff:ff:ff:ff"
    "01:00:5e:7f:ff:fa"
)

# Function to lookup vendor using online API
lookup_vendor() {
    local mac=$1
    echo -n "MAC: $mac -> "
    
    # Extract OUI (first 3 octets)
    oui=$(echo $mac | cut -d':' -f1-3)
    
    # Try online lookup first
    vendor=$(curl -s "https://api.macvendors.com/$oui" 2>/dev/null)
    
    if [ $? -eq 0 ] && [ ! -z "$vendor" ] && [[ "$vendor" != *"error"* ]]; then
        echo "$vendor"
    else
        # Fallback to known OUI patterns
        case $oui in
            "00:21:cc")
                echo "Unknown/Custom OUI"
                ;;
            "08:00:27")
                echo "PCS Systemtechnik GmbH / Oracle Corporation (VirtualBox)"
                ;;
            "30:23:03")
                echo "Unknown/Custom OUI"
                ;;
            "ff:ff:ff")
                echo "Broadcast Address"
                ;;
            "01:00:5e")
                echo "Multicast Address (IPv4)"
                ;;
            *)
                echo "Unknown OUI: $oui"
                ;;
        esac
    fi
}

# Loop through each MAC address
for mac in "${macs[@]}"; do
    lookup_vendor "$mac"
done

echo
echo "=== Manual OUI Lookup Commands ==="
echo "You can also manually lookup OUI prefixes using:"
echo "curl -s 'https://api.macvendors.com/08:00:27'"
echo "curl -s 'https://api.macvendors.com/00:21:cc'"
echo "curl -s 'https://api.macvendors.com/30:23:03'"
