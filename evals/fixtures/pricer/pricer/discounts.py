def apply_discounts(subtotal, coupons):
    """Apply coupons to an order.

    Percentage coupons are defined as a percentage of the order subtotal.
    Flat coupons subtract a fixed amount. The total never goes below zero.
    """
    total = subtotal
    for kind, value in coupons:
        if kind == "percent":
            total -= total * value / 100.0
        elif kind == "flat":
            total -= value
        else:
            raise ValueError("unknown coupon kind: " + kind)
    return round(max(total, 0.0), 2)
