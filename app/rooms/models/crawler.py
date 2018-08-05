import os
from django.conf import settings
import django
from django.contrib.auth import get_user_model
from selenium import webdriver
from bs4 import BeautifulSoup

django.setup()
User = get_user_model()
driver = webdriver.Chrome('/Users/sh/Downloads')
#
#
# def crawler():
#     city_list = ['서울특별시', '부산광역시', '대구광역시', '인천광역시',
#                  '광주광역시', '대전광역시', '울산광역시', '세종특별자치시',
#                  '경기도', '강원도']
#
#     num = 0
#     if num != 10:
#         num += 1
#         for city in city_list:
#             count = 0
#             for num in range(10):
#                 url = f'https://www.airbnb.co.kr/s/homes?query={city}&section_offset={num+1}'
#                 driver.get(url)
