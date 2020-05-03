import chardet

with open('Violent.Cop.srt', "rb") as f:
    data = f.read()
det = chardet.detect(data)
print(det.get("encoding"))