import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px


def run_eda_app():
	st.subheader("Exploratory Data Analysis")
	

	submenu = st.sidebar.selectbox("Submenu", ["Descriptive", "Plots"])
	df = pd.read_csv("diabetes_data_upload.csv")
	df_cleaned = pd.read_csv("diabetes_data_upload_clean.csv")
	freq = pd.read_csv("freqdist_of_age_data.csv")

	if submenu == "Descriptive":
		st.dataframe(df)

		with st.beta_expander("Data Types"):
			st.dataframe(df.dtypes)

		with st.beta_expander("Summary"):
			st.dataframe(df.describe())

		with st.beta_expander("Age"):
			st.dataframe(freq)

		with st.beta_expander("Gender Distribution"):
			st.dataframe(df["Gender"].value_counts())

		with st.beta_expander("Class Distribution"):
			st.dataframe(df["class"].value_counts())

	elif submenu == "Plots":
		st.subheader("Visualization Plots")

		with st.beta_expander("Plots based on Gender"):
			#fig = plt.figure()
			#sns.countplot(df['Gender'])
			#st.pyplot(fig)

			gender_df = df["Gender"].value_counts()
			gender_df = gender_df.reset_index()
			gender_df.columns = ["Gender", "Count"]
			#st.dataframe(gender_df)

			p1 = px.pie(gender_df, names = "Gender", values = "Count")
			st.plotly_chart(p1)

		with st.beta_expander("Plots based on Class"):
			fig = plt.figure()
			sns.countplot(df['class'])
			st.pyplot(fig)

			class_df = df["class"].value_counts()
			class_df = class_df.reset_index()
			class_df.columns = ["Class", "Count"]
			#st.dataframe(class_df)

		with st.beta_expander("Plots based on age"):
			#st.dataframe(freq)
			p2 = px.bar(freq,x = "s",y = "count")
			st.plotly_chart(p2)

		with st.beta_expander("Outlier Detection"):
			p3 = px.box(df, x = "Age")
			st.plotly_chart(p3)