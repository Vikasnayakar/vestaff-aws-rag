import streamlit as st
import requests
import pandas as pd


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AWS RAG Assistant",
    layout="wide"
)


st.title("AWS Customer Agreement RAG Assistant")


if "history" not in st.session_state:
    st.session_state.history = []


tab1, tab2 = st.tabs(
    ["Ask Question", "Analytics"]
)



# ================= ASK TAB =================

with tab1:

    st.subheader("Ask about AWS Customer Agreement")


    question = st.text_input(
        "Enter your question:"
    )


    if st.button("Ask"):


        if question.strip():


            with st.spinner("Searching document..."):


                try:

                    response = requests.post(
                        f"{API_URL}/ask",
                        json={
                            "query": question
                        },
                        timeout=120
                    )



                    if response.status_code == 200:


                        data = response.json()


                        answer = data.get(
                            "answer",
                            "No answer"
                        )


                        st.session_state.history.append(
                            {
                                "question": question,
                                "answer": answer
                            }
                        )



                        st.success("Answer")


                        st.info(
                            answer
                        )



                        st.caption(
                            f"Latency: {data.get('latency_seconds',0):.2f}s"
                        )



                        st.divider()



                        st.subheader(
                            "Sources"
                        )



                        sources = data.get(
                            "sources",
                            []
                        )



                        for i, source in enumerate(sources):


                            with st.expander(
                                f"Source Chunk {i+1}"
                            ):

                                st.text(
                                    source[:500] + "..."
                                )



                    else:

                        st.error(
                            f"Backend error: {response.text}"
                        )



                except requests.exceptions.ConnectionError:


                    st.error(
                        "Backend unreachable. Start FastAPI first."
                    )



                except Exception as e:


                    st.error(
                        str(e)
                    )




    # History

    if st.session_state.history:


        st.divider()


        st.subheader(
            "Previous Questions"
        )


        for item in reversed(
            st.session_state.history
        ):


            with st.expander(
                item["question"]
            ):

                st.write(
                    item["answer"]
                )





# ================= ANALYTICS TAB =================


with tab2:


    st.subheader(
        "RAG Analytics"
    )



    if st.button(
        "Load Analytics"
    ):


        try:


            response = requests.get(
                f"{API_URL}/analytics"
            )



            if response.status_code == 200:


                metrics = response.json()



                col1, col2 = st.columns(2)



                col1.metric(
                    "Average Latency",
                    f"{metrics.get('average_latency_seconds',0):.3f}s"
                )



                col2.metric(
                    "Unanswered Queries",
                    metrics.get(
                        "unanswered_queries_count",
                        0
                    )
                )



                st.subheader(
                    "Top Queries"
                )



                queries = metrics.get(
                    "top_queries",
                    []
                )



                if queries:


                    df = pd.DataFrame(
                        queries
                    )


                    st.dataframe(
                        df
                    )


                else:


                    st.info(
                        "No query data yet"
                    )



            else:


                st.error(
                    response.text
                )



        except Exception as e:


            st.error(
                f"Analytics unavailable: {e}"
            )