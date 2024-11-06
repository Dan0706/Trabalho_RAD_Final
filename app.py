import tkinter as tk
from tkinter import messagebox, simpledialog
from database_contas import DatabaseContas
from database_produtos import DatabaseProdutos

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela de Login")
        self.root.geometry("400x300")
        self.root.configure(bg='#f0f0f0')
        self.db_contas = DatabaseContas()
        self.db_produtos = DatabaseProdutos()


        self.frame = tk.Frame(self.root, bg='#f0f0f0')
        self.frame.pack(pady=20)

        self.label_username = tk.Label(self.frame, text="Usuário", font=('Arial', 12), bg='#f0f0f0')
        self.label_username.grid(row=0, column=0, pady=5, padx=10)

        self.entry_username = tk.Entry(self.frame, font=('Arial', 12), bd=2)
        self.entry_username.grid(row=0, column=1, pady=5, padx=10)

        self.label_password = tk.Label(self.frame, text="Senha", font=('Arial', 12), bg='#f0f0f0')
        self.label_password.grid(row=1, column=0, pady=5, padx=10)

        self.entry_password = tk.Entry(self.frame, show='*', font=('Arial', 12), bd=2)
        self.entry_password.grid(row=1, column=1, pady=5, padx=10)

        self.button_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.button_frame.pack(pady=20)

        self.button_login = tk.Button(self.button_frame, text="Login", font=('Arial', 12), bg='#4caf50', fg='white', command=self.login)
        self.button_login.grid(row=0, column=0, padx=10)

        self.button_cadastrar = tk.Button(self.button_frame, text="Cadastrar", font=('Arial', 12), bg='#2196f3', fg='white', command=self.abrirTelaCadastro)
        self.button_cadastrar.grid(row=0, column=1, padx=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Erro de Login", "Todos os campos são obrigatórios.")
            return

        if self.db_contas.verificarLogin(username, password):
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.root.withdraw()
            ProdutoApp(self.root, self.db_produtos)
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")

    def abrirTelaCadastro(self):

        self.cadastro_window = tk.Toplevel(self.root)
        self.cadastro_window.title("Cadastrar Novo Usuário")
        self.cadastro_window.geometry("400x300")
        self.cadastro_window.configure(bg='#f0f0f0')

        self.label_new_username = tk.Label(self.cadastro_window, text="Novo Usuário", font=('Arial', 12), bg='#f0f0f0')
        self.label_new_username.grid(row=0, column=0, pady=5, padx=10)

        self.entry_new_username = tk.Entry(self.cadastro_window, font=('Arial', 12), bd=2)
        self.entry_new_username.grid(row=0, column=1, pady=5, padx=10)

        self.label_new_password = tk.Label(self.cadastro_window, text="Nova Senha", font=('Arial', 12), bg='#f0f0f0')
        self.label_new_password.grid(row=1, column=0, pady=5, padx=10)

        self.entry_new_password = tk.Entry(self.cadastro_window, show='*', font=('Arial', 12), bd=2)
        self.entry_new_password.grid(row=1, column=1, pady=5, padx=10)

        self.button_confirm_cadastrar = tk.Button(self.cadastro_window, text="Cadastrar", font=('Arial', 12), bg='#4caf50', fg='white', command=self.cadastrar)
        self.button_confirm_cadastrar.grid(row=2, columnspan=2, pady=20)

    def cadastrar(self):
        new_username = self.entry_new_username.get()
        new_password = self.entry_new_password.get()

        if not new_username or not new_password:
            messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios.")
            return

        if self.db_contas.cadastrarUsuario(new_username, new_password):
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            self.cadastro_window.destroy()
        else:
            messagebox.showerror("Erro de Cadastro", "Erro ao cadastrar usuário.")


class ProdutoApp:
    def __init__(self, root, db_produtos):
        self.root = root
        self.db_produtos = db_produtos


        self.produtos_window = tk.Toplevel(root)
        self.produtos_window.title("Produtos da Loja")
        self.produtos_window.geometry("600x400")
        self.produtos_window.configure(bg='#f0f0f0')


        self.produtos_window.protocol("WM_DELETE_WINDOW", self.voltarTelaLogin)


        self.label_produtos = tk.Label(self.produtos_window, text="Produtos No Estoque", font=('Arial', 14), bg='#f0f0f0')
        self.label_produtos.pack(pady=10)

        self.label_instrucao = tk.Label(self.produtos_window, text="Clique para selecionar produto", font=('Arial', 10),
                                        bg='#f0f0f0')
        self.label_instrucao.pack(pady=(0, 10))

        self.frame_produtos = tk.Frame(self.produtos_window, bg='#f0f0f0')
        self.frame_produtos.pack(pady=10)

        self.listbox_produtos = tk.Listbox(self.frame_produtos, width=60, height=10, font=('Arial', 12))
        self.listbox_produtos.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        self.scrollbar_produtos = tk.Scrollbar(self.frame_produtos)
        self.scrollbar_produtos.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_produtos.config(yscrollcommand=self.scrollbar_produtos.set)
        self.scrollbar_produtos.config(command=self.listbox_produtos.yview)

        self.atualizarListaProdutos()


        self.frame_botoes = tk.Frame(self.produtos_window, bg='#f0f0f0')
        self.frame_botoes.pack(pady=10)

        self.btn_adicionar = tk.Button(self.frame_botoes, text="Adicionar Produto", font=('Arial', 12), bg='#4caf50', fg='white', command=self.adicionarProduto)
        self.btn_adicionar.grid(row=0, column=0, padx=10)

        self.btn_alterar = tk.Button(self.frame_botoes, text="Alterar Produto", font=('Arial', 12), bg='#2196f3', fg='white', command=self.alterarProduto)
        self.btn_alterar.grid(row=0, column=1, padx=10)

        self.btn_excluir = tk.Button(self.frame_botoes, text="Excluir Produto", font=('Arial', 12), bg='#f44336', fg='white', command=self.excluirProduto)
        self.btn_excluir.grid(row=0, column=2, padx=10)

    def voltarTelaLogin(self):
        self.produtos_window.destroy()
        self.root.deiconify()

    def atualizarListaProdutos(self):
        self.listbox_produtos.delete(0, tk.END)
        produtos = self.db_produtos.listarProdutos()
        for produto in produtos:
            self.listbox_produtos.insert(tk.END, f"ID: {produto[0]} | Nome: {produto[1]} | Quantidade: {produto[2]} | Preço: R${produto[3]:.2f}")

    def adicionarProduto(self):
        nome = simpledialog.askstring("Adicionar Produto", "Nome do Produto:")
        quantidade = simpledialog.askinteger("Adicionar Produto", "Quantidade do Produto:")
        preco = simpledialog.askfloat("Adicionar Produto", "Preço do Produto:")
        if nome and quantidade is not None and preco is not None:
            if self.db_produtos.adicionarProduto(nome, quantidade, preco):
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                self.atualizarListaProdutos()
            else:
                messagebox.showerror("Erro", "Erro ao adicionar produto.")

    def alterarProduto(self):
        selecionado = self.listbox_produtos.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um produto para alterar.")
            return
        produto_info = self.listbox_produtos.get(selecionado)
        produto_id = int(produto_info.split("|")[0].split(":")[1].strip())

        nome = simpledialog.askstring("Alterar Produto", "Novo Nome do Produto:")
        quantidade = simpledialog.askinteger("Alterar Produto", "Nova Quantidade do Produto:")
        preco = simpledialog.askfloat("Alterar Produto", "Novo Preço do Produto:")
        if nome and quantidade is not None and preco is not None:
            if self.db_produtos.atualizarProduto(produto_id, nome, quantidade, preco):
                messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
                self.atualizarListaProdutos()
            else:
                messagebox.showerror("Erro", "Erro ao alterar produto.")

    def excluirProduto(self):
        selecionado = self.listbox_produtos.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um produto para excluir.")
            return
        produto_info = self.listbox_produtos.get(selecionado)
        produto_id = int(produto_info.split("|")[0].split(":")[1].strip())

        if messagebox.askyesno("Excluir Produto", "Tem certeza que deseja excluir este produto?"):
            if self.db_produtos.excluirProduto(produto_id):
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                self.atualizarListaProdutos()
            else:
                messagebox.showerror("Erro", "Erro ao excluir produto.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
