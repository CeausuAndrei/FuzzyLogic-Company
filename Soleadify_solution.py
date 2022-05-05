"""
@author: Ceausu Dan Andrei
"""

import numpy as np
import pandas as pd
import re
from fuzzywuzzy import process
from iso3166 import countries
import Levenshtein as lev
import logging
logging.getLogger().setLevel(logging.ERROR)

#Functions

def count_cat(cat_split, text_split, desc_split):
    count_cat = 0
    
    for i in cat_split:
        rat_text = process.extract(i, text_split)
        rat_desc = process.extract(i, desc_split)
            
        for j in range(len(rat_text)):
            if rat_text[j][1] > 85:
                count_cat += 1
            else:
                break
            
                
        for j in range(len(rat_desc)):
            if rat_desc[j][1] > 85:
                count_cat += 1
            else:
                break
            
    return count_cat
                
def check_equal_fuzzy(hs):
    if len(hs) == 1:    
        return hs
    
    elif len(hs) == 2:
        if hs[0][1] > hs[1][1]:
            return hs[0][1]
        
        elif hs[0][1] == hs[1][1]:
            minim = min(len(hs[0][0]), len(hs[1][0]))
            
            if minim == len(hs[0][0]):
                return hs[0]
            
            elif minim == len(hs[1][0]):
                return hs[1]
                           
    elif len(hs) == 3:
        maxim = max(hs[0][1], hs[1][1], hs[2][1])

        if hs[2][1] != maxim == hs[0][1] != hs[1][1]:
            return hs[0]
        
        elif maxim == hs[0][1] == hs[1][1] != hs[2][1]:
            minim = min(len(hs[0][0]), len(hs[1][0]))
            
            if minim == len(hs[0][0]):
                return hs[0]
            
            elif minim == len(hs[1][0]):
                return hs[1]
            
        else:
            minim = min(len(hs[0][0]), len(hs[1][0]), len(hs[2][0]))
            
            if minim == len(hs[0][0]):
                return hs[0]
            
            elif minim == len(hs[1][0]):
                return hs[1]
            
            elif minim == len(hs[2][0]):
                return hs[2]
             
def company_name(name_1, name_2, name_3, site_name):
    
    s1 = name_1
    s2 = name_2
    s3 = name_3
    list_of_name = [name_1, name_2, name_3]
    l_s1 = s1.split(" ")
    l_s2 = s2.split(" ")
    l_s3 = s3.split(" ")

    l12 = []
    l13 = []
    
    for i in range(len(l_s1)):
        
        for j in range(len(l_s2)):
            list_ratio = lev.ratio(l_s1[i].lower(),  l_s2[j].lower())     
            
            if float(list_ratio * 100) > 85:
                l12.append(l_s1[i])
                
            else:
                break
        
        for j in range(len(l_s3)):
            list_ratio = lev.ratio(l_s1[i].lower(),  l_s3[j].lower())
            
            if float(list_ratio * 100) > 85:
                l13.append(l_s1[i])
                
            else:
                break

    l123 = []

    if len(l12) != 0 and len(l13) == 0:
        l123 = l12[:]
        
    elif len(l12) == 0 and len(l13) != 0:
        l123 = l13[:]
        
    elif len(l12) != 0 and len(l13) != 0:
        for i in range(len(l12)):
            for j in range(len(l13)):
                list_ratio = lev.ratio(l12[i].lower(),  l13[j].lower())
                
                if float(list_ratio * 100) > 85:
                    l123.append(l12[i])
                    
                else:
                    break
             
    l23 = []
    
    for i in range(len(l_s2)):
        for j in range(len(l_s3)):
            list_ratio = lev.ratio(l_s2[i].lower(),  l_s3[j].lower())   
            
            if float(list_ratio * 100) > 85:
                l23.append(l_s2[i])
                
            else:
                break
              
    l_final = []
        
    if len(l23) != 0 and len(l123) == 0:
        l_final = l23[:]
        
    elif len(l23) == 0 and len(l123) != 0:
        l_final = l123[:]
        
    elif len(l23) != 0 and len(l123) != 0:
        for i in range(len(l23)):
            for j in range(len(l123)):
                list_ratio = lev.ratio(l23[i].lower(),  l123[j].lower()) 
                
                if float(list_ratio * 100) > 85:
                    l_final.append(l23[i])
                    
                else:
                    break
        
    if len(l_final) != 0:
        l_final = list(dict.fromkeys(l_final))
        output_name = ' '.join(str(tok) for tok in l_final)
        
        highest_similarity = process.extract(output_name, list_of_name)

        return highest_similarity
    
    else:
        highest_similarity = process.extract(site_name, list_of_name)

        return highest_similarity

