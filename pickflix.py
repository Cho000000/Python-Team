# -*- coding: utf-8 -*-
"""PICKFLIX.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ms97HsIbkghuRKKliu4fnFhrLFP3uvQu

# 필요한 라이브러리 설치

이 프로젝트에서는 http 요청과 번역 기능을 위해 필요한 라이브러리를 설치하였다.

requests : TMDB 및 uNoGS API와 통신하기 위한 http 요청 라이브러리

googletrans==4.0.0-rc1 : 컨텐츠 설명을 한국어로 번역하기 위한 google 번역 API 라이브러리
"""

pip install requests googletrans==3.1.0a0

"""# 🎬 TMDB 기반 영화 추천 기능

TMDB API를 사용하여 영화 장르를 불러오고, 인기 영화를 장르별로 필터링하여 추천한다. 포스터 이미지도 함께 출력된다.

"""

import requests
from IPython.display import Image, display

TMDB_API_KEY = 'cba511a5cd8d9c9fdb4d7297c1e555bd'

# TMDB 장르 목록 조회
def get_tmdb_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {'api_key': TMDB_API_KEY, 'language': 'ko-KR'}
    response = requests.get(url, params=params)
    genres = response.json().get('genres', [])
    return {g['name']: g['id'] for g in genres}

# TMDB 인기 영화 + 장르 필터
def fetch_tmdb_movies_by_genre(selected_genre_id):
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {'api_key': TMDB_API_KEY, 'language': 'ko-KR'}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])
    if selected_genre_id:
        results = [m for m in results if selected_genre_id in m.get('genre_ids', [])]
    return results

# TMDB 결과 출력 (포스터 포함)
def display_tmdb_results(movies):
    if not movies:
        print("❌ 해당 장르의 추천 영화가 없습니다.")
        return
    for m in movies:
        title = m.get('title')
        date = m.get('release_date')
        overview = m.get('overview') or '내용 없음'
        poster_path = m.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        print(f"\n🎬 제목: {title}")
        print(f"📅 개봉일: {date}")
        print(f"📝 개요: {overview}")
        if poster_url:
            display(Image(url=poster_url, width=250))
        print("-" * 60)

"""# 📺 uNoGS 기반 넷플릭스 추천 기능

uNoGS API를 통해 넷플릭스에서 특정 장르와 연도 조건에 맞는 컨텐츠를 추천한다. 개요는 Google Translate로 한국어로 번역된다.
"""

from googletrans import Translator

UNOGS_API_KEY = 'e232918b50msh15dc890c9e18b2fp181942jsn078e62dc0b4b'
UNOGS_HOST = 'unogsng.p.rapidapi.com'
translator = Translator()

UNOGS_GENRES = [
    'action', 'adventure', 'animation', 'comedy', 'crime',
    'documentary', 'drama', 'family', 'fantasy', 'horror',
    'romance', 'sci-fi', 'thriller', 'war'
]

# uNoGS 넷플릭스 콘텐츠 추천
def fetch_unogs_recommendations(genre, year, limit=10):
    url = f"https://{UNOGS_HOST}/search"
    headers = {
        "X-RapidAPI-Key": UNOGS_API_KEY,
        "X-RapidAPI-Host": UNOGS_HOST
    }
    params = {
        "query": genre,
        "start_year": year,
        "countrylist": "78",  # 한국
        "limit": 50
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    all_results = response.json().get("results", [])
    final_results = [item for item in all_results if item.get('year') and int(item['year']) >= year]
    return final_results[:limit]

# uNoGS 결과 출력 (포스터 + 번역 포함)
def display_unogs_results(results):
    if not results:
        print("❌ 추천 결과가 없습니다. 조건을 다시 확인해 보세요.")
        return
    for item in results:
        title = item.get('title')
        year = item.get('year')
        synopsis = item.get('synopsis', '')
        translated = translator.translate(synopsis, dest='ko').text if synopsis else '내용 없음'
        img_url = item.get('img')

        print(f"\n🎬 제목: {title} ({year})")
        print(f"📝 개요: {translated}")
        if img_url:
            display(Image(url=img_url, width=250))
        print("-" * 60)

"""# 🔁 사용자 인터페이스(main 함수)

사용자가 메뉴를 선택하고 조건을 입력하면 각 추천 기능을 실행한다.

(메뉴 - 1번 : 영화, 2번 : 넷플릭스)

영화 선택 시 CGV 홈페이지 연결도 지원된다.
"""

import webbrowser

def main():
    print("🎥 영화/OTT 콘텐츠 탐색기")
    print("1. 인기 영화 보기 (TMDB)")
    print("2. 넷플릭스 추천 보기 (uNoGS)")

    choice = input("번호를 선택하세요 (1 또는 2): ").strip()

    if choice == '1':
        genres = get_tmdb_genres()
        print("\n[🎞 장르 목록]")
        for g in genres:
            print(f"- {g}")
        selected = input("추천을 원하는 장르를 입력하세요 (예: 액션): ").strip()
        genre_id = genres.get(selected)
        movies = fetch_tmdb_movies_by_genre(genre_id)
        display_tmdb_results(movies)

        print("\n👉 더 많은 정보를 보시려면 CGV 홈페이지를 방문하세요: https://www.cgv.co.kr/movies/")

    elif choice == '2':
        print("\n[📺 장르 목록 (영문 입력)]")
        print(", ".join(UNOGS_GENRES))
        genre = input("장르 입력 (예: comedy): ").strip().lower()
        year = input("몇 년 이후 콘텐츠를 추천받고 싶으신가요? (예: 2020): ").strip()
        year = int(year) if year.isdigit() else 2020

        print("\n⭐ 한국 넷플릭스에서 시청 가능한 콘텐츠를 추천합니다.")
        results = fetch_unogs_recommendations(genre, year)
        display_unogs_results(results)

    else:
        print("⚠️ 잘못된 입력입니다.")

"""# 🚀 실행

전체 프로그램을 실행한다.
"""

if __name__ == '__main__':
    main()

