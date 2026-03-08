import streamlit as st
import requests
import time

st.set_page_config(page_title="고래 추적기", layout="centered")
st.title("🐋 모시의 온체인 커플링 자동 분석기 (과부하 방지!)")
st.write("형! 무료 서버 문지기한테 안 걸리게 아주 조심조~심 천천히 고래들 주머니를 털어볼게유.")

token_address = st.text_input("🔍 분석할 코인의 컨트랙트 주소")

# 블랙리스트 (현금성 코인)
EXCLUDE_LIST = ['USDT', 'USDC', 'DAI', 'BUSD', 'ETH', 'WETH', 'BTC', 'WBTC', 'ERC20', 'TUSD', 'USDD']

if st.button("찐 커플링 코인 찾기 🚀"):
    if token_address:
        # 문지기 눈치채지 않게 넉넉히 기다려 달라는 안내 문구
        st.info("고래 명단 확보 완료! 이제 문지기 몰래 한 놈씩 천천히 지갑을 열어볼게유. 한 20초~30초 넉넉히 기다려주셔유!")
        
        try:
            url_holders = f"https://api.ethplorer.io/getTopTokenHolders/{token_address}?apiKey=freekey&limit=10"
            res_holders = requests.get(url_holders).json()
            
            if 'holders' in res_holders:
                holders = [h['address'] for h in res_holders['holders']]
                st.write(f"✅ 거대 고래 {len(holders)}마리 확인! 조심조심 작업 들어갑니다...")
                
                token_data = {}
                progress_bar = st.progress(0)
                
                for i, wallet in enumerate(holders):
                    try:
                        url_wallet = f"https://api.ethplorer.io/getAddressInfo/{wallet}?apiKey=freekey"
                        response = requests.get(url_wallet)
                        
                        # 429 에러(과부하) 방지! 응답이 정상(200)일 때만 데이터 빼오기
                        if response.status_code == 200:
                            res_wallet = response.json()
                            if 'tokens' in res_wallet:
                                for token in res_wallet['tokens']:
                                    token_info = token.get('tokenInfo', {})
                                    token_name = str(token_info.get('symbol', '이름모름')).upper()
                                    
                                    if token_name not in EXCLUDE_LIST:
                                        raw_balance = float(token.get('balance', 0))
                                        decimals = int(token_info.get('decimals', 0) or 0)
                                        # 소수점 계산 안전하게 처리
                                        actual_balance = raw_balance / (10 ** decimals) if decimals > 0 else raw_balance
                                        
                                        if token_name not in token_data:
                                            token_data[token_name] = {'count': 0, 'total': 0.0}
                                            
                                        token_data[token_name]['count'] += 1
                                        token_data[token_name]['total'] += actual_balance
                    except Exception:
                        pass # 중간에 에러 나도 멈추지 말고 조용히 다음 고래로 넘어가기!
                        
                    # 문지기한테 안 걸리게 진짜 넉넉하게 2초 쉬어주기 (이게 핵심이여유!)
                    time.sleep(2.0) 
                    progress_bar.progress((i + 1) / len(holders))
                
                st.success("🎉 휴, 안 들키고 무사히 다 털었슈! 결과 발표할게유!")
                
                sorted_tokens = sorted(token_data.items(), key=lambda x: x[1]['count'], reverse=True)
                
                for rank, (coin, info) in enumerate(sorted_tokens[:10], 1):
                    count = info['count']
                    total_amount = info['total']
                    formatted_amount = f"{total_amount:,.0f}"
                    
                    st.markdown(f"**{rank}위: {coin}**")
                    st.write(f"👉 고래 {len(holders)}명 중 **{count}명**이 같이 들고 있고, 총 **{formatted_amount}개**를 쟁여놨슈!")
                    st.divider()
                    
            else:
                st.error("앗, 고래 명단을 못 불러왔슈. 주소를 다시 확인해봐유.")
                
        except Exception as e:
            st.error("아이고 형, 서버가 아직도 쪼끔 삐져있나 봐유. 1분만 딱 숨 돌렸다가 파란 버튼 다시 한 번 눌러주셔유!")
    else:
        st.warning("형, 빈칸인디유? 코인 주소를 넣어주셔야 일을 하쥬!")
