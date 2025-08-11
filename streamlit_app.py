import streamlit as st
import database as db
import encoder as enc

# Page title and introductory text
st.title("Semantic Search Engine")
st.write(
    "Within the documents in the database, finds the ones that most closely match the meaning of the text you have written"
)

# Create a text input box to get the search query from the user
search_query = st.text_input(
    "Enter your search query: ",
    placeholder="e.g.: What are the main goals of AI research?"
)

# Create search button
if st.button("Search"):
    if search_query:
        # If the user entered a query and clicked the button
        with st.spinner("Similar documents are being searched... Please wait."):
            # Convert query to vector
            query_embedding = enc.encode_texts([search_query])[0]

            # Search the database
            results = db.search_similar_documents(query_embedding, top_n=3)

            # Print results on the screen
            st.subheader("Search Results")
            if not results:
                st.warning("No results were found for this query")
            else:
                for doc in results:
                    doc_id, doc_text, doc_similarity = doc

                    st.markdown(f"ID: `{doc_id}`  |  Similarity Score: `{float(doc_similarity):.4f}`")
                    st.info(doc_text)
                    st.markdown("---")

    else:
        # If the user left the box blank and clicked the button
        st.warning("Please enter a search query")