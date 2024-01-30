### Hexlet tests, linter status and climate:
[![Actions Status](https://github.com/Aston585/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Aston585/python-project-83/actions)
[![Linter Status](https://github.com/Aston585/python-project-83/actions/workflows/page-analyzer.yaml/badge.svg)](https://github.com/Aston585/python-project-83/actions/workflows/page-analyzer.yaml)
[![Maintainability](https://api.codeclimate.com/v1/badges/be16049af43f0fdb99c7/maintainability)](https://codeclimate.com/github/Aston585/python-project-83/maintainability)
---
### [Page Analyzer](https://page-analyzer-8g4d.onrender.com) – это сайт, который анализирует указанные страницы на SEO-пригодность
---
### How to install and use

#### First you need to create your own .env file and add with following variables:
```commandline
DATABASE_URL = postgresql://{yourusername}:{password}@{host}:{port}/{yourdb}
SECRET_KEY = '{your secret key}'
```
#### You have to setup your db connection and secret key, and then run one of next commands to run in locale machine
```commandline
make dev 
```
#### Demo
<img src=https://cdn2.hexlet.io/store/derivatives/original/c9a309a4417c7e21276e8d7bc233c72c.gif>