def count_country_code(country, country_codes):
    count = 0
    for i in country_codes:
        if len(i) != 0:
            if country in countries.get(i).name.lower():
                count += 1
            
    return count

def count_country_number_from_addr(country, address):
    count = 0
    for addr in address:
       if country in addr:
           count += 1
        
    return count

def count_phone_country_code(country, phone_country_code):
    count = 0
    for i in phone_country_code:
        if len(i) != 0:
            if country in countries.get(i).name.lower():
                count += 1
            
    return count
        
def city_or_region_name(city_name1, city_name2, city_name3, address):
    city_name = ''

    if len(city_name1) == len(city_name2) == len(city_name3) == 0:
        return city_name
            
    elif len(city_name1) == len(city_name2) == 0 != len(city_name3):
        return city_name3

    elif len(city_name1) == len(city_name3) == 0 != len(city_name2):
        return city_name2
        
    elif len(city_name2) == len(city_name3) == 0 != len(city_name1):
        return city_name1
                
    elif city_name1 == city_name2 == city_name3:
        return city_name1
    
    elif city_name1 == city_name3 and len(city_name2) == 0:
        return city_name1

    elif city_name2 == city_name3 and len(city_name1) == 0:
        return city_name2
        
    elif city_name1 != city_name2 == city_name3:
        count_city1 = 0
        count_city2 = 0
 
        for addr in address:
            if city_name1 in addr:
                count_city1 +=1
            
            elif city_name2 in addr:
                count_city2 +=1
                
        if count_city1 > count_city2:
            return city_name1
        
        else:
            return city_name2
            
    elif city_name1 == city_name2 != city_name3:
        count_city3 = 0
        count_city2 = 0
 
        for addr in address:
            if city_name3 in addr:
                count_city3 +=1
            
            elif city_name2 in addr:
                count_city2 +=1
                
        if count_city3 > count_city2:
            return city_name3
        
        else:
            return city_name2
            
    elif city_name2 != city_name1 == city_name3:
        count_city2 = 0
        count_city1 = 0
 
        for addr in address:
            if city_name2 in addr:
                count_city1 +=2
            
            elif city_name1 in addr:
                count_city1 +=1
                
        if count_city2 > count_city1:
            return city_name2
        
        else:
            return city_name1
        
def zip_or_region_code(code1, code2, address):
    code = ''
    
    if len(code1) == len(code2) == 0:
        return code
    
    elif code1 == code2:
        return code1
    
    elif len(code1) == 0 != len(code2):
        return code2
    
    elif len(code1) != 0 == len(code2):
        return code1
    
    elif code1 != code2:
        count_code1 = 0
        count_code2 = 0
        
        for addr in address:
            if code1 in addr:
                count_code1 += 1
                
            elif code2 in addr:
                count_code2 += 1
                
        if code1 > code2:
            return code1
        
        elif code1 < code2:
            return code2
        else:
            return code

def address_fuzzy(addr1, addr2, addr3):
    addr1_split = addr1.split(",")
    addr2_split = addr2.split(",")
    addr3_split = addr3.split(",")

    final_list1 = []
    final_list2 = []
    for i in addr1_split:
        rat1 = process.extract(i, addr2_split)
        rat2 = process.extract(i, addr3_split)
        
        for i in range(len(rat1)):
            if rat1[i][1] > 85:
                final_list1.append(rat1[i][0])
                
            else:
                break
                
        
        for i in range(len(rat2)):
            if rat2[i][1] > 85:
                final_list2.append(rat2[i][0])
            
            else:
                break

    final_list = final_list1 + final_list2
    final_list = list(dict.fromkeys(final_list))
    aux = final_list[:]
    
    for i in range(len(final_list)):
        j = i + 1
        aux_list = final_list[j:]
        rat = process.extract(final_list[i], aux_list)
        
        for j in range(len(rat)):
            if rat[j][1] > 85:
                if final_list[i] in aux:
                    aux.remove(final_list[i])
                
                else:
                    break
    
    return aux

