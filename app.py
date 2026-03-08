import streamlit as st
import requests

st.set_page_config(page_title="고래 추적기", layout="centered")
st.title("🐋 모시의 온체인 커플링 추적기")
st.write("형! 의심되는 코인 두 개의 '컨트랙트 주소(Contract Address)'를 넣으면, 양다리 걸친 고래가 있는지 1초 만에 싹 뒤져볼게유.")

# 폰 화면에 입력칸 만들기
token_a = st.text_input("🔍 첫 번째 코인 주소 (예: 0xdac17f958d2ee523a2206206994597c13d831ec7)")
token_b = st.text_input("🔍 두 번째 코인 주소 (예: 0x514910771af9ca656af840dff83e8264ecf986ca)")

if st.button("고래 지갑 털어보기 🚀"):
    if token_a and token_b:
        st.info("열심히 블록체인을 뒤지고 있어유... 쫌만 기다려봐유!")
        try:
            # 무료 공용 API를 써서 고래 100명 명단 빼오기
            url_a = f"https://api.ethplorer.io/getTopTokenHolders/{token_a}?apiKey=freekey&limit=100"
            url_b = f"https://api.ethplorer.io/getTopTokenHolders/{token_b}?apiKey=freekey&limit=100"

            res_a = requests.get(url_a).json()
            res_b = requests.get(url_b).json()

            if 'holders' in res_a and 'holders' in res_b:
                # 명단에서 지갑 주소만 쏙쏙 뽑아내기
                holders_a = set([h['address'] for h in res_a['holders']])
                holders_b = set([h['address'] for h in res_b['holders']])

                # 양다리 걸친 놈팽이들 찾기 (교집합)
                coupled = holders_a.intersection(holders_b)

                if len(coupled) > 0:
                    st.success(f"🚨 찾았슈! 총 {len(coupled)}명의 거대 고래가 두 코인을 꽉 쥐고 있어유!")
                    st.write("이 코인들은 한 놈팽이가 장난칠 때 같이 폭락하거나 폭등할 확률이 아주 높아유. 타점 잡을 때 조심하세유!")
                    for w in coupled:
                        st.code(w)
                else:
                    st.warning("형, 이 두 코인은 겹치는 고래가 없어유. 각자 따로 노는 코인들이어유.")
            else:
                st.error("앗! 주소가 잘못됐거나 데이터를 못 불러왔슈. 이더리움 기반 코인 주소가 맞는지 확인해봐유.")
        except Exception as e:
            st.error("서버에 잠깐 문제가 생겼나봐유. 다시 한 번 눌러봐유!")
    else:
        st.warning("형, 코인 주소 두 개를 싹 다 넣어주셔야 분석을 하쥬!")
