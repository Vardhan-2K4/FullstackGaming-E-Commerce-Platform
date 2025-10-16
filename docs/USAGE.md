# Usage Examples

## Start the app
```bash
python app.py
```

## Register a user
```bash
curl -X POST -L \
  -F username=alice \
  -F email=alice@example.com \
  -F password='S3cure!' \
  http://localhost:5000/register -c cookies.txt -b cookies.txt
```

## Login
```bash
curl -X POST -L \
  -F username=alice \
  -F password='S3cure!' \
  http://localhost:5000/login -c cookies.txt -b cookies.txt
```

## Add to cart (authenticated)
```bash
curl -X POST -L \
  -F product='GTA V' \
  -F price_cents=1999 \
  http://localhost:5000/add_to_cart -b cookies.txt -c cookies.txt
```

## View cart
```bash
curl -L http://localhost:5000/cart -b cookies.txt
```

## Checkout
```bash
curl -X POST -L \
  -F payment_method='COD' \
  -F shipping_address='123 Example St' \
  http://localhost:5000/checkout -b cookies.txt -c cookies.txt
```

## Post a comment
```bash
curl -X POST -L \
  -F post_slug='valorant' \
  -F content='Great game!' \
  http://localhost:5000/comment -b cookies.txt -c cookies.txt
```
