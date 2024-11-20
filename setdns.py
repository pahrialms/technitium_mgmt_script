import argparse
import requests
import csv
import logging

# Logging setup
LOG_FILE = "dns_management.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_zone(server_url, token, zones):
    """Create zones in the DNS server."""
    for zone in zones:
        url = f"{server_url}/api/zones/create"
        params = {
            "token": token,
            "zone": zone,
            "type": "Primary"
        }
        try:
            response = requests.post(url, params=params)
            if response.status_code == 200:
                logging.info(f"Zone '{zone}' created successfully.")
                print(f"Zone '{zone}' created successfully.")
            else:
                logging.error(f"Failed to create zone '{zone}': {response.status_code} - {response.text}")
                print(f"Failed to create zone '{zone}': {response.status_code} - {response.text}")
        except Exception as e:
            logging.error(f"Error creating zone '{zone}': {e}")
            print(f"Error creating zone '{zone}': {e}")

def process_csv(server_url, token, file_path):
    """Process the CSV file and add DNS records."""
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            records = list(reader)

        for record in records:
            domain = record["Domain"]
            zone = record["zone"]
            record_type = record["type"]
            ip_address = record.get("ipAddress", None)
            ttl = int(record["ttl"])
            ptr = record.get("ptr", "false")
            cname = record.get("cname", "")

            add_dns_record(server_url, token, domain, zone, record_type, ip_address, ttl, ptr, cname)
        logging.info("All records processed successfully.")
        print("All records processed successfully.")
    except Exception as e:
        logging.error(f"Error processing CSV file: {e}")
        print(f"Error processing CSV file: {e}")

def add_dns_record(server_url, token, domain, zone, record_type, ip_address=None, ttl=3600, ptr="false", cname=""):
    """Add DNS record to a zone."""
    url = f"{server_url}/api/zones/records/add"
    params = {
        "token": token,
        "domain": domain,
        "zone": zone,
        "type": record_type,
        "ttl": ttl
    }
    if record_type == "A":
        params["ipAddress"] = ip_address
        if ptr.lower() == "true":
            params["ptr"] = "true"
    elif record_type == "CNAME":
        params["cname"] = cname

    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            logging.info(f"Successfully added {record_type} record for {domain} in zone {zone}")
            print(f"Successfully added {record_type} record for {domain} in zone {zone}")
        else:
            logging.error(f"Failed to add {record_type} record for {domain}: {response.status_code} - {response.text}")
            print(f"Failed to add {record_type} record for {domain}: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Error adding record for {domain}: {e}")
        print(f"Error adding record for {domain}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Script untuk mengelola zone DNS dan menambahkan record di server Technitium DNS.\n\n"
            "Usage:\n"
            "  python3 script.py --server <server-url> --token <token> <zone1> <zone2> ... --csv <file.csv>\n"
            "Contoh:\n"
            "  python3 script.py --server http://192.168.91.130:5380 --token <your-token> btest.io 10.25.10.in-addr.arpa --csv dns_records.csv\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--server", required=True, help="Technitium DNS Server URL (e.g., http://192.168.91.130:5380)."
    )
    parser.add_argument(
        "--token", required=True, help="API token for Technitium DNS Server (generated manually)."
    )
    parser.add_argument(
        "zones", nargs="+", help="Daftar nama zona yang akan dibuat (pisahkan dengan spasi)."
    )
    parser.add_argument(
        "--csv",
        default="dns_records.csv",
        help="File CSV yang berisi record DNS (default: dns_records.csv)."
    )

    args = parser.parse_args()

    try:
        # Step 1: Create zones from command-line arguments
        create_zone(args.server, args.token, args.zones)

        # Step 2: Process CSV file and add records
        process_csv(args.server, args.token, args.csv)
    except Exception as e:
        logging.error(f"Script failed: {e}")
        print(f"Script failed: {e}")
