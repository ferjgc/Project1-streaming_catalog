import sqlite3
import pandas as pd


def cadastrar_filme(nome, data_lancamento=None, genero=None):
    kwargs = locals()
    kwargs = {v: kwargs[v] for v in kwargs if kwargs[v] != None}
    id_filme = conn.execute("select max(id_filme) from filmes").fetchone()[0] + 1

    cols = list(kwargs.keys())
    cols = ", ".join(cols)
    vals = list(kwargs.values())
    vals = ", ".join(["'{}'".format(x) for x in vals])

    query = f"""
    INSERT INTO filmes(id_filme, {cols})
    VALUES({id_filme}, {vals})
    """
    # breakpoint()
    conn.execute(query)
    conn.commit()


def procurar_filme_nome(nome):
    resultado = pd.read_sql(
        f"""
    select * from filmes where lower(nome) like '%{nome}%'
    """,
        conn,
    )

    return resultado


def mostrar_filmes():
    print(
        pd.read_sql(
            f"""
    select * from filmes
    """,
            conn,
        )
    )


def atualizar_filme(id_filme, nome=None, data_lancamento=None, genero=None):
    kwargs = locals()
    kwargs = {v: kwargs[v] for v in kwargs if kwargs[v] != None and v != "id_filme"}

    vals = [f"{x} = '{kwargs[x]}'" for x in kwargs]
    vals = ", ".join(vals)

    query = f"""
    UPDATE filmes
    SET {vals}
    WHERE id_filme = {id_filme}
    """
    conn.execute(query)


def delete_filme(id_filme):
    query = f"""
    DELETE FROM filmes
    WHERE id_filme = {id_filme}
    """
    conn.execute(query)


def main():
    while True:
        escolha = input(
            """
Digite uma opção
1 - Cadastrar novo filme
2 - Procurar filme pelo nome
3 - Mostrar todos os filmes
4 - Atualizar dados de um filme
5 - Deletear um filme
0 - Sair

"""
        )

        if escolha == "1":
            nome = input("Insira o nome: ")
            while not nome:
                nome = input(
                    "O nome é obrigatorio e não pode ser vazio. Insira um nome válido: "
                )
            data_lancamento = input(
                "Insira a data de lançamento(formato ISO YYYY-MM-DD): "
            )
            genero = input("Insira o gênero do filme: ")

            args = (nome, data_lancamento, genero)
            args = tuple([x if x else None for x in args])

            cadastrar_filme(*args)

        elif escolha == "2":
            nome = input(
                "Insira parte do nome do filme que deseja procurar (case insensitive): "
            )
            while not nome:
                nome = input(
                    "O nome é obrigatorio e não pode ser vazio. Insira um nome válido: "
                )

            print("\n", procurar_filme_nome(nome))

        elif escolha == "3":
            mostrar_filmes()

        elif escolha == "4":
            id_filme = int(input("Insira o ID do filme a ser atualizado."))
            while not id_filme:
                id_filme = int(
                    input(
                        "O ID é obrigatorio e deve ser um número inteiro. Insira um ID válido: "
                    )
                )

            print("Parametros que não queira atualizar deixe em branco.")
            nome = input("Insira o nome: ")
            data_lancamento = input(
                "Insira a data de lançamento(formato ISO YYYY-MM-DD): "
            )
            genero = input("Insira o gênero do filme: ")

            args = (nome, data_lancamento, genero)
            args = tuple([x if x else None for x in args])

            atualizar_filme(id_filme, nome=None, data_lancamento=None, genero=None)

        elif escolha == "5":
            id_filme = int(input("Insira o ID do filme a ser deletado"))
            delete_filme(id_filme)

        elif escolha == "0":
            break

        else:
            print("Opção invalida, digite uma opção valida")

        input("\nEnter pra continuar")
        # input('\n')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    conn = sqlite3.connect("db_filmes.db")

    query_cria_tabela_filmes = """
    CREATE TABLE IF NOT EXISTS filmes (
        id_filme integer PRIMARY KEY,
        nome text NOT NULL UNIQUE,
        data_lancamento text,
        genero text
    );
    """
    conn.execute(query_cria_tabela_filmes)
    conn.commit()

    if conn.execute("select max(id_filme) from filmes").fetchone()[0] is None:
        print("DB estava vazio, inicializando com Duro de Matar")
        conn.execute(
            """
        INSERT INTO filmes(id_filme, nome, data_lancamento, genero)
        VALUES(1, 'Duro de Matar', '1996-05-25', 'Ação')
        """
        )
        conn.commit()

    main()
