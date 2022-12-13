## 👨‍💻 Built with 
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>

##  Descripction about project

Simple application created to learn foreigns worlds. Running via terminal, using API to connect GoogleTranslateAPI to translate polish words.
Before use you need to reginster on link: https://rapidapi.com/googlecloud/api/google-translate1 to get:

- API key from API endpoint

## 🌲 Project tree
```bash
.
├── Dockerfile           # to create image.
├── README.md
├── apk.py 
├── dictionary.xlsx      # xlsx with polish words to transalte, collected in 4 categories.
└── requirements.txt     # necessary libraries.
```
## ⚙️ Run Locally
Clone the project

Go to the project directory and open terminal:
Type in CLI:
```bash
  $ ls
```
You should see this:
```bash
Dockerfile		README.md		apk.py			dictionary.xlsx		requirements.txt
```
Open Dockerfile and fill ENV values with values mentioned in description:
```bash
ENV API_KEY=
```
Build application image: 🚨to run this command docker should be running on your machine🚨
```bash
  $ docker build -t <your_image_name> .     
```
Run docker application container:
```bash
  $ docker run -it --name <your_container_name> <your_image_name>     
```
## Future updates?🆕:
  - letting choose a language source not only target.
  - adding more languages.
  - finding way to allow ASCII latin-2 with Google Translate API.
  - creating SQLserwer to connect for bigger base of words (now words are captured from xlsx file).
  - allow to choose categories, now category is randomly choosen from given 4.

