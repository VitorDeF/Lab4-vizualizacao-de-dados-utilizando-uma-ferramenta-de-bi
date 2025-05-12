# Lab4-vizualizacao-de-dados-utilizando-uma-ferramenta-de-bi

## 📁 Caracterização do Dataset

Este dataset foi construído para apoiar a pesquisa de TIS 6, cujo objetivo é analisar a presença de práticas de engenharia de software no desenvolvimento de jogos open-source hospedados no GitHub. A coleta de dados foi feita a partir de repositórios públicos relacionados ao desenvolvimento de jogos.

### 📊 Atributos Coletados

| Dimensão                    | Atributo                      | Descrição                                                                 |
|----------------------------|-------------------------------|---------------------------------------------------------------------------|
| **Informações Gerais**     | `repository_name`             | Nome do repositório                                                      |
|                            | `language`                    | Linguagem de programação principal                                       |
|                            | `created_at`                  | Data de criação do repositório                                           |
|                            | `stars`                       | Número de estrelas                                                       |
|                            | `forks`                       | Número de forks                                                          |
|                            | `contributors`                | Número de colaboradores                                                  |
| **Controle de Versão**     | `branching_strategy`          | Uso de Git Flow, trunk-based ou similar                                  |
|                            | `tags_releases`               | Presença de tags e releases no repositório                               |
| **Testes e Qualidade**     | `has_tests`                   | Indicação da presença de testes automatizados                            |
|                            | `test_coverage`               | Percentual de cobertura de testes (quando disponível)                    |
| **Gerenciamento de Tarefas** | `issues_active`             | Uso recente de issues (últimos 6 meses)                                  |
|                            | `issues_closed`               | Número de issues fechadas                                                |
|                            | `label_diversity`             | Diversidade de labels utilizadas (ex: mais de 5 tipos)                   |
|                            | `commit_issue_traceability`   | Commits que mencionam ou fecham issues                                   |
|                            | `commit_message_quality`      | Mensagens de commit estruturadas e informativas                          |
| **Documentação**           | `readme_presence`             | Presença e extensão do README.md                                         |
|                            | `additional_docs`             | Documentações complementares (wiki, tutoriais, manuais)                  |
| **Entrega e Manutenção**   | `releases_count`              | Número de releases públicas                                              |
|                            | `reviewed_prs`                | Percentual de PRs revisadas antes do merge                               |
| **Colaboração**            | `prs_with_tests`              | PRs que incluem testes automatizados                                     |
|                            | `prs_refactoring`             | PRs focadas em refatorações/melhorias estruturais                        |
|                            | `semantic_commits`            | Uso de commits semânticos nos PRs                                        |
| **Qualidade do Código**    | `bug_issue_ratio`             | Proporção de bugs reportados sobre o total de issues                     |
|                            | `bad_smells_per_kloc`         | Quantidade de bad smells por 1.000 linhas de código (KLOC)               |
|                            | `test_coverage_again`         | Cobertura de testes (reaproveitada como métrica de qualidade)            |
|                            | `coupling_level`              | Nível de acoplamento entre módulos do projeto                            |
