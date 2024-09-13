""" Class for relevant ebook data """

class Ebook:
    # Note that these are only the properties during ebook creation
    # More properties are added if/when ebook is listed for sale
    def __init__(
        self,
        title,
        topic,
        target_audience,
        docx_file,
        pdf_file,
        cover_img,
        assets,
        page_count,
    ):
        self._title = title
        self._topic = topic
        self._target_audience = target_audience
        self._docx_file = docx_file
        self._pdf_file = pdf_file
        self._cover_img = cover_img
        self._assets = assets
        self._page_count = page_count

    # Getter and setter for 'title'
    def get_title(self):
        return self._title

    def set_title(self, value):
        self._title = value

    # Getter and setter for 'topic'
    def get_topic(self):
        return self._topic

    def set_topic(self, value):
        self._topic = value

    # Getter and setter for 'target_audience'
    def get_target_audience(self):
        return self._target_audience

    def set_target_audience(self, value):
        self._target_audience = value

    # Getter and setter for 'pdf_file'
    def get_pdf_file(self):
        return self._pdf_file

    def set_pdf_file(self, value):
        self._pdf_file = value

    # Getter and setter for 'cover_img'
    def get_cover_img(self):
        return self._cover_img

    def set_cover_img(self, value):
        self._cover_img = value

    # Getter and setter for 'assets'
    def get_assets(self):
        return self._assets

    def set_assets(self, value):
        self._assets = value

    # Getter and setter for 'page_count'
    def get_page_count(self):
        return self._page_count

    def set_page_count(self, value):
        self._page_count = value

    # Getter and setter for 'shopify_product_id'
    def get_shopify_product_id(self):
        return self._shopify_product_id

    def set_shopify_product_id(self, value):
        self._shopify_product_id = value

    # Getter and setter for 'shopify_variant_id'
    def get_shopify_variant_id(self):
        return self._shopify_variant_id

    def set_shopify_variant_id(self, value):
        self._shopify_variant_id = value

    # Getter and setter for 'price'
    def get_price(self):
        return self._price

    def set_price(self, value):
        self._price = value

    def get_description(self):
        return self._description

    def set_description(self, value):
        self._description = value

    def get_tags(self):
        return self._tags

    def set_tags(self, value):
        self._tags = value

    def get_preview_dir(self):
        return self._preview_dir

    def set_preview_dir(self, value):
        self._preview_dir = value

    def get_docx_file(self):
        return self._docx_file

    def set_docx_file(self, value):
        self._docx_file = value

    # Property methods
    title = property(get_title, set_title)
    topic = property(get_topic, set_topic)
    target_audience = property(get_target_audience, set_target_audience)
    pdf_file = property(get_pdf_file, set_pdf_file)
    cover_img = property(get_cover_img, set_cover_img)
    assets = property(get_assets, set_assets)
    page_count = property(get_page_count, set_page_count)
    shopify_product_id = property(
        get_shopify_product_id, set_shopify_product_id
    )
    shopify_variant_id = property(
        get_shopify_variant_id, set_shopify_variant_id
    )
    price = property(get_price, set_price)
    description = property(get_description, set_description)
    tags = property(get_tags, set_tags)
    preview_dir = property(get_preview_dir, set_preview_dir)
    docx_file = property(get_docx_file, set_docx_file)
