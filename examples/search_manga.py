from __future__ import annotations

import asyncio
import datetime

import hondana


client = hondana.Client()


async def search_for_tags() -> hondana.MangaCollection:
    # Using the tag builder for ease during a query
    # This will add a restriction to search for a manga with all 3 of these tags using logical AND
    tags = hondana.QueryTags("action", "comedy", "isekai", mode="AND")

    # we now perform a search with a limit of 10 (returned manga)
    # an offset of 0 (pagination needs)
    # and using our predefined tags earlier.
    manga_response = await client.manga_list(limit=10, offset=0, included_tags=tags)

    # `manga_response` will be a list of up to 10 manga that match the search criteria above.
    return manga_response


async def more_refined_search() -> hondana.MangaCollection:
    # let's do a more refined search using many of the query parameters...
    tags = hondana.QueryTags("action", "comedy", "isekai", mode="AND")

    # Let's say we only way to show manga created in the last week, lets make an aware utc datetime for one week ago
    seven_days_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)

    # and we don't want anything but ongoing manga
    status: list[hondana.MangaStatus] = [hondana.MangaStatus.ongoing]

    # and we probably just want shounen... right?
    demographic: list[hondana.PublicationDemographic] = [hondana.PublicationDemographic.shounen]

    # let's try a search
    search = await client.manga_list(
        limit=10,
        offset=0,
        included_tags=tags,
        publication_demographic=demographic,
        status=status,
        created_at_since=seven_days_ago,
    )

    return search


async def main():
    manga = await search_for_tags()
    print(manga)

    other_manga = await more_refined_search()
    # this search was empty for me at the time of writing, but the fact you get a response at all means it worked.
    print(other_manga)

    await client.close()


asyncio.run(main())
