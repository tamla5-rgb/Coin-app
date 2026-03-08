import streamlit as st
import requests
import time
from collections import Counter

st.set_page_config(page_title="고래 추적기", layout="centered")
st.title("🐋 모시의 온체인 커플링 자동 분석기 (필터링 장착!)")
st.write("형! 코인 주소 '하나'만 딱 넣으세유. 뻔한 현금 코인은 싹 빼고 고래들이 몰래 매집하는 찐 알트코인만 발라올게유.")

# 코인 주소 하나만 입력받기
token_address = st.text_input("🔍 분석할 코인의 컨트랙트 주소")

# 👉 요기가 핵심이에유! 무시할 '현금성 코인' 블랙리스트!
EXCLUDE_LIST = ['USDT', 'USDC', 'DAI', 'BUSD', 'ETH', 'WETH', 'BTC', 'WBTC', 'ERC20', 'TUSD', 'USDD']

if st.button("찐 커플링 코인 찾기 🚀"):
    if token_address:
        st.info("고래 명단 확보하고 쓸데없는 동전들 걸러내는 중이유. 쫌만 기다려봐유!")
        
        try:
            # 1단계: A코인 상위 고래 명단 가져오기
            url_holders = f"https://api.ethplorer.io/getTopTokenHolders/{token_address}?apiKey=freekey&limit=10"
            res_holders = requests.get(url_holders).json()
            
            if 'holders' in res_holders:
                holders = [h['address'] for h in res_holders['holders']]
                st.write(f"✅ 거대 고래 {len(holders)}마리 주머니 탈탈 터는 중...")
                
                all_tokens = []
                progress_bar = st.progress(0)
                
                # 2단계: 고래 지갑 열어서 코인 이름 수집
                for i, wallet in enumerate(holders):
                    url_wallet = f"https://api.ethplorer.io/getAddressInfo/{wallet}?apiKey=freekey"
                    res_wallet = requests.get(url_wallet).json()
                    
                    if 'tokens' in res_wallet:
                        for token in res_wallet['tokens']:
                            token_name = token.get('tokenInfo', {}).get('symbol', '이름없는코인')
                            
                            # 🚨 걸러내기 작전: 대문자로 바꿔서 블랙리스트에 '없을 때만' 바구니에 담기!
                            if isinstance(token_name, str) and token_name.upper() not in EXCLUDE_LIST:
                                all_tokens.append(token_name.upper())
                    
                    time.sleep(0.5) 
                    progress_bar.progress((i + 1) / len(holders))
                
                # 3단계: 진짜 알트코인들만 통계 내기
                token_counts = Counter(all_tokens)
                
                st.success("🎉 분석 끝났슈! 뻔한 동전들 다 빼고 진짜 수상한 놈들만 남겼어유!")
                
                top_5_coupled = token_counts.most_common(5)
                for rank, (coin, count) in enumerate(top_5_coupled, 1):
                    st.markdown(f"**{rank}위: {coin}** (고래 {len(holders)}명 중 {count}명이 몰래 담았슈!)")
                    
                st.warning("💡 형, 이제 진짜 세력들이 엮어놓은 놈들이 보일 거여유. 타점 잡으실 때 요놈들 움직임도 꼬옥 같이 지켜보셔유!")
                
            else:
                st.error("주소가 잘못됐거나 고래 명단을 못 불러왔슈. 다시 확인해봐유.")
                
        except Exception as e:
            st.error("앗, 고래들 지갑 뒤지다가 쫓겨났슈. 쫌 이따 다시 해보셔유!")
    else:
        st.warning("형, 빈칸인디유? 코인 주소를 넣어주셔야 일을 하쥬!")