def categories_name(category1, category2, category3, text, description):
    category = ' '
    
    if len(category1) == len(category2) == len(category3) == 0:
        return category

    elif category1 == category2 == category3:
        return category1
        
    elif category1 == category2 and len(category3) == 0:
        return category1

    elif category1 == category3 and len(category2) == 0:
        return category1

    elif category2 == category3 and len(category1) == 0:
        return category2
        
    elif len(category1) == (category2) == 0 != len(category3):
        return category3

    elif len(category1) == (category3) == 0 != len(category2):
        return category2
        
    elif len(category2) == (category3) == 0 != len(category1):
        return category1
        
    else:
        cat1_split = category1.split(" ")
        cat2_split = category2.split(" ")
        cat3_split = category3.split(" ")
        
        text_split = text.split(" ")
        desc_split = description.split(" ")
        
        count_cat1 = 0
        count_cat2 = 0
        count_cat3 = 0
        
        count_cat1 += count_cat(cat1_split, text_split, desc_split)
        count_cat2 += count_cat(cat2_split, text_split, desc_split)
        count_cat3 += count_cat(cat3_split, text_split, desc_split)
        
        maxim = max(count_cat1, count_cat2, count_cat3)
        
        if count_cat1 == count_cat2 == count_cat3:
            return category1
            
        elif maxim == count_cat1 == count_cat2 != count_cat3:
            return category1

        elif maxim == count_cat1 == count_cat3 != count_cat2:
            return category1

        elif maxim == count_cat2 == count_cat3 != count_cat1:
            return category2
            
        elif maxim == count_cat1:
            return category1

        elif maxim == count_cat2:
            return category2
            
        elif maxim == count_cat3:
            return category3            
            

# Import all 3 csv they are all encoding in UTF-8

df_facebook = pd.read_csv("facebook dataset.csv", error_bad_lines=False, encoding='utf-8')
df_google = pd.read_csv("google dataset.csv", error_bad_lines=False, encoding='utf-8')
df_website = pd.read_csv("website dataset.csv", error_bad_lines=False, encoding='utf-8')


# Clean the data

df_website = df_website.loc[:, ~df_website.columns.str.contains('^Unnamed')]
df_facebook['phone'] = df_facebook['phone'].apply(lambda x: format(x, '.0f'))

phone_website = df_website['phone'].values

for i in range(len(phone_website)):
    s = str(phone_website[i])
    s = s.lower()
    if 'e+' in s:
        s = s.replace(s, '')
        phone_website[i] = s
        
    s = re.sub("[^0-9]", "", s)
    
phone_google = df_google['raw_phone'].values

for i in range(len(phone_google)):
    s = str(phone_google[i])
    s = re.sub("[^0-9]", "", s)
    phone_google[i] = s
        
    
df_website['phone'] = phone_website
df_google['raw_phone'] = phone_google

df_google = df_google.drop('phone', axis=1)
df_google.rename({"raw_phone" : "phone"}, inplace = True, axis = 1)
df_website.rename({"root_domain" : "domain"}, inplace = True, axis = 1)


# JOIN the csv with key on domain and phone

df = pd.merge(df_facebook, df_website, on = ['domain', 'phone'], how='inner')
df = pd.merge(df, df_google, on = ['domain', 'phone'], how='inner')
df = df.fillna('')

# Remove emoji from dataset

df = df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))


#Check country name

name_list = []

