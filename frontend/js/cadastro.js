async function cadastrar() {
    const nome = document.getElementById('nome').value
    const cpf = document.getElementById('cpf').value
    const fotos = document.getElementById('fotos').files
    const mensagem = document.getElementById('mensagem')

    try {
        if (!nome || !cpf) {
            mensagem.innerHTML = '<div class="alert alert-danger">Nome e CPF são obrigatórios!</div>'
            return
        }

        if (fotos.length < 3) {
            mensagem.innerHTML = '<div class="alert alert-danger">Envie pelo menos 3 fotos!</div>'
            return
        }

        const resposta = await fetch(`${API}/pessoas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, cpf })
        })

        const dados = await resposta.json()

        if (!resposta.ok) {
            mensagem.innerHTML = `<div class="alert alert-danger">${dados.error}</div>`
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

        mensagem.innerHTML = '<div class="alert alert-success">Pessoa cadastrada com sucesso!</div>'
        setTimeout(() => { mensagem.innerHTML = '' }, 45000)
    
    } catch(erro) {
        mensagem.innerHTML = `<div class="alert alert-danger">Erro: ${erro.message}</div>`
        console.error(erro)
    }
 
}