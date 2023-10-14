'''
This is the main file of the application and will handle all of the requirements as detailed out by Christian (my recruiter) for Anduril as set
by the Incident Reponse Team which I have placed in the README.
'''

# Import required libraries
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import re
import threading
import json

# Initialize the fastapi app
app = FastAPI()

# Create an empty set to store the IPv4 and IPv6 addresses
ipv4_set = set()
ipv6_set = set()

# Create a function to get the IP addresses from the URL provided by the team
def get_ips():
    global ipv4_set, ipv6_set

    url = "https://secureupdates.checkpoint.com/IP-list/TOR.txt"
    
    # Get the response from the URL
    response = requests.get(url)

    # Check the status code of the response and if it is 200, then continue
    if response.status_code == 200:
        # Create a list of IPv4 addresses found in the response.text via regex
        ipv4_list = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', response.text)

        # Create a list of IPv6 addresses found in the response.text via regex
        ipv6_list = re.findall(r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b', response.text)

        # Update the set with both lists
        ipv4_set = set(ipv4_list)
        ipv6_set = set(ipv6_list)

# Get IP addresses initially, but then follow up every 24 hours using the threading module and seconds as the time
get_ips()
threading.Timer(86400, get_ips).start()

# Create a FastAPI endpoint to reutrn a response as to wether an IP address is in the set or not and return a JSON response via decorator
# This function will take in an IP address and return a JSON response as to wether or not it is in the IPv4 or IPv6 set
## Using this opporunity to learn/leverage "async" operations in Python and FastAPI to make the application more efficient
@app.get("/search_ip/")
async def search_ip(ip: str):
    # Check to see if the IP address is in the IPv4 set and if it is, return a JSON response with the IP address and that it was found
    if ip in ipv4_set:
        return {"status": "found", "ip": ip, "type": "IPv4"}
    # If the IP is not in the IPv4 set, check whether or not it's in the IPv6 list
    elif ip in ipv6_set:
        return {"status": "found", "ip": ip, "type": "IPv6"}
    # If the IP is not in either set, return a JSON response with the IP address and that it was not found
    else:
        return {"status": "not found", "ip": ip}

# Create a FastAPI endpoint to allow the deletion of an IP address from the appropriate set and return a JSON response via decorator
## Using this opporunity to learn/leverage "async" operations in Python and FastAPI to make the application more efficient
@app.delete("/remove_ip/")
async def remove_ip(ip: str):
    # Check to see if the IP address is in the IPv4 set and if it is, remove it and return a JSON response with the IP address and that it was removed
    if ip in ipv4_set:
        ipv4_set.remove(ip)
        return {"status": "removeed", "ip": ip, "type": "IPv4"}
    # If the IP is not in the IPv4 set, check whether or not it's in the IPv6 list
    elif ip in ipv6_set:
        ipv6_set.remove(ip)
        return {"status": "removed", "ip": ip, "type": "IPv6"}
    # If the IP is not in either set, return a JSON response with the IP address and that it was not found
    else:
        return {"status": "not found", "ip": ip}

