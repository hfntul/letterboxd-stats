# Letterboxd Stats

Your Letterboxd is not pro or patron account? Me too. But here we go
- Export your Letterboxd data. Choose the one named `watched.csv` and `ratings.csv`
- Request API key to TMDb. I use their API because Letterboxd uses it too although it's not endorsed or certified by them. Also Letterboxd API is hard to be requested, it doesn't have much documentation and there's no wrapper too
- Install [tmdbsimple](https://github.com/celiao/tmdbsimple) as the API wrapper

An example of the result using my Letterboxd

![Screenshot from 2021-09-22 17-02-53](https://user-images.githubusercontent.com/60166588/134324227-66d14ab2-32bf-4b7d-aacb-f6389f4f0d36.png)

I always want to see this

![Untitled document (1)_page-0003](https://user-images.githubusercontent.com/60166588/134343253-a5e3c650-4eb9-45dc-a004-7c6b5ce797f5.jpg)

Also this 

![four](https://user-images.githubusercontent.com/60166588/134301263-80b5f6ac-c0e8-4163-8352-8a6adacede6f.jpg)

### Note
- Rewatch not included
- The stat is only for films. Tv shows are gonna be removed in the process
- Some films might have the wrong information because it takes the wrong TMDb id. Since the data that Letterboxd gives only provide the title and the release year of the film, I only can use those two as the parameter to fetch the id and it's kinda tough. So mistake may occur if there's another film that have the same title and the release year and its index is in front of the real one.
- Not much but some films on TMDb have different titles from the ones on Letterboxd so it will be removed immediately along with the tv shows.
- The result is not that accurate but it's good enough

