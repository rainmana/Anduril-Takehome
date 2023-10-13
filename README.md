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



# Alec's Design Decisions
