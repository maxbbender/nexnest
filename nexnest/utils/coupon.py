from nexnest.models.coupon import Coupon


def couponExists(couponKey):
    coupon = Coupon.query.filter_by(coupon_key=couponKey).first()

    if coupon is not None:
        return True

    return False
