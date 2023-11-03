"""

Checking the availability of service providers in MetConnect currently takes the form of two options:
    1. FIND OUT WHAT PROVIDERS ARE AVAILABLE IN YOUR CUSTOMERS ZIP CODE USING BROADBAND NOW
        a. Is not always accurate and can be misleading. Only works based on zipcode so further verification of
            providers tends to be a most.
    2. FIND OUT WHAT PROVIDERS ARE AVAILABLE USING THE FCC BROADBAND MAP
        a. mapping platform has become dated, as has the coverage data, which was collected through the National
        Telecommunications and Information Administration’s (NTIA) State Broadband Initiative (SBI); the last published
        SBI data set was current as of June 30, 2014.  Based on the age of the data, and the underlying technology, the
        National Broadband Map and its Application Program Interface (API), will be decommissioned on December 21, 2018.

To follow this protocol as close as possible this is a sample solution until the nessesary hoops are jumped through
    with the FCC and USAC.

"""
from ACP_Sample_Project.check_available_providers_supporting_functions import get_matched_providers, FCC_Provider, \
    check_available_providers_in_area

# Check this zip code for Available Providers
ZIP_CODE = '32825'
# Check this street address for Service Availability
STREET_ADDRESS = '12000 Fountainbrook Blvd'

'''Step 1: Find out what providers are available in your customers zip code'''

providers_in_customers_area = check_available_providers_in_area(zip_code=ZIP_CODE)
print("Providers in Customers Area:", providers_in_customers_area)

'''Match the providers you work with with the providers available in the customers zip code and return as a list ordered 
by biases'''
matched_providers_list = get_matched_providers(providers_in_customers_area.keys())
print("Matched Providers:", [provider for provider in matched_providers_list])

'''Check the websites of the providers to see if they exact customers address is serviceable'''
for provider in matched_providers_list:
    provider = provider()
    print(f"Checking {provider.__class__.__name__} service availability...")
    # If is a FCC_Provider then use the appropriate method to check service availability of that specific provider
    if isinstance(provider, FCC_Provider):
        provider.check_service_availability(zip_code=ZIP_CODE, street_address=STREET_ADDRESS)
    else:
        # These arent implemented yet
        NotImplementedError
