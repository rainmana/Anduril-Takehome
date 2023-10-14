# Anduril-Takehome
This repository is to host the code for my Anudril Takehome test with instructions sent on Friday, October 13th and code submission due at 2:00 PM PST on October 24, 2023.

**Demo App:** [https://anduril-takehome-production.up.railway.app](https://anduril-takehome-production.up.railway.app)

# Instructions and Requirements

## SecEng Take Home

### Prompt

Write a program that allows the detection and response team to query an API with a given IPv4 or IPv6 address and
receive an acknowledgement if it is a Tor exit node

### Requirements

- List of Tor exit nodes can be obtained from [https://secureupdates.checkpoint.com/IP-list/TOR.txt](https://secureupdates.checkpoint.com/IP-list/TOR.txt)
- This list contains IPv4 and IPv6

### Expected functionality

- Program is portable (suggest using Docker or Terraform/AWS CDK to deploy to AWS free tier)
- The API must front every request (every request made to program must transit through the API)
- Three types of requests
  - Search for exact IP address
  - Retrieve full list
  - Delete exact IP address from list
- Extra credit but not required
  - Schedule refresh of data
- Minimum supporting documentation (instructions to set up your program and how to make requests to your API)

### Time

- 24hrs


# Installation Procedures

This application was designed with Docker in mind as a way to make it portable per the instructions given by Christian and the team, but it can be run locally as well.


## Running Locally

**Note:** This was only tested on macOS 13.5.2 (22G91) locally, and within Docker Containers running Alpine 3.18 so instructions are for *Nix platforms. Given how simple the code is, it should work natively on Windows, but has not been tested for that use case. All instructions are written to assume you have macOS, Linux, or will just use Docker/containerization.

Additionally, this can and likely should be done in a Python Virtual Environment to ensure you don't cause issues with any of your other projects, but the instructions will not have these commands included. I also recommend this application be run as a Docker container instead of any type of local deployment for ease of use.

### Requirements

- Python 3.11.6
- `fastapi==0.103.2`
- `Requests==2.31.0`
- `uvicorn==0.23.2`

### Install Guide

**Clone the repository to your local machine:**

```bash
git clone https://github.com/rainmana/Anduril-Takehome
```

**Change directories into "Anduril-Takehome":**

```bash
cd Anduril-Takehome
```

**Install Python dependencies:**

```bash
python3 -m pip install requirements.txt
```

**Change directories into "app":**

```bash
cd app
```

**For running the server in a local dev envrionment with "hot reloading", use the following from inside the "app" directory:**

```bash
uvicorn main:app --reload
```

**For more production-focused deployemtns, you can use the following command from insdie the "app" directory. Note that this binds the app to all interfaces likely making the app publically accessable via 0.0.0.0 over port 80:**

```bash
uvicorn main:app --host 0.0.0.0 --port 80
```

## Running With Docker

### Requirements

**Note:** These instructions are assuming you have something like Docker Desktop installed on a server or local development machine.

- Docker Desktop
- Similar containerization platform (different commands will likely be used)

### Install Guide

**Clone the repository to your target machine:**

```bash
git clone https://github.com/rainmana/Anduril-Takehome
```

**Change directories into Anduril-Takehome:**

```bash
cd Anduril-Takehome
```

**Build the Docker imagine from the included Dockerfile:**

```bash
docker build -t anduril-takehome .
```

**Run the docker container on your chosen port (I use "4000" here, but you likely will want something like "80"):**

```bash
docker run -p 4000:80 anduril-takehome
```

## Cloud Hosting
**Note:** These instructions will be specific to [Railway](https://railway.app/about) which is an incredibly simple to use, and often times free way to host cloud projects. I choose it given the tight budget constraints and due to the free tier/credit system. If I were designing this as an enterprise application, I would use whatever the organization preferred (e.g. Google Cloud Platform, AWS, Azure, etc.).

**Railway Demo App:** [https://anduril-takehome-production.up.railway.app](https://anduril-takehome-production.up.railway.app)

### Requirements

- An account on your cloud provider of choice (I'm using [Railway](https://railway.app/about) in this example)
- A GitHub repository with the code for this app. This can be done via "forking" this repo which will add a version of it to your GitHub account

### Install Guide

1. Go to [https://railway.app](https://railway.app) and click "*Start a New Project*"
2. Click on "*Deploy from GitHub repo*"
3. Click "*Login With GitHub*" if you have not already done so
4. Click "*Add variables*" 
5. Next, add a variable name of "*PORT*" (without quotes) and give it a value of "*80*" (without quotes) and click "Add"
6. Autodeployment should begin once you do this. You'll wait for a minute or so for this process to complete
7. Next, click on "*Settings*" in the top right of your current window. You can also click on the rectangle displaying the GitHub icon with your repo name in it to get the control pane open where settings is displayed in the top right if you're in a different part of the user interface
8. Under the "Networking" section under "*Public Networking*," click on "*Generate Domain*" to create a randomly generated domain your application will be available at. After a few minutes (you may also need to clear your browser cache), the application should direct you to a simple HTML page with links to the interactive documents, this GitHub Repo, and the OpenAPI specification file

# Alec's Design Decisions

## Programming Language - Python

I chose Python since this is the one that I am most familiar with and have written simple Flask apps and Webhook listeners in for my various enterprise projects I've been assigned in the past. It has easy syntax and is easy to understand and write-in for many people which also makes it easy for someone looking at the code is this project for the first time, be able to more easily pick up and run with it.

## Python Modules

### FastAPI

I chose to use FastAPI since I found this to be a good opportunity to learn about it - regardless of the interview outcome. I knew that it allowed for asynchronous request processing and that it was incredibly easy to add with just a prefix of "async" before the various functions I'd be writing to handle requests for different routes. It also made much of the documentation easier for me in this "fast prototyping" type of challenge where I'd be either refreshing many different skills, or learning/growing ones that I was less comfortable with such as Docker. FastAPI auto-generated a Swagger Docs type of interface as well as an OpenAPI specification which would make it easier for users to pick up and run with this app.

### Requests

I chose the Requests library as it was the simplest choice that I had the most experience with to get the list or TOR IPs from the Checkpoint site. It's easy to use and operates quickly enough for a simple application like this one.

### Univcorn

Uvicorn is what ships with FastAPI and is designed to use it. Given my relative "newness" to FastAPI (though it's really not that much different from Flask), I wouldn't feel comfortable trying to use something else - and I'm not even sure that's an option?

### Pipreqs

I used pipreqs to generate the requirements file, though it was missing uvicorn when this was generated since I used `python3 -m pip install "fastapi[all]"` to install FastAPI, so I manually added the line item for uvicorn to the `requirements.txt` file along with it's specific version after the fact.

## Program Design Logic

### Getting Checkpoint's List of TOR IPs

I went as simple as I possibly could go since I knew I'd be learning as I went for several technologies in this stack. I used a simple Python requests function to go out to the Checkpoint site and grab the IP addresses and add them to a respective ipv4_set or ipv6_set by leveraging simple, known regular expressions for these particular versions of IP. When data matches the IP address type, it adds it to the respective set to be used later. Since this was also created as a function, I could use Python's threading module to run the function ever 86400 seconds to give the data refresh every 24 hours which was another opportunity for me to learn something since I'd not used threading before. Additionally, the program should ignore any of the removed IPs the user has manually added.

### Default Route

I realized during testing that the default route of "`/`" resulted in an error. I learned through FastAPI's docs that a simple HTML page can be shown instead, so I added some super simple HTML with links to various important areas of the API, as well as a quick description. I thought this could improve the overall "polish" of my project without incurring significant technical debt which is why I also used MVP.css which was a single line to add.

### Searching for an IP

To search for an IP, I created a FastAPI route for "`/search_ip/"` which allows the user to pass an IP (the human readable version) to this API endpoint. It then uses simple logic via an if/elif/else loop to check to see if the IP is in the ipv4_set, the ipv6_set, then returns a not found (respectively). For each stage of the if/elif/else logic, it will return a simple Python dictionary. I learned that FastAPI is smart enough to know to translate this into JSON which reduced time during developement as well as complexity.

### Removing an IP

To remove an IP, I created a FastAPI route for "`/remove_ip/`" which allows the user to pass an IP (the human readable version) to the API endpoint. Just like the "`/search_ip/`" endpoint, it uses if/elif/else logic to check wether the submitted value is in the ipv4_set or ipv6_set, or return "not found" if in neither.

### Downloading All IPs

To download all IP addresses (include the removed addresses) the application current has in memory, I created a FastAPI route that simply returns a `JSONResponse` object (something FastAPI can handle natively) which contains nested JSON describing a set of the IPv4 addresses as well as the IPv6 addresses by adding the respective set's data to the returned JSON content. I included headers to instruct the browser to download this document as a file instead of just displaying it in a new tab.

## Additional Routes
### Refresh IP
I added a route which will all the user to manually refresh the list of IPs while also ignoring any IPs that they have removed. This can help enable better testing.

### List Removed IPs
I also added another function which will return a list of the IPv4 and IPv6 addresses that the user has chose to manually remove so they can check what's been removed.


## Portability

I am most familiar with Docker, so I chose Docker as the way to make this portable. I created a Dockerfile which utilized a Python/Alpine image as a base, then coppied the app code to a directory in the new container, and installed all requirements from the `requirements.txt` file. I tested interations of this locally to ensure all functionality when run locally, also ran when the application was containerized. I then deployed it to the Cloud Hosting service "Railway" and tested functionality once more - all successfully.


## Future Improvements

- Add HTTPS via a reverse proxy or some type of middleware. HTTPS could help by increasing the trust and integrity in the data returned from the API. Additionally, more integrity checking could be added by computing hash values of the entirety of the downloaded Checkpoint data, inclusion of a date, etc. to further improve overall trust in the data
- Consider adding a database backend vs storing all data in volatile memory. I chose the volatile memory direction given the time limitation and my lack of experience when writing applications leveraging databases
- Consider deployment to services like AWS, GCP, or Azure during the design process to make the re-usability more centered toward the enterprise
- Provide another route for the user to manually add IPs the dataset


# API Docs

## FastAPI
## Version: 0.1.0

### /

#### GET
##### Summary:

The default route for the application.

##### Description:

This is the default route for the application. It will display links to resources for the application/API, such
as the Swagger UI, OpenAPI Spec, and GitHub repository along with a short description. It uses MVP.css for styling.

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /search_ip/

#### GET
##### Summary:

Search for an IP address.

##### Description:

Search for an IP address in a set of known TOR IP addresses. This function will take in an IP address in it's human readable format
and return a JSON response as to wether or not it is in the IPv4 or IPv6 set.

Please use the following format for the IP address:
- IPv4:
    - 10.10.10.10

- IPv6:
    - 2001:0db8:85a3:0000:0000:8a2e:0370:7334

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| ip | query |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /remove_ip/

#### DELETE
##### Summary:

Remove an IP address from the set.

##### Description:

Remove an IP address from the set of known TOR IP addresses. This function will take in an IP address in it's human readable format.
This will also ensure that when the dataset updates every 24 hours, the IP address will not be added back in. Note that this will only
persist as the machine is running as all sets are stored in volatile memory, a database or similar could be used to persist this data.

Please use the following format for the IP address:
- IPv4:
    - 10.10.10.10

- IPv6:
    - 2001:0db8:85a3:0000:0000:8a2e:0370:7334

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| ip | query |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /refresh_ips/

#### GET
##### Summary:

Manually refresh the IP addresses in the dataset.

##### Description:

Manually refresh the IP addresses in the dataset. This function will manually refresh the IP addresses in the dataset and return how many
new IPv4 and IPv6 addresses were added to the set as JSON.

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /list_removed_ips/

#### GET
##### Summary:

List the IPv4 and IPv6 addresses that have been removed from the dataset.

##### Description:

List the IPv4 and IPv6 addresses that have been removed from the dataset.
This function will return a JSON response with the IPv4 and IPv6 addresses that have been removed by the user via the "/remove_ip/" endpoint.

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /download_ips/

#### GET
##### Summary:

Download the IPv4 and IPv6 sets as a JSON file.

##### Description:

This function will return a JSON response with the IPv4 and IPv6 sets as a JSON file.
Respective IPv4 and IPv6 addresses will be stored in a nested structure denoting each type of IP address.
Additionally, this will also include the IPv4 and IPv6 addresses that have been removed by the user via API call and store those
in a nested structure denoting each type of IP address and the addresses themselves.

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

