import requests

# API Endpoints
COLLECTION_API_URL = "https://ps99.biggamesapi.io/api/collection/Pets"
EXISTS_API_URL = "https://ps99.biggamesapi.io/api/exists"
RAP_API_URL = "https://ps99.biggamesapi.io/api/rap"

def capitalize_pet_name(pet_name):
    """Capitalize the first letter of each word in the pet name."""
    return " ".join(word.capitalize() for word in pet_name.split())

def parse_pet_name(pet_name):
    parts = pet_name.lower().split()  # Convert input to lowercase for case-insensitive parsing
    sh = False
    pt = None
    
    # Check for shiny, golden, or rainbow
    if "shiny" in parts:
        sh = True
        parts.remove("shiny")
    if "golden" in parts:
        pt = 1
        parts.remove("golden")
    if "rainbow" in parts:
        pt = 2
        parts.remove("rainbow")
    
    # Reconstruct the base pet name and capitalize it
    base_name = capitalize_pet_name(" ".join(parts))
    
    return base_name, sh, pt

def search_rap_api(base_name, sh, pt):
    # Make the API request
    response = requests.get(RAP_API_URL)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            for item in data.get("data", []):
                config_data = item.get("configData", {})
                if config_data.get("id") == base_name:
                    # Check conditions based on pt and sh
                    if pt is None and not sh:  # Normal pet
                        if "pt" not in config_data and "sh" not in config_data:
                            return item
                    elif pt is not None and sh:  # Golden Shiny or Rainbow Shiny
                        if config_data.get("pt") == pt and config_data.get("sh") == sh:
                            return item
                    elif pt is not None and not sh:  # Golden or Rainbow
                        if config_data.get("pt") == pt and "sh" not in config_data:
                            return item
                    elif pt is None and sh:  # Shiny only
                        if config_data.get("sh") == sh and "pt" not in config_data:
                            return item
    else:
        print(f"Error searching RAP API: {response.status_code}")
    return None

def search_exist_api(base_name, sh, pt):
    # Make the API request
    response = requests.get(EXISTS_API_URL)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            for item in data.get("data", []):
                config_data = item.get("configData", {})
                if config_data.get("id") == base_name:
                    # Check conditions based on pt and sh
                    if pt is None and not sh:  # Normal pet
                        if "pt" not in config_data and "sh" not in config_data:
                            return item
                    elif pt is not None and sh:  # Golden Shiny or Rainbow Shiny
                        if config_data.get("pt") == pt and config_data.get("sh") == sh:
                            return item
                    elif pt is not None and not sh:  # Golden or Rainbow
                        if config_data.get("pt") == pt and "sh" not in config_data:
                            return item
                    elif pt is None and sh:  # Shiny only
                        if config_data.get("sh") == sh and "pt" not in config_data:
                            return item
    else:
        print(f"Error searching Exist API: {response.status_code}")
    return None

def search_collection_api(base_name):
    # Make the API request
    response = requests.get(COLLECTION_API_URL)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            for pet in data.get("data", []):
                if pet.get("configName") == base_name:
                    return pet
    else:
        print(f"Error searching Collection API: {response.status_code}")
    return None

def main():
    pet_name = input("Enter the pet name: ")
    base_name, sh, pt = parse_pet_name(pet_name)
    
    print("\nParsed Pet Details:")
    print(f"Base Name: {base_name}")
    print(f"Shiny: {sh}")
    print(f"Type (pt): {pt}")
    
    # Search RAP API
    rap_result = search_rap_api(base_name, sh, pt)
    if rap_result:
        print("\nRAP API Result:")
        print(f"Value: {rap_result.get('value', 'N/A')}")
    else:
        print("\nRAP API: No matching pet found.")
    
    # Search Exist API
    exist_result = search_exist_api(base_name, sh, pt)
    if exist_result:
        print("\nExist API Result:")
        print(f"Value: {exist_result.get('value', 'N/A')}")
    else:
        print("\nExist API: No matching pet found.")
    
    # Search Collection API
    collection_result = search_collection_api(base_name)
    if collection_result:
        print("\nCollection API Result:")
        print(f"Description: {collection_result['configData']['indexDesc']}")
        thumbnail_id = collection_result["configData"]["thumbnail"].split("//")[1]
        print(f"Thumbnail URL: https://ps99.biggamesapi.io/image/{thumbnail_id}")
    else:
        print("\nCollection API: No matching pet found.")

if __name__ == "__main__":
    main()
