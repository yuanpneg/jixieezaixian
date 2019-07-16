import qrcode

data = "www.baidu.com"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4
)

qr.add_data('hello！！！')
qr.make(fit=True)
img = qr.make_image()
img.save('123.png')
