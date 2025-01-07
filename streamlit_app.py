import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 기본 설정
st.set_page_config(page_title="설 선물 신청", layout="wide")

# 업로드된 데이터 저장
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

# 초기화
if "requests" not in st.session_state:
    st.session_state["requests"] = []

# 상품 정보 및 신청 화면
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.header("설 선물 리스트")
    st.markdown("아래에서 선물을 선택해 신청하세요.")

    for i, row in df.iterrows():
        # 사진, 상품명, 상세설명 표시
        st.image(row["사진"], caption=row["상품명"], width=200)
        st.markdown(f"**상품명:** {row['상품명']}")
        st.markdown(f"[상세보기 링크](https://{row['상세설명']})")

        # 신청 버튼
        if st.button(f"신청 - {row['상품명']}"):
            with st.form(f"form_{i}"):
                st.write(f"**{row['상품명']} 신청하기**")
                affiliation = st.text_input("소속")
                name = st.text_input("이름")
                address = st.text_input("배송지")
                contact = st.text_input("연락처")
                submit = st.form_submit_button("신청")
                cancel = st.form_submit_button("취소")

                if submit:
                    st.session_state["requests"].append({
                        "순번": i + 1,
                        "상품명": row["상품명"],
                        "소속": affiliation,
                        "이름": name,
                        "배송지": address,
                        "연락처": contact,
                        "신청일자": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                    st.success("신청이 완료되었습니다. 신청기한 내 변경을 희망하시면 담당자 이메일로 번호 및 상품명을 보내주세요.")
                elif cancel:
                    st.info("신청이 취소되었습니다.")

# 관리자 화면
st.sidebar.title("관리자 메뉴")
if st.sidebar.checkbox("신청 내역 보기"):
    st.sidebar.markdown("### 신청 내역")
    if st.session_state["requests"]:
        request_df = pd.DataFrame(st.session_state["requests"])
        st.sidebar.dataframe(request_df)

        # 엑셀 다운로드
        @st.cache
        def convert_to_excel(dataframe):
            return dataframe.to_excel(index=False, engine="openpyxl")

        st.sidebar.download_button(
            label="신청 내역 엑셀 다운로드",
            data=convert_to_excel(request_df),
            file_name="신청내역.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.sidebar.write("신청 내역이 없습니다.")
