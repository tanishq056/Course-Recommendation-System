import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset
@st.cache_data  # Use st.cache_data instead of st.cache
def load_data():
    df = pd.read_csv('udemy_courses.csv')
    df = df[['course_title','is_paid','level','subject']]
    df['course_title'] = df['course_title'].str.replace('-','')
    df['course_title'] = df['course_title'].str.replace(':','')
    df['course_title'] = df['course_title'].str.replace('&','')
    df['course_title'] = df['course_title'].str.replace(' ',',')
    df['level'] = df['level'].str.replace(' ',',')
    df['subject'] = df['subject'].str.replace(' ',',')
    df['combined_features'] = df['course_title'] + ' ' + df['is_paid'].astype(str) + ' ' + df['level'] + ' ' + df['subject']
    df['combined_features'] = df['combined_features'].str.replace(',',' ')
    df['course_title'] = df['course_title'].str.replace(',',' ')
    df.rename(columns = {'course_title':'COURSE_TITLE'}, inplace = True)
    df['combined_features'] = df['combined_features'].apply(lambda x:x.lower())
    return df

# Function to calculate Jaccard similarity
def jaccard_similarity(features1, features2):
    set1 = set(features1.lower().split())
    set2 = set(features2.lower().split())
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

# Function to recommend courses
def recommend_courses(input_features, df, top_n=5):
    similarities = []
    for idx, features in enumerate(df['combined_features']):
        similarity = jaccard_similarity(input_features, features)
        course_title = df.iloc[idx]['COURSE_TITLE']
        similarities.append((course_title, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]

# Load data
df = load_data()

# Streamlit App Title
st.title('Udemy Course Recommendation System')

# User Input for Course Features
input_features = st.text_input("Enter course details (e.g., 'Ultimate Investment Banking Course True All Levels Business Finance'):")

# Recommend Courses
if input_features:
    recommendations = recommend_courses(input_features, df)
    st.subheader('Top 5 Recommended Courses:')
    for i, (course_title, similarity) in enumerate(recommendations, 1):
        st.write(f"{i}. {course_title} (Similarity: {similarity:.2f})")

# Show the dataset
if st.checkbox('Show Dataset'):
    st.subheader('Udemy Courses Dataset')
    st.write(df)
