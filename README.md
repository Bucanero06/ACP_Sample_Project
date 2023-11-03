(*disclaimer: this should not be treated as a typical public repository, it is specific to the work related to MetConnect's and Carbonyl R&D communications but is here nonetheless as publicly available information for whom it may serve*)
# Providers Serviceability MVP Report
To follow MetConnects protocol as close as possible this is a sample solution until the nessesary 
steps are taken to meet the FCC and USAC databases and security policies.

## Sample MVP solution based on current MetConnect methodology (i.e. not api based)
Below is a working example with ATT as the implemented provider. Should take the process down to under 3 seconds without
any asynchronous or optimization techniques.

//-> *BrooadbandNow* -> *MetConnect-Providers-Check* -> *Providers(website scraped)-Check* ->//

```python
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
```

an example output of the above code would be:
```
response.status_code = 200

Available Providers in 32825:
   ----------
   Provider Name: AT&T Internet
   Speeds Up To: 5 Gbps
   Connection Type: IPBB, Fiber
   Availability: IPBB, Fiber
   ----------
   Provider Name: Spectrum
   Speeds Up To: 1 Gbps
   Connection Type: Cable
   Availability: Cable
   ----------
   Provider Name: Xfinity
   Speeds Up To: 1.2 Gbps
   Connection Type: Cable
   Availability: Cable
   ----------
   Provider Name: Viasat
   Speeds Up To: 150 Mbps
   Connection Type: Satellite
   Availability: Satellite
   ----------
   Provider Name: HughesNet
   Speeds Up To: 25 Mbps
   Connection Type: Satellite
   Availability: Satellite
   ----------
   Provider Name: Always ON
   Speeds Up To: 25 - 150 Mbps
   Connection Type: Fixed Wireless
   Availability: Fixed Wireless
   ----------
   Provider Name: Verizon
   Speeds Up To: 300 Mbps
   Connection Type: 5G Internet
   Availability: 5G Internet
   ----------
   Provider Name: Starlink
   Speeds Up To: 50 - 220 Mbps
   Connection Type: Satellite
   Availability: Satellite
   ----------
   Provider Name: T-Mobile 5G Home Internet
   Speeds Up To: 33 - 245 Mbps
   Connection Type: 5G Internet
   Availability: 5G Internet
   ----------
   
Providers in Customers Area: {'AT&T Internet': {'speeds_up_to': '5 Gbps', 'connection_type': 'IPBB, Fiber', 'availability': 'IPBB, Fiber'}, 'Spectrum': {'speeds_up_to': '1 Gbps', 'connection_type': 'Cable', 'availability': 'Cable'}, 'Xfinity': {'speeds_up_to': '1.2 Gbps', 'connection_type': 'Cable', 'availability': 'Cable'}, 'Viasat': {'speeds_up_to': '150 Mbps', 'connection_type': 'Satellite', 'availability': 'Satellite'}, 'HughesNet': {'speeds_up_to': '25 Mbps', 'connection_type': 'Satellite', 'availability': 'Satellite'}, 'Always ON': {'speeds_up_to': '25 - 150 Mbps', 'connection_type': 'Fixed Wireless', 'availability': 'Fixed Wireless'}, 'Verizon': {'speeds_up_to': '300 Mbps', 'connection_type': '5G Internet', 'availability': '5G Internet'}, 'Starlink': {'speeds_up_to': '50 - 220 Mbps', 'connection_type': 'Satellite', 'availability': 'Satellite'}, 'T-Mobile 5G Home Internet': {'speeds_up_to': '33 - 245 Mbps', 'connection_type': '5G Internet', 'availability': '5G Internet'}}
Matched Providers: [<class '__main__.ATT_Provider'>] # There would be more providers here if they were implemented
Checking ATT_Provider service availability...
profile = {'LIGHTSPEEDPending': False, 'isUverseAvailable': False, 'isGIGAFiberAvailable': False, 'zipCode': None, 'customerSubType': 'residential', 'city': None, 'isVOIPAvailable': False, 'wirelessHomePhoneEligible': False, 'addressId': None, 'isIPDSLAM': False, 'customerType': 'Consumer', 'LIGHTSPEEDExists': False, 'maskServiceAddress': None, 'zipExtension': None, 'addressLine1': None, 'addressLine2': None, 'state': None, 'isIPTVAvailable': False, 'isHSIAAvailable': False, 'isDTVAvailable': False, 'ATTEmployeeId': None, 'migrationTargetIdentifier': None, 'referralAppId': None, 'fccWireCenterStatus': None, 'isCheckAvailabilityPerformed': False, 'isPOTSAvailable': False, 'isWirelessAvailable': False, 'dma': None, 'isFBSAvailable': False, 'isDSLAvailable': False, 'employeeSegment': None, 'wireCenterCode': None, 'isFWIAvailable': False}
   
   light_speed_pending = False
   is_giga_fiber_available = False
   is_uverse_available = False
   
```
## Whats the problem?
The problem is that the current MetConnect methodology is not scalable, likely to to get IP-Blocked when automating
this way, security and maintainibility are a nightmare specially as the government website transition to more 
preventative measures. 

On top of waiting for likely breaking changes to occur across all the parties involved, checking the availability of service providers in MetConnect currently takes the form of two options:
    
   1. FIND OUT WHAT PROVIDERS ARE AVAILABLE IN YOUR CUSTOMERS ZIP CODE USING BROADBAND NOW
        a. Is not always accurate and can be misleading. Only works based on zipcode so further verification of
            providers tends to be a most.


   2. FIND OUT WHAT PROVIDERS ARE AVAILABLE USING THE FCC BROADBAND MAP
        a. mapping platform has become dated, as has the coverage data, which was collected through the National
        Telecommunications and Information Administration’s (NTIA) State Broadband Initiative (SBI); the last published
        SBI data set was current as of June 30, 2014.  Based on the age of the data, and the underlying technology, the
        National Broadband Map and its Application Program Interface (API), will be decommissioned on December 21, 2018.

Metadata updates have occured as recent as 2021 but the data is still however in the next sections an overview of the
ACP processes is broken into sections to aid in our understanding as well as MetConnects. Useful links with further 
information are embedded in the text, deciding to follow more closely the Service Providers, NLAD 
(National Lifeline Accountability Database) and USAC's sections of the ACP available knowledgebase.

## Application Development and Maintenance Best Practices 
i.e. Things to keep in mind which go into a project but don't tend to be discussed when creating solutions under and MVP
mentality (NLAD as an example).

[National-Verifier-Pre-Production-User-Guide.pdf](National-Verifier-Pre-Production-User-Guide.pdf)

[NLAD-Pre-Production-Guide-Testing-RAD-with-Individual-User-Accounts.pdf](NLAD-Pre-Production-Guide-Testing-RAD-with-Individual-User-Accounts.pdf)

[Lifeline-and-Affordable-Connectivity-Program-Interconnection-Security-Agreement.docx.pdf](Lifeline-and-Affordable-Connectivity-Program-Interconnection-Security-Agreement.docx.pdf)

[Universal Service Administrative Company.pdf](..%2F..%2F..%2FDownloads%2FUniversal%20Service%20Administrative%20Company.pdf)
1. **Backup and Redundancy**: Ensure you have a backup plan if there are delays in getting access or if there are issues with the staging environment. Always have contingency plans.

2. **Feedback Loop**: After you review the API documentation and start development, it might be helpful to maintain a feedback loop with the National Verifier support team. They could provide clarifications on ambiguous parts of the documentation or specific use cases.

3. **Security**: Ensure that the application you develop is secure, especially when dealing with personal information and API authentication. Consider regular security audits.

4. **Error Handling**: Make sure your application has robust error handling, especially for the API calls. This includes not just technical errors, but also user errors (like entering incorrect data).

5. **Documentation for Users**: As you develop the application, ensure you have clear documentation for the end-users. This could be in the form of FAQs, user manuals, or even video tutorials.

6. **Regular Updates**: Ensure that you regularly check for updates to the National Verifier's API. APIs can change, and you'll want to ensure compatibility.

7. **Stress Testing**: Before deploying, it might be a good idea to stress-test your application. This will help you identify how it performs under heavy loads or traffic.

8. **Feedback Collection Post-Deployment**: After deploying your application, collect feedback from the users to understand any potential pain points or areas of improvement.

9. **Stay Compliant**: Ensure that you're always compliant with any legal or regulatory requirements, especially concerning data privacy.

10. **Ongoing Communication**: Stay in regular communication with the National Verifier support team, even post-deployment, to be updated on any changes, enhancements, or potential issues.




# ACP Processes Report
The Affordable Connectivity Program uses the National Eligibility Verifier (National Verifier), the National Lifeline Accountability Database (NLAD), and the Lifeline Claims System (LCS) for consumer eligibility, enrollment, and service provider reimbursement. As these systems are adapted to meet the requirements of the ACP, USAC will update these pages with additional information.

* Use the National Verifier to [check consumer eligibility](https://www.usac.org/about/affordable-connectivity-program/acp-processes/check-consumer-eligibility/)
* Use the NLAD to [enroll subscribers](https://www.usac.org/about/affordable-connectivity-program/acp-processes/manage-acp-subscribers/common-transactions-in-nlad/)
* Use the Affordable Connectivity Claims System ([ACCS](https://www.usac.org/about/affordable-connectivity-program/acp-processes/file-acp-reimbursement-claims/)) to seek reimbursement

## Service Provider Participation
Broadband service providers, including providers that have not been designated as eligible telecommunications carriers 
(ETCs), are able to participate in the ACP.

To participate, service providers must obtain an FCC Registration Number (FRN) through the Commission Registration 
System (CORES), register with the System for Award Management ([SAM](https://sam.gov/SAM/)), and cannot be listed on the Treasury Do Not Pay 
List. Non-ETCs must receive FCC approval to participate in the program prior to filing an Election Notice with USAC.

ACP service providers will use the National Verifier to check consumer eligibility, NLAD to enroll subscribers, and 
ACCS to submit reimbursement requests. In order to perform subscriber transactions in the National Verifier or NLAD, 
service provider representatives must register for a Representative ID (Rep ID) in the Representative Accountability 
Database (RAD).

Providers with existing low-income programs can seek FCC approval to use an alternative eligibility verification 
process. Once a service provider has completed all of the initial registration steps, USAC will create system access 
for all of the necessary systems. Visit the USAC's Get Started page for more information. In addition, check out the NLAD or 
National Verifier staging environments to practice performing system transactions.

## API Access to USAC Systems
If your company intends to utilize an Application Programming Interface (API) to access either the National Verifier or 
the National Lifeline Accountability Database (NLAD) for the ACP, please complete and sign the 
[ISA](https://www.usac.org/wp-content/uploads/about/documents/acp/Lifeline-and-Affordable-Connectivity-Program-Interconnection-Security-Agreement.docx) and include it with 
your election notice for the ACP.

## System Updates
USAC provides ACP updates via email bulletins. To receive ACP email outreach, please sign up. Find past ACP bulletins 
on the Learn page.

USAC has published a list of known system issues to help service providers who are working in the ACP systems.

# Check Consumer Eligibility

The National Eligibility Verifier (National Verifier) is the ACP’s centralized application system. Service Providers can use the National Verifier to determine whether consumers are eligible for the ACP. USAC manages the National Verifier and provides customer service to consumers through the ACP Support Center.

## How It Works
Consumers have three ways to apply using the National Verifier:

* Online: Visit the ACP’s [consumer website](https://affordableconnectivity.gov/) and click the “Apply Now” button
* By mail: Fill out a [paper application](https://www.affordableconnectivity.gov/wp-content/uploads/ACP-Application-Form-English.pdf) and send it, along with copies of their [eligibility documents](https://www.usac.org/about/affordable-connectivity-program/application-and-eligibility-resources/application-documents/), to the ACP Support Center; or
* With the help of a service provider using the National Verifier [service provider portal of National Verifier carrier API](https://nationalverifier.servicenowservices.com/lifeline)

In each method, the consumer will enter their name, date of birth, address, phone and email (email is optional), and select how they want to prove their identity.

If the consumer is qualifying through a benefit qualifying person (BQP), they will enter the BQP’s name, date of birth, and select how they want to prove the BQP’s identity.

The consumer will then choose from the list of [qualifying programs](https://www.usac.org/about/affordable-connectivity-program/application-and-eligibility-resources/how-to-prove-participation/) or indicate that they [qualify by income](https://www.usac.org/about/affordable-connectivity-program/application-and-eligibility-resources/how-to-prove-income/).

The consumer completes the application by initialing a series of program certifications, signing, and dating the application.

If a service provider helps a consumer apply, the service provider should use an interview style approach to complete the consumer information section. Consumers must initial the certifications and sign and date the form themselves – the service provider cannot do this on their behalf.

The National Verifier will check the consumer’s identity and eligibility against available state, federal, and other electronic [databases](https://www.usac.org/about/affordable-connectivity-program/acp-processes/check-consumer-eligibility/database-connections/). If the consumer is found eligible, the service provider can enroll them in the ACP. If the consumer’s identity and eligibility cannot be validated through the electronic checks, the National Verifier will provide information on the documentation needed to resolve any errors.

## National Verifier Staging Site
To practice conducting eligibility checks and document upload processes, service providers can use the [National Verifier staging site](https://nationalverifiertraining.servicenowservices.com/lifeline). Visit our [staging site page](https://forms.universalservice.org/portal/login) to learn more about the staging site and how to access and use it.

# Manage ACP Subscribers
The National Lifeline Accountability Database (NLAD) allows service providers to manage the enrollment of their Affordable Connectivity Program (ACP) subscribers. It works in conjunction with the National Verifier and service providers’ approved alternative verification processes: consumers apply to the ACP through the National Verifier or their provider, and their service provider enrolls them in NLAD.

Service providers must enroll subscribers in NLAD to claim reimbursements.

## How to Use NLAD
Like many of the ACP systems, NLAD is a Lifeline system that USAC has expanded to administer the ACP. To learn more about the basics of using NLAD, as well as how to use it for the ACP, please refer to these pages:

* [NLAD User Accounts](https://www.usac.org/about/affordable-connectivity-program/acp-processes/manage-acp-subscribers/nlad-user-accounts/)
* [Common Transactions in NLAD](https://www.usac.org/about/affordable-connectivity-program/acp-processes/manage-acp-subscribers/common-transactions-in-nlad/)
* [NLAD Staging Environment](https://www.usac.org/about/affordable-connectivity-program/acp-processes/manage-acp-subscribers/nlad-staging-environment/)
* [Enroll Consumers Using the Batch Upload Template](https://www.usac.org/about/affordable-connectivity-program/acp-processes/manage-acp-subscribers/enroll-consumers-using-the-batch-template/)

## Keep NLAD Up-to-Date
NLAD confirms that a customer has qualified through the National Verifier (unless the customer was enrolled through an approved alternative verification process) and prevents subscribers form claiming more than one ACP discount. Service providers cannot claim reimbursement for a subscriber unless they are entered in NLAD at the time of the monthly snapshot. Please update NLAD every time a subscriber’s status changes, including changes to their information (for example, a change of address) within ten (10) business days.

When a service provider de-enrolls a subscribers from the ACP, they must update NLAD within one (1) business day.

## Learn More
Beyond the NLAD resources in the ACP pages, you can also:

Visit the NLAD pages on the Lifeline section of the USAC website, which include general NLAD Resources, FAQs, and a maintenance schedule,
Sign up to receive system maintenance notices by selecting “NLAD Bulletin” in the USAC subscription center.

# File ACP Reimbursement Claims

Additional Resources:
* [Claims Input Template Sample](https://www.usac.org/wp-content/uploads/about/documents/acp/Claims_Input_Template.csv)
* [Error Descriptions List](https://www.usac.org/wp-content/uploads/about/documents/ACCS-Error-Descriptions.docx)
* [USAC Webinar (slides)](https://www.usac.org/wp-content/uploads/about/documents/acp/Training-Slides/ACP-Claims_April-21.pdf)

The Affordable Connectivity Program (ACP) launched on December 31, 2021. It is a modification and extension of the Emergency Broadband Benefit (EBB) Program.  Providers must use the ACP Program Claims Process to file reimbursement claims for both legacy EBB subscribers and ACP subscribers. The ACP Claims Process is built on the Lifeline Claims System. Service providers can access the claims process through the USAC OnePortal.

On the first of the month, USAC takes a snapshot of all subscribers entered in the [National Lifeline Accountability Database (NLAD)](https://www.usac.org/about/affordable-connectivity-program/acp-processes/manage-acp-subscribers/common-transactions-in-nlad/). Consumers who have not been entered in NLAD when the snapshot is taken are not eligible for reimbursement for the corresponding data month. Subscribers should only be claimed if they are receiving ACP service (e.g., subscribers who have enrolled but have not started receiving service are not eligible to be claimed). Until the new non-usage rules take effect, consumers must receive and use service in the data month to be claimed for reimbursement if they are not assessed and do not pay a fee for their ACP service.

Service providers have up to six months to submit original claims or upward revisions of previous claims. (There is no time restriction on downward revisions.) Revisions can be made starting with the March 2022 data month (January and February 2022 are not eligible for revisions.) However, if the provider would like to be reimbursed in the snapshot month (i.e. receive reimbursement in April 2022 for the April 1st snapshot, which is the March 2022 data month), they need to certify their claims by the 15th of the snapshot month. If the 15th of the month falls on a weekend or holiday, service providers can certify on the first business day following the 15th.

To complete ACP reimbursement claims, a service provider’s [497 Officer or 497 User*](https://www.usac.org/about/affordable-connectivity-program/acp-processes/manage-acp-subscribers/nlad-user-accounts/) will follow the process below on or after the first of the month. For further context, download our Claims Input Template Sample and the Error Descriptions List.

1. Select the ACP File or Revise Claim in the Claims System and choose the correct data month and year. Select “Original” in the Filing type.
   * Download the list of subscribers eligible for reimbursement.
   * The list is a report in the ACP Claims Process based on the NLAD “Subscriber Snapshot” report.
2. Review the list of all subscribers available for reimbursement claims and modify the appropriate data on the list as needed.
   * Add the dollar amount claimed for each subscriber on the report (the system automatically defaults to the value from the prior month).
   * The support amount claimed cannot be more than the actual discount provided to the ACP subscriber in the relevant service month, and the ACP support must be fully passed through to the consumer in the form of a discount.
   * Add the dollar amount for the device claim (if appropriate). Service providers must subtract the household co-pay from the device claim.
   * Indicate which subscribers are not being claimed and why (using the appropriate reason code).
3. Upload the report back into the ACP Claims Process and review the information to ensure the system data matches your company data.
4. Set the claim as “ready to certify” and complete your contact information in case USAC has questions about the claim. Submit the claim.

Once the claim is ready to certify, the 497 Officer must:
1. Select ACP Certify Claim in the ACP Claims Process and select the correct data month and year. Confirm that the data uploaded is correct and ready to be certified. 497 Officers can review the claim using the “View” link in the Support Details column.
2. Select all the claims to be certified using the check box on the left-hand side of the screen. To certify all available claims, check “Select All”.
3. Review and sign the ACP certifications.
4. Select the blue button to certify claims. When the claims are successfully submitted, the 497 Officer will receive a green success message. Review to ensure the number of claims submitted matches the number the company planned to submit.
* Non-Lifeline ETC participating in the ACP should email ACProgram@USAC.org to create a 497 User role. All other service providers can create this user role in NLAD.

## ACP Claims & Reimbursement FAQ

### ACP Discounts and Lifeline Discounts: Can I apply the ACP discount to a top-up for my Lifeline-supported service? Can a provider be reimbursed through the ACP for a discount applied to a top-up of a household’s Lifeline service?

Pursuant to the FCC’s 2022 Affordable Connectivity Program Report and Order (ACP Order), eligible households may receive both the Lifeline and ACP discounts and can apply both benefits to their qualifying broadband service. The full Lifeline discount must be applied first to the standard rate for the ACP offering.  The ACP discount can then be applied to the remaining amount.  Providers cannot apply the ACP support to a separate service offered by the provider as a “top-up” on an existing customer’s service plan.  Providers are also reminded that the ACP discount cannot be applied to a service plan that is already offered with no fee to the end-user as a result of Lifeline program support or other benefit programs.

Households can receive a Lifeline-supported service and a separate ACP-supported service from the same provider as long as the services are eligible for the benefit that is applied to the service.


### How should a provider account for households that were not served for the entire month when submitting a reimbursement claim in the Affordable Connectivity Claims System?

On the first day of each month, USAC will create a snapshot of each ACP provider’s currently enrolled subscribers, including ACP households enrolled in NLAD since the last snapshot was taken.  Each provider will have until the 15th of the month, or the next business day, to select the households they would like to claim for reimbursement.  This process will include indicating the amount for reimbursement, which should equal the ACP discount provided to that household for the service month.  The amount of the ACP reimbursement cannot exceed the amount of the ACP discount that was passed through to the ACP subscriber, up to $30 per month (or $75 per month for residents of qualifying Tribal lands).  If a provider prorates its standard rate for subscribers who enrolled in the middle of a month, the ACP reimbursement is not necessarily prorated as well, but the ACP reimbursement cannot exceed the ACP discount that the provider actually passed through to the consumer for that month.  So, if the prorated price of the service is less than $30 for that month, then the provider must ensure it is not claiming reimbursement for more than the price of the service in that month.

For households that a provider claimed in the previous month, the snapshot report will automatically pre-populate the amount the provider claimed for the household in the previous month. Providers should review the snapshot report closely and verify that the amount pre-populated for the current month is accurate.  For example, if a household received a higher ACP discount in the current month because the prior month’s discount was for a partial month of service, the provider should update the amount to reflect the actual discount passed to the household in the current month.

USAC does not prorate or adjust reimbursement amounts. It is the responsibility of the provider to input the amount equal to the discount passed to the subscriber in the service month.

### What are the deadlines for submitting reimbursement claims in the Affordable Connectivity Claims System?
Service providers have up to six months to submit original claims or upward revisions of previous claims. (There is no time restriction on downward revisions.) Revisions can be made starting with the March 2022 data month (January and February 2022 are not eligible for revisions.) However, if the provider would like to be reimbursed in the snapshot month (i.e. receive reimbursement in April 2022 for the April 1st snapshot, which is the March 2022 data month), they need to certify their claims by the 15th of the snapshot month. If the 15th of the month falls on a weekend or holiday, service providers can certify on the first business day following the 15th.

### How can a provider determine the correct amount to seek reimbursement for?
USAC understands that providers may have billing cycles that do not align with the calendar month. For purposes of ACP reimbursement, providers should claim the discount associated with the given service month, even if that amount has not been invoiced yet. For example, assume a subscriber began a $20 ACP service plan on May 25 and the provider enrolled the subscriber in NLAD the same day. The provider’s billing cycle runs from the 15th to the 15th of the following month. On the June 1 snapshot, the provider may only claim the discount actually associated with the service provided in May, which would likely be less than $20 due to the late-in-the-month enrollment if the provider prorates its pricing for service only provided for part of the month. On the July 1 snapshot, the provider would claim the full $20 discount for the June service month, as long as that entire discount was passed through to the household.

Providers cannot claim an ACP household for reimbursement if that household transferred or was de-enrolled during the service month and did not appear on the snapshot report for that month. For example, if an ACP household transferred to another provider on June 15, they will not appear on the original provider’s July 1 snapshot and therefore cannot be claimed for reimbursement. The new provider, however, will be able to claim the subscriber for reimbursement for the discounts provided in the month of June.

### What is the support amount?

ACP consumers can receive reimbursement up to $30. Consumers living on Tribal lands are eligible for reimbursement for up to $75.

## Plan of action acquiring access and API documentation (in case this 
To get access and API documentation to create your consumer and business-facing applications, these are the steps:

1. Visit the National Verifier staging site.

2. Request access to the staging site by contacting the National Verifier support team. You can reach out to them at *ACPinfo@fcc.gov* and include your name, organization or institution, email, and phone contact.

3. Once your request is approved, you will receive login credentials to access the staging site.

4. Use the provided login credentials to log in to the staging site.

5. Once logged in, you will have access to the API documentation, which provides information on how to integrate your application with the National Verifier.

6. Review the API documentation to understand the available endpoints, request/response formats, and authentication methods.

7. If your company plans to use an API to access the National Verifier or NLAD for the ACP, complete and sign the Interconnection Security Agreement (ISA) and include it with your ACP election notice.

8. Use the API documentation to develop and test your consumer and business-facing application, ensuring that it meets the requirements and guidelines provided.

9. Stay informed about ACP developments through USAC's email bulletins and sign up to receive ACP email outreach.

10. Test your application thoroughly to ensure it functions correctly and meets the necessary requirements to be deployed for consumer and business use.




