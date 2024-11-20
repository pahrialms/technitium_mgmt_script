Berikut adalah dokumentasi untuk script Anda, diformat untuk GitHub dalam file `README.md`:

---

# Technitium DNS Management Script

## Overview
This Python script automates the creation of DNS zones and DNS records on a Technitium DNS server. It uses the Technitium API to perform these operations. You can specify a pre-generated token, a list of zones, and a CSV file containing DNS records.

## Features
- **Add Zones:** Creates primary DNS zones on the Technitium DNS server.
- **Add Records:** Adds DNS records (A, CNAME) to the specified zones from a CSV file.
- **Logging:** All actions and errors are logged for easier debugging.
- **Command-Line Options:** Flexible configuration via command-line arguments.

---

## Prerequisites
1. A Technitium DNS server running and accessible via HTTP.
2. Python 3.x installed on your system.
3. A pre-generated API token from the Technitium server.
4. `requests` library installed:
   ```bash
   pip install requests
   ```

---

## Usage
### Generate API Token
Before running the script, generate an API token manually using the Technitium DNS Web UI or API.

---

### Command-Line Options
The script accepts the following command-line arguments:

| Argument      | Description                                                                                  | Required | Default           |
|---------------|----------------------------------------------------------------------------------------------|----------|-------------------|
| `--token`     | API token for Technitium DNS Server.                                                        | Yes      | None              |
| `zones`       | List of zones to create.                                                                    | Yes      | None              |
| `--csv`       | Path to the CSV file containing DNS records.                                                | No       | `dns_records.csv` |

---

### Example Command
```bash
python3 setdns.py --token <your-token> btest.io 10.25.10.in-addr.arpa --csv dns_records.csv
```

### Example CSV File
The script expects a CSV file with the following headers:

| Column       | Description                                      |
|--------------|--------------------------------------------------|
| `Domain`     | Full domain name of the record.                 |
| `zone`       | Zone to which the record belongs.               |
| `type`       | Record type (`A`, `CNAME`).                     |
| `ipAddress`  | IP address for `A` records (leave blank for CNAME). |
| `ttl`        | Time to live for the record.                    |
| `ptr`        | Whether to create a PTR record (true/false).    |
| `cname`      | Canonical name for `CNAME` records.             |

#### Example Content:
```csv
Domain,zone,type,ipAddress,ttl,ptr,cname
jkt03-utility01.btest.io,btest.io,A,192.168.10.7,3600,true,
api.jkt03-ocp01.btest.io,btest.io,A,192.168.10.9,3600,true,
api-int.jkt03-ocp01.btest.io,btest.io,CNAME,,3600,false,api.jkt03-ocp01.btest.io
```

---

## How It Works
1. **Create Zones:** The script first creates all specified zones using the API.
2. **Add Records:** It processes the CSV file and adds DNS records (A and CNAME) to the respective zones.
3. **Error Handling:** Errors during zone or record creation are logged but do not stop the execution.

---

## Logs
All actions and errors are logged in `dns_management.log`. This log includes:
- Successful zone creation.
- Successful DNS record addition.
- Errors encountered during API requests.

---

## Troubleshooting
### No Output or Records Added
1. Ensure the Technitium server is accessible via the specified URL.
2. Verify that the API token is valid and not expired.
3. Check the log file `dns_management.log` for any error messages.

### Example Errors
- **Invalid Token:** Ensure the `--token` value is correct.
- **HTTP Errors:** Verify the Technitium server URL is reachable.

---

## Contributing
If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.

---

## License
This project is licensed under the MIT License.

---

## Acknowledgments
Thanks to the Technitium DNS team for providing a powerful and extensible DNS solution.

---

Save this content into a file named `README.md` in your GitHub repository. It provides a clear and comprehensive guide for users to set up and use the script effectively.
