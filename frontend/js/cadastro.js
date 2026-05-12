async function cadastrar() {
    const nome = document.getElementById('nome').value
    const cpf = document.getElementById('cpf').value
    const fotos = document.getElementById('fotos').files
    const modalConteudo = document.getElementById('modalConteudo')
    const modal = new bootstrap.Modal(document.getElementById('modalResultado'))

    if (!nome || !cpf) {
        modalConteudo.innerHTML = '<div class="alert alert-danger">Nome e CPF são obrigatórios!</div>'
        modal.show()
        return
    }

    if (fotos.length < 3) {
        modalConteudo.innerHTML = '<div class="alert alert-danger">Envie pelo menos 3 fotos!</div>'
        modal.show()
        return
    }

    try {
        modalConteudo.innerHTML = '<p class="text-center">⏳ Cadastrando... aguarde.</p>'
        document.getElementById('modalFooter').style.display = 'none'
        modal.show()

        const resposta = await fetch(`${API}/pessoas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, cpf })
        })

        const dados = await resposta.json()

        if (!resposta.ok) {
            modalConteudo.innerHTML = `<div class="alert alert-danger">${dados.error}</div>`
            return
        }

        for (let foto of fotos) {
            const formData = new FormData()
            formData.append('imagem', foto)
            await fetch(`${API}/imagem/${dados.id}`, {
                method: 'POST',
                body: formData
            })
        }

        modalConteudo.innerHTML = `
            <div class="alert alert-success">
                <h5>✅ Pessoa cadastrada com sucesso!</h5>
                <p><strong>Nome:</strong> ${nome}</p>
                <p><strong>ID:</strong> ${dados.id}</p>
                <p><strong>Fotos enviadas:</strong> ${fotos.length}</p>
            </div>
        `
        document.getElementById('modalFooter').style.display = 'flex'
        

    } catch(erro) {
        modalConteudo.innerHTML = `<div class="alert alert-danger">Erro: ${erro.message}</div>`
        console.error(erro)
    }
}