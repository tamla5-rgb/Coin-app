import streamlit as st
import requests
import time

st.set_page_config(page_title="고래 추적기", layout="centered")
st.title("🐋 모시의 온체인 커플링 자동 분석기 (보유량 추가!)")
st.write("형! 뻔한 동전은 빼고, 고래들이 어떤 코인을 '얼마나' 들고 있는지 10위까지 싹 다 캐올게유.")

token_address = st.text_input("🔍 분석할 코인의 컨트랙트 주소")

# 블랙리스트 (현금성 코인)
EXCLUDE_LIST = ['USDT', 'USDC', 'DAI', 'BUSD', 'ETH', 'WETH', 'BTC', 'WBTC', 'ERC20', 'TUSD', 'USDD']

if st.button("찐 커플링 코인 찾기 🚀"):
    if token_address:
        st.info("고래 명단 확보하고 주머니 속 갯수까지 세는 중이유. 쫌만 기다려봐유!")
        
        try:
            url_holders = f"https://api.ethplorer.io/getTopTokenHolders/{token_address}?apiKey=freekey&limit=10"
            res_holders = requests.get(url_holders).json()
            
            if 'holders' in res_holders:
                holders = [h['address'] for h in res_holders['holders']]
                st.write(f"✅ 거대 고래 {len(holders)}마리 주머니 탈탈 터는 중...")
                
                # 코인 정보 저장할 바구니 (이름: {몇명, 총 몇개})
                token_data = {}
                progress_bar = st.progress(0)
                
                for i, wallet in enumerate(holders):
                    url_wallet = f"https://api.ethplorer.io/getAddressInfo/{wallet}?apiKey=freekey"
                    res_wallet = requests.get(url_wallet).json()
                    
                    if 'tokens' in res_wallet:
                        for token in res_wallet['tokens']:
                            token_info = token.get('tokenInfo', {})
                            token_name = str(token_info.get('symbol', '이름모름')).upper()
                            
                            if token_name not in EXCLUDE_LIST:
                                # 갯수 계산 (블록체인은 소수점 자리가 복잡해서 이걸 나눠줘야 진짜 갯수가 나와유)
                                raw_balance = float(token.get('balance', 0))
                                decimals = int(token_info.get('decimals', 0) or 0)
                                actual_balance = raw_balance / (10 ** decimals)
                                
                                if token_name not in token_data:
                                    token_data[token_name] = {'count': 0, 'total': 0.0}
                                    
                                token_data[token_name]['count'] += 1
                                token_data[token_name]['total'] += actual_balance
                    
                    time.sleep(0.5) 
                    progress_bar.progress((i + 1) / len(holders))
                
                st.success("🎉 분석 끝났슈! 수량까지 싹 다 셌어유!")
                
                # 고래들이 '가장 많이 같이 들고 있는(count)' 순으로 정렬해유
                sorted_tokens = sorted(token_data.items(), key=lambda x: x[1]['count'], reverse=True)
                
                # 1위부터 10위까지 보여주기!
                for rank, (coin, info) in enumerate(sorted_tokens[:10], 1):
                    count = info['count']
                    total_amount = info['total']
                    
                    # 보기 좋게 숫자 콤마 찍고 소수점 자르기
                    formatted_amount = f"{total_amount:,.0f}"
                    
                    st.markdown(f"**{rank}위: {coin}**")
                    st.write(f"👉 고래 {len(holders)}명 중 **{count}명**이 같이 들고 있고, 총 **{formatted_amount}개**를 쟁여놨슈!")
                    st.divider() # 줄바꿈 선 그어주기
                    
                st.warning("💡 형, 갯수까지 보니까 세력들이 진짜로 힘주고 있는 찐 코인이 딱 보이쥬? 타점 분석하실 때 요것들 위주로 파고드셔유!")
                
            else:
                st.error("주소가 잘못됐거나 고래 명단을 못 불러왔슈. 다시 확인해봐유.")
                
        except Exception as e:
            st.error("앗, 고래들 지갑 뒤지다가 쫓겨났슈. 무료 통로라 막혔나 봐유. 쫌 이따 다시 해보셔유!")
    else:
        st.warning("형, 빈칸인디유? 코인 주소를 넣어주셔야 일을 하쥬!")
