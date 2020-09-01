from urllib.request import urlopen

from bs4 import BeautifulSoup
import pandas as pd
import re
import sys


cat_mobiles="https://www.prisjakt.nu/kategori.php?k=103&s=0"
cat_graphics="https://www.prisjakt.nu/kategori.php?k=350&s=0"
cat_TV="https://www.prisjakt.nu/kategori.php?k=107"
cat_headphones="https://www.prisjakt.nu/kategori.php?k=148"
cat_laptops="https://www.prisjakt.nu/kategori.php?k=353"

def visit_url(url):
    try:
        if "www.prisjakt.nu" in url:
            return urlopen(url)
        else:
            return urlopen("https://www.prisjakt.nu" + url)
    except TimeoutError:
        print("Connection failed. Try again later. Exiting...")
        sys.exit()


def get_list_of_products(url):
    html = visit_url(url)
    soup = BeautifulSoup(html, 'lxml')
    print(soup)


    all_rows= soup(name=re.compile("tr|li"), id=re.compile("erow_prod-\d{4,}"))

    print(all_rows)

    products=[]
    for row in all_rows:
        #z=row.find(href=re.compile("/produkt\.php\?o=\d{7,}"))
        try:
            alink=row.a
            url1=alink['href']
            url=re.sub(r"(.*)\?p=(.*)", r"\g<1>?o=\g<2>", url1) #changes 'p' to 'o'
            print(url)
        except TypeError:
            url="N/A"

        try:
            content=alink.contents[1]
            prod_name=content['alt'] #name of product eg iPhone X
            print(prod_name)
        except TypeError:
            prod_name="N/A"
        except IndexError:
            prod_name = "N/A"

        try:
            id= re.match(".*(\d{7,}.*)", url).group(1)
            print(id)
        except TypeError:
            id="N/A"
        except AttributeError:
            id = "N/A"

        product_entry ={
            "id": id,
            "url": url,
            "prod_name": prod_name,
        }
        products.append(product_entry)
    return products


print("hej")
#list_of_products_mobiles=get_list_of_products(cat_mobiles)
#list_of_products_graphics=get_list_of_products(cat_graphics)

#list_of_products_TV=get_list_of_products(cat_TV)
#list_of_products_headphones=get_list_of_products(cat_headphones)


#df_products_mobiles = pd.DataFrame(list_of_products_mobiles)
#df_products_graphics = pd.DataFrame(list_of_products_graphics)
#df_prod_TV=pd.DataFrame(list_of_products_TV)
#df_prod_headphones=pd.DataFrame(list_of_products_headphones)


#df_products_mobiles.head(5)
#print(df_products_mobiles)
#print(df_products_graphics)
#print(df_prod_TV)
#print(df_prod_headphones)

#print(df['url'])

# removes any <br/>
# returns string
def clean_br(tag_to_clean):
    output=""
    for s in tag_to_clean.contents:
        output += re.sub(r"<br/>", r"", str(s))
    return output

def extract_opinions(opinions):
    opinionsList = []
    for o in opinions:

        print("-------")
        #print(o)
        #COMMENT_ID
        try:
            comment_id = o.a['id']
        #print(comment_id)
        except TypeError:
            comment_id="N/A"

        #RATING
        rating=""
        try:
            rating=o.find(name="meta", itemprop="ratingValue")
            #print(type(rating))
            rating=rating['content']
        except TypeError:
            rating="N/A"

        #print(rating)

        #DATE PUBLISHED
        try:
            date_published=o.find(name="meta", itemprop="datePublished")
            date_published =date_published['content']
            #print(date_published)
        except TypeError:
            date_published="N/A"

        #USERS
        try:
            user=o.find(name="h4", attrs={'class': 'name'})
            user=user.contents[0]
            #print(user.contents[0])
        except TypeError:
            user="N/A"
        except AttributeError:
            user = "N/A"


        #PREVIOUS NUMBER OF REVIEWS
        try:
            prev_num_reviews=o.find(name="a", attrs={'class': re.compile("text-small .*")})
            link_prev_num_reviews=prev_num_reviews['href'] + "&do=opinions"
            #print(link_prev_num_reviews)
            prev_num_reviews=prev_num_reviews.contents[0]
            prev_num_reviews=re.sub(r"\n", r"", prev_num_reviews)
        except TypeError:
            link_prev_num_reviews = "N/A"
            prev_num_reviews = "N/A"
        except AttributeError:
            link_prev_num_reviews = "N/A"
            prev_num_reviews = "N/A"

        # print(o(name="div", itemprop="reviewBody"))
        try:
            reviewBody = o(name="div", itemprop="reviewBody")[0]  # [0] tar ut texten ur listan så den blir string
            review = clean_br(reviewBody)
        except TypeError:
            reviewBody = "N/A"
            review= "N/A"
        except IndexError:
            reviewBody = "N/A"
            review = "N/A"
        # print(reviewBody.contents)


        #print(review)
        #print(reviewBody)
        # print(reviewBody[0].contents[0])

        review_entry = {
            "comment_id": comment_id,
            "user": user,
            "prev_num_reviews": prev_num_reviews,
            "link_prev_num_reviews": link_prev_num_reviews,
            "rating": rating,
            "product_review": review,
            "date_published": date_published,
        }
        opinionsList.append(review_entry)
    return opinionsList



#TEST
#html3 = urlopen("https://www.prisjakt.nu/produkt.php?o=4389341")

#html4 = urlopen("https://www.prisjakt.nu/produkt.php?o=4236150")
#soup2 = BeautifulSoup(html3, 'lxml')
#soup3 = BeautifulSoup(html4, 'lxml')

