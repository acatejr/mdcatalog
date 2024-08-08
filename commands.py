import typer
import requests
from bs4 import BeautifulSoup
import re, os
import arrow
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from models import Domain, Asset

load_dotenv()

Base = declarative_base()

PG_USER = os.environ.get("POSTGRES_USER")
PG_PASS = os.environ.get("POSTGRES_PASSWORD")
dburl = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@mdcatalogdb/postgres"
engine = create_engine(dburl)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = typer.Typer()


def remove_html(text):
    txt = re.sub("<[^<]+?>", "", text).replace("\n", "")
    return txt


@app.command()
def load_data_dot_gov():
    SEED_URLS = [
        "https://catalog.data.gov/harvest/object/203bed83-5da3-4a64-b156-ea016f277b07",
        "https://catalog.data.gov/harvest/object/04643a90-e5fd-4602-a8fa-e8195dd16c5e",
        "https://catalog.data.gov/harvest/object/abf916ec-6ddd-4030-8f5e-3b317a33ba1e",
        "https://catalog.data.gov/harvest/object/589436ca-1324-4773-9201-acecd5d83448",
        "https://catalog.data.gov/harvest/object/21392fa4-ff86-4ac8-9f38-33d67aef770c",
        "https://catalog.data.gov/harvest/object/9216c0ce-d083-48a6-b017-e0efc0fada37",
        "https://catalog.data.gov/harvest/object/0b20b4e4-34f8-4d1d-ae1c-7a405d0f6d36",
        "https://catalog.data.gov/harvest/object/36b9144a-dc24-43cf-85c3-49a08dbed762",
        "https://catalog.data.gov/harvest/object/9d60be08-5c3b-45a7-8ae6-017a4ca9433c",
        "https://catalog.data.gov/harvest/object/a4a75240-4fac-40f7-a327-6596becff636",
        "https://catalog.data.gov/harvest/object/8df82322-0812-46c7-b2b3-52829a8417e1",
        "https://catalog.data.gov/harvest/object/0419db56-01a4-4a97-a4f0-1fb903e77cdf",
        "https://catalog.data.gov/harvest/object/32d5b113-e83c-48f3-b05a-fd99ed7a3a92",
        "https://catalog.data.gov/harvest/object/f2e66a1c-10b6-4243-920a-0b64352b8c63",
        "https://catalog.data.gov/harvest/object/a0a63e30-b3cb-418b-8616-d89ee2e9e100",
    ]

    domain = session.query(Domain).filter(Domain.name == "data.gov").first()

    for url in SEED_URLS:
        resp = requests.get(url).json()
        description = resp["description"]
        desc = remove_html(description)
        title = resp["title"]
        modified = arrow.get(resp["modified"])

        asset = Asset(title=title, description=desc, domain_id=domain.id, metadata_url=url)

        session.add(asset)
        session.commit()


@app.command()
def load_fsgeodata():
    domain = session.query(Domain).filter(Domain.name == "US Forest Service Geodata").first()
    base_url = "https://data.fs.usda.gov/geodata/edw/datasets.php"
    
    print("Loading data from FSGeodata Clearinghouse Metdata URLs.")
    # Read the page that has the matedata links and cache locally
    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.content, "html.parser")

    anchors = soup.find_all("a")
    metadata_urls = []
    for anchor in anchors:
        if anchor and anchor.get_text() == "metadata":
            metadata_urls.append(anchor["href"])

    for url in metadata_urls:
        url = f"https://data.fs.usda.gov/geodata/edw/{url}"
       
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        title = remove_html(soup.find("title").get_text())   
        desc_block = soup.find("descript")
        abstract = remove_html(desc_block.find("abstract").get_text())

        existing_asset = session.query(Asset).filter(or_(Asset.metadata_url == url, Asset.title == title)).first()
        if not existing_asset:

            asset = Asset(
                metadata_url=url,
                title=title,
                description=abstract,
                domain_id=domain.id,
                # modified=str(date_of_last_refresh),
            )
            session.add(asset)

    session.commit()

if __name__ == "__main__":
    app()


"""
asset = Asset.objects.filter(Q(metadata_url=url) | Q(title=title))
if asset:
    asset = asset[0]
    asset.description = abstract
    asset.domain = domain
    asset.save()
else:
    asset = Asset(
        metadata_url=url,
        title=title,
        description=abstract,
        domain=domain,
        # modified=str(date_of_last_refresh),
    )
    asset.save()

print(f"{url}")

"""
