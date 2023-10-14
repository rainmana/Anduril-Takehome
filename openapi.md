# FastAPI
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
