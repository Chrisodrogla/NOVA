import pandas as pd
from datetime import date
import time
from selenium import webdriver
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json

# Set up Chrome WebDriver with custom options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--display=:99")  # Set display to Xvfb

# Google Sheets setup
SHEET_ID = '1Y-h3p_iHqvOXRkM1opCzo6tlCOM1mLzbaOJ57VnaFU8'
SHEET_NAME1 = 'Review'  # Sheet to clear data below header and write new data
SHEET_NAME2 = 'History_Review'  # Sheet to append new data without modifying existing

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# List of websites to scrape
link_websites = [
"https://www.airbnb.com/rooms/7146166",
"https://www.airbnb.com/rooms/796474546246084466",
"https://www.airbnb.com/rooms/37941371",
"https://www.airbnb.com/rooms/994897495772736141",
"https://www.airbnb.com/rooms/53642812",
"https://www.airbnb.com/rooms/760854242202697132",
"https://www.airbnb.com/rooms/51465037",
"https://www.airbnb.com/rooms/53699752",
"https://www.airbnb.com/rooms/1050859485309789128",
"https://www.airbnb.com/rooms/53542247",
"https://www.airbnb.com/rooms/892145528929581566",
"https://www.airbnb.com/rooms/29828888",
"https://www.airbnb.com/rooms/1075808915500918249",
"https://www.airbnb.com/rooms/639093225461069229",
"https://www.airbnb.com/rooms/1034850921926296677",
"https://www.airbnb.com/rooms/30374855",
"https://www.airbnb.com/rooms/862225236403589050",
"https://www.airbnb.com/rooms/1095021360351651647",
"https://www.airbnb.com/rooms/31572231",
"https://www.airbnb.com/rooms/805787704495151180",
"https://www.airbnb.com/rooms/1042003756371097226",
"https://www.airbnb.com/rooms/31041744",
"https://www.airbnb.com/rooms/724751471621735873",
"https://www.airbnb.com/rooms/938322820404201166",
"https://www.airbnb.com/rooms/842715702282301234",
"https://www.airbnb.com/rooms/51464198",
"https://www.airbnb.com/rooms/607805837215056615",
"https://www.airbnb.com/rooms/29057616",
"https://www.airbnb.com/rooms/28986286",
"https://www.airbnb.com/rooms/30569087",
"https://www.airbnb.com/rooms/30587914",
"https://www.airbnb.com/rooms/726797791762309974",
"https://www.airbnb.com/rooms/33297252",
"https://www.airbnb.com/rooms/745517798832633224",
"https://www.airbnb.com/rooms/783438310557347832",
"https://www.airbnb.com/rooms/1079900607064150533",
"https://www.airbnb.com/rooms/757905515382248564",
"https://www.airbnb.com/rooms/21879855",
"https://www.airbnb.com/rooms/557931274468753963",
"https://www.airbnb.com/rooms/563061034458193391",
"https://www.airbnb.com/rooms/897748901350874764",
"https://www.airbnb.com/rooms/607996043990435730",
"https://www.airbnb.com/rooms/655851097480261248",
"https://www.airbnb.com/rooms/53935222",
"https://www.airbnb.com/rooms/54003121",
"https://www.airbnb.com/rooms/41926624",
"https://www.airbnb.com/rooms/818808980294592759",
"https://www.airbnb.com/rooms/910243374096737518",
"https://www.airbnb.com/rooms/888535082546615005",
"https://www.airbnb.com/rooms/53905490",
"https://www.airbnb.com/rooms/805787804668716793",
"https://www.airbnb.com/rooms/51444791",
"https://www.airbnb.com/rooms/1076240628121073255",
"https://www.airbnb.com/rooms/1031868725939524364",
"https://www.airbnb.com/rooms/954991868458915427",
"https://www.airbnb.com/rooms/1142996183974898781",
"https://www.airbnb.com/rooms/1165972751097834093",
"https://www.airbnb.com/rooms/570359369689296789",
"https://www.airbnb.com/rooms/1113219669718192703",
"https://www.airbnb.com/rooms/1136360425762834414",
"https://www.airbnb.com/rooms/946617655515855386",
"https://www.airbnb.com/rooms/834175163702868485",
"https://www.airbnb.com/rooms/49612095",
"https://www.airbnb.com/rooms/910164420748216135",
"https://www.airbnb.com/rooms/990641443060144144",
"https://www.airbnb.com/rooms/826137636518983708",
"https://www.airbnb.com/rooms/949385102419491356",
"https://www.airbnb.com/rooms/760969744755324887",
"https://www.airbnb.com/rooms/1076968397509164945",
"https://www.airbnb.com/rooms/1050127081836690246",
"https://www.airbnb.com/rooms/26005379",
"https://www.airbnb.com/rooms/786329086863037403",
"https://www.airbnb.com/rooms/51963573",
"https://www.airbnb.com/rooms/37932879",
"https://www.airbnb.com/rooms/1076647410356569199",
"https://www.airbnb.com/rooms/48318526",
"https://www.airbnb.com/rooms/37938829",
"https://www.airbnb.com/rooms/904360106135155927",
"https://www.airbnb.com/rooms/803651754039471916",
"https://www.airbnb.com/rooms/40083939",
"https://www.airbnb.com/rooms/866663572875064288",
"https://www.airbnb.com/rooms/1076647429394038254",
"https://www.airbnb.com/rooms/25396298",
"https://www.airbnb.com/rooms/26521913",
"https://www.airbnb.com/rooms/23190272",
"https://www.airbnb.com/rooms/838459330070610028",
"https://www.airbnb.com/rooms/947760909472876352",
"https://www.airbnb.com/rooms/861683985433638341",
"https://www.airbnb.com/rooms/933446278486516018",
"https://www.airbnb.com/rooms/800697914487131964",
"https://www.airbnb.com/rooms/50212538",
"https://www.airbnb.com/rooms/783452456583177550",
"https://www.airbnb.com/rooms/1131831559412513348",
"https://www.airbnb.com/rooms/981120989536057134",
"https://www.airbnb.com/rooms/860831202321728447",
"https://www.airbnb.com/rooms/978166940536444449",
"https://www.airbnb.com/rooms/1042003712113364927",
"https://www.airbnb.com/rooms/604398018806882504",
"https://www.airbnb.com/rooms/1085699716941563659",
"https://www.airbnb.com/rooms/782603780940799545",
"https://www.airbnb.com/rooms/945044294292549232",
"https://www.airbnb.com/rooms/1131831539618072124",
"https://www.airbnb.com/rooms/944920764405587161",
"https://www.airbnb.com/rooms/1030538591333449115",
"https://www.airbnb.com/rooms/49343702",
"https://www.airbnb.com/rooms/990031193822434771",
"https://www.airbnb.com/rooms/957888455526887416",
"https://www.airbnb.com/rooms/1050821870682745148",
"https://www.airbnb.com/rooms/805787737386091039",
"https://www.airbnb.com/rooms/777659652608777776",
"https://www.airbnb.com/rooms/731243523553958261",
"https://www.airbnb.com/rooms/782703665616562456",
"https://www.airbnb.com/rooms/934235039382631269",
"https://www.airbnb.com/rooms/1065769680885195405",
"https://www.airbnb.com/rooms/1027936391154196841",
"https://www.airbnb.com/rooms/973875354304828353",
"https://www.airbnb.com/rooms/1008840674146919720",
"https://www.airbnb.com/rooms/35681371",
"https://www.airbnb.com/rooms/705127962698567441",
"https://www.airbnb.com/rooms/756641747143688292",
"https://www.airbnb.com/rooms/816076415461957447",
"https://www.airbnb.com/rooms/755163388432693249",
"https://www.airbnb.com/rooms/786951700961595417",
"https://www.airbnb.com/rooms/1036993779134062225",
"https://www.airbnb.com/rooms/853588629391260401",
"https://www.airbnb.com/rooms/999220572832362368",
"https://www.airbnb.com/rooms/908744644752740153",
"https://www.airbnb.com/rooms/1047224654410054017",
"https://www.airbnb.com/rooms/873999899483756758",
"https://www.airbnb.com/rooms/873817166721037429",
"https://www.airbnb.com/rooms/939783099662189198",
"https://www.airbnb.com/rooms/955789623469064247",
"https://www.airbnb.com/rooms/953562785617772309",
"https://www.airbnb.com/rooms/887899763516426190",
"https://www.airbnb.com/rooms/1021989674443871557",
"https://www.airbnb.com/rooms/1039248371267406725",
"https://www.airbnb.com/rooms/924821108022403394",
"https://www.airbnb.com/rooms/968187624157610437",
"https://www.airbnb.com/rooms/1022580739268065943",
"https://www.airbnb.com/rooms/1148726239902098576",
"https://www.airbnb.com/rooms/1015363142553312848",
"https://www.airbnb.com/rooms/1106482531167089383",
"https://www.airbnb.com/rooms/1097201811717296445",
"https://www.airbnb.com/rooms/1009422704218853107",
"https://www.airbnb.com/rooms/1008612218258117806",
"https://www.airbnb.com/rooms/962985257513035512",
"https://www.airbnb.com/rooms/1076780580862135211",
"https://www.airbnb.com/rooms/834142836698095871",
"https://www.airbnb.com/rooms/1050195214810043236",
"https://www.airbnb.com/rooms/1097369463318457469",
"https://www.airbnb.com/rooms/592728131979157301",
"https://www.airbnb.com/rooms/886831553748022682",
"https://www.airbnb.com/rooms/975448512532210038",
"https://www.airbnb.com/rooms/995763813290807634",
"https://www.airbnb.com/rooms/1047224676448180120",
"https://www.airbnb.com/rooms/1103288077320277710",
"https://www.airbnb.com/rooms/993606019538483430",
"https://www.airbnb.com/rooms/623800381886559424",
"https://www.airbnb.com/rooms/950908727734458240",
"https://www.airbnb.com/rooms/47069678",
"https://www.airbnb.com/rooms/29735607",
"https://www.airbnb.com/rooms/1080557902929477424",
"https://www.airbnb.com/rooms/1024760658855576495",
"https://www.airbnb.com/rooms/50879442",
"https://www.airbnb.com/rooms/897748881007679334",
"https://www.airbnb.com/rooms/47054188",
"https://www.airbnb.com/rooms/34473610",
"https://www.airbnb.com/rooms/1153791334221199409",
"https://www.airbnb.com/rooms/53830234",
"https://www.airbnb.com/rooms/698162509016402967",
"https://www.airbnb.com/rooms/894996626436696750",
"https://www.airbnb.com/rooms/877628153832743245",
"https://www.airbnb.com/rooms/785631343553027555",
"https://www.airbnb.com/rooms/53951403",
"https://www.airbnb.com/rooms/988528048108079239",
"https://www.airbnb.com/rooms/53738223",
"https://www.airbnb.com/rooms/715276271341771907",
"https://www.airbnb.com/rooms/33988930",
"https://www.airbnb.com/rooms/625973762731219742",
"https://www.airbnb.com/rooms/1158812597782935422",
"https://www.airbnb.com/rooms/46104590",
"https://www.airbnb.com/rooms/43679726",
"https://www.airbnb.com/rooms/1045634226433291187",
"https://www.airbnb.com/rooms/25129364",
"https://www.airbnb.com/rooms/31650019",
"https://www.airbnb.com/rooms/953562785617772309",
"https://www.airbnb.com/rooms/20842811",
"https://www.airbnb.com/rooms/53188505",
"https://www.airbnb.com/rooms/48939589",
"https://www.airbnb.com/rooms/1060335247580958306",
"https://www.airbnb.com/rooms/897963012858385842",
"https://www.airbnb.com/rooms/25548573",
"https://www.airbnb.com/rooms/1118085675466754285",
"https://www.airbnb.com/rooms/1118085697437915657",
"https://www.airbnb.com/rooms/33990781",
"https://www.airbnb.com/rooms/1118748453825614028",
"https://www.airbnb.com/rooms/32358587",
"https://www.airbnb.com/rooms/1175583169188948074",
"https://www.airbnb.com/rooms/28105157",
"https://www.airbnb.com/rooms/874576033916222052",
"https://www.airbnb.com/rooms/1042003843639500595",
"https://www.airbnb.com/rooms/52617221",
"https://www.airbnb.com/rooms/965959236038176496",
"https://www.airbnb.com/rooms/1014534960594628050",
"https://www.airbnb.com/rooms/34336916",
"https://www.airbnb.com/rooms/36668728",
"https://www.airbnb.com/rooms/1177271590148127455",
"https://www.airbnb.com/rooms/33067595",
"https://www.airbnb.com/rooms/54081691",
"https://www.airbnb.com/rooms/33073575",
"https://www.airbnb.com/rooms/955107616627638300",
"https://www.airbnb.com/rooms/940638312300885619",
"https://www.airbnb.com/rooms/823155460080163160",
"https://www.airbnb.com/rooms/874058281090322337",
"https://www.airbnb.com/rooms/881137986854850087",
"https://www.airbnb.com/rooms/881138921809210265",
"https://www.airbnb.com/rooms/889232271666476805",
"https://www.airbnb.com/rooms/1127057220252352925",
"https://www.airbnb.com/rooms/1127061396214828918",
"https://www.airbnb.com/rooms/985576433639311786",
"https://www.airbnb.com/rooms/751390625816660039",
"https://www.airbnb.com/rooms/1049393737893008941",
"https://www.airbnb.com/rooms/763115309438666807",
"https://www.airbnb.com/rooms/720376585440505157",
"https://www.airbnb.com/rooms/675364370940591304",
"https://www.airbnb.com/rooms/971038139081369306",
"https://www.airbnb.com/rooms/765333675463864639",
"https://www.airbnb.com/rooms/1127068754740193330",
"https://www.airbnb.com/rooms/697219047472579604",
"https://www.airbnb.com/rooms/985491774123385924",
"https://www.airbnb.com/rooms/959474348410918154",
"https://www.airbnb.com/rooms/1108970575915708107",
"https://www.airbnb.com/rooms/764807706737137386",
"https://www.airbnb.com/rooms/1030522085440736837",
"https://www.airbnb.com/rooms/969628264375924718",
"https://www.airbnb.com/rooms/45549853",
"https://www.airbnb.com/rooms/1076275611613180477",
    # Add more URLs as needed
]