for i in range(len(df)):
    
    list_address = [str(df.address_y[i]).lower(), str(df.raw_address[i]).lower(), str(df.address_x[i]).lower()]
    country_code_list = [str(df.country_code_x[i]).lower(), str(df.country_code_y[i]).lower()]
    phone_country_code_list = [str(df.phone_country_code_x[i]).lower(), str(df.phone_country_code_y[i]).lower()]
    
    name_1 = str(df.main_country[i]).lower()
    name_2 = str(df.country_name_x[i]).lower()
    name_3 = str(df.country_name_y[i]).lower()
    name = ''
    
    if len(name_1) == len(name_2) == len(name_3) == 0:  
        if len(country_code_list) == 0:  
            if len(phone_country_code_list) == 0:    
                name_list.append(name)
                
            elif phone_country_code_list[0] == phone_country_code_list[1]:
                name = countries.get(phone_country_code_list[0]).name.lower()
                name_list.append(name)
                
            elif phone_country_code_list[0] != phone_country_code_list[1]:
                name_1 = countries.get(phone_country_code_list[0]).name.lower()
                name_2 = countries.get(phone_country_code_list[1]).name.lower()
                
                count_phone1 = count_country_number_from_addr(name_1, list_address)
                count_phone2 = count_country_number_from_addr(name_2, list_address)
                
                if count_phone1 > count_phone2:
                    name_list.append(name_1)
                    
                elif count_phone1 < count_phone2:
                    name_list.append(name_2)
                    
                elif count_phone1 == count_phone2:
                    name_list.append(name)
                    
        elif country_code_list[0] != country_code_list[1]:
            name_1 = countries.get(country_code_list[0]).name.lower()
            name_2 = countries.get(country_code_list[1]).name.lower()
                
            count_code1 = count_country_number_from_addr(name_1, list_address)
            count_code2 = count_country_number_from_addr(name_2, list_address)
                
            if count_code1 > count_code2:
                name_list.append(name_1)
                    
            elif count_code1 < count_code2:
                    name_list.append(name_2)
                    
            elif count_code1 == count_code2:
                count_code1 += count_phone_country_code(name_1, phone_country_code_list)
                count_code2 += count_phone_country_code(name_2, phone_country_code_list)
                    
                if count_code1 > count_code2:
                    name_list.append(name_1)
                        
                elif count_code1 < count_code2:
                        name_list.append(name_2)
                        
                elif count_code1 == count_code2:
                    name_list.append(name)
                    
        elif country_code_list[0] == country_code_list[1]:
            name = countries.get(country_code_list[0]).name.lower()
            name_list.append(name)           
                    
    elif name_1 == name_2 == name_3:
        name_list.append(name_1)
        
    elif len(name_1) != len(name_2) == len(name_3) == 0:
        name_list.append(name_1)
        
    elif len(name_2) != len(name_1) == len(name_3) == 0:
        name_list.append(name_2)
        
    elif len(name_3) != len(name_1) == len(name_2) == 0:
        name_list.append(name_3)
        
    elif len(name_1) == 0:
        
        if name_2 == name_3:
            name_list.append(name_2)
            
        elif name_2 != name_3:
            count_name2 = 0
            count_name3 = 0
            
            count_name2 += count_country_number_from_addr(name_2, list_address) + count_country_code(name_2, country_code_list)
            count_name3 += count_country_number_from_addr(name_3, list_address) + count_country_code(name_3, country_code_list)
            
            if count_name2 > count_name3:
                name_list.append(name_2)
                    
            elif count_name2 < count_name3:
                name_list.append(name_3)
                
            elif count_name2 == count_name3:
                count_name2 += count_phone_country_code(name_2, phone_country_code_list)
                count_name3 += count_phone_country_code(name_3, phone_country_code_list)
                
                if count_name2 > count_name3:
                    name_list.append(name_2)
                elif count_name2 < count_name3:
                    name_list.append(name_3)
                elif count_name2 == count_name3:
                    name_list.append(name)
                    
    elif len(name_2) == 0:
        
        if name_1 == name_3:
            name_list.append(name_1)
            
        elif name_1 != name_3:
            count_name1 = 0
            count_name3 = 0
            
            count_name1 += count_country_number_from_addr(name_1, list_address) + count_country_code(name_1, country_code_list)
            count_name3 += count_country_number_from_addr(name_3, list_address) + count_country_code(name_3, country_code_list)
            
            if count_name1 > count_name3:
                name_list.append(name_1)
                    
            elif count_name1 < count_name3:
                name_list.append(name_3)
                
            elif count_name1 == count_name3:
                count_name1 += count_phone_country_code(name_1, phone_country_code_list)
                count_name3 += count_phone_country_code(name_3, phone_country_code_list)
                
                if count_name1 > count_name3:
                    name_list.append(name_1)
                elif count_name1 < count_name3:
                    name_list.append(name_3)
                elif count_name1 == count_name3:
                    name_list.append(name)
            
    elif len(name_3) == 0:
        
        if name_1 == name_2:
            name_list.append(name_1)
            
        elif name_1 != name_2:
            count_name1 = 0
            count_name2 = 0
            
            count_name1 += count_country_number_from_addr(name_1, list_address) + count_country_code(name_1, country_code_list)
            count_name2 += count_country_number_from_addr(name_2, list_address) + count_country_code(name_2, country_code_list)
            
            if count_name1 > count_name2:
                name_list.append(name_1)
                    
            elif count_name1 < count_name2:
                name_list.append(name_2)
                
            elif count_name1 == count_name2:
                count_name1 += count_phone_country_code(name_1, phone_country_code_list)
                count_name2 += count_phone_country_code(name_2, phone_country_code_list)
                
                if count_name1 > count_name2:
                    name_list.append(name_1)
                elif count_name1 < count_name2:
                    name_list.append(name_2)
                elif count_name1 == count_name2:
                    name_list.append(name)    
    
    elif name_1 != name_2 == name_3:
        
        count_name1 = 0
        count_name2 = 0
        
        count_name1 += count_country_number_from_addr(name_1, list_address) + count_country_code(name_1, country_code_list)
        count_name2 += count_country_number_from_addr(name_2, list_address) + count_country_code(name_2, country_code_list)
        
        if count_name1 > count_name2:
            name_list.append(name_1)
        elif count_name1 < count_name2:
            name_list.append(name_2)
        elif count_name1 == count_name2:
            count_name1 += count_phone_country_code(name_1, phone_country_code_list)
            count_name2 += count_phone_country_code(name_2, phone_country_code_list)
                
            if count_name1 > count_name2:
                name_list.append(name_1)
            elif count_name1 < count_name2:
                name_list.append(name_2)
            elif count_name1 == count_name2:
                name_list.append(name)
                
    elif name_1 == name_2 != name_3:
        
        count_name1 = 0
        count_name3 = 0
        
        count_name1 += count_country_number_from_addr(name_1, list_address) + count_country_code(name_1, country_code_list)
        count_name3 += count_country_number_from_addr(name_3, list_address) + count_country_code(name_3, country_code_list)
        
        if count_name1 > count_name3:
            name_list.append(name_1)
        elif count_name1 < count_name3:
            name_list.append(name_3)
        elif count_name1 == count_name3:
            count_name1 += count_phone_country_code(name_1, phone_country_code_list)
            count_name3 += count_phone_country_code(name_3, phone_country_code_list)
                
            if count_name1 > count_name3:
                name_list.append(name_1)
            elif count_name1 < count_name3:
                name_list.append(name_3)
            elif count_name1 == count_name3:
                name_list.append(name)
                
    elif name_1 == name_3 != name_2:
        
        count_name1 = 0
        count_name2 = 0
        
        count_name1 += count_country_number_from_addr(name_1, list_address) + count_country_code(name_1, country_code_list)
        count_name2 += count_country_number_from_addr(name_2, list_address) + count_country_code(name_2, country_code_list)
        
        if count_name1 > count_name2:
            name_list.append(name_1)
        elif count_name1 < count_name2:
            name_list.append(name_2)
        elif count_name1 == count_name2:
            count_name1 += count_phone_country_code(name_1, phone_country_code_list)
            count_name2 += count_phone_country_code(name_2, phone_country_code_list)
                
            if count_name1 > count_name2:
                name_list.append(name_1)
            elif count_name1 < count_name2:
                name_list.append(name_2)
            elif count_name1 == count_name2:
                name_list.append(name)

