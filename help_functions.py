def overlay_image_alpha(img, img_overlay, pos, alpha_mask):
    """Overlay img_overlay on top of img at the position specified by
    pos and blend using alpha_mask.

    Alpha mask must contain values within the range [0, 1] and be the
    same size as img_overlay.
    """

    x, y = pos

    # Image ranges
    y1 = max(0, y-img_overlay.shape[0]//2)
    y2 = min(y1+img_overlay.shape[0], img.shape[0])
    x1 = max(0, x - img_overlay.shape[1] // 2)
    x2 = min(x1 + img_overlay.shape[1], img.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y1), min(img_overlay.shape[0], img.shape[0] - y1)
    x1o, x2o = max(0, -x1), min(img_overlay.shape[1], img.shape[1] - x1)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    channels = img.shape[2]

    alpha = alpha_mask[y1o:y2o, x1o:x2o]
    alpha_inv = 1.0 - alpha

    for c in range(channels):
        img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] +
                                alpha_inv * img[y1:y2, x1:x2, c])

    return img
