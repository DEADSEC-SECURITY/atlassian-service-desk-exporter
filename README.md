# Atlassian Service Desk Exporter ![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/DEADSEC-SECURITY/atlassian-service-desk-exporter?label=Version&style=flat-square) ![Python_Version](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square) ![GitHub](https://img.shields.io/github/license/DEADSEC-SECURITY/atlassian-service-desk-exporter?label=Licence&style=flat-square)
This project uses selenium to export atlassian service desk tickets into PDFs

## 📧 CONTACT

Email: amng835@gmail.com

General Discord: https://discord.gg/dFD5HHa

Developer Discord: https://discord.gg/rxNNHYN9EQ

## 📥 INSTALLING
```bash
git clone https://github.com/DEADSEC-SECURITY/atlassian-service-desk-exporter.git
```
Then cd into the repo directory and run
````commandline
pip3 install -r requirements.txt 
````
This will install all the packages it depends on

## ⚙ HOW TO USE

### Using as a package
To import this as a package for your project copy the repository folder into your project dir and then you should be
able to import it like a normal package

### Single run
Open main.py, at the bottom you should find the following code:
```python
if __name__ == '__main__':
    AtlassianServiceDeskExporter(
        atlassian_domain='YOUR_DOMAIN',
        email='YOUR_EMAIL',
        password='YOUR_PASSWORD',
        export_folder_destination=Path.cwd().joinpath('export')
    ).export()
```
Now edit the values YOUR_DOMAIN, YOUR_EMAIL, YOUR_PASSWORD to your information and then run:
````commandline
python3 main.py
````

## 🤝 PARAMETERS
- atlassian_domain : str, required
  - The domain for atlassian service desk
  - Example: https://examplesub.atlassian.net
- email : str, required
  - The email to login into atlassian service desk
- password : str, required
  - The password to login into atlassian service desk
- export_folder_destination : str, optional
  - Default: Current dir
