import requests
import time
import json
from fake_useragent import UserAgent

usr_agnt = UserAgent()
print(usr_agnt.random)
heads = {'user-agent':f'{usr_agnt.random}'}

cookies = {'Device-Id':'rMCccRj1cCguxFjIfSNl',
           'P_INFO':'7-9154469986|1702111728|1|netease_buff|00&99|null&null&null#RU&null#10#0|&0||7-9154469986',
           'remember_me':'U1077483481|O9lPJtMLz9VLGBfmfXoHljspMWVOTjWx',
           'Locale-Supported':'ru',
           'game':'csgo',
           'session':'1-PETT71mfF_xo3wez01m1QskXRsNaRpiJK5TGuXLPKgoY2029488257',
           'csrf_token':'ImFhZTEwODgxOGQ1YTEwZDEyMzRiMGJiNzQ3OWZlN2FmZWRiY2FmMDki.GFW7lg.Fxy5R8EIpksa7A1ooo9hzcFlo7Y'}


gun_id = 886981


def find(weapon_type):
    id_data_dic = {}
    foundedw = {}
    with open('buffids.txt', 'r', encoding='utf-8') as f:
        id_data = f.readlines()
    for k in id_data:
        strip = k.partition(';')
        id_data_dic[strip[0].rstrip()] = {'type':strip[2].partition('|')[0].rstrip(),'name':strip[2].partition('|')[2].rstrip().lstrip()}
    ids = []
    for k, v in id_data_dic.items():
        weapon = weapon_type.split(" ",1)
        if (weapon[0].lower() == v['type'].lower()) and (weapon[1].lower() in v['name'].lower()):
            ids.append(k)
            print((k,v))
        else:
            continue
    print(ids)
    return ids

def initialize(max_page_numbers = 1, gun_id = 886981):
    k = 1
    page_numbers = requests.get('https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=' + str(gun_id) + '&page_num='+str(k)+'&sort_by=default&mode=&allow_tradable_cooldown=1&extra_tag_ids=non_empty&wearless_sticker=1&_=1', headers=heads, cookies=cookies)
    total = page_numbers.json().get('data').get('total_page')
    while total != False:
        if total == 10:
            k = k+9
            page_numbers = requests.get('https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=' + str(gun_id) + '&page_num='+str(k)+'&sort_by=default&mode=&allow_tradable_cooldown=1&extra_tag_ids=non_empty&wearless_sticker=1&_=1', headers = heads, cookies = cookies)
            total = page_numbers.json().get('data').get('total_page')
        elif ((total-10)%4==0) and (total < max_page_numbers):
            time.sleep(1)
            page_numbers = requests.get('https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=' + str(gun_id) + '&page_num='+str(k)+'&sort_by=default&mode=&allow_tradable_cooldown=1&extra_tag_ids=non_empty&wearless_sticker=1&_=1', headers = heads, cookies = cookies)
            try:
                total = page_numbers.json().get('data').get('total_page')
            except:
                break
            k = k+8
        else:
            break
        print("total pages:" + str(total))
        print("---------------")
    return total

def min_price(gun_id = 886981):
    page = requests.get('https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=' + str(gun_id) + '&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1', headers=heads, cookies=cookies)
    res = page.json()
    data = res.get('data')
    name = data.get('goods_infos').get(str(gun_id)).get('name')
    items = data.get('items')
    return items[0].get('price')


def collect(gun_id, weapon_min_price, num_of_all_pages):
    x=1
    final_result = []
    for k in range(1, num_of_all_pages):
        req = requests.Session()
        page = req.get('https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=' + str(gun_id) + '&page_num=' + str(k) + '&sort_by=default&mode=&allow_tradable_cooldown=1&extra_tag_ids=non_empty&wearless_sticker=1', headers=heads, cookies=cookies)
        res = page.json()
        data = res.get('data')
        name = data.get('goods_infos').get(str(gun_id)).get('name')
        items = data.get('items')
        for i in items:
            price = i.get('price')
            classid = i.get('asset_info').get('classid')
            instanceid = i.get('asset_info').get('instanceid')
            assetid = i.get('asset_info').get('assetid')
            contextid = i.get('asset_info').get('contextid')
            sell_order_id = i.get('id')
            stickers = i.get('asset_info').get('info').get('stickers')
            link = 'https://buff.163.com/api/market/item_desc_detail?appid=730&classid=' + str(classid) + '&instanceid=' + str(instanceid) + '&origin=selling-list&assetid=' + str(assetid) + '&contextid=' + str(contextid) + '&sell_order_id=' + str(sell_order_id) + '&_1'
            stick_page = req.get(link, headers=heads, cookies=cookies)
            page_json = stick_page.json()
            stickers = page_json.get('data').get('stickers')
            dat_link = page_json.get('data')
            qrlink = dat_link.get('qr_code_url')
            pic = dat_link.get('content_pic')
            prices = []
            for k in stickers:
                stick_name = k.get("name")
                stick_id = k.get('goods_id')
                lowest_price = k.get('sell_reference_price')
                prices.append(float(lowest_price))
            all_stickers_price = float(sum(prices))
            prices.clear()
            profit_proc = 100 - (float(price) / (float(weapon_min_price) + all_stickers_price)) * 100

            if ((float(weapon_min_price) + all_stickers_price) > float(price)) and (profit_proc > 48):
                if qrlink == "":
                    continue
                else:
                    print("⭕➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖⭕")
                    print("🟢Name: " + name)
                    print("Price: " + str(price) + "¥; " + str(float(price) * 12.8) + "₽\n")
                    print("Price without stickers: " + str(weapon_min_price) + "¥; " + str(float(weapon_min_price) * 12.8) + "₽\n")
                    print("Stickers price: " + str(all_stickers_price) + "¥; " + str(all_stickers_price * 12.8) + "₽\n")
                    print("💲PROFIT💲: " + str(int(profit_proc)) + "%")
                    print("В Юанях: " + str(int(profit_proc * (float(weapon_min_price) + float(all_stickers_price)) * 0.01))+"¥")
                    print("В Рублях: " + str(int(profit_proc * (float(weapon_min_price) + float(all_stickers_price)) * 0.01 * 12.8))+ "₽")

                    overprice = float(price) - float(weapon_min_price)

                    print("Переплата (и процент от цены наклеек): " + str(overprice) + " (" + str(int(overprice / float(all_stickers_price) * 100)) + "%)\n")
                    print('Link:\n' + str(qrlink) + '\n')
                    
                    fin_dic = {'pic':pic,
                               'Name':name, 
                               'Price(Y)': price,
                               'Price(rub)':str(float(price) * 12.8),
                               'Price without stickers(Y)':str(weapon_min_price),
                               'Stickers price':str(int(all_stickers_price)),
                               'Profit':str(int(profit_proc)),
                               'Overprice(Y)':str(int(overprice)),
                               'Overprice(rub)':str(overprice*12.8),
                               'Overprice(proc)':str(int(overprice / float(all_stickers_price) * 100)),
                               'Link':str(qrlink)
                              }
                    
                    final_result.append(fin_dic)
        time.sleep(1)
            
    with open('result.json', 'w') as file:
        json.dump(final_result, file, indent=4)
    return final_result



#wp_min_price = min_price()
#run = collect(886981,weapon_min_price=wp_min_price)
#print(run)


