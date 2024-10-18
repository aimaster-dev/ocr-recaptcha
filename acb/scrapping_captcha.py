import requests

# URL of the image
url = "https://online.acb.com.vn/acbib/Captcha.jpg"

# Download and save the image five times
for i in range(10):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"Captcha_{i}.jpg", "wb") as file:
            file.write(response.content)
        print(f"Captcha_{i}.jpg saved successfully")
    else:
        print(f"Failed to retrieve image {i}, status code: {response.status_code}")
