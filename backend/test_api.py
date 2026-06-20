import requests

url = "http://localhost:8000/analyze"

job_description = "Python developer with cloud experience and REST API knowledge"

files = [
    ("files", open("test_resume.pdf", "rb"))
]

data = {
    "job_description": job_description
}

response = requests.post(url, data=data, files=files)
print(response.status_code)
print(response.json())
