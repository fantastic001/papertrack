# Papertrack 

A tool for managing documents, their states and their metadata as well as their collection. 

Example of downloading package from arxiv:

```
papertrack get --downloader simple --collector simple \
    --title "A consumption-investment model with state-dependent lower bound constraint on consumption" \
    --year 2021 \
    --author "Chonghu Guan" --author "Zuo Quan Xu" --author "Fahuai Yi" \
    --download-url https://arxiv.org/pdf/2109.06378.pdf \
    --field "Math/Finance"

```


Papertrack can be configured using configuration file as one below in `~/.papertrack/config.json`:


```
{
	"states": {
		  "READY": {
			   "READING": "Start reading",
		  },
		  "READING": {
			     "DONE": "Finish reading",
			     "READY": "Bring back to to-read state"
		  }, 
          "DONE": {}
	},
	"default_state": "READY",
	"storage_location": "/home/user/MyPapers/",
	"fields": {
		  "Computer Science": {
			    "default": "Algorithms",
			    "categories": ["Algorithms", "Theory"]
		  }
	},
	"default_field": "Computer Science"
}
```

