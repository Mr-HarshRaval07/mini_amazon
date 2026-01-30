import numpy as np
from products.models import Product


def build_feature_matrix():
    products = Product.objects.all()

    categories = list(set(p.category_id for p in products))
    specs_keys = set()

    for p in products:
        specs_keys.update(p.specifications.keys())

    cat_map = {c: i for i, c in enumerate(categories)}
    spec_map = {k: i + len(categories) for i, k in enumerate(specs_keys)}

    vectors = []
    product_ids = []

    for p in products:
        vec = np.zeros(len(categories) + len(specs_keys))

        vec[cat_map[p.category_id]] = 1

        for k in p.specifications:
            vec[spec_map[k]] = 1

        vectors.append(vec)
        product_ids.append(p.id)

    return np.array(vectors), product_ids


def recommend(product_id, top_n=4):
    matrix, ids = build_feature_matrix()

    if product_id not in ids:
        return []

    idx = ids.index(product_id)
    target = matrix[idx]

    sims = matrix @ target / (
        np.linalg.norm(matrix, axis=1) * np.linalg.norm(target) + 1e-9
    )

    ranked = np.argsort(sims)[::-1]

    rec_ids = [ids[i] for i in ranked if ids[i] != product_id][:top_n]

    return Product.objects.filter(id__in=rec_ids)
