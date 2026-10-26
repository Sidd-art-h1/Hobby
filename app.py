"""
Hobby Social Media App Entrypoint for Streamlit.
Run with:
    streamlit run app.py
or
    streamlit run streamlit_app.py
"""
import runpy

if __name__ == "__main__":
    runpy.run_module("streamlit_app", run_name="__main__")
