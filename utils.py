from google.cloud import bigquery
import pandas as pd
# returns table of recommendations

def getRecs(client:bigquery.Client,search:str):
    search = search.replace("%20"," ").replace("+"," ")
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(None, "STRING", search)
        ]

    )
    getId = client.query("select id from `heroic-throne-301401.animeDB2.anime_info1` order by animeDB2.levenshtein('?',anime_title) limit 1;",  job_config=job_config).result()
    input = list(getId)[0][0]
    print(input)
    # Start the query, passing in the extra configuration.
    query_job = client.query(
        f"""
    select c,anime_title,image_url,score from
    (select corr(u.score,f.score) c, f.anime_id id2 from 
    (select * from animeDB2.user_records3 where anime_id = {input}) u inner join `heroic-throne-301401.animeDB2.user_records2` f
     on u.username = f.username group by id2 having count(id2)>10000) inner join `heroic-throne-301401.animeDB2.anime_info1` on id2 = id  order by c    desc; 
    """  )  # Make an API request.
    result = query_job.result()
    df = result.to_dataframe()
    table = df.to_html()
    table['image_url'] = table['image_url'].apply(lambda x: f'<img src="{x}">')
    return df.to_html()