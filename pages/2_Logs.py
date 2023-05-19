from pathlib import Path
import streamlit as st
from loguru import logger

with open('style.css') as ww:
    st.markdown(f'<style>{ww.read()}</style>', unsafe_allow_html=True)

logname = "log_geral.log"

logger.add(logname)

st.write("## Arquivo de Log")

lines = "\n".join(Path(logname).read_text().splitlines()[-15:])

st.code(lines)