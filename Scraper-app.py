import re
import phonenumbers
import requests
import streamlit as st
import pandas as pd
import neattext.functions as nfx
import base64
import time
import random

import aiohttp
import asyncio

# from bs4 import BeautifulSoup

# User-Agent Rotation
user_agents = [
    # Chrome User Agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",

    # Firefox User Agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0",

    # Safari User Agents
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A5341f Safari/604.1",

    # Edge User Agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.54",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.45",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63",

    # Opera User Agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.254",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.177",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 OPR/76.0.4017.94",
    
    # Mobile User Agents
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A705FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36"
]


# Expanded country codes list
countries_list = [
    "US", "IN", "GB", "AU", "CA", "DE", "FR", "ZA", "AF", "AL", "DZ", "AO", "AR", "AM", "AT", "AZ",
    "BD", "BE", "BJ", "BO", "BR", "BG", "KH", "CM", "CL", "CN", "CO", "CR", "HR", "CU", "CY", "CZ",
    "DK", "DO", "EC", "EG", "SV", "EE", "ET", "FI", "GE", "GH", "GR", "GT", "HN", "HK", "HU", "ID",
    "IR", "IQ", "IE", "IL", "IT", "JM", "JP", "JO", "KZ", "KE", "KR", "KW", "KG", "LA", "LV", "LB",
    "LY", "LT", "LU", "MG", "MY", "MV", "ML", "MT", "MX", "MD", "MN", "ME", "MA", "MM", "NP", "NL",
    "NZ", "NI", "NG", "NO", "OM", "PK", "PA", "PY", "PE", "PH", "PL", "PT", "QA", "RO", "RU", "SA",
    "RS", "SG", "SK", "SI", "ES", "LK", "SD", "SE", "CH", "SY", "TW", "TJ", "TH", "TN", "TR", "UA",
    "AE", "UY", "UZ", "VE", "VN", "YE", "ZM", "ZW"
]

# Expanded email extensions list
email_extensions_list = [
    "gmail.com", "yahoo.com", "hotmail.com", "icloud.com", "aol.com", "yandex.com", "outlook.com",
    "live.com", "protonmail.com", "mail.com", "zoho.com", "gmx.com", "inbox.com", "rediffmail.com",
    "fastmail.com", "yahoo.co.uk", "yahoo.fr", "orange.fr", "comcast.net", "yahoo.co.in", "free.fr",
    "gmx.de", "web.de", "libero.it", "yahoo.co.jp", "yahoo.de", "btinternet.com", "cox.net",
    "hotmail.it", "sbcglobal.net", "wanadoo.fr", "live.co.uk", "yahoo.es", "bell.net", "verizon.net",
    "sky.com", "earthlink.net", "optonline.net", "freenet.de", "t-online.de", "aliceadsl.fr",
    "virgilio.it", "bigpond.com", "blueyonder.co.uk", "bluewin.ch", "skynet.be", "sympatico.ca",
    "windstream.net", "mac.com", "centurytel.net", "chello.nl", "live.ca", "bigpond.com.au"
]

# Function to clean emails
def clean_emails(emails):
    cleaned_emails = []
    unwanted_emails = [
        "email@icloud.com", "2Bemail@icloud.com", "email@gmail.com", "2Bemail@gmail.com",
        "email@yahoo.com", "2Bemail@yahoo.com", "email@hotmail.com", "2Bemail@hotmail.com",
        "email@yahoo.fr", "2Bemail@yahoo.fr", "email@hotmail.fr", "2Bemail@hotmail.fr",
        ".@.", ".@.null", "null"
    ]
    
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    for email in emails:
        if email_pattern.match(email) and email not in unwanted_emails:
            cleaned_emails.append(email)

    return cleaned_emails

