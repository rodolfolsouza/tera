from pathlib import Path
import streamlit as st
from loguru import logger

logname = "log_geral.log"

logger.add(logname)

st.write("## Arquivo de Log")

lines = "\n".join(Path(logname).read_text().splitlines()[-15:])

st.code(lines)