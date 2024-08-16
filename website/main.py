import sys
import streamlit.web.cli as stcli

if __name__ == '__main__':
    sys.argv = ['streamlit', 'run', r'website\website.py']
    sys.exit(stcli.main())
