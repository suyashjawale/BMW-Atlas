from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import requests
import os

IMAGE_DIR = "model_images"
BASE_URL = "https://www.bmw-motorrad.com/en/home.html"

INVALID_KEYWORDS = (
    "importer",
    "facebook",
    "alfardanmotor"
)
os.makedirs(IMAGE_DIR, exist_ok=True)


def download_image(url: str, filename: str) -> bool:
    try:
        print(f"Downloading : {filename}")
        response = requests.get(url, timeout=15, stream=True)
        response.raise_for_status()
        with open(os.path.join(IMAGE_DIR, filename), "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  [!] Failed to download {url}: {e}")
        return False

# ─── Fetch & Parse ────────────────────────────────────────────────────────────
modelCode = {
    "0C61": "C 400 GT",
    "0C06": "C 400 GT",
    "0S01": "C 400 GT",
    "0C31": "C 400 X",
    "0C09": "C 400 X",
    "0S11": "C 400 X",
    "0131": "C 600 Sport",
    "0C05": "C 650 GT",
    "0133": "C 650 GT",
    "0C04": "C 650 Sport",
    "0C03": "C evolution",
    "0C71": "CE 02",
    "0C81": "CE 02 AM",
    "0C51": "CE 04",
    "0R31": "F 450 GS",
    "0B01": "F 700 GS 2013",
    "0B06": "F 700 GS 2017",
    "0B08": "F 750 GS",
    "0B08_S047B": "F 750 GS - Edition 40 Years GS",
    "0K51": "F 800 GS",
    "0218": "F 800 GS",
    "0219": "F 800 GS",
    "0B02": "F 800 GS",
    "0B07": "F 800 GS",
    "0B05": "F 800 GS Adventure",
    "0B55": "F 800 GS Adventure",
    "0B53": "F 800 GT",
    "0B03": "F 800 GT",
    "0B54": "F 800 R",
    "0B04": "F 800 R",
    "0234": "F 800 ST",
    "0B09": "F 850 GS",
    "0B09_S047B": "F 850 GS - Edition 40 Years GS",
    "0K01": "F 850 GS Adventure",
    "0K01_S047B": "F 850 GS Adventure - Edition 40 Years GS",
    "0K61": "F 900 GS",
    "0K61_S0499": "F 900 GS (Lower Suspension)",
    "0K71": "F 900 GS Adventure",
    "0K11": "F 900 R",
    "0K81": "F 900 R",
    "0K91": "F 900 R (A2)",
    "0K21": "F 900 XR",
    "0R01": "F 900 XR",
    "0R11": "F 900 XR (A2)",
    "0G31": "G 310 GS",
    "0G02": "G 310 GS",
    "0G31_S047B": "G 310 GS - Edition 40 Years GS",
    "0G41": "G 310 R",
    "0G01": "G 310 R",
    "0178": "G 650 GS",
    "0188": "G 650 GS",
    "0136": "G 650 GS Sert\u00e3o",
    "0D01": "HP 4",
    "0E31": "HP4 RACE",
    "0587": "K 1200 GT",
    "0584": "K 1200 R",
    "0585": "K 1200 R Sport",
    "0581": "K 1200 S",
    "0538": "K 1300 GT",
    "0518": "K 1300 R",
    "0508": "K 1300 S",
    "0F51": "K 1600 B",
    "0F61": "K 1600 B - Option 719 Midnight",
    "0F01": "K 1600 GT",
    "0F21": "K 1600 GT",
    "0601": "K 1600 GT 2014",
    "0F02": "K 1600 GTL",
    "0F31": "K 1600 GTL",
    "0602": "K 1600 GTL 2014",
    "0603": "K 1600 GTL Exclusive",
    "0F51_S047A": "K 1600 Grand America",
    "0F61_S047A": "K 1600 Grand America - Option 719 Midnight",
    "0E81": "M 1000 R",
    "0P51": "M 1000 R",
    "0P01": "M 1000 RR",
    "0E71": "M 1000 RR",
    "0P41": "M 1000 RR",
    "0E71_S047B": "M 1000 RR 50 Years M",
    "0E91": "M 1000 XR",
    "0N51": "R 12",
    "0N21": "R 12 G/S",
    "0N01_S0424": "R 12 S",
    "0N11_S0424": "R 12 S (A2)",
    "0N01": "R 12 nineT",
    "0N11": "R 12 nineT (A2)",
    "0A51": "R 1200 GS",
    "0A01": "R 1200 GS",
    "0307": "R 1200 GS",
    "0303": "R 1200 GS",
    "0450": "R 1200 GS",
    "0A02": "R 1200 GS Adventure",
    "0382": "R 1200 GS Adventure",
    "0380": "R 1200 GS Adventure",
    "0470": "R 1200 GS Adventure",
    "0A04": "R 1200 R",
    "0400": "R 1200 R",
    "0A05": "R 1200 RS",
    "0A03": "R 1200 RT",
    "0368": "R 1200 RT 2005",
    "0430": "R 1200 RT 2010",
    "0366": "R 1200 S",
    "0328": "R 1200 ST",
    "0M01": "R 1250 GS",
    "0J91": "R 1250 GS",
    "0M01_S047B": "R 1250 GS - Edition 40 Years GS",
    "0M11": "R 1250 GS Adventure Ultimate Edition",
    "0J51": "R 1200 GS Adventure",
    "0M11_S047B": "R 1250 GS Adventure - Edition 40 Years GS",
    "0J71": "R 1250 R",
    "0M71": "R 1250 R",
    "0J81": "R 1250 RS",
    "0M81": "R 1250 RS",
    "0L01": "R 1250 RT",
    "0J61": "R 1250 RT",
    "0M21": "R 1300 GS",
    "0M31": "R 1300 GS Adventure",
    "0M51": "R 1300 R",
    "0M61": "R 1300 RS",
    "0M41": "R 1300 RT",
    "0L11": "R 18 Midnight SE",
    "0N71": "R 18",
    "0L11_S0424": "R 18 100 Years",
    "0L31": "R 18 B",
    "0L21": "R 18 Classic",
    "0N81": "R 18 Classic",
    "0N61": "R 18 Roctane",
    "0N91": "R 18 Roctane",
    "0L41": "R 18 Transcontinental",
    "0L51": "R nineT",
    "0A06": "R nineT",
    "0J01": "R nineT",
    "0L51_S0424": "R nineT 100 Years",
    "0L61": "R nineT Pure",
    "0J11": "R nineT Pure",
    "0M91": "R nineT Pure A2",
    "0J21": "R nineT Racer",
    "0L71": "R nineT Scrambler",
    "0J31": "R nineT Scrambler",
    "0L91": "R nineT Urban G/S",
    "0J41": "R nineT Urban G/S",
    "0L91_S047B": "R nineT Urban G/S - Edition 40 Years GS",
    "0E51": "S 1000 R",
    "0P31": "S 1000 R",
    "0D02": "S 1000 R",
    "0D52": "S 1000 R",
    "0E21": "S 1000 RR",
    "0E61": "S 1000 RR",
    "0P21": "S 1000 RR",
    "0507": "S 1000 RR",
    "0524": "S 1000 RR",
    "0D10": "S 1000 RR",
    "0D50": "S 1000 RR",
    "0E41": "S 1000 XR",
    "0P11": "S 1000 XR",
    "0D03": "S 1000 XR",
    "ZC61": "C 400 GT",
    "ZS01": "C 400 GT",
    "ZS0N": "C 400 GT ion",
    "ZC31": "C 400 X",
    "ZS11": "C 400 X",
    "ZS1N": "C 400 X ion",
    "ZC51": "CE 04",
    "ZC5A": "CE 04 Avantgarde",
    "ZB08": "F 750 GS",
    "ZK51": "F 800 GS",
    "ZK5S": "F 800 GS Sport",
    "ZK5B": "F 800 GS Triple Black",
    "ZB09": "F 850 GS",
    "ZK01": "F 850 GS Adventure",
    "ZK61": "F 900 GS",
    "ZK71": "F 900 GS Adventure",
    "ZK7R": "F 900 GS Adventure RIDE PRO",
    "ZK6E": "F 900 GS Enduro",
    "ZK81": "F 900 R",
    "ZK8S": "F 900 R Sport",
    "ZK8B": "F 900 R Triple Black",
    "ZK21": "F 900 XR",
    "ZR01": "F 900 XR",
    "ZR1S": "F 900 XR Sport",
    "ZR1B": "F 900 XR Triple Black",
    "ZF61": "K 1600 B - Option 719 Midnight",
    "ZF6E": "K 1600 B Exclusive",
    "ZF6C": "K 1600 B Grand America Exclusive",
    "ZF67": "K 1600 B Grand America Option 719",
    "ZF6X": "K 1600 B Option 719",
    "ZF21": "K 1600 GT",
    "ZF27": "K 1600 GT Option 719",
    "ZF2S": "K 1600 GT Sport",
    "ZF31": "K 1600 GTL",
    "ZF3E": "K 1600 GTL Exclusive",
    "ZF37": "K 1600 GTL Option 719",
    "ZF6G": "K 1600 Grand America - Option 719 Midnight",
    "ZP51": "M 1000 R",
    "ZP5C": "M 1000 R Competition",
    "ZE91": "M 1000 XR",
    "ZE9C": "M 1000 XR Competition",
    "ZN51": "R 12",
    "ZN21": "R 12 G/S",
    "ZN2E": "R 12 G/S Enduro",
    "ZN5H": "R 12 HL",
    "ZN57": "R 12 Option 719",
    "ZN01": "R 12 nineT",
    "ZN0H": "R 12 nineT HL",
    "ZN07": "R 12 nineT Option 719",
    "ZM01": "R 1250 GS",
    "ZM11": "R 1250 GS Adventure",
    "ZM14": "R 1250 GS Adventure - Edition 40 Years GS",
    "ZM1R": "R 1250 GS Adventure Rallye",
    "ZM1X": "R 1250 GS Adventure Rallye X",
    "ZM1B": "R 1250 GS Adventure Triple Black",
    "ZM1T": "R 1250 GS Adventure Trophy",
    "ZM1Z": "R 1250 GS Adventure Trophy X",
    "ZM04": "R 1250 GS \u2013 Edition 40 Years GS",
    "ZM71": "R 1250 R",
    "ZM7S": "R 1250 R Sport",
    "ZM7B": "R 1250 R Triple Black",
    "ZM81": "R 1250 RS",
    "ZM8S": "R 1250 RS Sport",
    "ZM8B": "R 1250 RS Triple Black",
    "ZL01": "R 1250 RT",
    "ZL17": "R 1250 RT Option 719",
    "ZL1S": "R 1250 RT Sport",
    "ZL1B": "R 1250 RT Triple Black",
    "ZM21": "R 1300 GS",
    "ZM37": "R 1300 GS Adventure Option 719",
    "ZM3B": "R 1300 GS Adventure Triple Black",
    "ZM3T": "R 1300 GS Adventure Trophy",
    "ZM3X": "R 1300 GS Adventure Trophy X",
    "ZM27": "R 1300 GS Option 719",
    "ZM2P": "R 1300 GS Pure",
    "ZM2B": "R 1300 GS Triple Black",
    "ZM2T": "R 1300 GS Trophy",
    "ZM2X": "R 1300 GS Trophy X",
    "ZM51": "R 1300 R",
    "ZM5E": "R 1300 R Exclusive",
    "ZM57": "R 1300 R Option 719",
    "ZM5P": "R 1300 R Performance",
    "ZM61": "R 1300 RS",
    "ZM67": "R 1300 RS Option 719",
    "ZM6P": "R 1300 RS Performance",
    "ZM6B": "R 1300 RS Triple Black",
    "ZM41": "R 1300 RT",
    "ZM4I": "R 1300 RT Impulse",
    "ZM47": "R 1300 RT Option 719",
    "ZM4B": "R 1300 RT Triple Black",
    "ZL11": "R 18",
    "ZN71": "R 18",
    "ZL1Y": "R 18 100 Year Edition",
    "ZL31": "R 18 B",
    "ZL3B": "R 18 B Blacked Out",
    "ZL3X": "R 18 B Option 719",
    "ZL1Z": "R 18 BL",
    "ZN7B": "R 18 Blacked Out",
    "ZL21": "R 18 Classic",
    "ZN81": "R 18 Classic",
    "ZN8B": "R 18 Classic Blacked Out",
    "ZL2D": "R 18 Classic Deluxe",
    "ZL2H": "R 18 Classic HL",
    "ZL2X": "R 18 Classic Option 719",
    "ZN87": "R 18 Classic Option 719",
    "ZL1D": "R 18 Deluxe",
    "ZL1H": "R 18 HL",
    "ZN77": "R 18 Option 719",
    "ZN61": "R 18 Roctane",
    "ZN6H": "R 18 Roctane HL",
    "ZL4X": "R 18 Transcontinental Option 719",
    "ZL51": "R nineT 100 Year Edition",
    "ZL1X": "R18 Option 719",
    "ZE51": "S 1000 R",
    "ZP31": "S 1000 R",
    "ZE5C": "S 1000 R Clubsport",
    "ZE5M": "S 1000 R M Sport",
    "ZP3M": "S 1000 R M Sport",
    "ZE5R": "S 1000 R Race",
    "ZP3R": "S 1000 R Race",
    "ZE5S": "S 1000 R Sport",
    "ZP3S": "S 1000 R Sport",
    "ZE21": "S 1000 RR",
    "ZE61": "S 1000 RR",
    "ZP21": "S 1000 RR",
    "ZP2M": "S 1000 RR M Sport",
    "ZP2R": "S 1000 RR Race",
    "ZP2S": "S 1000 RR Sport",
    "ZE41": "S 1000 XR",
    "ZP11": "S 1000 XR",
    "ZP1M": "S 1000 XR M Sport",
    "ZP1S": "S 1000 XR Sport"
}

