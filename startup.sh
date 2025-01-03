if ! command -v pip3 &> /dev/null
then
    echo "pip3 not found, installing..."
    curl https://bootstrap.pypa.io/pip/3.7/get-pip.py -o get-pip.py
    python3 get-pip.py
fi
#!/bin/bash
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# gunicorn -w 3 -b 0.0.0.0:8000 app:app
.venv/bin/gunicorn -w 3 -b 0.0.0.0:8000 app:app