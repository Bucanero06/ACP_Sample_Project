import requests
from pydantic import BaseModel


class FCC_Provider(BaseModel):

    def __init__(self, **data: dict):
        super().__init__(**data)

    @staticmethod
    def check_service_availability(zip_code, street_address):
        NotImplementedError


class ATT_Provider(FCC_Provider):

    @staticmethod
    def check_service_availability(zip_code, street_address):
        base_url = "https://www.att.com/services/shop/model/ecom/shop/view/unified/qualification/service/CheckAvailabilityRESTService/invokeCheckAvailability"

        headers = {
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Content-Type": "Application/Json"
        }

        params = {
            "userInputZip": zip_code,
            "userInputAddressLine1": street_address,
            "mode": "fullAddress"  # other options are "zip" and "street"
        }

        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        response_json = response.json()

        # Extract the needed information
        profile = response_json.get("profile", {})
        light_speed_pending = profile.get("LIGHTSPEEDPending", False)
        is_uverse_available = profile.get("isUverseAvailable", False)
        is_giga_fiber_available = profile.get("isGIGAFiberAvailable", False)

        print(f'{profile = }')
        print(f'{light_speed_pending = }')
        print(f'{is_giga_fiber_available = }')
        print(f'{is_uverse_available = }')

        return is_giga_fiber_available


def check_available_providers_in_area(zip_code: str):
    import requests
    from bs4 import BeautifulSoup  # If you need to parse HTML

    base_url = "https://broadbandnow.com/api/broadband/providers"

    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
    }

    params = {
        "zip": zip_code
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        print(f'{response.status_code = }')

        # Check if the response header indicates JSON content
        if 'application/json' in response.headers.get('Content-Type', ''):
            data = response.json()
            # Process JSON data
        else:
            # If the content is HTML, parse with Beautiful Soup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract and process information from the HTML
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6+
    except Exception as err:
        print(f"An error occurred: {err}")

    # Navigate to the 'cityProvidersListing' section
    providers_section = soup.find('section', id='cityProvidersListing')

    # Extract all provider items
    providers_html = providers_section.find_all('div', class_='f-provider-card')

    # Loop through each provider and extract desired information
    output_providers_obj = {}
    for provider in providers_html:
        # Extracting provider name
        provider_name = provider.find('span', class_='f-provider-card__provider-name').text.strip()

        output_providers_obj[provider_name] = {
            'speeds_up_to': provider.find('strong', class_='f-provider-card__speeds-value').text.strip(),
            'connection_type': provider.find('span', class_='f-provider-card__connection-value').text.strip(),
            'availability': provider.find('span', class_='f-provider-card__connection-value').text.strip()
        }

        # Print the extracted data
        print(f"Provider Name: {provider_name}")
        print(f"Speeds Up To: {output_providers_obj[provider_name]['speeds_up_to']}")
        print(f"Connection Type: {output_providers_obj[provider_name]['connection_type']}")
        print(f"Availability: {output_providers_obj[provider_name]['availability']}")
        print("----------")

    return output_providers_obj


def get_matched_providers(providers_data):
    """Returns matched providers that we work with."""
    matched_providers = []
    for provider in providers_data:
        if provider in PROVIDERS_NAME_MAPPING:
            matched_providers.append(PROVIDERS_NAME_MAPPING[provider])
        elif provider in PROVIDERS_WE_WORK_WITH:
            matched_providers.append(PROVIDERS_WE_WORK_WITH[provider])

    # Here, if there are any biases (e.g., prefer one provider over another) you would adjust the order of the matched_providers list.
    # For now, I'm just returning it as is.

    return matched_providers
