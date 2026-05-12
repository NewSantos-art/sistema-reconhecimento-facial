async function carregarPessoas() {
    const lista = document.getElementById('lista')

    const resposta = await fetch(`${API}/pessoas`)
    const pessoas = await resposta.json()

    if (pessoas.length === 0) {
        lista.innerHTML = '<p class="text-muted">Nenhuma pessoa cadastrada.</p>'
        return
    }

    pessoas.forEach(pessoa => {
        lista.innerHTML += `
            <div class="col-md-4">
                <div class="card p-3">
                    <h5>${pessoa.nome}</h5>
                    <p class="text-muted mb-1">ID: ${pessoa.id}</p>
                    <p class="text-muted mb-1">CPF: ${pessoa.cpf}</p>
                    <p class="text-muted mb-0">Cadastrado em: ${pessoa.data_cadastro}</p>
                </div>
            </div>
        `
    })
}

carregarPessoas()