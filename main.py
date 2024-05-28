import tkinter as tk
from tkinter import messagebox
import connection as conn
import query as crud

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Notas de Alunos")
        self.geometry("600x400")

        self.cursor, self.cnx = conn.connection()
        if not self.cursor:
            messagebox.showerror("Erro", "Falha na conexão com o banco de dados")
            self.destroy()
            return

        self.create_widgets()
        self.listar_todos()
    
    def create_widgets(self):
        # Labels e Entradas
        tk.Label(self, text="Nome").grid(row=0, column=0, padx=10, pady=10)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Curso").grid(row=1, column=0, padx=10, pady=10)
        self.entry_curso = tk.Entry(self)
        self.entry_curso.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Nota").grid(row=2, column=0, padx=10, pady=10)
        self.entry_nota = tk.Entry(self)
        self.entry_nota.grid(row=2, column=1, padx=10, pady=10)

        # Botões
        self.btn_insert = tk.Button(self, text="Inserir", command=self.insert_aluno)
        self.btn_insert.grid(row=3, column=0, padx=10, pady=10)

        self.btn_update = tk.Button(self, text="Atualizar", command=self.update_aluno)
        self.btn_update.grid(row=3, column=1, padx=10, pady=10)

        self.btn_delete = tk.Button(self, text="Deletar", command=self.delete_aluno)
        self.btn_delete.grid(row=4, column=0, padx=10, pady=10)

        self.btn_select = tk.Button(self, text="Listar Todos", command=self.listar_todos)
        self.btn_select.grid(row=4, column=1, padx=10, pady=10)

        # Listbox para exibir resultados
        self.listbox_result = tk.Listbox(self, width=70, height=15, selectmode=tk.SINGLE)
        self.listbox_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def insert_aluno(self):
        nome = self.entry_nome.get()
        curso = self.entry_curso.get()
        nota = self.entry_nota.get()
        if nome and curso and nota:
            try:
                crud.insert(self.cursor, self.cnx, nome, curso, float(nota))
                messagebox.showinfo("Sucesso", "Aluno inserido com sucesso!")
                self.listar_todos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao inserir aluno: {e}")
        else:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios")
    
    def update_aluno(self):
        id = self.get_selected_id()
        if id is not None:
            nome = self.entry_nome.get()
            curso = self.entry_curso.get()
            nota = self.entry_nota.get()
            if nome and curso and nota:
                try:
                    crud.update(self.cursor, self.cnx, id, nome, curso, float(nota))
                    messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
                    self.listar_todos()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar aluno: {e}")
            else:
                messagebox.showwarning("Aviso", "Todos os campos são obrigatórios")
    
    def delete_aluno(self):
        id = self.get_selected_id()
        if id is not None:
            try:
                crud.delete(self.cursor, self.cnx, id)
                messagebox.showinfo("Sucesso", "Aluno deletado com sucesso!")
                self.listar_todos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar aluno: {e}")

    def listar_todos(self):
        self.listbox_result.delete(0, tk.END)
        try:
            results = crud.select(self.cursor)
            for row in results:
                self.listbox_result.insert(tk.END, f"ID: {row[0]}, Nome: {row[1]}, Curso: {row[2]}, Nota: {row[3]}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos: {e}")

    def get_selected_id(self):
        try:
            selected = self.listbox_result.get(self.listbox_result.curselection())
            return int(selected.split(",")[0].split(":")[1].strip())
        except:
            messagebox.showwarning("Aviso", "Selecione um aluno na lista")
            return None

if __name__ == '__main__':
    app = Application()
    app.mainloop()