# Function to validate phone numbers
def validate_phone_numbers(phone_numbers, country_code):
    valid_phone_numbers = []
    for number in phone_numbers:
        try:
            parsed_number = phonenumbers.parse(number, country_code)
            if phonenumbers.is_valid_number(parsed_number):
                formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                valid_phone_numbers.append(formatted_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            continue

    return valid_phone_numbers

# Asynchronous Function to Fetch a Single Page
async def fetch_single_page(session, url):
    headers = {"User-Agent": random.choice(user_agents)}
    async with session.get(url, headers=headers) as response:
        return await response.text()

# Asynchronous Fetch Query with Pagination
async def fetch_query_async(query, num_pages=1, min_sleep=10, max_sleep=20):
    results = set()
    async with aiohttp.ClientSession() as session:
        for page in range(num_pages):
            start = page * 10
            url = f"https://www.google.com/search?q={query}&start={start}"
            result = await fetch_single_page(session, url)
            results.add(result)
            sleep_time = random.uniform(min_sleep, max_sleep)
            await asyncio.sleep(sleep_time)  # User-configurable sleep between requests
    return results

# Function to run async tasks in a synchronous Streamlit app
def run_async_task(task):
    return asyncio.run(task)

# Function to make DataFrame downloadable
def make_downloadable_df(dataframe):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # B64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="extracted_data.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

def main():
    st.title("Email Extractor App")
    menu = ["Home", "Single Extractor", "Bulk Extractor", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Mapping country codes to full country names
    country_mapping = {
        "US": "United States",
        "IN": "India",
        "GB": "United Kingdom",
        "AU": "Australia",
        "CA": "Canada",
        "DE": "Germany",
        "FR": "France",
        "ZA": "South Africa",
        "AF": "Afghanistan",
        "AL": "Albania",
        "DZ": "Algeria",
        "AO": "Angola",
        "AR": "Argentina",
        "AM": "Armenia",
        "AT": "Austria",
        "AZ": "Azerbaijan",
        "BD": "Bangladesh",
        "BE": "Belgium",
        "BJ": "Benin",
        "BO": "Bolivia",
        "BR": "Brazil",
        "BG": "Bulgaria",
        "KH": "Cambodia",
        "CM": "Cameroon",
        "CL": "Chile",
        "CN": "China",
        "CO": "Colombia",
        "CR": "Costa Rica",
        "HR": "Croatia",
        "CU": "Cuba",
        "CY": "Cyprus",
        "CZ": "Czech Republic",
        "DK": "Denmark",
        "DO": "Dominican Republic",
        "EC": "Ecuador",
        "EG": "Egypt",
        "SV": "El Salvador",
        "EE": "Estonia",
        "ET": "Ethiopia",
        "FI": "Finland",
        "GE": "Georgia",
        "GH": "Ghana",
        "GR": "Greece",
        "GT": "Guatemala",
        "HN": "Honduras",
        "HK": "Hong Kong",
        "HU": "Hungary",
        "ID": "Indonesia",
        "IR": "Iran",
        "IQ": "Iraq",
        "IE": "Ireland",
        "IL": "Israel",
        "IT": "Italy",
        "JM": "Jamaica",
        "JP": "Japan",
        "JO": "Jordan",
        "KZ": "Kazakhstan",
        "KE": "Kenya",
        "KR": "South Korea",
        "KW": "Kuwait",
        "KG": "Kyrgyzstan",
        "LA": "Laos",
        "LV": "Latvia",
        "LB": "Lebanon",
        "LY": "Libya",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "MG": "Madagascar",
        "MY": "Malaysia",
        "MV": "Maldives",
        "ML": "Mali",
        "MT": "Malta",
        "MX": "Mexico",
        "MD": "Moldova",
        "MN": "Mongolia",
        "ME": "Montenegro",
        "MA": "Morocco",
        "MM": "Myanmar",
        "NP": "Nepal",
        "NL": "Netherlands",
        "NZ": "New Zealand",
        "NI": "Nicaragua",
        "NG": "Nigeria",
        "NO": "Norway",
        "OM": "Oman",
        "PK": "Pakistan",
        "PA": "Panama",
        "PY": "Paraguay",
        "PE": "Peru",
        "PH": "Philippines",
        "PL": "Poland",
        "PT": "Portugal",
        "QA": "Qatar",
        "RO": "Romania",
        "RU": "Russia",
        "SA": "Saudi Arabia",
        "RS": "Serbia",
        "SG": "Singapore",
        "SK": "Slovakia",
        "SI": "Slovenia",
        "ES": "Spain",
        "LK": "Sri Lanka",
        "SD": "Sudan",
        "SE": "Sweden",
        "CH": "Switzerland",
        "SY": "Syria",
        "TW": "Taiwan",
        "TJ": "Tajikistan",
        "TH": "Thailand",
        "TN": "Tunisia",
        "TR": "Turkey",
        "UA": "Ukraine",
        "AE": "United Arab Emirates",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VE": "Venezuela",
        "VN": "Vietnam",
        "YE": "Yemen",
        "ZM": "Zambia",
        "ZW": "Zimbabwe"
    }

    if choice == "Home":
        st.subheader("Search & Extract")
        country_code = st.sidebar.selectbox("Country Code", countries_list)
        country_name = country_mapping.get(country_code, country_code)  # Default to code if name not in mapping
        city = st.text_input("Enter City")
        state = st.text_input("Enter State")
        email_type = st.sidebar.selectbox("Email Type", email_extensions_list)
        tasks_list = ["Emails", "URLS", "Phonenumbers"]
        task_option = st.sidebar.multiselect("Task", tasks_list, default="Emails")
        search_text = st.text_input("Paste Term Here")
        num_pages = st.sidebar.slider("Number of Pages to Scrape", 1, 10, 1)
        min_sleep = st.sidebar.slider("Min Sleep Time (sec)", 1, 10, 5)
        max_sleep = st.sidebar.slider("Max Sleep Time (sec)", 10, 30, 20)
        generated_query = f"{search_text} + {city} + {state} + {country_name} + email@{email_type} + site:linkedin.com/in"


        st.info(f"Generated Query: {generated_query}")

        # Option to clear cache before the search
        if st.button("Clear Cache"):
             st.cache_data.clear()  # Clear the cache explicitly

        if st.button("Search & Extract"):
            if generated_query:
                fetched_data = run_async_task(fetch_query_async(generated_query, num_pages=num_pages, min_sleep=min_sleep, max_sleep=max_sleep))

                # Combine all fetched data into a single string
                combined_text = ' '.join(fetched_data)

                task_mapper = {
                    "Emails": clean_emails(nfx.extract_emails(combined_text)),
                    "URLS": nfx.extract_urls(combined_text),
                    "Phonenumbers": validate_phone_numbers(nfx.extract_phone_numbers(combined_text), country_code)
                }

                all_results = []
                for task in task_option:
                    results = task_mapper[task]
                    all_results.append(results)

                st.write(all_results)

                with st.expander("Results As DataFrame"):
                    results_df = pd.DataFrame(all_results).T
                    results_df.columns = task_option
                    st.dataframe(results_df)
                    make_downloadable_df(results_df)

    elif choice == "Single Extractor":
        st.subheader("Extract A Single Term")
        text = st.text_area("Paste Text Here")
        task_option = st.sidebar.selectbox("Task", ["Emails", "URLS", "Phonenumbers"])
        if st.button("Extract"):
            if task_option == "Emails":
                results = clean_emails(nfx.extract_emails(text))
            elif task_option == "Phonenumbers":
                country_code = st.sidebar.selectbox("Country Code", countries_list)
                results = validate_phone_numbers(nfx.extract_phone_numbers(text), country_code)
            else:
                results = nfx.extract_urls(text)

            st.write(results)
            with st.expander("Results As DataFrame"):
                results_df = pd.DataFrame(results, columns=[task_option])
                st.dataframe(results_df)
                make_downloadable_df(results_df)

    elif choice == "Bulk Extractor":
        st.subheader("Extract Multiple Terms")
        uploaded_file = st.file_uploader("Upload File", type=["txt", "csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            tasks_list = ["Emails", "URLS", "Phonenumbers"]
            task_option = st.sidebar.multiselect("Task", tasks_list, default="Emails")

            all_results = []
            for task in task_option:
                if task == "Emails":
                    cleaned = clean_emails(nfx.extract_emails_from_list(df.iloc[:, 0].tolist()))
                    all_results.append(cleaned)
                elif task == "Phonenumbers":
                    country_code = st.sidebar.selectbox("Country Code", countries_list)
                    cleaned = validate_phone_numbers(nfx.extract_phone_numbers_from_list(df.iloc[:, 0].tolist()), country_code)
                    all_results.append(cleaned)
                else:
                    cleaned = nfx.extract_urls_from_list(df.iloc[:, 0].tolist())
                    all_results.append(cleaned)

            st.write(all_results)

            with st.expander("Results As DataFrame"):
                results_df = pd.DataFrame(all_results).T
                results_df.columns = task_option
                st.dataframe(results_df)
                make_downloadable_df(results_df)

    else:
        st.subheader("About")

if __name__ == "__main__":
    main()
