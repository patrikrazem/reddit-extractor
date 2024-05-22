# Reddit-extractor

A simple Python tool to extract Reddit threads into a JSON file.

## Dev setup

1. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

1. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

1. Place an `.env` file in the root directory with the following content:
    ```bash
    REDDIT_CLIENT_ID=<your Reddit client ID>
    REDDIT_CLIENT_SECRET=<your Reddit client secret>
    REDDIT_USERNAME=<your Reddit username>
    REDDIT_PASSWORD=<your Reddit password>
    REDDIT_USER_AGENT=<your Reddit user agent>
    ```

1. Add threads you want to extract in the `main.py` file:
    ```python
    # List of URLs/posts to extract
    TARGETED_URLS = [
        "https://www.reddit.com/r/funny/comments/1crnefz/a_man_returns_from_the_doctor_and_tells_his_wife/",
        "https://www.reddit.com/r/AmItheAsshole/comments/1cu5vzu/aita_for_sticking_to_my_word_and_not_giving_my/"
    ]
    ```

1. Run the script:
    ```bash
    python main.py
    ```

1. The extracted threads will be saved in the `output` directory.