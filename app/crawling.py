import json
import os
import re
from multiprocessing import Pool
import django
import requests
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from selenium import webdriver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()
from rooms.models import Rooms, RoomImage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

User = get_user_model()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')

driver = webdriver.Chrome('/Users/sh/Downloads/chromedriver')
city_list = ['서울특별시', '부산광역시', '대구광역시', '대전광역시', '강원도']


# city_list = ['인천광역시']


def source_page_download(page_range):
    """
    source html file download
    :param page_range:
    :return:
    """
    try:
        # 도시 리스트의 목록을 순환하라
        for city in city_list:

            # 현제 페이지가 끝나면 다음페이지로 이동
            for num in range(page_range):
                num += 1
                html_file_root = f'utils/crawling_data/html_source_{city}_{num}.html'
                html_source_url = f'https://www.airbnb.co.kr/s/homes?query={city}&section_offset={num+1}'

                driver.get(html_source_url)
                if os.path.exists(html_file_root):
                    html = open(html_file_root, 'rt').read()
                    print(f'{html} source 읽어오기 성공')
                else:
                    response = driver.page_source
                    html = response
                    html = open(html_file_root, 'wt').write(html)
                    print(f'{html} 저장 성공')
    except Exception as ex:
        print(f'Error 발생 : {ex}')
        driver.quit()


