# Setup second router as a switch
## Tools
- Router 1 - master - connected to the internet
- Router 2 - Slave
- Laptop

## Setup Router 1

1.	In the wireless security settings of the router, disable Automatic Channel selection and manually set the channel some channel.
2.	add an IP address reservation for router 2 to routers 1 setting, e.g. 192.168.0.2

## Setup Router 2
3.	On the laptop, log off from wifi and connect the cable to router 2
4.	Disable the DHCP server on this router to prevent IP conflicts or network configuration issues allowing only Router 1 to manage the network.
5.	Restart the router
6.	Set the IPv4 address on the laptop manually for both laptop and gateway, the gateway has to be the fixed address of the router 2 (e.g. 192.168.0.1)
7.	Manually set the IP Address of this router to the IP reserved in step 2.
8.	Set the internet connection to static IP.
9.	Restart the router
10.	Set the IP on the laptop again (to the new address) if the network does not work
11.	Connect the two routers using a cable from any of LAN port in router 1 to any LAN port in router 2. 
12.	In the wireless security settings of this router, disable Automatic Channel selection and manually set the channel to channel a different channel than the one set in step 1
13.	Set up wireless security to be identical in router 2 as it is in router 1.
