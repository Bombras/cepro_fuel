#  streamlit run ./cepro_fuel_app/test.py [-- kokot]
import os
import argparse
import streamlit as st

parser = argparse.ArgumentParser()

parser.add_argument(
    "--dev",
    action="append",
    default=None,
    help="Start development mode",
)

try:
    args = parser.parse_args()
except SystemExit as e:
    os._exit(e.code)

st.title("Command line example app")
st.write(f"You entered: {args.dev}")

