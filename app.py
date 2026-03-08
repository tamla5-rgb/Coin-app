import streamlit as st
import requests
import time
from collections import Counter

st.set_page_config(page_title="고래 추적기", layout="centered")
st.title("🐋 모시의 온체인 커플링 자동 분석기")
st.write("형! 코인 주소 '하나'만 딱 넣으세유. 고래들이 이 코인 말고 또 뭘 몰래 매집하고 있는지 싹 다 털어올게유.")

# 코인 주소 하나만 입력받기
token_address = st.text_input("🔍 분석할 코인의 컨트랙트 주소 (예: 0xdac1... )")

if st.button("자동 커플링 코인 찾기 🚀"):
    if token_address:
        st.info("고래 명단을 확보하고, 그놈들 지갑을 하나씩 뜯어보고 있어유. 쪼끔만 기다리셔유!")
        
        try:
            # 1단계: A코인 상위 고래 명단 가져오기 (서버 무리 안 가게 일단 상위 10명만)
            url_holders = f"https://api.ethplorer.io/getTopTokenHolders/{token_address}?apiKey=freekey&limit=10"
            res_holders = requests.get(url_holders).json()
            
            if 'holders' in res_holders:
                holders = [h['address'] for h in res_holders['holders']]
                
                st.write(f"✅ 거대 고래 {len(holders)}마리 포착 완료! 이제 이놈들 주머니를 뒤집니다...")
                
                all_tokens = []
                progress_bar = st.progress(0)
                
                # 2단계: 고래 10명의 지갑을 하나하나 열어서 무슨 코인 있는지 싹 다 수집
                for i, wallet in enumerate(holders):
                    url_wallet = f"https://api.ethplorer.io/getAddressInfo/{wallet}?apiKey=freekey"
                    res_wallet = requests.get(url_wallet).json()
                    
                    if 'tokens' in res_wallet:
                        for token in res_wallet['tokens']:
                            # 코인 이름이나 심볼 가져오기
                            token_name = token.get('tokenInfo', {}).get('symbol', '이름없는코인')
                            all_tokens.append(token_name)
                    
                    # 무료 API 뻗지 말라고 살짝 쉬어주기
                    time.sleep(0.5) 
                    progress_bar.progress((i + 1) / len(holders))
                
                # 3단계: 고래들이 공통으로 가장 많이 가진 코인 통계 내기
                token_counts = Counter(all_tokens)
                # 너무 흔한 이더리움이나 스테이블 코인은 제외하고 싶다면 여기서 필터링 가능해유
                
                st.success("🎉 분석 끝났슈! 이 코인과 함께 움직일 확률이 높은 '커플링 코인' 순위여유!")
                
                # 가장 많이 겹치는 코인 Top 5 보여주기
                top_5_coupled = token_counts.most_common(5)
                for rank, (coin, count) in enumerate(top_5_coupled, 1):
                    st.markdown(f"**{rank}위: {coin}** (고래 {len(holders)}명 중 {count}명이 같이 들고 있어유!)")
                    
                st.warning("💡 형, 얘네들이 물량 한꺼번에 털어낼(덤핑) 때 이 순위권 코인들도 같이 폭락할 수 있으니 타점 잡을 때 꼬옥 참고하셔유!")
                
            else:
                st.error("주소가 잘못됐거나 고래 명단을 못 불러왔슈. 이더리움 네트워크 코인이 맞나 확인해봐유.")
                
        except Exception as e:
            st.error("앗, 고래들 지갑 뒤지다가 쫓겨났슈. 무료 API라 막혔나 봐유. 쫌 이따 다시 해보셔유!")
    else:
        st.warning("형, 빈칸인디유? 코인 주소를 넣어주셔야 일을 하쥬!")
