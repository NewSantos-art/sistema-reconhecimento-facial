async function reconhecer() {
    const imagem = document.getElementById('imagem').files[0]
    const modalConteudo = document.getElementById('modalConteudo')
    const modal = new bootstrap.Modal(document.getElementById('modalResultado'))

    if (!imagem) {
        alert('Selecione uma imagem!')
        return
    }

    try {
        const formData = new FormData()
        formData.append('imagem', imagem)

        modalConteudo.innerHTML = '<p class="text-center">⏳ Analisando imagem... aguarde.</p>'
        modal.show()

        const resposta = await fetch(`${API}/reconhecer`, {
            method: 'POST',
            body: formData
        })

        const dados = await resposta.json()

        if (dados.error) {
            modalConteudo.innerHTML = `<div class="alert alert-danger">${dados.error}</div>`
            return
        }

        if (dados.resultado === 'Pessoa identificada') {
            modalConteudo.innerHTML = `
                <div class="alert alert-success">
                    <h5>✅ Pessoa Identificada!</h5>
                    <p><strong>Nome:</strong> ${dados.nome}</p>
                    <p><strong>ID:</strong> ${dados.id}</p>
                    <p><strong>Confiança:</strong> ${dados.confianca}</p>
                </div>
            `
        } else {
            modalConteudo.innerHTML = '<div class="alert alert-warning">⚠️ Pessoa não identificada no sistema.</div>'
        }

    } catch(erro) {
        modalConteudo.innerHTML = `<div class="alert alert-danger">Erro: ${erro.message}</div>`
        console.error(erro)
    }
}