df = df.drop(['main_country', 'country_name_x', 'country_name_y'], axis=1)
df['Country_Name'] = name_list
df['Country_Name'] = df['Country_Name'].apply(lambda x: x.title())

#Check country code

df['Country_Name'] = df['Country_Name'].replace("United States", "United States of America")
df['Country_Name'] = df['Country_Name'].replace("South Korea", "Korea, Republic of")
df['Country_Name'] = df['Country_Name'].replace("Russia", "Russian Federation")
df['Country_Name'] = df['Country_Name'].replace("United Kingdom", "United Kingdom of Great Britain and Northern Ireland")
df['Country_Name'] = df['Country_Name'].replace("Saint Martin", "Saint Martin (French part)")
df['Country_Name'] = df['Country_Name'].replace("U.S. Virgin Islands", "Virgin Islands, U.S.")
df['Country_Name'] = df['Country_Name'].replace("Hashemite Kingdom Of Jordan", "Jordan")

name_country_code_list = []

for i in range(len(df)):
    name = str(df.Country_Name[i])
    if name == 'Vietnam':
        name = 'Viet Nam'
    name = countries.get(name).alpha2.upper()
    name_country_code_list.append(name)
    
df = df.drop(['country_code_x', 'country_code_y'], axis=1)
df['Country_Code'] = name_country_code_list
    

