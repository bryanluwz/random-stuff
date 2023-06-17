from PIL import Image

PIL_SUPPORTED_FORMATS = [
    x.replace(".", "") for x in Image.registered_extensions().keys()
]

if __name__ == '__main__':
    print('ico' in (PIL_SUPPORTED_FORMATS))
