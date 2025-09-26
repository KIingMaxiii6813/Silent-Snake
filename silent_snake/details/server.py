import requests
from socket import getaddrinfo

class Server:
    """
    server details like city, country, org
    """
    def __init__(self, host: str):
        self.host = host
        self.city = None
        self.country = None
        self.org = None
        self.ip = None
        self.server = None
        self.__fetch_details()
        
        
    def __fetch_details(self):
        """
        fetch server details from ipinfo.io
        """

        try:
            response = requests.get(f"https://ipinfo.io/{getaddrinfo(self.host, None)[0][4][0]}/json")
            
            if response.status_code == 200:
                data = response.json()
                self.server = requests.get(f"https://{self.host}").headers.get("server")
                self.city = data.get("city")
                self.country = data.get("country")
                self.ip = data.get("ip")
                self.org = data.get("org")
                

        except Exception as e:
            print(f"Error fetching server details through ipinfo: {e}")

    def __str__(self):
        return f"\nHost: {self.host}\n City: {self.city}\n Country: {self.country}\n Org: {self.org}\n server: {self.server}\n IP: {self.ip}\n"
    
    