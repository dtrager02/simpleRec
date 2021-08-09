import sqlite3
import random
import itertools

# con = sqlite3.connect('../animeInfo.sqlite3')
# cur = con.cursor()

def getAnimeQuery(num, diff):
    if diff == "easy":
        return f"select anime_title,image_url,opening_song_ids,opening_titles,english_title from anime_info where occurances > 100000 and opening_song_ids not null order by random() limit {num}"
    elif diff == "medium":
        return f"select anime_title,image_url,opening_song_ids,opening_titles,english_title  from anime_info where occurances > 30000 and opening_song_ids not null order by random() limit {num}"
    else:
        return f"select anime_title,image_url,opening_song_ids,opening_titles,english_title from anime_info where occurances < 30000 and occurances > 2000 and opening_song_ids not null order by random() limit {num}"

def flatten_lists(the_lists):
    result = []
    for _list in the_lists:
        result += _list
    return result

def select(w,x,y,z,a):
    """
    w=anime_title
    x=image_url
    y=opening_song_ids
    z=opening_titles
    """
    links = y.split('||')
    titles = z.split('||')
    choice = random.randint(0,len(links)-1)
    return (w,x,links[choice].replace('/watch?v=',''),titles[choice].replace('/watch?v=',''),a)

def queryProcessing(cur, num, diff):
    items = cur.execute(getAnimeQuery(num,diff)).fetchall()
    #processes query using select function which shortens youtube vidio IDs and picks random videos from sets
    return list(itertools.starmap(select,items)) 

def autocomplete(cur,string):
    titles = cur.execute("select a1.anime_title,a2.english_title from anime_info a1 left join anime_info a2 on a1.id = a2.id where a1.anime_title like ? or a2.english_title like ?",("%"+string+ "%","%"+string+"%")).fetchall()
    check = lambda x: (x[0],) if x[0]==x[1] else x
    #print(titles[:5])
    titles = list(map(check,titles))
    print(titles[:5])
    titlesSingle = itertools.chain.from_iterable(titles)
    
    #print({'data':list(titlesSingle)[:5]})
    return {'data':list(titlesSingle)[:5]}
    #return {'data':["a","b","c"]}