def fetch_soup(url: str):
    response = requests.get(url,timeout=15)
    return BeautifulSoup(response.content, "html.parser", from_encoding='utf-8')

def get_extension(url: str) -> str:
    path = urlparse(url).path
    ext = os.path.splitext(path)[-1]
    return ext if ext else ".jpg"

# ─── Resolve Redirects ────────────────────────────────────────────────────────

def resolve_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=15, allow_redirects=True)
        return response.url
    except requests.RequestException:
        return url

# ─── Build Model Overview URL ─────────────────────────────────────────────────

def build_model_url(country_url: str) -> str:
    parsed = urlparse(country_url)
    lang = parsed.path.split("/")[1]  # e.g. 'en', 'de', 'fr'
    return f"{parsed.scheme}://{parsed.netloc}/{lang}/models/modeloverview.html"


def extract_countries(soup: BeautifulSoup) -> list[dict]:
    locations = []

    parent = soup.select("div.cm-xp-country-selection__country-overview.mnm-country-overview-desktop")
    country_div = parent[1]

    anchor_tags = country_div.select("a.cm-xp-country-selection__country-overview-country-list-item.country-list-item")

    for tag in anchor_tags:
        url = tag.get("href", "")
        locations.append({
            "location": tag.text.strip(),
            "url": url,
        })

    multiDropDownDiv = country_div.select("div.country-list-item.multi")
    
    for country in multiDropDownDiv:
        mainName = country.find('div',class_='cm-xp-country-selection__language-accordion-headline-wrapper').text.strip()
        anchor_tags = country.select("a.cm-xp-country-selection__language-label")
        for tag in anchor_tags:
            url = tag.get("href", "")
            locations.append({
                "location": f"{mainName}-{tag.text.strip()}",
                "url": url,
            })

    for location in locations:
        if location['url'].startswith("/"):
            print(f"Resolving : {location['url']}")
            location['url'] = resolve_url(f"https://www.bmw-motorrad.com{location['url']}")
        else:
            print(f"Current Url : {location['url']}")
    return locations

