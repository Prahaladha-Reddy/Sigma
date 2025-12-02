from deepsearcher.configuration import Configuration, init_config
from deepsearcher.online_query import query
from deepsearcher.offline_loading import load_from_local_files
from dotenv import load_dotenv
load_dotenv()
config = Configuration()
your_local_path="thinkdsp.pdf"
config.set_provider_config('llm', 'Gemini', { 'model': 'gemini-2.0-flash' })
config.set_provider_config("embedding", "GeminiEmbedding", {"model": "text-embedding-004"})
config.set_provider_config("web_crawler", "Crawl4AICrawler", {"browser_config": {"headless": True, "verbose": True}})
init_config(config = config)

load_from_local_files(paths_or_directory=your_local_path)


# Query
result = query("Write a report about the book thinkdsp") #

print(result)