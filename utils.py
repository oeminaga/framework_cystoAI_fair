import imquality.brisque as brisque
import PIL.Image
def GetImageQualityScore(path):
    img = PIL.Image.open(path)
    return brisque.score(img)