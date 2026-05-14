async function fazerLogin() {
    const usuario = document.getElementById('usuario').value
    const senha = document.getElementById('senha').value
    const mensagem = document.getElementById('mensagem')

    if (!usuario || !senha) {
        mensagem.innerHTML = '<div class="alert alert-danger">Preencha todos os campos!</div>'
        return
    }

    try {
        const resposta = await fetch(`${API}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usuario, senha })
        })

        const dados = await resposta.json()

        if (dados.success) {
            sessionStorage.setItem('logado', 'true')
            window.location.href = 'index.html'
        } else {
            mensagem.innerHTML = `<div class="alert alert-danger">${dados.mensagem}</div>`
        }

    } catch(erro) {
        mensagem.innerHTML = `<div class="alert alert-danger">Erro: ${erro.message}</div>`
    }
}