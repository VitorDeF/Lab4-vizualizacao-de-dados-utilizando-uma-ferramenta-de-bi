import os
import requests
import pandas as pd
import tempfile
import shutil
import git
import stat

GITHUB_TOKEN = ""
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

SEARCH_QUERY = """
{
  search(query: "language:Python topic:game", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        name
        nameWithOwner
        url
        defaultBranchRef {
          name
        }
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
    data = response.json()
    return data["data"]["search"]["nodes"]

def handle_remove_readonly(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def analisar_testes_em_repositorio(clone_url):
    tmp_dir = tempfile.mkdtemp()
    try:
        git.Repo.clone_from(clone_url, tmp_dir, depth=1)
        has_test_folder = False
        test_files = []
        test_frameworks = set()
        
        for root, dirs, files in os.walk(tmp_dir):
            for d in dirs:
                if d.lower() in ["test", "tests"]:
                    has_test_folder = True
            for f in files:
                if f.startswith("test_") or f.endswith("_test.py"):
                    test_files.append(os.path.join(root, f))
                if f.endswith(".py"):
                    path = os.path.join(root, f)
                    try:
                        with open(path, "r", encoding="utf-8") as file:
                            content = file.read()
                            if "unittest" in content:
                                test_frameworks.add("unittest")
                            if "pytest" in content:
                                test_frameworks.add("pytest")
                            if "nose" in content:
                                test_frameworks.add("nose")
                    except Exception:
                        continue

        return {
            "has_test_folder": has_test_folder,
            "num_test_files": len(test_files),
            "frameworks": ", ".join(test_frameworks) if test_frameworks else "Nenhum"
        }
    except Exception as e:
        return {
            "has_test_folder": False,
            "num_test_files": 0,
            "frameworks": f"Erro: {str(e)}"
        }
    finally:
        shutil.rmtree(tmp_dir, onerror=handle_remove_readonly)

def main():
    repos = buscar_repositorios()
    resultados = []

    for repo in repos:
        if repo["isFork"]:
            continue

        result = analisar_testes_em_repositorio(f"https://github.com/{repo['nameWithOwner']}.git")
        resultados.append({
            "repo": repo["nameWithOwner"],
            "url": repo["url"],
            "has_test_folder": result["has_test_folder"],
            "num_test_files": result["num_test_files"],
            "frameworks_detected": result["frameworks"]
        })

    df = pd.DataFrame(resultados)
    df.to_csv("repositorios_python_jogos_com_testes.csv", index=False)

if __name__ == "__main__":
    main()
