# Mini Search Engine

![CI status](https://github.com/ryjpink/mini-search-engine/actions/workflows/build-and-test.yml/badge.svg)

Search a recipe collection with a query parser and evaluation engine allowing arbitrary boolean queries

## Installation

Create a virtual environment and use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate.bat # on Windows
. venv/bin/activate # on macOS/Linux

# Install the dependencies
pip3 install -r requirements.txt
```

## Usage

Populate some test data:

```bash
$ python database.py
````

To search from the command line:

```bash
$ python main.py
```

To run the API server:
```bash
$ python server.py
```

From another terminal, make a request:
```
$ curl -G "http://localhost:5000/api/v1/search" \
  --data-urlencode "q=(butter and (egg or taro)) and not (caramel or salt)"

{
  "results":[
    {
      "title":"french toast",
      "body":"toast butter milk egg"
    },
    {
      "title":"pancakes",
      "body":"butter flour water sugar baking-soda egg"
    }
  ]
}