# ─── Check URL Exists ─────────────────────────────────────────────────────────

def url_exists(url: str) -> bool:
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 405:
            response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


def main():

    print(f"Fetching main page: {BASE_URL}\n")
    soup = fetch_soup(BASE_URL)

    locations = extract_countries(soup)
    print(f"Total locations found: {len(locations)}\n")

    # Direct: valid BMW URLs with no invalid keywords
    direct = [
        i for i in locations
        if not any(keyword in i['url'] for keyword in INVALID_KEYWORDS)
    ]

    # Indirect: everything that didn't pass the direct filter
    indirect = [i for i in locations if i not in direct]

    print(f"Direct: {len(direct)} | Indirect: {len(indirect)}\n")

    for location in direct:
        location['model_url'] = build_model_url(location['url'])
        location['exists'] = url_exists(location['model_url'])
        print(f"{location['model_url']} (Exists: {location['exists']})")

    # Move non-existing URLs from direct to indirect
    indirect += [i for i in direct if not i['exists']]
    direct = [i for i in direct if i['exists']]

    locations = {"direct": direct, "indirect": indirect}
    
    with open("locations.json", "w", encoding="utf-8") as f:
        json.dump(locations, f, indent=4, ensure_ascii=False)
    
    modelList = dict()
    
    for location in locations['direct']:
        print(f"Processing location: {location['location']}")
        soup = fetch_soup(location['model_url'])
        div = soup.find("div", class_="wall__itemsInner")

        currentType = None

        for child in div.find_all("div", recursive=False):
            if "modelcategorywallitem" in child.get('class'):
                currentType = child.text.strip()
            elif "modelfreewallitem" in child.get('class') and child.has_attr("data-model-code"):
                parsed = urlparse(location['model_url'])
                base = f"{parsed.scheme}://{parsed.netloc}"

                img_tag = child.find("div", class_="image-loader")
                img_src = img_tag.get("data-src", "") if img_tag else ""
                img_src = f"{base}{img_src}" if img_src.startswith("/") else img_src

                model_link = child.find("a", class_="wall__item-btn")
                model_link = model_link.get("href", "") if model_link else ""
                model_link = f"{base}{model_link}" if model_link.startswith("/") else model_link

                model_name = child.find("div", class_="wall__item-headline")
                model_name = model_name.text.strip() if model_name else "Unknown"

                model_code = child.get("data-model-code").upper()
                
                newModelName = modelCode.get(model_code,model_name)

                if newModelName not in modelList:
                    modelList[newModelName] = {"segment":currentType,"modelCode":model_code, "locations":[]}

                image_name = f"{model_code.replace(" ","_")}_{location['location'].replace(" ","_")}{get_extension(img_src)}".lower()
                if not os.path.exists(os.path.join(IMAGE_DIR, image_name)):
                    download_image(img_src,image_name)
                modelList[newModelName]['locations'].append({
                    "imgLink": img_src,
                    "modelLink": model_link,
                    "location" : location['location'],
                    "imageName" : image_name
                })
    with open("modelList.json", "w", encoding="utf-8") as f:
        json.dump(modelList, f, indent=4, ensure_ascii=False)
    

if __name__ == "__main__":
    main()