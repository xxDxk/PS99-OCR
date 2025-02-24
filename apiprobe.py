import requests

# API Endpoints
COLLECTION_API_URL = "https://ps99.biggamesapi.io/api/collection/Pets"
EXISTS_API_URL = "https://ps99.biggamesapi.io/api/exists"
RAP_API_URL = "https://ps99.biggamesapi.io/api/rap"

def parse_pet_name(pet_name):
    parts = pet_name.split()
    sh = False
    pt = None
    
    # Check for shiny, golden, or rainbow
    if "Shiny" in parts:
        sh = True
        parts.remove("Shiny")
    if "Golden" in parts:
        pt = 1
        parts.remove("Golden")
    if "Rainbow" in parts:
        pt = 2
        parts.remove("Rainbow")
    
    # Reconstruct the base pet name
    base_name = " ".join(parts)
    
    return base_name, sh, pt

def search_rap_api(base_name, sh, pt):
    # Make the API request
    response = requests.get(RAP_API_URL)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            for item in data.get("data", []):
                if item.get("configData", {}).get("id") == base_name:
                    # For normal pets, ignore sh and pt conditions
                    if pt is None and sh is False:
                        return item
                    # For special pets, check sh and pt
                    elif item.get("configData", {}).get("pt") == pt and item.get("configData", {}).get("sh") == sh:
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
                if item.get("configData", {}).get("id") == base_name:
                    # For normal pets, ignore sh and pt conditions
                    if pt is None and sh is False:
                        return item
                    # For special pets, check sh and pt
                    elif item.get("configData", {}).get("pt") == pt and item.get("configData", {}).get("sh") == sh:
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
