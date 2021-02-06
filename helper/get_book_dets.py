import re
from helper.souper import souper
import json

async def book_dets(book_url):

  soup = await souper(book_url)

  if not soup:
    dets = {"title":"❌ Error","description":"Goodreads not responding or something like that. Try Again.\n If problem persists deal with it. Don't bother Allfather"}
    with open('details.json', 'w+') as f:
        json.dump(dets, f, indent=4)
    return()
  
  book_desc = soup.find(id = "topcol")

  
  embed_dict = {}
  embed_dict["color"] = 6555343

  #Saves the title in the dict
  title =  list(book_desc.find(id = 'bookTitle').stripped_strings)
  titles = " ".join(title) if title else ""
  #print(titles + "\n")
  embed_dict["title"] = titles

  #Link for the book
  embed_dict["url"] = book_url

  #Save book description
  blurb = book_desc.find(id = 'description')
  if blurb is not None:
    descri = blurb.find_all(id=re.compile("freeText"))[-1]
    for br in descri.find_all("br"):
      br.replace_with("\n")
    descri = descri.text
    # print(descri)
    if len(descri) > 2048:
      descri = descri[:2044]+" ..."
    embed_dict["description"] = descri

  #Saves the author Name
  embed_dict["author"] = {}
  auth_name = soup.find(class_= "bookAuthorProfile__name").a.stripped_strings
  auth_name = " ".join(auth_name) if auth_name else ""
  if auth_name is not None:
    embed_dict["author"]["name"] = auth_name

  #Save link to goodreads author link
  auth_link = soup.find(class_= "bookAuthorProfile__name").a['href']
  if auth_link is not None:
    embed_dict["author"]["url"] = "https://www.goodreads.com" + auth_link

  #Save author image
  result = soup.find('div', class_="bookAuthorProfile__photo",style =True)
  # print(result['style'])
  if result is not None:
    ptr = re.search("http.*[)]",result['style']) # regex to search url till ')'
    embed_dict["author"]["icon_url"] = result['style'][ptr.start():ptr.end()-1] # end() -1 to remove ')' 
    # print(url)

  #Saves the book cover
  image = book_desc.find('img',{'id':'coverImage'})
  embed_dict["thumbnail"] = {}
  if image is not None:
    embed_dict["thumbnail"]["url"] = image['src']

  embed_dict["fields"] = []
    
  #Saves the book Rating
  rating = book_desc.find(itemprop = "ratingValue").stripped_strings
  rating = "".join(rating) if rating else ""
  if rating is not None:
    embed_dict["fields"].append(dict({"name":"⭐ Avg. Rating","value":rating,"inline":True}))

  #Saves the number of pages
  pages = book_desc.find(itemprop = "numberOfPages")
  if pages is not None:
    pages = pages.stripped_strings
    pages = " ".join(pages) if pages else ""
    if pages is not None:
      embed_dict["fields"].append(dict({"name":"📄 Pages","value":pages,"inline":True}))

  #Saves the genres
  right_container = soup.find(class_= "rightContainer")
  if right_container is not None:
    genres = right_container.find_all(class_= "bookPageGenreLink")
    # print(type(genres))
    genre_list ="Goodreads doesn't care enough for this book's genres"
    if genres:
      genre_list = ""
      for genre in genres:
        # print(genre)
        if genre.parent['class'][0] == 'left':
          genre_list += genre.text + ', ' 
          # print(genre_list)
  embed_dict["fields"].append(dict({"name":"➡️ Genres","value":genre_list}))

  # print(embed_dict)
  return embed_dict