DateToday = date.today()
UpdatedAt = DateToday.strftime("%Y-%m-%d")

data = []
for website in link_websites:
    driver = webdriver.Chrome(options=options)
    driver.get(website)
    time.sleep(5)
    try:
        click_x = driver.find_element("xpath", """/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button""").click()
    except:
        pass    
    try:
        listing_id = website.split('/')[-1]
    except:
        listing_id = ""

    try:
        review_counts = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div[2]/span/span[3]""").get_attribute("innerText").strip(' reviews')
    except:
        try:
            
            review_counts = driver.find_element("xpath", """//*[@id="react-application"]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[12]/div/div/div/div[2]/div/section/div[1]/div[1]/span/h2/div//span""").text.strip(' reviews')
            
        except: 
            review_counts = ""
    try:
        AirbnbBadge1 = driver.find_element("xpath", """//div[@data-plugin-in-point-id='GUEST_FAVORITE_BANNER']""")
        if AirbnbBadge1:
            AirbnbBadge = "Guest favorite"
        else:
            AirbnbBadge = "Guest favorite"
    except:
        AirbnbBadge = ''
            
    try:
        star_reviews = driver.find_element("xpath", """//span[@class="_12si43g"]""").get_attribute("innerText").strip(" ·")
    except:
        
        try:
            star_reviews = driver.find_element("xpath", """//div[@class="r1lutz1s atm_c8_o7aogt atm_c8_l52nlx__oggzyc dir dir-ltr"]""").get_attribute("innerText").strip(" ·")
        except:
                try:
                    star_reviews = driver.find_element("xpath", """//span[@class="_1m3uwyl"]""").get_attribute("innerText").strip(" ·")
                except:
                    star_reviews = "No reviews yet"

    try:
        hosted_by = driver.find_element("xpath", """//div[@class="t1pxe1a4 atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_9dzvea dir dir-ltr"]""").get_attribute("innerText").replace('Hosted by','')
    except:
        hosted_by = ""

    try:
        CohostName = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[2]/div[1]/ul/li[1]/span""").get_attribute("innerText")
    except:
        CohostName = ""
    try:
        Cohost2nd = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[2]/div[1]/ul/li[2]/span""").get_attribute("innerText")
    except:
        Cohost2nd = ""
        
    try:
        Cleanliness = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Accuracy = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[3]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Checkin = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[4]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Communication = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[5]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Location = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[6]/div/div/div[2]/div[2]""").get_attribute("innerText")
        Value = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[2]/div/div/div[3]/div/div/div/div/div[7]/div/div/div[2]/div[2]""").get_attribute("innerText")
    except:
        Cleanliness = ''
        Accuracy = ''
        Checkin = ''
        Communication = ''
        Location = ''
        Value = ''
        
    try:
        Title = driver.find_element("xpath", """//div[@data-plugin-in-point-id="TITLE_DEFAULT"]//h1""").get_attribute("innerText")
    except:
        Title = ''


    try:
        click_x = driver.find_element("xpath", """/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button""").click()
    except:
        pass       




    
    try:
        ResponseRate = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]""").text
    except:

        try:
            ResponseRate = driver.find_element("xpath", """//*[@id="react-application"]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[13]/div/div/div/div/section/div/div/div[2]/div[5]/div/div[2]/div[1]""").text
        except:
            try:                                           

                ResponseRate = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[5]/div/div[2]/div[1]""").text
            except:
                ResponseRate = ''
                
                
    if ResponseRate == '' and Title != '':
        

        ResponseRate = 'Response rate: 99%'
    else:
        pass



    try:

        ResponseTime = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[2]/div[2]/div/div[2]/div[2]""").text
    except:

        try:
            ResponseTime = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[6]/div/div/div/div[2]/section/div[2]/div/div/div[5]/div/div[2]/div[2]""").text
        except:
            try:                                           

                ResponseTime = driver.find_element("xpath", """//*[@id="react-application"]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[13]/div/div/div/div/section/div/div/div[2]/div[5]/div/div[2]/div[2]""").text
            except:
                ResponseTime = ''

    if ResponseTime == '' and Title != '':
        ResponseTime = 'Responds within an hour'
    else:
        pass





    try:
        LastReviewName = driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[3]/div/div/div[1]//h3""").get_attribute("innerText")
    except:

        try:
            LastReviewName = driver.find_element("xpath", """//*[@id="review_1168908391037552156_title"]/h3""").get_attribute("innerText")
        except:                                              
            try:                                           

                LastReviewName = driver.find_element("xpath", """/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[3]/div/div/div[1]/div/div[1]/div[1]/div/div[1]/h3""").get_attribute("innerText")
            except:
                LastReviewName = ''


    try:
        LastReviewStar = driver.find_element("xpath", """(//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[3]/div/div/div[1]//span)[1]""").get_attribute("innerText")
    except:

        try:
            LastReviewStar = driver.find_element("xpath", """//*[@id="react-application"]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[12]/div/div/div/div/div/section/div[2]/div/div/ul/li[1]/div/div/div[1]/div[1]/div[1]/span""").get_attribute("innerText")
        except:                                              
            try:                                           

                LastReviewStar= driver.find_element("xpath", """//*[@id="site-content"]/div/div[1]/div[4]/div/div/div/div[2]/div/section/div[3]/div/div/div[1]/div/div[1]/div[2]/div[1]/span""").get_attribute("innerText")
            except:
                LastReviewStar = ''


    driver.quit()



    data.append({
        "Listing ID": listing_id,
        "Score": star_reviews,
        "ReviewNumber": review_counts,
        "AirbnbBadge": AirbnbBadge,
        "MainHost": hosted_by,
        "CohostName": CohostName,
        "Cohost2nd": Cohost2nd,
        "Original_URL": website,
        "Cleanliness": Cleanliness,
        "Accuracy": Accuracy,
        "Checkin": Checkin,
        "Communication": Communication,
        "Location": Location,
        "Value": Value,
        "Title": Title,
        "ResponseRate": ResponseRate,
        "ResponseTime": ResponseTime,
        "LastReviewName": LastReviewName,
        "LastReviewStar": LastReviewStar,
        "UpdatedAt": UpdatedAt,
    })

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Clear all data below header in the "Review" sheet
service.spreadsheets().values().clear(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2:Z"
).execute()

# Write new data to the "Review" sheet starting from row 2
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2",
    valueInputOption="RAW",
    body={"values": df.values.tolist()}
).execute()

# Append new data to the "History_Review" sheet
service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME2}!A1",
    valueInputOption="RAW",
    body={"values": df.values.tolist()}
).execute()