def crawling_parse_save(page_range):
    rooms_id_list = []
    for city in city_list:
        for num in range(page_range):
            num += 1
            html_file_root = f'utils/crawling_data/html_source_{city}_{num}.html'
            html = open(html_file_root, 'rt').read()

            soup = BeautifulSoup(html, 'lxml')
            target = soup.select('div._v72lrv > div > a')

            if os.path.exists(html_file_root):
                for room_id in target:
                    rooms_id_list.append(room_id.get('href'))
            else:
                break

            # print(rooms_id_list, len(rooms_id_list))

    detail_url = 'https://www.airbnb.co.kr'

    for detail in rooms_id_list:
        driver.get(detail_url + detail)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # json file
        bootstrap_data = re.search(
            r'data-hypernova-key="spaspabundlejs" data-hypernova-id=".*?">&lt;!--(.*?)--&gt;</script>',
            html)
        bootstrap_json = json.loads(bootstrap_data.group(1))
        listing_dict = bootstrap_json['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing']

        # image cover list
        rooms_image_list = []
        rooms_image_count = 0
        for image in listing_dict['photos']:
            rooms_image_count += 1
            rooms_image_list.append(image['large'])
            if rooms_image_count == 7:
                break

        # room name
        rooms_name = soup.select_one('h1._1xu9tpch').get_text(strip=True)

        # room price
        try:
            rooms_price_source = soup.select_one('span._doc79r > span').get_text(strip=True)
            # rooms_price_parse = re.findall(r'[^₩\W]', rooms_price_source)
            rooms_price_parse = re.findall('(\d)', rooms_price_source)
            rooms_price = ''.join(rooms_price_parse)
        except:
            rooms_price = '32800'

        # 디테일 페이지 커버 이미지
        try:
            room_detail_image_cover_source = soup.select_one('div._30cuyx5').get('style')
            room_detail_image_cover = re.findall(r'\w*http\S*\w*jpg', room_detail_image_cover_source)[0]
        except:
            room_detail_image_cover_source = soup.select_one('div._1e3y8tsi > img').get('src')
            room_detail_image_cover = re.findall(r'\w*http\S*\w*jpg', room_detail_image_cover_source)[0]

        # host 정보
        rooms_host_id = listing_dict['user']['id']
        rooms_host_first_name = listing_dict['user']['host_name']
        rooms_host_profile_img = listing_dict['user']['profile_pic_path']

        location_tag_source = soup.select_one('div._1hpgssa1 > div:nth-of-type(2) > div').get('data-location')

        if location_tag_source is True:
            # 지역 테그
            location_tag = location_tag_source
        else:
            location_tag = listing_dict['localized_city']

        try:
            # 숙박 인원
            rooms_personnel_source = soup.select_one(
                'div#summary > div > div > div:nth-of-type(2) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > span').get_text(
                strip=True)
            rooms_personnel = re.findall('(\d)', rooms_personnel_source)[0]
        except:
            rooms_personnel = 1
        # 객실 수
        try:
            rooms_amount_source = soup.select_one(
                'div#summary > div > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div:nth-of-type(2) > span').get_text(
                strip=True)
            rooms_amount = re.findall('(\d)', rooms_amount_source)[0]
        except:
            rooms_amount = 1

        # 샤워실 갯수
        try:
            rooms_bathroom_source = soup.select_one(
                'div#summary > div > div > div:nth-of-type(2) > div > div:nth-of-type(4) > div > div:nth-of-type(2) > span').get_text(
                strip=True)
            rooms_bathroom = re.findall('(\d)', rooms_bathroom_source)[0]
        except:
            rooms_bathroom = 1

        try:
            # 침대 갯수
            rooms_bed_source = soup.select_one(
                'div#summary > div > div > div:nth-of-type(2) > div > div:nth-of-type(3) > div > div:nth-of-type(2) > span').get_text(
                strip=True)
            rooms_bed = re.findall('(\d)', rooms_bed_source)[0]
        except:
            rooms_bed = 1
        # 숙소 개요
        rooms_discription = soup.select_one('div#details > div > div > div').get_text(strip=True)

        # 편의 시설
        rooms_facilities_source = soup.select('div._iq8x9is > div > div._qtix31 > div._ni9axhe ')
        rooms_facilities = []
        for facilities in rooms_facilities_source:
            if facilities.select_one('div._ncwphzu') == None:
                continue
            else:
                rooms_facilities.append(facilities.select_one('div._ncwphzu').get_text(strip=True))

        # 숙소 이용규칙
        rooms_rules_source = soup.select('div#house-rules > div > section > div > div._ncwphzu')
        rooms_rules = []
        for rules in rooms_rules_source:
            rooms_rules.append(rules.get_text(strip=True))

        # 주소 목록
        address_list = listing_dict['location_title'].split(', ')
        length = len(address_list)

        # 최소 예약 가능일
        minimum_check_in_duration = listing_dict['min_nights']

        # 환불규정
        refund = '일반 정책 More information 체크인 5일 전까지 예약을 취소하면 에어비앤비 서비스 수수료을 제외한 요금이 환불됩니다.체크인까지 5일이 남지 않은 시점에 예약을 취소하면 첫 1박 요금과 나머지 숙박 요금의 50%는 환불되지 않습니다. 에어비앤비 서비스 수수료는 예약 후 48시간 이내에 취소하고 체크인 전인 경우에만 환불됩니다.'

        # 주소
        try:
            country = address_list[length - 1]
        except:
            country = 'null'

        try:
            citys = address_list[length - 2]
        except:
            citys = 'null'

        try:
            district = listing_dict['localized_city']
        except:
            district = 'null'

        try:
            address1 = address_list[0] if length > 3 else ''
        except:
            address1 = 'null'

        # 위도, 경도
        lat = listing_dict['lat']
        lng = listing_dict['lng']

        user_data = {
            'username': rooms_host_first_name + '@airbnb.net',
            'password': rooms_host_id,
            'first_name': rooms_host_first_name,
            'phone_number': '01000000000',
            'profile_image': rooms_host_profile_img,
        }
        try:
            user = User.objects.get(username=user_data['username'])
        except:
            user = User.objects.create_django_user(**user_data)
            user.is_host = True
            user.profile_image.save('profile_image.png',
                                    ContentFile(requests.get(user_data['profile_image']).content))
            user.save()

        rooms_data = {
            'rooms_name': rooms_name,
            'rooms_type': Rooms.ROOMS_TYPE[1][1],
            'rooms_tag': location_tag,
            'rooms_host': user,
            'days_price': rooms_price,
            'rooms_description': rooms_discription,
            'rooms_amount': rooms_amount,
            'rooms_bed': rooms_bed,
            'rooms_personnel': rooms_personnel,
            'rooms_bathroom': rooms_bathroom,
            'check_in_minimum': minimum_check_in_duration,
            'refund': refund,
            'address_country': country,
            'address_city': citys,
            'address_district': district,
            'address_detail': address1,
            'address_latitude': lat,
            'address_longitude': lng,

        }

        rooms, rooms_created = Rooms.objects.update_or_create(
            rooms_name=rooms_data['rooms_name'],
            defaults=rooms_data,
        )

        rooms.rooms_cover_image.save(room_detail_image_cover,
                                     ContentFile(requests.get(room_detail_image_cover).content))
        # driver.implicitly_wait(3)
        rooms.save()
        num = 1
        for image_add in rooms_image_list:
            num += 1
            # driver.implicitly_wait(3)
            rooms_images = RoomImage.objects.create(room=rooms)
            rooms_images.room_image.save(f'rooms_profile_image{num}.png',
                                         ContentFile(requests.get(image_add).content))
            rooms.save()

        for facilities_add in rooms_facilities:
            rooms.room_facilities.update_or_create(facilities=facilities_add)

        for rules_add in rooms_rules:
            rooms.room_rules.update_or_create(rule_list=rules_add)
            rooms.save()

        if rooms_created is True:
            print(f'{rooms_name} 생성 완료')
        else:
            print(f'{rooms_name} 업데이트 완료')

        print('크롤링 완료')


if __name__ == '__main__':
    pool = Pool(processes=4)
    # pool.map(source_page_download(1))
    pool.map(crawling_parse_save(1))
