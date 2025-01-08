import streamlit as st
import pandas as pd

# 스타일 적용
st.set_page_config(page_title="설 선물 신청", layout="wide")  # 페이지 제목 및 레이아웃 설정

# CSS 스타일 추가
st.markdown(
    """
    <style>
    .category-title {
        font-size: 22px;
        font-weight: bold;
        color: #2E8B57;
        margin-top: 30px;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 5px;
    }
    .product-card {
        background-color: #F9F9F9;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .product-card img {
        border-radius: 10px;
        max-height: 150px;
    }
    .apply-button {
        background-color: #2E8B57;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
    }
    .apply-button:hover {
        background-color: #1E6A40;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 제목
st.title("🎁 설 선물 신청 화면")

# 엑셀 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])
if uploaded_file:
    # 엑셀 파일 읽기
    df = pd.read_excel(uploaded_file)

    # 데이터 확인
    st.write("업로드된 데이터 미리 보기:")
    st.write(df.head())

    # 카테고리별로 그룹화
    if '카테고리' in df.columns and '사진' in df.columns:
        categories = df['카테고리'].unique()  # 카테고리 목록

        for category in categories:
            st.markdown(f'<div class="category-title">{category}</div>', unsafe_allow_html=True)

            # 해당 카테고리의 상품 필터링
            category_items = df[df['카테고리'] == category]

            cols = st.columns(3)  # 3개의 컬럼으로 상품 표시
            for idx, (_, row) in enumerate(category_items.iterrows()):
                with cols[idx % 3]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(row['사진'], caption=row['상품명'], use_column_width=True)
                    st.write(f"**상품명:** {row['상품명']}")
                    st.write(f"**상세 설명:** {row['상세설명']}")

                    if st.button(f"신청하기 ({row['상품명']})", key=f"apply_{row['상품명']}"):
                        st.success(f"✅ {row['상품명']} 신청이 완료되었습니다!")

                    st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("엑셀 파일에 '카테고리' 또는 '사진' 열이 없습니다.")
