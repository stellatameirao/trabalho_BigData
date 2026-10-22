# Análise de Candidaturas e Financiamento Eleitoral — Eleições Municipais de 2024

## 1. Apresentação do projeto

Este projeto foi desenvolvido na disciplina de Big Data e tem como objetivo preparar, integrar, modelar e armazenar dados públicos das eleições municipais brasileiras de 2024.

O estudo investiga a representatividade de gênero e raça/cor nas candidaturas, considerando também a distribuição dos recursos financeiros de campanha.

Nesta etapa, o trabalho contempla a construção de um processo de ETL (Extração, Transformação e Carga), o armazenamento dos dados tratados em PostgreSQL na nuvem e a representação da infraestrutura utilizando Terraform.

## 2. Fontes de dados

Os dados foram obtidos no Repositório de Dados Eleitorais do Tribunal Superior Eleitoral (TSE).

Fonte: https://dadosabertos.tse.jus.br/

Foram utilizadas duas bases:

| Base | Arquivo | Registros originais |
|---|---|---:|
| Candidaturas de 2024 | `consulta_cand_2024_BRASIL.csv` | 463.875 |
| Receitas de candidatos de 2024 | `receitas_candidatos_2024_BRASIL.csv` | 2.041.006 |

O recorte temporal corresponde às eleições municipais de 2024, abrangendo candidaturas de municípios brasileiros.

As bases originais são mantidas localmente em `dados/brutos/` e não são versionadas no GitHub.

## 3. Tecnologias utilizadas

- Python e Pandas: leitura, limpeza, transformação e integração dos dados.
- SQL: modelagem da tabela e consultas de validação.
- PostgreSQL: armazenamento relacional dos dados tratados.
- Aiven: hospedagem do PostgreSQL em ambiente de nuvem.
- Terraform: representação e gerenciamento da infraestrutura como código.
- Git e GitHub: controle de versão e disponibilização do projeto.
- Visual Studio Code: ambiente de desenvolvimento.

## 4. Processo de ETL

O processamento é realizado pelo script `etl/tratamento_dados.py`.

### 4.1 Extração

Os arquivos CSV originais são lidos com Python e Pandas.

A base de receitas é processada em blocos de 100.000 registros, reduzindo a necessidade de carregar todo o arquivo simultaneamente na memória.

### 4.2 Seleção e transformação

Foram selecionados os atributos relevantes para o objetivo da análise, descartando informações pessoais desnecessárias, como CPF, e-mail e título de eleitor.

As principais transformações incluem:

- Padronização de campos textuais.
- Conversão de tipos numéricos e datas.
- Tratamento de valores ausentes e marcadores de nulidade.
- Conversão dos valores monetários das receitas.
- Agregação dos recursos financeiros por identificador de candidatura (`SQ_CANDIDATO`).
- Integração das bases por meio do identificador da candidatura.
- Substituição por zero dos valores de receita não encontrados na integração.

### 4.3 Tratamento de duplicidades

Durante o processamento, foram identificados registros repetidos associados às candidaturas e às informações de turnos eleitorais.

Para evitar a contagem duplicada de uma mesma candidatura, foram aplicadas regras de seleção e deduplicação, incluindo a remoção de registros intermediários do segundo turno e a priorização de informações com situação eleitoral definitiva.

A base final possui um registro por identificador de candidatura.

### 4.4 Resultados do tratamento

| Indicador | Resultado |
|---|---:|
| Candidaturas na base original | 463.875 |
| Registros originais de receitas | 2.041.006 |
| Candidaturas na base tratada | 463.669 |
| Atributos da base tratada | 15 |
| Identificadores duplicados na base final | 0 |
| Datas de nascimento ausentes | 46 |
| Situações eleitorais ausentes | 16.167 |

A versão tratada foi exportada para `dados/tratados/base_eleicoes_2024_tratada.csv`.

Também foi gerada a versão `dados/tratados/base_eleicoes_2024_banco.csv`, organizada para a importação no PostgreSQL.

## 5. Modelagem e armazenamento

Os dados são armazenados em uma tabela relacional denominada `candidaturas_2024`.

O identificador `sq_candidato` é utilizado como chave primária, garantindo a unicidade de cada candidatura.

A estrutura possui 15 atributos:

| Atributo | Tipo | Descrição |
|---|---|---|
| `sq_candidato` | BIGINT | Identificador único da candidatura |
| `ano_eleicao` | INTEGER | Ano da eleição |
| `sg_uf` | CHAR(2) | Unidade federativa |
| `nm_ue` | TEXT | Unidade eleitoral |
| `ds_cargo` | TEXT | Cargo disputado |
| `nm_candidato` | TEXT | Nome da candidatura |
| `sg_partido` | TEXT | Sigla do partido |
| `dt_nascimento` | DATE | Data de nascimento |
| `ds_genero` | TEXT | Gênero |
| `ds_cor_raca` | TEXT | Raça/cor |
| `ds_grau_instrucao` | TEXT | Grau de instrução |
| `ds_ocupacao` | TEXT | Ocupação |
| `ds_situacao_candidatura` | TEXT | Situação da candidatura |
| `ds_sit_tot_turno` | TEXT | Resultado eleitoral |
| `total_receitas` | NUMERIC(15,2) | Total de receitas de campanha |

O script de criação da tabela está disponível em `dados/sql/criar_tabela.sql`.

As consultas para verificação da carga e integridade dos registros estão em `dados/sql/consultas_validacao.sql`.

## 6. Infraestrutura em nuvem

O banco de dados PostgreSQL está hospedado na plataforma Aiven.

