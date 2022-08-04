# CheekyGit  
  
Scrape a Github user/orgs repositiories for all names and emails of the authors.  
  
Initially used for OSINT tasks to try find emails used 'accidentally' to perform commits.  

Reqs?
```
python-dotenv
```

Usage:  
```
python3 cheekygit.py Hacker0x01 | jq
```
  
Recommended: Populate the .env file with your github auth token to allow more requests before rate limiting kicks in. I haven't accounted for rate limiting yet so it will just fall over if you hit it.  
  
## TODO
- Async the requests?
- Account for rate limiting
- More output options, currently just spits out json