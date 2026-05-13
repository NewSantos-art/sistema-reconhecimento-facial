async function carregarHistorico() {
    const tabela = document.getElementById('tabela')

    const resposta = await fetch(`${API}/historico`)
    const registros = await resposta.json()

    if (registros.length === 0) {
        tabela.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Nenhum reconhecimento realizado ainda.</td></tr>'
        return
    }

    registros.forEach(r => {
        const cor = r.nome === 'Desconhecido' ? 'table-danger' : 'table-success'
        const metodo = r.metodo === 'webcam' ? '📷 Webcam' : '🖼️ Imagem'
        tabela.innerHTML += `
            <tr class="${cor}">
                <td>${r.id}</td>
                <td>${r.nome}</td>
                <td>${r.confianca}</td>
                <td>${metodo}</td>
                <td>${r.data_hora}</td>
            </tr>
        `
    })
}

carregarHistorico()