#print(soup2.prettify())

#opinions=soup2.find_all(name="li", attrs={'class': 'opinion-row'})
#opinions2=soup3.find_all(name="li", attrs={'class': 'opinion-row'})
#print(opinions2)

#opinionsList=extract_opinions(opinions)


#df2 = pd.DataFrame(opinionsList)
#df2.head(5)
#print(df2) #funkar

path=r"C:\Users\Emil\PycharmProjects\web_scraper\\"
#df2.to_csv(path+'reviews.csv', encoding='utf-8', index=False)


###########



def extract_previous_reviews_from_user(url):
    prevReviewsList = []
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("dummy")
    user=re.sub(r".*a=([a-zåäöA-ZÅÄÖ0-9_!? ]+)\&do.*", r"\g<1>", url)
    print(user)

    h = urlopen(url)
    soup4 = BeautifulSoup(h, 'lxml')
    prev_opinions = soup4.find_all(name="div", attrs={'class': 'contentbox'}, id=re.compile("omdome_\d+_"))
   # print(prev_opinions)
    for prev in prev_opinions:
        print("---")
        print(prev)
        previous_review = prev.find(name="div", id=re.compile("comment_\d+"))
        previous_review=clean_br(previous_review)
        #print(previous_review)
        prev_rating=prev.find(name="img", attrs={'class': re.compile("stars10 s10_\d+")})
        prev_rating = prev_rating['class'][1]
        prev_rating = re.sub(r"s10_(\d+)",r"\g<1>",prev_rating)

        info=prev.find(name="a", attrs={'class': 'drg-sidebar'}, href=re.compile("/produkt.php\?p=\d+"), id=re.compile("ss_prod_\d+"))
        #print(info)
        #print(info['href'])
        link=info['href']
        link= re.sub(r"(.*)\?p=(.*)", r"\g<1>?o=\g<2>", link)
        info=info.contents
        info=re.sub(r"\n", "", info[2]).strip()
        print(info)

        prev_review_entry = {
            'user': user,
            'prev_rating': prev_rating,
            'prev_review': previous_review,
            'prev_prod_name': info,
            'link': link,
        }
        prevReviewsList.append(prev_review_entry)
    return prevReviewsList


    #print(clean_br(c))




#jj=extract_previous_reviews_from_user("https://www.prisjakt.nu/minsida.php?a=jn99&do=omdomen&do=opinions")

#df3=pd.DataFrame(jj)
#print(df3) #funkar

#print(df_products['url'])
results_df = pd.DataFrame
def extract_opinions_from_url_list_in_dataframe(dataframe):
    frames=[]
    for url in dataframe['url']:
        print("--")
        print(url)
        html=visit_url(url)
        soup=BeautifulSoup(html, "lxml")

        opinions = soup.find_all(name="li", attrs={'class': 'opinion-row'})
        opinionsList=extract_opinions(opinions)
        df=pd.DataFrame(opinionsList)
        frames.append(df)
    return frames


def save_dataframe_to_csv(frames, name):
    print("Saving dataframe to CSV in" + path)
    result = pd.concat(frames)
    result.to_csv(path + name, encoding='utf-8', index=False)

#TV
#frames=extract_opinions_from_url_list_in_dataframe(df_prod_TV)
#save_dataframe_to_csv(frames,"reviews_TV.csv")

#Headphones
#frames=extract_opinions_from_url_list_in_dataframe(df_prod_headphones)
#save_dataframe_to_csv(frames,"reviews_headphones.csv")

#frames_graphics=extract_opinions_from_url_list_in_dataframe(df_products_graphics)
#save_dataframe_to_csv(frames_graphics, "reviews_graphics.csv")

def run_mining_procedure(input_url, output_csv):
    list=get_list_of_products(input_url)
    df_products = pd.DataFrame(list)
    print(df_products)
    frames = extract_opinions_from_url_list_in_dataframe(df_products)
    save_dataframe_to_csv(frames, output_csv)


cat_monitors="https://www.prisjakt.nu/kategori.php?k=393" #bildskärmar
cat_tablets="https://www.prisjakt.nu/kategori.php?k=1594"
cat_routers="https://www.prisjakt.nu/kategori.php?k=386"
cat_processors="https://www.prisjakt.nu/kategori.php?k=500"
cat_consoles="https://www.prisjakt.nu/kategori.php?k=401"
cat_microphones="https://www.prisjakt.nu/kategori.php?k=663"
cat_hemmabio="https://www.prisjakt.nu/kategori.php?k=2"
cat_smartwatch="https://www.prisjakt.nu/kategori.php?k=1808"
cat_activityband="https://www.prisjakt.nu/kategori.php?k=1760"
cat_pulsewatches="https://www.prisjakt.nu/kategori.php?k=879"

#date of retrieval: 2018-03-10
#run_mining_procedure(cat_laptops, "reviews_laptop.csv")
#run_mining_procedure(cat_monitors, "reviews_monitors.csv")
#run_mining_procedure(cat_tablets, "reviews_tablets.csv")
#run_mining_procedure(cat_routers, "reviews_routers.csv")
#run_mining_procedure(cat_processors, "reviews_processors.csv")
#run_mining_procedure(cat_consoles, "reviews_consoles.csv")
#run_mining_procedure(cat_microphones, "reviews_microphones.csv")
#run_mining_procedure(cat_hemmabio, "reviews_hemmabio.csv")
#run_mining_procedure(cat_smartwatch, "reviews_smartwatch.csv")
#run_mining_procedure(cat_activityband, "reviews_activityband.csv")
#run_mining_procedure(cat_pulsewatches, "reviews_pulsewatches.csv")