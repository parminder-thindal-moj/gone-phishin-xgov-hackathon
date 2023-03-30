import pandas as pd
import regex as re

import urllib.parse as urlparse
from tld import get_tld
import urllib.request as urlreq


## Columns

cols = ['qty_dot_url',
'qty_hyphen_url',
'qty_underline_url',
'qty_slash_url',
'qty_questionmark_url',
'qty_equal_url',
'qty_at_url',
'qty_and_url',
'qty_asterisk_url',
'qty_tld_url',
'length_url', 
'qty_dot_domain',
'qty_hyphen_domain',
'qty_vowels_domain',
'domain_length',
'qty_dot_directory',
'qty_hyphen_directory',
'qty_underline_directory',
'qty_slash_directory',
'qty_equal_directory',
'qty_at_directory',
'qty_and_directory',
'qty_asterisk_directory',
'qty_percent_directory',
'directory_length',
'qty_dot_params',
'qty_hyphen_params',
'qty_underline_params',
'qty_slash_params',
'qty_questionmark_params',
'qty_equal_params',
'qty_at_params',
'qty_and_params',
'qty_percent_params',
'params_length',
'tld_present_params',
'qty_params',
'email_in_url']


##test urls 
url_list_extras = ['https://yogakyibzs.duckdns.org/',
'https://6oj.cn/ncsbrank',
'https://regler-ma-contravention.fr/',
'https://nevincan.av.tr/otp.html',
'https://s.id/Gruppo-Bper-VerificaClienti']


##extracting from a string 
url_list = []

myString = "This is my tweet check it out https://nevincan.av.tr/otp.html"
url_test = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
url_list.append(url_test)


## adding vectors to a dataframe
new_df = []

for url_test in url_list:
    
    underline_pattern = re.compile(r'__(.*?)__') 
    #url_test = str(url_test)
    path = urlparse.urlparse(url_test)

    
    #Extracting column information
    
    qty_dot_url = url_test.count('.')
    qty_hyphen_url = url_test.count('-')
    qty_underline_url = re.findall(underline_pattern, url_test)
    qty_slash_url = url_test.count('/')
    qty_questionmark_url = url_test.count('?')
    qty_equal_url = url_test.count('=')
    qty_at_url = url_test.count('@')
    qty_and_url = url_test.count('&')
    qty_asterisk_url = url_test.count('*')
    qty_tld_url = url_test.count('~')
    length_url = len(url_test)

    if not qty_underline_url:
        qty_underline_url = 0

    qty_dot_domain = path.netloc.count('.')
    qty_hyphen_domain = path.netloc.count('-')
    qty_vowels_domain = len([char for char in path.netloc if char in "aeiouAEIOU"])
    domain_length = len(path.netloc)


    qty_dot_directory = path.path.count('.')
    qty_hyphen_directory = path.path.count('-')
    qty_underline_directory = re.findall(underline_pattern, path.path)
    qty_slash_directory = path.path.count('/')
    qty_equal_directory = path.path.count('=')
    qty_at_directory = path.path.count('@')
    qty_and_directory = path.path.count('&')
    qty_asterisk_directory = path.path.count('*')
    qty_percent_directory = path.path.count('%')
    directory_length = len(path.path)

    if not qty_underline_directory:
        qty_underline_directory = 0


    qty_dot_params = path.query.count('.')
    qty_hyphen_params = path.query.count('-')
    qty_underline_params = re.findall(underline_pattern, path.query)
    qty_slash_params = path.query.count('/')
    qty_questionmark_params = path.query.count('?')
    qty_equal_params = path.query.count('=')
    qty_at_params = path.query.count('@')
    qty_and_params = path.query.count('&')
    qty_percent_params = path.query.count('%')
    params_length = len(path.query)

    if not qty_underline_params:
        qty_underline_params = 0

    qty_params = qty_dot_params+qty_hyphen_params+qty_underline_params+qty_slash_params+qty_questionmark_params+qty_equal_params+qty_at_params+qty_and_params+qty_percent_params

    tld_present_params = get_tld(url_test)

    if len(tld_present_params) > 0:
        tld_present_params = 1
    else:
        tld_present_params = 0


    email_in_url = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', url_test)
    if len(email_in_url) > 0:
        email_in_url = 1
    else:
        email_in_url = 0


#     url_shortened = urlreq.urlopen(url_test)
#     url_shortened = url_shortened.url

#     if url_shortened<url_test:
#         url_shortened = 1
#     else:
#         url_shortened=0
    
    #adding to df
    
    row1 = [qty_dot_url,qty_hyphen_url,qty_underline_url,qty_slash_url,qty_questionmark_url,qty_equal_url,
        qty_at_url,qty_and_url,qty_asterisk_url,qty_tld_url,length_url,qty_dot_domain,qty_hyphen_domain,
        qty_vowels_domain,domain_length,qty_dot_directory,qty_hyphen_directory,qty_underline_directory,
        qty_slash_directory,qty_equal_directory,qty_at_directory,qty_and_directory,qty_asterisk_directory,
        qty_percent_directory,directory_length,qty_dot_params,qty_hyphen_params,qty_underline_params,
        qty_slash_params,qty_questionmark_params,qty_equal_params,qty_at_params,qty_and_params,
        qty_percent_params,params_length,qty_params,tld_present_params,email_in_url] 
    
    #,url_shortened
    new_df.append(row1)
    #print(new_df)
    
combined = pd.DataFrame(new_df, columns=cols)
display(combined)
