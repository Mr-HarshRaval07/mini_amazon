from products.models import Product

BASE_URL = "http://127.0.0.1:8000"

def product_link(product):
    return f'<a href="http://127.0.0.1:8000/product/{product.id}/" target="_blank">View product</a>'


def get_bot_reply(message):
    msg = message.lower()

    # Cheapest product
    if "cheapest" in msg or "lowest price" in msg:
        product = Product.objects.order_by('price').first()
        if product:
            return (
                f"Cheapest product is {product.name} at ₹{product.price}\n"
                f"👉 {product_link(product)}"
            )
        return "No products found."

    # Most expensive product
    if "costliest" in msg or "most expensive" in msg or "highest price" in msg:
        product = Product.objects.order_by('-price').first()
        if product:
            return (
                f"Most expensive product is {product.name} at ₹{product.price}\n"
                f"👉 {product_link(product)}"
            )
        return "No products found."

    # Specific product search by name
    products = Product.objects.filter(name__icontains=msg)
    if products.exists():
        product = products.first()
        return (
            f"Found {product.name} at ₹{product.price}\n"
            f"👉 {product_link(product)}"
        )

    # Products under price
    if "under" in msg:
        for word in msg.split():
            if word.isdigit():
                price = int(word)
                products = Product.objects.filter(price__lte=price)
                if products.exists():
                    reply = f"Products under ₹{price}:\n"
                    for p in products[:5]:
                        reply += f"{p.name} – ₹{p.price}\n👉 {product_link(p)}\n"
                    return reply
                return "No products in that range."

    # Greeting
    if "hi" in msg or "hello" in msg:
        return "Hi 👋 I can help you find products and prices. Try asking 'cheapest mobile' or product name."

    return "Sorry, I didn't understand. Try asking about cheapest, expensive, or product name."
