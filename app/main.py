'''
This is the main file of the application and will handle all of the requirements as detailed out by Christian (my recruiter) for Anduril as set
by the Incident Reponse Team which I have placed in the README.
'''

# Import required libraries
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
import requests
import re
import threading

# Initialize the fastapi app
app = FastAPI()

# Create an empty set to store the IPv4 and IPv6 addresses
# I've chosen to use a set because it is more efficient than a list and will not allow duplicates
ipv4_set = set()
ipv6_set = set()

# Create a function to get the IP addresses from the URL provided by the team
# This function is used later to update the set of IP addresses every 24 hours
def get_ips():
    global ipv4_set, ipv6_set

    url = "https://secureupdates.checkpoint.com/IP-list/TOR.txt"
    
    # Get the response from the URL
    response = requests.get(url)

    # Check the status code of the response and if it is 200, then continue
    if response.status_code == 200:
        # Create a list of IPv4 addresses found in the response.text via regex
        # This will make it easier to handle the data and update the set, but relies on the assumption that the data will always be in the same format
        ipv4_list = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', response.text)

        # Create a list of IPv6 addresses found in the response.text via regex
        # This will make it easier to handle IPv6 addresses and update the set, but relies on the assumption that the data will always be in the same format
        # Additonally, this strips the leading and following brackets from the IPv6 addresses to make it easier to handle when querying the API later
        ipv6_list = re.findall(r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b', response.text)

        # Update the set with both lists
        ipv4_set = set(ipv4_list)
        ipv6_set = set(ipv6_list)

# Get IP addresses initially, but then follow up every 24 hours using the threading module and seconds as the time
# Note that at the moment, any removed IP addresses will be added back in after 24 hours (if they are still in the list)
get_ips()
threading.Timer(86400, get_ips).start()

# Because there's no default route, instead of showing the user a non-descript error, I've chosen to show them a custom HTML page with simple instructions
# We'll use a decorator like normal to define the route and specifiy the response type as HTMLResponse
@app.get("/", response_class=HTMLResponse)
def default_route():
    # We'll create a variable to contain some simple HTML to display to the user
    html_content = """
     <html>
        <head>
            <title>Alec's Anduril-Takehome Test App</title>
        </head>
        <body>
            <h1>Welcome to Alec's Anduril-Takehome Test APP!</h1>
            <p>Built by W. Alec Akin for an Anduril Interview, this application will get a list of known TOR IPs from Checkpoint, then let a user check to see if their IP is in the list (among other requirements).</p>
            <ul>
                <li><a href="/docs">API Documentation</a></li>
                <li><a href="/openapi.json">OpenAPI Spec</a></li>
                <li><a href="https://github.com/rainmana/Anduril-Takehome">GitHub Repository</a></li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
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

# Create a FastAPI endpoint to allow the deletion of an IP address from the appropriate set and return a JSON response via decorator as FastAPI requires
# Note that this function will only remove the IP address from the set for 24 hours as the get_ips() function will add it back in (if present in Checkpoints' txt file)
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

# Create a FastAPI endpoint to allow the download of both IPv4 and IPv6 sets and return a JSON response via decorator
@app.get("/download_ips/")
async def download_ips():
    # I'm using the "JSONResponse" function to return a JSON response with the apppropriate headers to instruct the browser to download the file
    # I also learned through this process that FastAPI is smart enough to know that the content is JSON and will automatically format it as such when using Python dicts like above
    return JSONResponse(content={"IPv4": list(ipv4_set), "IPv6": list(ipv6_set)}, headers={"Content-Disposition": "attachment; filename=TOR_ips.json"})