# Core Pkgs
import requests
import streamlit as st
import streamlit.components.v1 as stc
from typing import Any, Dict, Iterator, List, NoReturn

# EDA Pkgs
import pandas as pd
import neattext.functions as nfx

# Utils
import base64
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

#Fxn to Download
def make_downloadable(data,task_type):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()   #B64 encoding
    st.markdown("### ** Download Results File ** ")
    new_filename = "extracted_{}_result_{}.csv".format(task_type,timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)

def make_downloadable_df(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()   #B64 encoding
    st.markdown("### ** Download Results File ** ")
    new_filename = "extracted_dat_result_{}.csv".format(timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)


# Fxn to Fetch Results
@st.cache
def fetch_query(query):
    base_url = "https://www.google.com/search?q={}".format(query)
    r = requests.get(base_url)
    return r.text


# Beautifucation

  # custom_title = """
  # <div style="font-size:60px;font-weight:bolder;background-color:#fff;padding:10px;
  # border-radius:10px;border:5px solid #464e5f;text-align:center;">
  #        <span style='color:blue'>E</span>
  #        <span style='color:black'>m</span>
  #        <span style='color:red'>a</span>
  #        <span style='color:green'>i</span>
  #        <span style='color:purple'>l</span>
  #
  #        <span style='color:blue'>E</span>
  #        <span style='color:red'>x</span>
  #        <span style='color:yellow'>t</span>
  #        <span style='color:#464e5f'>r</span>
  #        <span style='color:red'>a</span>
  #        <span style='color:green'>c</span>
  #        <span style='color:yellow'>t</span>
  #        <span style='color:black'>o</span>
  #        <span style='color:blue'>r</span>
  #
  # </div>
  # """

def main():
    """Email Extraction Streamlit App"""
    st.title("Email Extractor App")

    # stc.html(custom_title)

    menu = ["Home","Single Extractor","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Search & Extract")
        countries_list = ["Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia","Australia","Austria","Azerbaijan","The Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Central African Republic","Chad","Chile","China","Colombia","Comoros","Congo","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","France","Gabon","The Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Korea, North","Korea, South","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia","Saint Vincent and the Grenadines","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States of America","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]
        email_extensions_list = ["gmail.com","yahoo.com","hotmail.com","aol.com","icloud.com","hotmail.co.uk","hotmail.fr","msn.com","yahoo.fr","wanadoo.fr","orange.fr","comcast.net","yahoo.co.uk","yahoo.com.br","yahoo.co.in","live.com","rediffmail.com","free.fr","gmx.de","web.de","yandex.ru","ymail.com","libero.it","outlook.com","uol.com.br","bol.com.br","mail.ru","cox.net","hotmail.it","sbcglobal.net","sfr.fr","live.fr","verizon.net","live.co.uk","googlemail.com","yahoo.es","ig.com.br","live.nl","bigpond.com","terra.com.br","yahoo.it","neuf.fr","yahoo.de","alice.it","rocketmail.com","att.net","laposte.net","bellsouth.net","yahoo.in","hotmail.es","charter.net","yahoo.ca","yahoo.com.au","rambler.ru","hotmail.de","tiscali.it","shaw.ca","yahoo.co.jp","sky.com","earthlink.net","optonline.net","freenet.de","t-online.de","aliceadsl.fr","virgilio.it","home.nl","qq.com","telenet.be","me.com","yahoo.com.ar","tiscali.co.uk","yahoo.com.mx","voila.fr","gmx.net","mail.com","planet.nl","tin.it","live.it","ntlworld.com","arcor.de","yahoo.co.id","frontiernet.net","hetnet.nl","live.com.au","yahoo.com.sg","zonnet.nl","club-internet.fr","juno.com","optusnet.com.au","blueyonder.co.uk","bluewin.ch","skynet.be","sympatico.ca","windstream.net","mac.com","centurytel.net","chello.nl","live.ca","aim.com","bigpond.com.au","titan.com"]
        country_name = st.sidebar.selectbox("Country",countries_list)
        email_type = st.sidebar.selectbox("Email Type",email_extensions_list)
        tasks_list = ["Emails","URLS",""]
        task_option = st.sidebar.multiselect("Task",tasks_list,default="Emails")
        search_text = st.text_input("Paste Term Here")
        # dentist + USA + email@aol.com
        generated_query = f"{search_text} + {country_name} + email@{email_type} + site:linkedin.com/in&num=200"
        st.info("Generated Query: {}".format(generated_query))

        if st.button("Search & Extract"):
            if generated_query is not None:
                text = fetch_query(generated_query)
                # st.write(text)

                task_mapper = {"Emails": nfx.extract_emails(text), "URLS": nfx.extract_urls(text),
                               "Phonenumbers": nfx.extract_phone_numbers(text)}

                all_results = []
                for task in task_option:
                    results = task_mapper[task]
                    # st.write(results)
                    all_results.append(results)
                st.write(all_results)

                with st.beta_expander("Results As DataFrame"):
                    results_df = pd.DataFrame(all_results).T
                    results_df.columns = task_option
                    st.dataframe(results_df)
                    make_downloadable_df(results_df)

    elif choice == "Single Extractor":
        st.subheader("Extract A Single Term")
        text = st.text_area("Paste Text Here")
        task_option = st.sidebar.selectbox("Task",["Emails","URLS",""])
        if st.button("Extract"):

            if task_option == "URLS":
                results = nfx.extract_urls(text)
            # elif task_option == "Phonenumbers":
            #     results = nfx.extract_phone_numbers(text)
            else:
                results = nfx.extract_emails(text)

            st.write(results)

            with st.beta_expander("Results As DataFrame"):
                results_df = pd.DataFrame({'Results':results})
                st.dataframe(results_df)
                make_downloadable(results_df,task_option)


#     elif choice == "Bulk Extractor":
#         st.subheader("Bulk Extractor")
#         text = st.text_area("Paste Text Here")
#         tasks_list = ["Emails","URLS",""]
#         task_option = st.sidebar.multiselect("Task",tasks_list,default="Emails")
#         task_mapper = {"Emails":nfx.extract_emails(text),"URLS":nfx.extract_urls(text),
#                        "Phonenumbers":nfx.extract_phone_numbers(text)}

#         all_results = []
#         for task in task_option:
#             results =task_mapper[task]
#             # st.write(results)
#             all_results.append(results)
#         st.write(all_results)

#         with st.beta_expander("Results As DataFrame"):
#             results_df = pd.DataFrame(all_results).T
#             results_df.columns = task_option
#             st.dataframe(results_df)
#             make_downloadable_df(results_df)
    else:
        st.subheader("About")

if __name__ == "__main__":
    main()
