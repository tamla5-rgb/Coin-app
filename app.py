import streamlit as st

# 폰 화면에 예쁘게 보이게 설정하는 거여유
st.set_page_config(page_title="고래 추적기", layout="centered")

st.title("🐋 모시의 코인 커플링 추적기")
st.write("형! 코인 이름을 넣으면, 이 코인을 가진 고래들이 또 무슨 코인을 몰래 사고 있는지 알아봐 드릴게유.")

# 코인 이름 입력받는 칸
coin_name = st.text_input("🔍 분석할 코인 주소나 이름을 적어주세유 (예: SHIB)")

# 버튼을 누르면 작동해유
if st.button("고래 지갑 털어보기 🚀"):
    if coin_name:
        st.info(f"지금부터 '{coin_name}' 코인을 꽉 쥐고 있는 고래 상위 100명을 찾고 있어유...")
        st.success("찾았다! 이 고래들은 'A코인'과 'B코인'도 엄청나게 가지고 있네유! 🚨커플링 확률 99%🚨")
        st.write("👉 (여기에 진짜 블록체인 데이터를 끌어와서 보여줄 거여유!)")
    else:
        st.warning("형, 코인 이름을 입력해야쥬!")
