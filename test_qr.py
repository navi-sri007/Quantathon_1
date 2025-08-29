import qrcode

img = qrcode.make("Hello Naveena")
img.save("test_qr.png")