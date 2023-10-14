'''
This is the main file of the application and will handle all of the requirements as detailed out by Christian (my recruiter) for Anduril as set
by the Incident Reponse Team which I have placed in the README.

Note: Since this application stores it's data entirely in volatile memory, it will not persist across restarts. This is by design as I did not want to
complicate the application by adding a database or other persistent storage mechanism due to time limits, but it's certainly something that could be added later.

Note2: I've not implemented HTTPS or similar security mesures, though in production I would definitely do so. I wanted to keep complexity low and given
that FastAPI doesn't support HTTPS out of the box, I chose to leave it out for now so I wouldn't need to add middleware or a reverse proxy to handle it.
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

# Create an empty set to store the IPv4 and IPv6 addresses that have been removed by the user via API call
# This should prevent the update of the intel from Checkpoint from overwriting the user's removal of an IP address from the set
## Note that this will only persist as the machine is running as all sets are stored in volatile memory, a database or similar could be used to persist this data
removed_ipv4_set = set()
removed_ipv6_set = set()

# Create a function to get the IP addresses from the URL provided by the team
# This function is used later to update the set of IP addresses every 24 hours
def get_ips():
    
    # Declare the global variables so we can update them in the function
    global ipv4_set, ipv6_set, removed_ipv4_set, removed_ipv6_set
    
    # Define the URL we use to get a list of TOR IP intelligence from Checkpoint
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
        ipv4_set = set(ipv4_list) - removed_ipv4_set
        ipv6_set = set(ipv6_list) - removed_ipv6_set

# Get IP addresses initially
get_ips()

# Follow up every 24 hours using the threading module and seconds as the time
# Since we have sets that track removed IP addresses, the update shouldn't overwrite IPs the user has removed
threading.Timer(86400, get_ips).start()

# Because there's no default route, instead of showing the user a non-descript error, I've chosen to show them a custom HTML page with simple instructions
# We'll use a decorator like normal to define the route and specifiy the response type as HTMLResponse
@app.get("/", response_class=HTMLResponse, summary="The default route for the application.")
def default_route():
    """
    This is the default route for the application. It will display links to resources for the application/API, such
    as the Swagger UI, OpenAPI Spec, and GitHub repository along with a short description. It uses MVP.css for styling.
    """
    
    # We'll create a variable to contain some simple HTML to display to the user
    html_content = """
     <html>
        <head>
            <title>Alec's Anduril-Takehome Test App</title>
            <link rel="stylesheet" href="https://unpkg.com/mvp.css"> 
        </head>
        <body>
            <h1>Welcome to Alec's Anduril-Takehome Test App!</h1>
            <p>Built by W. Alec Akin for an Anduril Interview, this application will get a list of known TOR IPs from Checkpoint, then let a user check to see if their IP is in the list (among other requirements).</p>
            <p>For more information, please see the links below:</p>
            <ul>
                <li><a href="/docs">API Documentation</a></li>
                <li><a href="/openapi.json">OpenAPI Spec</a></li>
                <li><a href="https://github.com/rainmana/Anduril-Takehome">GitHub Repository</a></li>
            </ul>
        </body>
    </html>
    """
    # Return the HTML content to the user using FastAPI's HTMLResponse function
    return HTMLResponse(content=html_content)

# Create a FastAPI endpoint to reutrn a response as to wether an IP address is in the set or not and return a JSON response via decorator
# This function will take in an IP address and return a JSON response as to wether or not it is in the IPv4 or IPv6 set
## Using this opporunity to learn/leverage "async" operations in Python and FastAPI to make the application more efficient
@app.get("/search_ip/", summary="Search for an IP address.")
async def search_ip(ip: str):
    """
    Search for an IP address in a set of known TOR IP addresses. This function will take in an IP address in it's human readable format
    and return a JSON response as to wether or not it is in the IPv4 or IPv6 set.

    Please use the following format for the IP address:
    - IPv4:
        - 10.10.10.10

    - IPv6:
        - 2001:0db8:85a3:0000:0000:8a2e:0370:7334
    """
    
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
@app.delete("/remove_ip/", summary="Remove an IP address from the set.")
async def remove_ip(ip: str):
    """
    Remove an IP address from the set of known TOR IP addresses. This function will take in an IP address in it's human readable format.
    This will also ensure that when the dataset updates every 24 hours, the IP address will not be added back in. Note that this will only
    persist as the machine is running as all sets are stored in volatile memory, a database or similar could be used to persist this data.

    Please use the following format for the IP address:
    - IPv4:
        - 10.10.10.10

    - IPv6:
        - 2001:0db8:85a3:0000:0000:8a2e:0370:7334
    """

    # Check to see if the IP address is in the IPv4 set and if it is, remove it and return a JSON response with the IP address and that it was removed
    if ip in ipv4_set:
        
        # Remove the IP address from the primary IPv4 set
        ipv4_set.remove(ip)
        
        # Add the IP address to a secondary set to keep track of removed IPv4 addresses and return JSON response
        removed_ipv4_set.add(ip)
        return {"status": "removeed", "ip": ip, "type": "IPv4"}
    
    # If the IP is not in the IPv4 set, check whether or not it's in the IPv6 list
    elif ip in ipv6_set:
        
        # Remove the IP address from the primary IPv6 set
        ipv6_set.remove(ip)
        
        # Add the IP address to a secondary set to keep track of removed IPv6 addresses and return JSON response
        removed_ipv6_set.add(ip)
        return {"status": "removed", "ip": ip, "type": "IPv6"}
    
    # If the IP is not in either set, return a JSON response with the IP address and that it was not found
    else:
        return {"status": "not found", "ip": ip}

# Create a FastAPI endpoint to allow the download of both IPv4 and IPv6 sets and return a JSON response via decorator
@app.get("/download_ips/", summary="Download the IPv4 and IPv6 sets as a JSON file.")
async def download_ips():
    """
    Download the IPv4 and IPv6 sets as a JSON file. This function will return a JSON response with the IPv4 and IPv6 sets as a JSON file.
    Respective IPv4 and IPv6 addresses will be stored in a nested structure denoting each type of IP address.
    """
    
    # I'm using the "JSONResponse" function to return a JSON response with the apppropriate headers to instruct the browser to download the file
    # I also learned through this process that FastAPI is smart enough to know that the content is JSON and will automatically format it as such when using Python dicts like above
    return JSONResponse(content={"IPv4": list(ipv4_set), "IPv6": list(ipv6_set)}, headers={"Content-Disposition": "attachment; filename=TOR_ips.json"})