# Plano de Implementação - StockFlow SSD Stock Control

Esta é uma aplicação web para controle de estoque de SSDs (SATA e NVMe) construída com **Flask (Python)** no backend, e **HTML, CSS (Vanilla moderno com Glassmorphism)** e **JavaScript** no frontend.

## User Review Required

> [!NOTE]
> Para testar a aplicação localmente, criaremos um banco de dados SQLite (`stock.db`) local pré-configurado com o usuário `admin` e senha `admin`.

> [!IMPORTANT]
> A exportação de dados para Excel e PDF será disponibilizada tanto para as páginas de Entrada quanto para Saída. Utilizaremos bibliotecas Python como `openpyxl` (para Excel) e `reportlab` (para PDF) para gerar os relatórios diretamente no backend e enviá-los ao cliente.

## proposed changes

### Backend (Flask App)

#### [NEW] [app.py](file:///c:/Users/SamSung/Downloads/Devs%20Projects/Python/stockflow/app.py)
Arquivo principal do Flask. Conterá:
* Configuração do Flask e sessão de usuário.
* Conexão com o banco de dados SQLite (`stock.db`).
* Sistema de login e autenticação com usuário `admin` / senha `admin`.
* Rotas da API e views:
  * `/login` - Tela de login.
  * `/` (Dashboard) - Tela principal mostrando status atual do estoque (quantos SSDs de cada modelo restam e quantos saíram).
  * `/entradas` - Tela de cadastro de novas entradas de produtos + listagem histórica.
  * `/saidas` - Tela de registro de novas saídas de produtos + listagem histórica.
  * `/export/excel/<type>` - Rota para download do Excel (entradas ou saídas).
  * `/export/pdf/<type>` - Rota para download do PDF (entradas ou saídas).

#### [NEW] [database.py](file:///c:/Users/SamSung/Downloads/Devs%20Projects/Python/stockflow/database.py)
Script utilitário para inicializar o banco de dados SQLite (`stock.db`) e criar as tabelas necessárias:
* `users`: `id`, `username`, `password` (hash ou texto claro para testes).
* `products`: `id`, `ssd_type` (SATA / NVMe), `brand`, `size` (opcional), `quantity_in_stock`, `quantity_exited`.
* `entries`: `id`, `entry_date`, `ssd_type`, `brand`, `size`, `quantity`, `supplier`, `price`.
* `exits`: `id`, `exit_date`, `ssd_type`, `brand`, `size`, `quantity`, `supplier`, `client`.

### Frontend (Templates & Static Files)

#### [NEW] [templates/base.html](file:///c:/Users/SamSung/Downloads/Devs%20Projects/Python/stockflow/templates/base.html)
Layout base do site com:
* Meta tags para responsividade e SEO.
* Link para Google Fonts (`Outfit` ou `Inter`).
* Barra de navegação moderna (sidebar ou navbar superior) com link para Dashboard, Entradas, Saídas e Logout.
* Estrutura geral de grid/flexbox e container de conteúdo.

#### [NEW] [templates/login.html](file:///c:/Users/SamSung/Downloads/Devs%20Projects/Python/stockflow/templates/login.html)
Página de login:
* Card centralizado com efeito glassmorphism (desfoque de fundo e borda translúcida).
* Formulário estilizado para usuário e senha.
* Mensagens de erro em caso de credenciais inválidas com animações suaves.

#### [NEW] [templates/dashboard.html](file:///c:/Users/SamSung/Downloads/Devs%20Projects/Python/stockflow/templates/dashboard.html)
Painel principal de controle de estoque:
* Estatísticas resumidas no topo (Total de itens em estoque, total saídas, proporção SATA vs NVMe).
* Tabela responsiva com efeito de hover listando todos os SSDs agregados por Marca, Tipo (SATA/NVMe) e Tamanho, mostrando a quantidade atual no estoque e a quantidade total que saiu.
* Alertas visuais (ex: baixa quantidade em estoque com cores de aviso pulsantes).

