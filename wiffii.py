import wifi

# Get available Wi-Fi interfaces
interfaces = wifi.interfaces()

# Get Wi-Fi networks in range
networks = interfaces[0].networks()

# Print Wi-Fi network information
for network in networks:
    print("SSID: ", network.ssid)
    print("BSSID: ", network.bssid)
    print("Encryption: ", network.encryption)
    print("Signal Strength: ", network.signal)


# import wifi

# # Get a list of all available wireless interfaces
# wifi_list = wifi.scan()

# # Print the name and signal strength of each Wi-Fi network
# for wifi_network in wifi_list:
#     print(f"Name: {wifi_network.ssid}, Signal Strength: {wifi_network.signal}")

