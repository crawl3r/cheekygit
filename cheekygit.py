import requests
import sys
import json
import os
from dotenv import load_dotenv

def get_repo_list(user):
    #################################################
    # https://api.github.com/users/{git-user}/repos #
    #################################################
    repo_req = requests.get(
        "https://api.github.com/users/{}/repos".format(user),
        auth=(os.getenv("GITHUB_USERNAME"), os.getenv("GITHUB_TOKEN"))
    )
    repo_json = repo_req.json()

    repo_count = len(repo_json)
    if repo_count > 0:
        #print("[*] Found %d repositories" % repo_count)

        repo_names = []
        for r in repo_json:
            name = r["name"]
            repo_names.append(name)
            #print("\t%s" % name)

        return repo_names
    else:
        #print("[*] No repositories found")
        return []


def get_repo_commit_data(user, name):
    #######################################################
    # https://api.github.com/repos/{git-user}/{repo-name} #
    #######################################################
    repo_req = requests.get(
        "https://api.github.com/repos/{}/{}/commits".format(user, name),
        auth=(os.getenv("GITHUB_USERNAME"), os.getenv("GITHUB_TOKEN"))
    )
    repo_json = repo_req.json()
    #print("--%s-- (%d)" % (name, len(repo_json)))

    commit_data = []
    for commit in repo_json:
        data = {}
        data["sha"] = commit["sha"]
        data["author_name"] = commit["commit"]["author"]["name"]
        data["author_email"] = commit["commit"]["author"]["email"]
        data["commit"] = commit["commit"]["url"]
        commit_data.append(data)

    return commit_data


def main(user):
    # 1) GET REPOSITORY NAMES
    repos_name = get_repo_list(user)

    # 2) LOOP THE REPOSITORY COMMITS
    names_and_emails = []

    for name in repos_name:
        commit_data = get_repo_commit_data(user, name)

        for c in commit_data:
            if object_exists(c, names_and_emails) == False:
                names_and_emails.append({"name": c["author_name"], "email": c["author_email"]})

    # Final print out (json)
    print(json.dumps(names_and_emails))


# utility
def object_exists(obj, arr):
    for a in arr:
        if a["name"] == obj["author_name"] and a["email"] == obj["author_email"]:
            return True
        
    return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 %s username" % sys.argv[0])
        sys.exit()

    load_dotenv()
    if os.getenv("GITHUB_USERNAME") == "username" or os.getenv("GITHUB_TOKEN") == "token":
        print("Not Github user/token found. Rate limiting might kick in")

    main(sys.argv[1])