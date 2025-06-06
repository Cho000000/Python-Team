# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VkpOfaFSfQ3eyYADd16NSn8WXgZdn1jl

# 필요 라이브러리 및 모듈 불러오기
"""

!pip install requests googletrans==3.1.0a0

import requests
from IPython.display import Image, display
from googletrans import Translator
import webbrowser

"""# API_KEY

TMDB_API_KEY = 'cba511a5cd8d9c9fdb4d7297c1e555bd'

UNOGS_API_KEY = 'e232918b50msh15dc890c9e18b2fp181942jsn078e62dc0b4b'

UNOGS_HOST = 'unogsng.p.rapidapi.com'

# 사용자 인터페이스
"""

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

"""# 실행"""

if __name__ == '__main__':
    main()