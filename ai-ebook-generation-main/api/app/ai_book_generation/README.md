# AI EBook Generator 🤖📚

## Description 📖

This repository is designed to automate the generation of eBooks. 🤖📚

## Usage 🚀

To generate eBook content, run the following command in your terminal:

1. Install dependencies.
    ```
    pip3 install -r requirements.txt
    brew install poppler
    ```

2. Edit the variables in runner.py appropriately

3. Configure your API keys. Ask a dev for the secret.sh and then run (within api/)

    ```
    source app/secret.sh
    aws configure
    ```

4. Run script

    ```
    python3 -m app.ai_book_generation.runner
    ```

5. The ebook will be generated in the specified directory and be [listed](https://fcfcec.myshopify.com/products/retirement-in-cupertino-the-ultimate-guide-to-securing-your-dream-e-book-3) on our shopify store.

## Example

[View Example](mvp/cupertino_retirement_ebook.pdf)

## Current E2E Flow

1. Dev chooses a topic and target audience for the ebook
2. Dev runs runner.py script
3. Ebook is completed. It will be listed on the Shopify store if the add_to_shop param is set to True.

On to the selling / marketing parts!

## Dev

To run individual components, we have setup scripting such that you can run them in isolation:
```
    python3 -m app.ai_book_generation.store.shopify_generator
```

or

```
    python3 -m app.ai_book_generation.content.ebook_content_generator
```

