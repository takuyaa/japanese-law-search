import streamlit as st

from japanese_law_search.search import search_law

st.title("Japanese Law Search")

query = st.text_input("Query", value="")
if query:
    res = search_law(es_host="http://localhost:9200/", index_name="ja_law", keyword=query, size=20)
    st.write(f"{res.total_hits} hits")
    for doc in res.docs:
        c = st.container(border=True)
        c.markdown(
            f"[{doc.law_title}（{doc.law_num}）](https://elaws.e-gov.go.jp/document?lawid={doc.id})"
        )
        c.caption(
            "".join(["".join(highlites[0]) for highlites in doc.highlight.values()])
        )
