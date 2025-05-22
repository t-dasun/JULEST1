import qrcode
import io

def generate_qr_code_to_bytes(data_string: str) -> bytes:
    """
    Generates a QR code image from the given data_string and returns it as bytes.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

if __name__ == '__main__':
    # Example usage (not part of the utility function itself)
    # This part will not run when imported, but can be used for direct testing of this file.
    test_url = "https://www.example.com"
    qr_bytes = generate_qr_code_to_bytes(test_url)
    
    # To save to a file for testing:
    # with open("test_qr.png", "wb") as f:
    #     f.write(qr_bytes)
    # print("Test QR code generated as test_qr.png")
    print(f"Generated QR code for '{test_url}' as bytes (length: {len(qr_bytes)}). First 10 bytes: {qr_bytes[:10]}")
