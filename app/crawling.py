import json
import os
import re

import django
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model

from selenium import webdriver

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()
User = get_user_model()
driver = webdriver.Chrome('/Users/sh/Downloads/chromedriver')


def crawler():
    city_list = ['서울특별시', '부산광역시', '대구광역시', '인천광역시',
                 '광주광역시', '대전광역시', '울산광역시', '세종특별자치시',
                 '경기도', '강원도']

    # 도시 리스트의 목록을 순환하라
    for city in city_list:

        # 현제 페이지가 끝나면 다음페이지로 이동
        for num in range(10):
            num += 1
            url = f'https://www.airbnb.co.kr/s/homes?query={city}&section_offset={num+1}'
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            target = soup.select('div._v72lrv > div > a')
            rooms_id_list = []

            for room_id in target:
                rooms_id_list.append(room_id.get('href'))

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

                # 디테일 페이지 커버 이미지
                room_detail_image_cover_source = soup.select_one('div._30cuyx5').get('style')
                room_detail_image_cover = re.findall(r'\w*http\S*\w*jpg', room_detail_image_cover_source)[0]

                # host 정보
                rooms_host_id = listing_dict['user']['id']
                rooms_host_first_name = listing_dict['user']['host_name']
                rooms_host_profile_img = listing_dict['user']['profile_pic_path']

                # 지역 테그
                location_tag = soup.select_one('div._1hpgssa1 > div:nth-of-type(2) > div').get('data-location')

                # 숙박 인원
                rooms_personnel_source = soup.select_one(
                    'div#summary > div > div > div:nth-of-type(2) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > span').get_text(
                    strip=True)
                rooms_personnel = re.findall('(\d)', rooms_personnel_source)[0]

                # 객실 수
                try:
                    rooms_amount_source = soup.select_one(
                        'div#summary > div > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div:nth-of-type(2) > span').get_text(
                        strip=True)
                    rooms_amount = re.findall('(\d)', rooms_amount_source)[0]
                except:
                    rooms_amount = 1

                # 샤워실 갯수
                rooms_bathroom_source = soup.select_one(
                    'div#summary > div > div > div:nth-of-type(2) > div > div:nth-of-type(4) > div > div:nth-of-type(2) > span').get_text(
                    strip=True)
                rooms_bathroom = re.findall('(\d)', rooms_bathroom_source)[0]

                # 침대 갯수
                rooms_bed_source = soup.select_one(
                    'div#summary > div > div > div:nth-of-type(2) > div > div:nth-of-type(3) > div > div:nth-of-type(2) > span').get_text(
                    strip=True)
                rooms_bed = re.findall('(\d)', rooms_bed_source)[0]

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

                # 주소
                country = address_list[length - 1]
                city = address_list[length - 2]
                district = listing_dict['localized_city']
                address1 = address_list[0] if length > 3 else ''

                # 위도, 경도
                lat = listing_dict['lat']
                lng = listing_dict['lng']

            print('detail cover image :', room_detail_image_cover)
            print('room host id :', rooms_host_id)
            print('room host first name :', rooms_host_first_name)
            print('room host profile image :', rooms_host_profile_img)


if __name__ == '__main__':
    crawler()
