from datetime import datetime
import sys

_next_id = 1

def _generate_id():
    global _next_id
    id_ = _next_id
    _next_id += 1
    return id_

def validarData(dataStr):
    try:
        datetime.strptime(dataStr, "%Y-%m-%d")
        return True
    except:
        return False

def adicionarEvento(listaEventos, nome, data, local, categoria):
    if nome.strip() == "":
        print("Nome do evento não pode ser vazio")
        return None
    if not validarData(data):
        print("Data inválida — use AAAA-MM-DD")
        return None
    if local.strip() == "":
        print("Local não pode ser vazio")
        return None
    if categoria.strip() == "":
        print("Categoria não pode ser vazia")
        return None

    evento = {
        "id": _generate_id(),
        "nome": nome.strip(),
        "data": data,
        "local": local.strip(),
        "categoria": categoria.strip(),
        "participado": False
    }
    listaEventos.append(evento)
    return evento

def listarEventos(listaEventos):
    try:
        return sorted(listaEventos, key=lambda e: datetime.strptime(e["data"], "%Y-%m-%d"))
    except:
        return listaEventos

def procurarEventoPorNome(listaEventos, nome):
    nome_proc = nome.strip().lower()
    encontrados = [e for e in listaEventos if nome_proc in e["nome"].lower()]
    return encontrados

def deletarEvento(listaEventos, id_or_name):
    if isinstance(id_or_name, int):
        for i, e in enumerate(listaEventos):
            if e["id"] == id_or_name:
                del listaEventos[i]
                return True
        return False
    else:
        name = str(id_or_name).strip().lower()
        for i, e in enumerate(listaEventos):
            if e["nome"].lower() == name:
                del listaEventos[i]
                return True
        return False

def displayMenu():
    print("\n=== Planejador de Eventos do Campus ===")
    print("1. Adicionar um Evento")
    print("2. Ver Todos os Eventos")
    print("3. Filtrar por Categoria")
    print("4. Marcar Evento como Participado")
    print("5. Gerar Relatório")
    print("6. Deletar um Evento")
    print("7. Buscar por Nome")
    print("8. Sair")

def getEscolhaDoUsuario():
    try:
        escolha = int(input("\nEscolha uma opção: ").strip())
        return escolha
    except:
        return -1

def filtrarEventosPorCategoria(listaEventos, categoria):
    categ = categoria.strip().lower()
    return [e for e in listaEventos if e["categoria"].lower() == categ]

def marcarEventoAtendido(listaEventos, id_):
    for e in listaEventos:
        if e["id"] == id_:
            e["participado"] = True
            return True
    return False

def gerarRelatorio(listaEventos):
    total = len(listaEventos)
    por_categoria = {}
    participados = 0
    for e in listaEventos:
        if e.get("participado"):
            participados += 1
        cat = e.get("categoria", "(Sem categoria)")
        por_categoria[cat] = por_categoria.get(cat, 0) + 1

    if total > 0:
        perc_part = (participados / total) * 100
    else:
        perc_part = 0

    print("\n--- RELATÓRIO DE EVENTOS ---")
    print("Total de Eventos:", total)
    print("Por Categoria:", por_categoria)
    print("Participados: {:.0f}% ({}/{})".format(perc_part, participados, total))

def _mostrar_evento(evento):
    print("ID:", evento['id'], "|", evento['nome'], "|", evento['data'], "|", evento['local'], "|", evento['categoria'], "| Participado:", evento['participado'])

def _input_evento_e_adicionar(listaEventos):
    nome = input("Nome do evento: ").strip()
    data = input("Data (AAAA-MM-DD): ").strip()
    local = input("Local: ").strip()
    categoria = input("Categoria: ").strip()
    ev = adicionarEvento(listaEventos, nome, data, local, categoria)
    if ev:
        print("\nEvento adicionado com sucesso! (ID:", ev["id"], ")")
        
def main():
    listaEventos = []
    print("Bem-vindo ao Planejador de Eventos do Campus")

    while True:
        displayMenu()
        escolha = getEscolhaDoUsuario()

        if escolha == 1:
            _input_evento_e_adicionar(listaEventos)
        if escolha == 2:
            eventos = listarEventos(listaEventos)
            if not eventos:
                print("Nenhum evento cadastrado.")
            else:
                print("\n--- Eventos ---")
                for e in eventos:
                    _mostrar_evento(e)
        if escolha == 3:
            cat = input("Categoria para filtrar: ").strip()
            filtrados = filtrarEventosPorCategoria(listaEventos, cat)
            if not filtrados:
                print("Nenhum evento encontrado para essa categoria.")
            else:
                print("\nEventos na categoria", cat, ":")
                for e in listarEventos(filtrados):
                    _mostrar_evento(e)
        if escolha == 4:
            try:
                id_str = input("ID do evento a marcar como participado: ").strip()
                id_ = int(id_str)
                ok = marcarEventoAtendido(listaEventos, id_)
                if ok:
                    print("Evento marcado como participado.")
                else:
                    print("Evento não encontrado.")
            except:
                print("ID inválido. Informe um número inteiro.")
        if escolha == 5:
            gerarRelatorio(listaEventos)
        if escolha == 6:
            chave = input("Informe o ID ou nome do evento a deletar: ").strip()
            try:
                chave_int = int(chave)
                ok = deletarEvento(listaEventos, chave_int)
            except:
                ok = deletarEvento(listaEventos, chave)
            if ok:
                print("Evento deletado com sucesso.")
            else:
                print("Evento não encontrado.")
        if escolha == 7:
            termo = input("Termo para buscar no nome: ").strip()
            encontrados = procurarEventoPorNome(listaEventos, termo)
            if not encontrados:
                print("Nenhum evento encontrado com esse termo.")
            else:
                print("\nEventos encontrados para:", termo)
                for e in encontrados:
                    _mostrar_evento(e)
        if escolha == 8:
            print("Saindo. Até logo!")
            break
        if escolha < 1 or escolha > 8:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário. Saindo...")
        sys.exit(0)
