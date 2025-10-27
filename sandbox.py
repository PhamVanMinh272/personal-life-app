# python
import argparse
import sys
import requests

def try_url_param(base_url, product_id, image_path, timeout=5):
    url = f"{base_url.rstrip('/')}/products/{product_id}/attach-picture"
    with open(image_path, "rb") as f:
        files = {"pictureFile": (image_path, f, "image/jpeg")}
        try:
            resp = requests.post(url, files=files, timeout=timeout)
            return resp
        except requests.RequestException as e:
            print("URL-parameter request failed:", e)
            return None

def try_form_param(base_url, product_id, image_path, timeout=5):
    url = f"{base_url.rstrip('/')}/products/attach-picture"
    with open(image_path, "rb") as f:
        files = {"pictureFile": (image_path, f, "image/jpeg")}
        data = {"productId": str(product_id)}
        try:
            resp = requests.post(url, files=files, data=data, timeout=timeout)
            return resp
        except requests.RequestException as e:
            print("Form-parameter request failed:", e)
            return None

def main():
    p = argparse.ArgumentParser(description="Test attach-picture API")
    p.add_argument("--base", default="http://127.0.0.1:5000/api", help="Base URL of the API")
    p.add_argument("--product-id", type=int, default=1, help="Product ID to attach the picture to")
    p.add_argument("--image", default="test.jpg", help="Path to image file to upload")
    args = p.parse_args()

    # Try route-style endpoint first
    resp = try_url_param(args.base, args.product_id, args.image)
    if resp is None:
        sys.exit(1)

    if resp.status_code == 404:
        # Fallback to form-style endpoint
        print("Route-style endpoint returned 404, trying form-style endpoint...")
        resp = try_form_param(args.base, args.product_id, args.image)
        if resp is None:
            sys.exit(1)

    print("Status code:", resp.status_code)
    # Try to print JSON if possible, else print text
    try:
        print("Response JSON:", resp.json())
    except ValueError:
        print("Response text:", resp.text)

if __name__ == "__main__":
    main()
