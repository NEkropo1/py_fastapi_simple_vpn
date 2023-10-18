import random
import httpx
import asyncio
import main

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from engine import get_session
from models import Site


PROXIES = {
    "proxy1": {
        "address": "proxy1.example.com",
        "port": 8000,
        "username": "user1",
        "password": "password1"
    },
    "proxy2": {
        "address": "proxy2.example.com",
        "port": 8000,
        "username": "user2",
        "password": "password2"
    },

}


def select_random_proxy() -> dict:
    return random.choice(list(PROXIES.values()))


created_endpoints = set()  # hoho haha, if you want to save it to db - refactor this!


async def get_site_content_with_random_proxy(original_site_url: str) -> str:
    proxy = select_random_proxy()
    url = f"https://{proxy['address']}:{proxy['port']}/{original_site_url}"
    async with httpx.AsyncClient(
            proxies={
                "https": f"https://{proxy['username']}:{proxy['password']}@{proxy['address']}:{proxy['port']}"
            }
    ) as client:
        try:
            response = await asyncio.wait_for(client.get(url), timeout=3)
            if response.status_code == 200:
                with get_session() as session:
                    site = session.query(Site).filter(Site.url == original_site_url).first()
                    if site:
                        site.follow_counter += 1
                        site.data_uploaded += len(response.content)
                        site.data_downloaded += len(response.text)
            return response.text
        except httpx.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except asyncio.TimeoutError as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except Exception as err:
            print(f"An error occurred: {err}")


def create_endpoint(modified_link: str):
    async def handler():
        site_content = await get_site_content_with_random_proxy(modified_link)
        refactored_content = await refactor_site_content(site_content,
                                                         modified_link)
        return refactored_content

    @main.router.get(f"/{modified_link}/", response_model=None)
    async def dynamic_route():
        return await handler()

    main.app.include_router(main.router)


async def refactor_site_content(site_content: str, user_site_name: str) -> str:
    soup = BeautifulSoup(site_content, "html.parser")
    for link in soup.find_all("a", href=True):
        parsed_url = urlparse(link["href"])
        if user_site_name in parsed_url.netloc:
            modified_link = link["href"].replace(user_site_name, f"localhost.{user_site_name}")
            link["href"] = modified_link
            if modified_link not in created_endpoints:
                create_endpoint(modified_link)
                created_endpoints.add(modified_link)
    return str(soup)
