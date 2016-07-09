# MySQL soccer database

## Installation Instructions
### MySQL

Follow this link: http://dev.mysql.com/doc/refman/5.5/en/getting-mysql.html

### Requirements

(Need to add `requirements.txt`)

Run the following to get install all requirements in a virtual environment called `ss`

```bash 
$ git clone https://github.com/fordb/soccer-statistically
$ cd soccer-statistically
$ pip install virtualenv virtualenvwrapper # if not already installed
$ mkvirtualenv ss -a . -r requirements.txt
```

Alternatively, you can just install all the requirements
```bash
$ pip install -r requirements.txt
```
