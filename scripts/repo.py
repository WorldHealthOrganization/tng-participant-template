import os
from git import Repo

with open('temp/repo') as f:  
  repo = Repo.clone_from(f.readline().replace("\n", ""), "repo")
  tagList=repo.git.ls_remote("--tags", "origin")
  tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
  latest_tag = tags[-1]
  repo.git.checkout(latest_tag)
  os.system("echo '"+latest_tag.object.hexsha+"'> temp/tag")