#Check phone country code

phone_code_list =[]

for i in range(len(df)):
    name_1 = str(df.phone_country_code_x[i]).lower()
    name_2 = str(df.phone_country_code_y[i]).lower()
    name_3 = str(df.Country_Code[i]).lower()
    name = ''
    if name_1 == name_2:
        phone_code_list.append(name_1)
    
    elif len(name_1) == len(name_2) == 0 and len(name_3) != 0:
        phone_code_list.append(name_3)
        
        
    elif len(name_1) != 0 and len(name_2) == 0:
        phone_code_list.append(name_1)
        
    elif len(name_1) == 0 and len(name_2) != 0:
        phone_code_list.append(name_2)
        
    elif name_1 != name_2 and len(name_3) != 0:
        
        if name_1 == name_3:
            phone_code_list.append(name_1)
        
        elif name_2 == name_3:
            phone_code_list.append(name_2)
            
        else:
            phone_code_list.append(name_3)
        
    else:
        phone_code_list.append(name)

df = df.drop(['phone_country_code_x', 'phone_country_code_y'], axis=1)
df['Phone_Country_Code'] = name_country_code_list
    

# Check company name

company_name_list_and_ratio = []
company_name_list = []

for i in range(len(df)):
        name_1 = str(df.name_x[i])
        name_2 = str(df.name_y[i])
        name_3 = str(df.legal_name[i])
        site_name = str(df.site_name[i])

        aux = company_name(name_1, name_2, name_3, site_name)
        aux1 = check_equal_fuzzy(aux)
        company_name_list_and_ratio.append(aux1)

# Uncomment next line to see all the company with the percentage accuracy 
# print(company_name_list_and_ratio)

for i in range(len(company_name_list_and_ratio)):
    company_name_list.append(company_name_list_and_ratio[i][0])

df = df.drop(['name_x', 'name_y', 'legal_name'], axis=1)
df['Company_Name'] = company_name_list


# Check city name, region name, region code and zip code

zip_code_list = []
city_name_list = []
region_name_list = []
region_code = []

for i in range(len(df)):
    zip_code1 = str(df.zip_code_x[i]).lower()
    zip_code2 = str(df.zip_code_y[i]).lower()
    
    region_code1 = str(df.region_code_x[i]).lower()
    region_code2 = str(df.region_code_y[i]).lower()
    
    city_name1 = str(df.city_x[i]).lower()
    city_name2 = str(df.city_y[i]).lower()
    city_name3 = str(df.main_city[i]).lower()
    
    region_name1 = str(df.region_name_x[i]).lower()
    region_name2 = str(df.region_name_y[i]).lower()
    region_name3 = str(df.main_region[i]).lower()
    
    list_address = [str(df.address_y[i]).lower(), str(df.raw_address[i]).lower(), str(df.address_x[i]).lower()]
    
    city_name_list.append(city_or_region_name(city_name1, city_name2, city_name3, list_address))
    region_name_list.append(city_or_region_name(region_name1, region_name2, region_name3, list_address))
    zip_code_list.append(zip_or_region_code(zip_code1, zip_code2, list_address))
    region_code.append(zip_or_region_code(region_code1, region_code2, list_address))
    
    