Configuração utilizada:

| Parâmetro | Valor |
|---|---|
| Plataforma | Aiven |
| Serviço | PostgreSQL |
| Projeto | `big-data-eleicoes-2024` |
| Nome do serviço | `postgres-eleicoes-2024` |
| Plano | `developer-1` |
| Região | `do-nyc` |
| Provedor de nuvem | DigitalOcean |
| CPU | 1 |
| Memória RAM | 1 GB |
| Armazenamento | 8 GB |

O serviço foi criado inicialmente na plataforma Aiven e posteriormente importado para o Terraform, permitindo sua representação e seu gerenciamento como infraestrutura como código.

A importação foi realizada com o comando:

```bash
terraform import aiven_pg.eleicoes big-data-eleicoes-2024/postgres-eleicoes-2024
```

Após a importação, foi executado `terraform plan`, que retornou:

```text
No changes. Your infrastructure matches the configuration.
```

Esse resultado demonstra que a configuração declarada corresponde ao serviço existente, sem alterações pendentes naquele momento.

## 7. Infraestrutura como código com Terraform

Os arquivos de infraestrutura estão disponíveis na pasta `terraform/`:

| Arquivo | Finalidade |
|---|---|
| `main.tf` | Configuração do provedor e do recurso PostgreSQL |
| `variables.tf` | Declaração das variáveis |
| `outputs.tf` | Definição das saídas |
| `terraform.tfvars.example` | Exemplo de configuração |
| `.terraform.lock.hcl` | Registro das versões dos provedores |

A configuração inclui a proteção `prevent_destroy`, com o objetivo de impedir a destruição acidental do recurso gerenciado.

Para preparar o ambiente:

```bash
cd terraform
terraform init
terraform validate
```

Para utilizar os valores de configuração, deve-se criar uma cópia local de `terraform.tfvars.example` com o nome `terraform.tfvars`.

A autenticação com a Aiven é realizada por meio da variável de ambiente `AIVEN_TOKEN`.

A importação é necessária somente quando o serviço já existe e ainda não está registrado no estado do Terraform. Não se deve executar novamente a importação sem verificar previamente o estado atual.

Antes de aplicar qualquer mudança na infraestrutura, deve-se executar `terraform plan` e analisar as operações propostas.

## 8. Segurança e gerenciamento de credenciais

As credenciais do banco de dados e os tokens de acesso à Aiven não são armazenados nos arquivos versionados do projeto.

O arquivo `.gitignore` impede o versionamento de arquivos locais e potencialmente sensíveis, incluindo:

- `.env`
- `terraform/terraform.tfvars`
- `terraform/terraform.tfstate`
- `terraform/.terraform/`

O token de acesso à API da Aiven deve ser fornecido por uma variável de ambiente denominada `AIVEN_TOKEN`.

O arquivo de estado do Terraform pode conter informações sensíveis e deve ser protegido. Sua ausência no repositório público significa que outro ambiente precisará configurar seu próprio estado e, quando aplicável, importar os recursos existentes.

## 9. Organização do repositório

```text
projeto-big-data/
├── dados/
│   ├── brutos/
│   ├── tratados/
│   └── sql/
│       ├── criar_tabela.sql
│       └── consultas_validacao.sql
├── etl/
│   ├── tratamento_dados.py
│   └── contar_registros.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   └── .terraform.lock.hcl
├── .gitignore
└── README.md
```

## 10. Reprodução do processamento

### 10.1 Pré-requisitos

- Python 3
- Biblioteca Pandas
- PostgreSQL para armazenamento dos dados
- Terraform para gerenciamento da infraestrutura
- Conta e serviço Aiven, quando for utilizada a infraestrutura em nuvem

### 10.2 Preparação das bases

Obter os arquivos públicos do TSE e armazená-los na pasta `dados/brutos/`, mantendo os nomes esperados pelo script.

### 10.3 Instalação da dependência Python

```bash
python -m pip install pandas
```

### 10.4 Execução do ETL

Na raiz do projeto:

```bash
python etl/tratamento_dados.py
```

O processamento gera os arquivos CSV tratados em `dados/tratados/`.

### 10.5 Preparação do banco

Executar `dados/sql/criar_tabela.sql` em uma instância PostgreSQL.

Em seguida, importar o arquivo `dados/tratados/base_eleicoes_2024_banco.csv` para a tabela `candidaturas_2024`, respeitando a ordem das colunas, os tipos definidos e o cabeçalho do CSV.

### 10.6 Validação

Executar as consultas disponíveis em `dados/sql/consultas_validacao.sql` para verificar a quantidade de registros e a integridade da carga.

### 10.7 Infraestrutura

A configuração do Terraform descreve o serviço PostgreSQL utilizado na Aiven. Para gerenciar o serviço existente, é necessário configurar a autenticação, os valores das variáveis e o estado do Terraform.

A execução de `terraform apply` não faz parte da reprodução automática do ETL e exige revisão prévia das alterações propostas, especialmente porque o recurso contém dados armazenados.

## 11. Considerações finais

A etapa de preparação e armazenamento resultou em uma base integrada com 463.669 candidaturas municipais de 2024 e 15 atributos, disponibilizada em arquivos CSV e em uma instância PostgreSQL na nuvem.

O uso de Python e Pandas permitiu tratar e consolidar os dados eleitorais, enquanto o PostgreSQL possibilitou sua organização relacional. A utilização do Terraform complementou a solução com uma representação versionada da infraestrutura.

A base preparada poderá apoiar análises posteriores sobre representatividade de gênero, raça/cor, distribuição de recursos financeiros e resultados eleitorais.