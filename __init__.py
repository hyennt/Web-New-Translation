import requests
import openai
from bs4 import BeautifulSoup

# Define a function to split text into chunks of a given maximum length
def split_text(text, max_len):
    # Split the text into words
    words = text.split()
    chunks = []
    chunk = ""
    for word in words:
        # If adding the next word to the current chunk would exceed the maximum length,
        # append the current chunk to the list of chunks and start a new chunk
        if len(chunk) + len(word) + 1 > max_len:
            chunks.append(chunk.strip())
            chunk = ""
        # Otherwise, add the word to the current chunk
        chunk += " " + word
    # Append the last chunk to the list of chunks
    if chunk:
        chunks.append(chunk.strip())
    return chunks

# Define a function to translate a given text into a target language using OpenAI's GPT
def translate(lang, text):
    key = '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'
    openai.api_key = key
    print("Translating to:", lang)
    print("Please wait ... ")
    # Split the text into smaller chunks using a maximum token length of 990
    chunks = split_text(text, 990)
    # Translate each chunk and append the translated text to a list
    translated_chunks = []
    for chunk in chunks:
        # Use the translation API
        translation = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Translate this {len(chunk)}-character text into {lang}: {chunk}",
            temperature=0.7,
            max_tokens=1024,
            n=1,
            timeout=10,
            stop=None
        )
        # Extract the translated text from the API response
        translated_text = translation.choices[0].text.strip()
        translated_chunks.append(translated_text)
    # Join the translated chunks into a single string and return it
    translated_text = " ".join(translated_chunks)
    return translated_text

def save_to_file(lang,title, content, content_trans):
    f = open('Data.txt', 'w', encoding="utf-8")
    f.write("Title: ")
    f.writelines(title)
    f.write("\n")
    f.write("Content: ")
    f.writelines(content)
    f.write("\n")
    f.write("Translate: ")
    f.writelines(translate(lang, content_trans))
    f.write("\n")
    f.close()

# Define a function to crawl content from a given number of pages on a website, translate the content,
# and output the translated text into a PDF file
def crawlContent(nPage):
    url = "https://vnexpress.net"

    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser", from_encoding='utf-8')

    # find all article links in the homepage
    article_links = [a['href'] for i, a in enumerate(soup.select('h3.title-news a[href]')) if i < nPage]
    print(article_links)

    # loop through each article link and extract the content
    for link in article_links:
        article_req = requests.get(link)
        article_soup = BeautifulSoup(article_req.content, "html.parser")

        # extract the article title and content
        title = article_soup.find('h1', {'class': 'title-detail'})
        if title is None:
            break
        else:
            title = title.text.strip()
        content = [p.get_text() for p in article_soup.find_all('p')]
        string = ''.join(content)
        print("Title:", title)

        # split content into chunks of 1000 tokens or less and translate each chunk
        chunk_size = 1000
        chunks = [string[i:i + chunk_size] for i in range(0, len(string), chunk_size)]
        translated_chunks = [translate('English', chunk) for chunk in chunks]

        # join the translated chunks into a single string
        translated_text = ''.join(translated_chunks)

        # print the translated text
        print("Translated content:", translated_text)
        print('\n')

        # Translate the content if it hasn't already been translated
        if not string.startswith("Translated to"):
            # Split the content into chunks of 1000 tokens or less
            chunks = [string[i:i + 1000] for i in range(0, len(string), 1000)]
            translated_chunks = []

            # Translate each chunk
            for chunk in chunks:
                translated_chunk = translate('English', chunk)
                translated_chunks.append(translated_chunk)

            # Combine the translated chunks into a single string
            translated_string = ''.join(translated_chunks)

            # Print the translated text
            print("Translating is in progress. Please wait ... ")
            print(translated_string)
            print('\n')

            # Write the translated text to a PDF file
    save_to_file('English', title, content, translated_string)

if __name__ == "__main__":
    crawlContent(1)