df = df.drop(['city_x', 'city_y', 'main_city', 'region_name_x', 'region_name_y', 'main_region',
              'zip_code_x', 'zip_code_y', 'region_code_x', 'region_code_y', 'email', 'link', 'domain_suffix',
              'tld', 'page_type', 'site_name', 'language'], axis=1)

df['City_Name'] = city_name_list
df['Region_Name'] = region_name_list
df['Zip_Code'] = zip_code_list
df['Region_Code'] = region_code


# Check address

address_list = []

for i in range(len(df)):
    addr1 = str(df.address_y[i])
    addr2 = str(df.raw_address[i])
    addr3 = str(df.address_x[i])
    addr = ' '
    
    if addr1 == addr2 == addr3:
        address_list.append(addr1)
    
    elif len(addr1) == len(addr2) == 0 != len(addr3):
        address_list.append(addr3)

    elif len(addr1) == len(addr3) == 0 != len(addr1):
        address_list.append(addr1)
        
    elif len(addr2) == len(addr3) == 0 != len(addr1):
        address_list.append(addr1)
        
    elif addr1 == addr2 and len(addr3) == 0:
        address_list.append(addr1)

    elif addr1 == addr3 and len(addr2) == 0:
        address_list.append(addr1)

    elif addr2 == addr3 and len(addr1) == 0:
        address_list.append(addr2)
        
    else:
        fuzzy_addr1 = address_fuzzy(addr1, addr2, addr3)
        fuzzy_addr2 = address_fuzzy(addr2, addr1, addr3)
        fuzzy_addr3 = address_fuzzy(addr3, addr1, addr2)
        
        addr1_name = ', '.join(fuzzy_addr1)
        addr2_name = ', '.join(fuzzy_addr2)
        addr3_name = ', '.join(fuzzy_addr3)
        
        maxim = max(len(fuzzy_addr1), len(fuzzy_addr2), len(fuzzy_addr3))
     
        if maxim == 0:
            address_list.append(addr)
        
        elif maxim == len(fuzzy_addr1):
            address_list.append(addr1_name)
            
        elif maxim == len(fuzzy_addr2):
            address_list.append(addr2_name)
            
        elif maxim == len(fuzzy_addr3):
            address_list.append(addr3_name)
        
df = df.drop(['address_y', 'address_x', 'raw_address'], axis=1)
df['Address'] = address_list


# Check category

categories_list = []

for i in range(len(df)):
    category1 = str(df.s_category[i])
    category2 = str(df.category[i])
    category3 = str(df.categories[i])    

    text = str(df.text[i])
    description = str(df.description[i])
    
    categories_list.append(categories_name(category1, category2, category3, text, description))
    
df = df.drop(['categories', 'description', 's_category', 'category', 'text'], axis=1)
df['Category'] = categories_list
 
   
# Make some more data clean

df = df[['domain', 'Company_Name', 'phone', 'Phone_Country_Code', 'Category', 'Address', 'Zip_Code', 
         'City_Name', 'Region_Name', 'Region_Code','Country_Name', 'Country_Code']]
df.rename({"domain" : "Domain"}, inplace = True, axis = 1)
df.rename({"phone" : "Phone_Number"}, inplace = True, axis = 1)
df.replace(np.nan, "", inplace=True)
df['City_Name'] = df['City_Name'].apply(lambda x: x.title())
df['Region_Name'] = df['Region_Name'].apply(lambda x: x.title())
df['Region_Code'] = df['Region_Code'].apply(lambda x: x.upper())

df_final = df.copy(deep=True)
df_final.replace('', np.nan, inplace=True)
df_final.replace(' ', np.nan, inplace=True)
df_final.dropna(inplace=True)
df_final.drop_duplicates(subset = ["Company_Name", "Phone_Number"], keep=False, inplace=True)
df_final.reset_index(drop=True, inplace=True)


# Export to csv in current folder

df_final.to_csv('Company.csv', index=False)