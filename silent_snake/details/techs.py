import bs4
from requests import Response
import re

class UiFrameworks:

    """UI Frameworks Tech Details."""

    def __init__(self, data: Response):
        self.data = data
        self.framework = set()
        self.__detect()

    # Supported UI Frameworks Detection ["Bootstrap", "Tailwind CSS", "Animate.css"]

    def __bootstrap(self) -> None:
        
        soup = bs4.BeautifulSoup(self.data.text, 'html.parser')
        
        links = soup.find("head").find_all("link", href=True)
        
        for link in links:
            if "bootstrap" in link['href']:
                self.framework.add("Bootstrap")
                return 
            
        src = soup.find("head").find_all("script", src=True)
        for link in src:
            if "bootstrap" in link['src']:
                self.framework.add("Bootstrap")
                return 
            
        
        bootstrap_classes = ["row", "col"]
        
        for cls in bootstrap_classes:
            if f"class=\"{cls}" in self.data.text.lower():  # crude but works
                self.framework.add("Bootstrap")
                return
            
    def __tailwind(self) -> None:
        
        classes = []

        soup = bs4.BeautifulSoup(self.data.text, 'html.parser')

        for tag in soup.find("body").find_all(class_=True):
            classes.extend(tag['class'])

        patterns = [
            r"^w-\d+/?\d*$",      # w-1/2, w-12
            r"^h-\d+/?\d*$",
            r"^text-(xs|sm|lg|xl|\d+x?l)$",
            r"^bg-(red|blue|green|gray|indigo|purple)-\d{3,4}$",
            r"^space-[xy]-\d+$",
            r"^divide-[xy]$",
            r"^ring(-\d+)?$",
            r"^(sm|md|lg|xl):",   # responsive prefixes
        ]

        for cls in classes:
            for pat in patterns:
                if re.match(pat, cls):
                    self.framework.add("Tailwind CSS")
                    return  
                
    def __animate(self) -> None:
        soup = bs4.BeautifulSoup(self.data.text, 'html.parser')
        
        links = soup.find("head").find_all("link", href=True, rel="stylesheet")

        classes = soup.find("body").find_all(class_=True)

        for link in links:
            if "animate.min.css" in link['href']:
                self.framework.add("Animate.css")
                return
            
        for cls in classes:
            if "animate__" in cls['class']:
                self.framework.add("Animate.css")
                return
        
    def __detect(self) -> None:
        self.__bootstrap()
    
        if "Bootstrap" not in self.framework:
            self.__tailwind()
            
        self.__animate()


    def __str__(self):
        return f"\nDetected UI Frame work : {list(self.framework)}\n" if len(self.framework) > 0 else "No UI Framework Detected"
            
    