#### [NEW] [templates/entradas.html](file:///c:/Users/SamSung/Downloads/Devs%20Projects/Python/stockflow/templates/entradas.html)
Página para registrar e visualizar entradas:
* Formulário de cadastro de entrada: Tipo (SATA/NVMe), Data de Entrada, Marca, Tamanho (opcional), Quantidade, Fornecedor, Preço.
* Tabela histórica de entradas com paginação ou scroll infinito.
* Botões de exportação destacados ("Exportar Excel" e "Exportar PDF") com ícones modernos.

#### [NEW] [templates/saidas.html](file:///c:/Users/SamSung/Downloads/Devs%20Projects/Python/stockflow/templates/saidas.html)
Página para registrar e visualizar saídas:
* Formulário de registro de saída: Tipo (SATA/NVMe), Data de Saída, Marca, Tamanho (opcional), Quantidade, Fornecedor, Cliente.
  * *Validação*: O formulário deve validar em tempo real se o produto selecionado tem quantidade suficiente em estoque antes de permitir a saída.
* Tabela histórica de saídas.
* Botões de exportação destacados ("Exportar Excel" e "Exportar PDF").

#### [NEW] [static/css/style.css](file:///c:/Users/SamSung/Downloads/Devs%20Projects/Python/stockflow/static/css/style.css)
Sistema de estilos centralizado:
* Paleta de cores moderna (fundo escuro azulado/violeta profundo, detalhes em verde neon, roxo gradiente e ciano).
* Efeito Glassmorphism (`background: rgba(...)`, `backdrop-filter: blur(...)`).
* Animações de transição suaves para botões, inputs e troca de telas.
* Layouts responsivos para celular, tablet e desktop.

#### [NEW] [static/js/main.js](file:///c:/Users/SamSung/Downloads/Devs%20Projects/Python/stockflow/static/js/main.js)
Código JavaScript interativo para:
* Validação dinâmica de formulários.
* Consulta assíncrona ao estoque para validar quantidade de saída permitida.
* Efeitos de transição e feedback visual ao salvar dados.

---

## Verification Plan

### Automated Tests
* Não há testes automatizados planejados no momento, a validação será manual e interativa.

### Manual Verification
1. **Acesso e Login**: Testar tela de login com credenciais incorretas (exibir alerta) e com `admin`/`admin` (redirecionar para o dashboard).
2. **Dashboard**: Verificar se as contagens e tabela mostram 0 itens inicialmente.
3. **Entrada de Produtos**:
   * Cadastrar um SSD SATA de 240GB da marca Kingston, fornecedor "Distribuidora X", preço R$ 150, quantidade 10.
   * Cadastrar um SSD NVMe de 1TB da marca XPG, fornecedor "Distribuidora Y", preço R$ 400, quantidade 5.
   * Validar se os itens aparecem na lista de entradas e se as quantidades refletem no Dashboard.
4. **Saída de Produtos**:
   * Registrar saída de 3 unidades do SSD SATA Kingston 240GB para o cliente "Cliente A".
   * Tentar registrar saída de 6 unidades do SSD NVMe XPG 1TB (deve falhar e exibir erro, pois o estoque é 5).
   * Registrar saída de 2 unidades do SSD NVMe XPG 1TB para o cliente "Cliente B".
   * Verificar se o Dashboard atualiza corretamente as quantidades (SATA Kingston: 7 em estoque, 3 saíram. NVMe XPG: 3 em estoque, 2 saíram).
5. **Exportação**:
   * Clicar em "Exportar Excel" na página de Entradas e verificar o arquivo `.xlsx` gerado.
   * Clicar em "Exportar PDF" na página de Entradas e verificar o arquivo `.pdf` gerado.
   * Clicar nos botões correspondentes na página de Saídas e verificar a integridade dos arquivos.
