from src.parser.science_direct import new_science_direct_articles

FEED_URL = "http://rss.sciencedirect.com/publication/science/03787753"

def main():
  _, last_title = new_science_direct_articles(FEED_URL, "Tuning the localized dissolution environment of polysulfides for practical Li-S cells")
  print(last_title)

if __name__ == "__main__":
  main()