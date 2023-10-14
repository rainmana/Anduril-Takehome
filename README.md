# Anduril-Takehome
This repository is to host the code for my Anudril Takehome test with instructions sent on Friday, October 13th and code submission due at 2:00 PM PST on October 24, 2023.

# Instructions and Requirements

## SecEng Take Home

### Prompt

Write a program that allows the detection and response team to query an API with a given IPv4 or IPv6 address and
receive an acknowledgement if it is a Tor exit node

### Requirements

- List of Tor exit nodes can be obtained from https://secureupdates.checkpoint.com/IP-list/TOR.txt
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

**Clone the repository to your local machine:**

```bash
git clone https://github.com/rainmana/Anduril-Takehome
```

**Change directories into Anduril-Takehome:**

```bash
cd Anduril-Takehome
```

**Install Python dependencies:**

```bash
python3 -m pip install requirements.txt
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

**Clone the repository to your target machine:**

```bash
git clone https://github.com/rainmana/Anduril-Takehome
```

**Change directories into Anduril-Takehome:**

```bash
cd Anduril-Takehome
```





# Alec's Design Decisions
