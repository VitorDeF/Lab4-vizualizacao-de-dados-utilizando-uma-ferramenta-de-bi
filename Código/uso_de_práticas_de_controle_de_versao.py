import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = ""
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

SEARCH_QUERY = """
{
  search(query: "language:Python topic:game", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        nameWithOwner
        url
        isFork
      }
    }
  }
}
"""

def buscar_repositorios():
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": SEARCH_QUERY},
        headers=HEADERS
    )

    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")
    
    dados = response.json()
    if "data" not in dados or "search" not in dados["data"]:
        raise Exception(f"Erro inesperado na resposta: {dados}")
    
    return dados["data"]["search"]["nodes"]

def obter_branches(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/branches"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return []
    return [branch["name"] for branch in r.json()]

def detectar_branching_strategy(branches):
    branches_lower = [b.lower() for b in branches]

    if "develop" in branches_lower or any(b.startswith("release/") or b.startswith("hotfix/") for b in branches_lower):
        return "git-flow"

    if set(branches_lower).issubset({"main", "master"}) or len(branches_lower) <= 2:
        return "trunk-based"

    return "outro"

def tem_tags(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/tags"
    r = requests.get(url, headers=HEADERS)
    return len(r.json()) > 0 if r.status_code == 200 else False

def tem_releases(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/releases"
    r = requests.get(url, headers=HEADERS)
    return len(r.json()) > 0 if r.status_code == 200 else False

def main():
    repos = buscar_repositorios()
    resultados = []

    for repo in repos:
        if repo["isFork"]:
            continue
        nome = repo["nameWithOwner"]

        try:
            branches = obter_branches(nome)
            branching_strategy = detectar_branching_strategy(branches)
            usa_git_flow = branching_strategy == "git-flow"
            usa_trunk_based = branching_strategy == "trunk-based"
            tags = tem_tags(nome)
            releases = tem_releases(nome)

            resultados.append({
                "repo": nome,
                "url": repo["url"],
                "usa_git_flow": usa_git_flow,
                "usa_trunk_based": usa_trunk_based,
                "tem_tags": tags,
                "tem_releases": releases
            })
        except Exception as e:

    df = pd.DataFrame(resultados)
    df.to_csv("repositorios_python_controle_versao.csv", index=False)

if __name__ == "__main__":
    main()
