import requests

if __name__ == "__main__":
    url = "https://prediction-gaxsrkp74a-de.a.run.app"
    test_audio = 'D:\FINALMLAPI\doja.wav'
    audio_file = open(test_audio,"rb")
    values = {"file":(test_audio,audio_file,"audio/wav")}
    resp = requests.post(url=url,files=values)
    print(resp.json())